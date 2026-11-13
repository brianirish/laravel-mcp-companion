Source: https://laravel.com/cloud/docs/deploy-guides/go.md

# Go deploy guide

Configure your Go application for production on Laravel Cloud.

The [Go quickstart](https://laravel.com/cloud/docs/quickstart#go) walks you through your first deployment to Laravel Cloud. Once your application is up and running, this guide helps you get it ready for production. We'll cover how to compile your Go application, start it, and configure it so that it runs smoothly on Cloud.

## Listen on the right port

Cloud routes traffic to your application on the port set by the `PORT` environment variable, which is `3000` by default. Have your application read this value and leave the host out of its listen address:

```go theme={null}
port := os.Getenv("PORT")

log.Fatal(http.ListenAndServe(":"+port, mux))
```

When you use a bare `:port` address with Go's `net/http` server, it listens on all of the available IPv4 and IPv6 interfaces. Listening on IPv6 matters because Cloud's startup probes reach your application over IPv6. If you use an IPv4-only listener such as `net.Listen("tcp4", ...)`, or a loopback-only address, Cloud can't reach your application.

If your application deploys successfully but still isn't reachable, take a look at the [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide.

## Compile during the build

Cloud installs your Go modules automatically and pre-fills a build command based on your application's entrypoint. If your `main` package lives at the root of your repository, the default build command looks like this:

```sh theme={null}
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o app .
```

If your entrypoint lives in a directory such as `cmd/server`, Cloud builds that package instead. When your repository contains more than one entrypoint, you may select the one you would like to deploy. Cloud also sets `CGO_ENABLED=1` for you when it detects cgo dependencies or C source files. Of course, if your application has additional requirements, you're free to edit the command.

The default start command, `./app`, runs the binary produced by your build. Because you compile in your [build commands](https://laravel.com/cloud/docs/environments#build-commands), there's nothing left to compile at runtime. Your application starts quickly when a new instance boots or when your environment wakes up after [scaling to zero](https://laravel.com/cloud/docs/compute#scale-to-zero).

If your application includes other executables, compile them during the build as well. For example, an application with both a server and a migration command might use the following build command:

```sh theme={null}
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o app ./cmd/server && CGO_ENABLED=0 go build -o migrate ./cmd/migrate
```

Remember to use `CGO_ENABLED=1` for any binary that requires cgo. If you change your server binary's name or output path, update your start command to match.

## Shut down gracefully

When an instance stops, whether during a deployment or while scaling down, Cloud sends a `SIGTERM` signal to your process. To avoid cutting off requests that are still in progress, handle this signal in your application and wait for those requests to finish before exiting. If you are using a `net/http` server, you may use the following function with your application's handler:

```go theme={null}
import (
    "context"
    "errors"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func serve(handler http.Handler) {
    ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, os.Interrupt)
    defer stop()

    srv := &http.Server{Addr: ":" + os.Getenv("PORT"), Handler: handler}

    go func() {
        if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
            log.Fatal(err)
        }
    }()

    <-ctx.Done()

    shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(shutdownCtx); err != nil {
        log.Printf("HTTP shutdown: %v", err)
    }
}
```

Call this function from `main`, and your process keeps running until `Shutdown` returns. Keep your application's shutdown timeout shorter than your environment's **graceful shutdown timeout** so the rest of the instance has time to stop cleanly. Once that timeout passes, Cloud terminates any process that is still running.

## Running behind the proxy

Cloud handles TLS for you before forwarding requests to your application, so your server only needs to speak plain HTTP. Cloud's proxy also passes the original request scheme in the `X-Forwarded-Proto` header and the client's address chain in the `X-Forwarded-For` header.

Before relying on these headers to determine the request scheme or client IP address, configure your framework's trusted proxy settings. Frameworks such as Gin and Echo include these settings. In general, avoid trusting forwarded headers from arbitrary sources, since clients can set them to any value they like.

## Databases and caches

When you attach a database or cache from the infrastructure canvas, Cloud injects a `DATABASE_URL` (`postgresql://...` or `mysql://...`) or `REDIS_URL` (`rediss://...`) variable into your application's environment. You may read these values with `os.Getenv`.

For Postgres, you may pass the connection URL straight to [pgx](https://pkg.go.dev/github.com/jackc/pgx/v5/pgxpool):

```go theme={null}
pool, err := pgxpool.New(ctx, os.Getenv("DATABASE_URL"))
if err != nil {
    log.Fatal(err)
}
defer pool.Close()
```

For Redis, [go-redis](https://pkg.go.dev/github.com/redis/go-redis/v9#ParseURL) can parse the URL for you, and it configures TLS automatically when it sees the `rediss://` scheme:

```go theme={null}
options, err := redis.ParseURL(os.Getenv("REDIS_URL"))
if err != nil {
    log.Fatal(err)
}

client := redis.NewClient(options)
defer client.Close()
```

The [MySQL driver](https://pkg.go.dev/github.com/go-sql-driver/mysql#Config) is a little different, since it expects its own DSN format rather than a URL. You may parse the connection URL and let `mysql.Config` build the DSN for you:

```go theme={null}
import (
    "database/sql"
    "errors"
    "net/url"
    "os"
    "strings"

    "github.com/go-sql-driver/mysql"
)

func connectMySQL() (*sql.DB, error) {
    u, err := url.Parse(os.Getenv("DATABASE_URL"))
    if err != nil || u.Scheme != "mysql" || u.User == nil || u.Host == "" {
        return nil, errors.New("DATABASE_URL must be a MySQL connection URL")
    }

    config := mysql.NewConfig()
    config.User = u.User.Username()
    config.Passwd, _ = u.User.Password()
    config.Net = "tcp"
    config.Addr = u.Host
    config.DBName = strings.TrimPrefix(u.Path, "/")
    config.ParseTime = true

    return sql.Open("mysql", config.FormatDSN())
}
```

If your application needs any driver-specific options, you may add them to the configuration before opening the connection.

## Migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live. If one of them fails, Cloud cancels the rollout.

If your application includes the `cmd/migrate` executable from the [build example](#compile-during-the-build), your deploy command is:

```sh theme={null}
./migrate
```

If you prefer a separate migration tool, install or compile it during your build, then use its command here instead.
