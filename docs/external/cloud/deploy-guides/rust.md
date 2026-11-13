Source: https://laravel.com/cloud/docs/deploy-guides/rust.md

# Rust deploy guide

Configure your Rust application for production on Laravel Cloud.

The [Rust quickstart](https://laravel.com/cloud/docs/quickstart#rust) walks you through your first deployment to Laravel Cloud. Once your application is up and running, this guide helps you get it ready for production. We'll cover how to compile your Rust application, start it, and configure it so that it runs smoothly on Cloud.

## Listen on the right port

Cloud routes traffic to your application on the port set by the `PORT` environment variable, which is `3000` by default. Have your application read this value and listen on the IPv6 wildcard address, `::`:

```rust theme={null}
use std::net::SocketAddr;

let port: u16 = std::env::var("PORT")
    .ok()
    .and_then(|port| port.parse().ok())
    .unwrap_or(3000);

let addr = SocketAddr::from(([0u16; 8], port));
let listener = tokio::net::TcpListener::bind(addr).await.unwrap();

axum::serve(listener, app).await.unwrap();
```

On Linux, binding to `::` accepts both IPv6 and IPv4 connections. Binding to `::` matters because Cloud's startup probes reach your application over IPv6. If you bind to `0.0.0.0` or `127.0.0.1`, Cloud can't reach your application, and the deployment fails its startup probe. Actix Web accepts the same address as a string, for example `.bind(("::", port))`.

Rocket reads its own `ROCKET_ADDRESS` and `ROCKET_PORT` variables rather than `PORT`. Cloud sets both for you, so a Rocket application only needs to use its default configuration.

If your application deploys successfully but still isn't reachable, take a look at the [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide.

## Compile during the build

Cloud detects your application from the `Cargo.toml` file at the root of your repository and recognizes axum, Actix Web, Rocket, and warp from your dependencies. Cloud downloads your crates automatically and pre-fills the following build command:

```sh theme={null}
cargo build --release
```

Cloud copies the executables from your release output into `/var/www/bin` and adds that directory to your `PATH`. Cloud leaves the compiled build directory out of the image that runs your application, so your instances stay small and quick to start. Of course, if your application has additional requirements, you're free to edit the build command.

Cloud detects which binary to run from your `Cargo.toml` and sets the start command when you create your environment. Cloud chooses the binary named by `default-run`, then the one built from `src/main.rs`, then the only binary if there is just one. If none of these apply, Cloud runs the first executable it finds in `/var/www/bin`, sorted alphabetically. To be explicit, set `default-run` in your manifest before you create the environment:

```toml theme={null}
[package]
name = "my-app"
default-run = "my-app"
```

Cloud doesn't detect the binary again after your environment exists. If you add or change `default-run` later, update your environment's start command to match, for example `my-app`.

Each environment keeps its compiled output between builds, so a binary you have renamed or removed may remain in `/var/www/bin` and on your `PATH`. Naming your binary in the start command, rather than relying on the alphabetical fallback, keeps Cloud from running a stale one.

Since your binaries are on the `PATH`, you may refer to them by name in your start command, [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands), and [background processes](https://laravel.com/cloud/docs/workers). For example, if your application builds both a `my-app` and a `migrate` binary, you may run `my-app serve` or `migrate` without spelling out the full path.

Because you compile in your [build commands](https://laravel.com/cloud/docs/environments#build-commands), there's nothing left to compile at runtime. Your application starts quickly when a new instance boots or when your environment wakes up after [scaling to zero](https://laravel.com/cloud/docs/compute#scale-to-zero).

Cloud caches your downloaded crates and compiled dependencies between builds of the same environment, so later builds can recompile only what changed. The cache is best effort, so an occasional build may start from scratch. To make the most of the cache, commit your `Cargo.lock` file.

Release builds can take a while on larger applications. Build commands must complete within 15 minutes, so you may want to tune your release profile for compile time if you approach that limit.

> [!NOTE]
>
> Build commands run without root privileges, so you can't install system packages with `apt-get`. When a crate offers a choice, prefer pure Rust options, such as `rustls` instead of OpenSSL.

## Rust versions

Cloud builds your application with a recent stable Rust release, and there is no version setting to manage. If you need a specific toolchain, pin it with a `rust-toolchain.toml` file at the root of your repository. The `rustup` tool installs the pinned toolchain during your build:

```toml theme={null}
[toolchain]
channel = "1.90.0"
```

## Shut down gracefully

When an instance stops, whether during a deployment or while scaling down, Cloud sends a `SIGTERM` signal to your process. To avoid cutting off requests that are still in progress, handle this signal in your application and wait for those requests to finish before exiting. The `tokio::signal::ctrl_c` function listens only for `SIGINT`, so also listen for `SIGTERM`. If you are using axum, you may use the following function with `with_graceful_shutdown`:

```rust theme={null}
use tokio::signal::unix::{signal, SignalKind};

async fn shutdown_signal() {
    let mut sigterm = signal(SignalKind::terminate()).expect("failed to install SIGTERM handler");
    let mut sigint = signal(SignalKind::interrupt()).expect("failed to install SIGINT handler");

    tokio::select! {
        _ = sigterm.recv() => {},
        _ = sigint.recv() => {},
    }
}

axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await
    .unwrap();
```

Your process keeps running until the in-flight requests have finished. Actix Web and Rocket also stop on `SIGTERM`. For warp, pass the same `shutdown_signal` future to `bind_with_graceful_shutdown`. Keep your application's shutdown timeout shorter than your environment's **graceful shutdown timeout** (30 seconds by default) so the rest of the instance has time to stop cleanly. Once that timeout passes, Cloud terminates any process that is still running. Actix Web also waits 30 seconds by default, so lower its timeout with `HttpServer::shutdown_timeout`.

## Logging

Anything your application writes to standard output or standard error, including panic messages, appears in your environment's [logs](https://laravel.com/cloud/docs/logs). The [tracing-subscriber](https://docs.rs/tracing-subscriber) crate writes to standard output by default, so a single line of setup is enough:

```rust theme={null}
tracing_subscriber::fmt().init();

tracing::info!(order_id = 1234, "order shipped");
```

If you would rather log each entry as a single JSON object, enable the `json` feature of `tracing-subscriber` and call `.json()` on the builder.

## Running behind the proxy

Cloud handles TLS for you before forwarding requests to your application, so your server only needs to speak plain HTTP. Cloud's proxy also passes the original request scheme in the `X-Forwarded-Proto` header and the client's address chain in the `X-Forwarded-For` header.

Before relying on these headers to determine the request scheme or client IP address, configure your framework or middleware to trust them only when a request comes through Cloud's proxy. In general, avoid trusting forwarded headers from arbitrary sources, since clients can set them to any value they like.

## Databases and caches

When you attach a database or cache from the infrastructure canvas, Cloud injects a `DATABASE_URL` (`postgresql://...` or `mysql://...`) or `REDIS_URL` (`rediss://...`) variable into your application's environment. You may read these values with `std::env::var`.

For Postgres and MySQL, [sqlx](https://docs.rs/sqlx) accepts the connection URL as is. Enable the `runtime-tokio` and `tls-rustls` features, along with the feature for your database (`postgres` or `mysql`):

```rust theme={null}
let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");

let pool = sqlx::postgres::PgPoolOptions::new()
    .max_connections(10)
    .connect(&database_url)
    .await?;
```

For Redis, the [redis](https://docs.rs/redis) crate configures TLS automatically when it sees the `rediss://` scheme, provided you enable its `tokio-rustls-comp` feature:

```rust theme={null}
let client = redis::Client::open(std::env::var("REDIS_URL")?)?;
let mut connection = client.get_multiplexed_async_connection().await?;
```

## Migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live. If one of them fails, Cloud cancels the rollout.

If you use sqlx, you may embed your migrations in a small binary that lives alongside your application at `src/bin/migrate.rs`, so there's no extra tooling to install. The binary needs sqlx's `migrate` and `macros` features, and this example uses Postgres. For MySQL, use `sqlx::MySqlPool` instead:

```rust theme={null}
#[tokio::main]
async fn main() -> Result<(), sqlx::Error> {
    let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = sqlx::PgPool::connect(&database_url).await?;

    sqlx::migrate!("./migrations").run(&pool).await?;

    Ok(())
}
```

Because Cloud builds this binary with the rest of your package and adds it to your `PATH`, your deploy command is:

```sh theme={null}
migrate
```

If you prefer a separate migration tool, install it during your build, then use its command here instead.

Cloud records the output of your deploy commands with each deployment rather than in your environment's logs.
