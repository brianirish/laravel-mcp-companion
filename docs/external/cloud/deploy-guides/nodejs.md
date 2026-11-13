Source: https://laravel.com/cloud/docs/deploy-guides/nodejs.md

# Node.js deploy guide

Configure your Express, Hono, or other Node.js application for production on Laravel Cloud.

The [Node.js quickstart](https://laravel.com/cloud/docs/quickstart#node-js) walks you through your first deployment to Laravel Cloud. Once your application is up and running, this guide will help you get it ready for production. We'll cover how to build, start, and configure your Express, Hono, or other Node.js application for Cloud.

## Choose a runtime version

Cloud can run your JavaScript application on Node.js, Bun, or Deno. There's nothing to configure here, since Cloud detects the right runtime from the files in your repository:

| Runtime | Detected by |
| - | - |
| Bun | `bun.lock`, `bun.lockb`, or `bunfig.toml` |
| Deno | `deno.json` or `deno.lock` |
| Node.js | `package-lock.json` |

You may choose your Node.js, Bun, or Deno version from the **Runtime** section of your environment's **General Settings** page. After changing it, redeploy your environment so the new version takes effect. If you're using Node.js, it's also a good idea to keep the `engines` field in your `package.json` compatible with the version you select. You can find the supported versions in the [Runtimes](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno) documentation.

## Listen on the right port

Cloud routes traffic to your application on the port set by the `PORT` environment variable. This is `3000` by default, or the port you chose when creating your application. Your application should read this value and leave the host out of its listen call:

```js theme={null}
app.listen(process.env.PORT || 3000);
```

When you don't pass a host, Node.js listens on all of the available IPv4 and IPv6 interfaces. Cloud's startup probes reach your application over IPv6. If you pass an IPv4-only host such as `0.0.0.0`, or a loopback-only host such as `127.0.0.1` or `localhost`, Cloud won't be able to reach your application.

If you are using Hono on Node.js, you will start your server through `@hono/node-server`:

```js theme={null}
import { serve } from "@hono/node-server";

serve({ fetch: app.fetch, port: Number(process.env.PORT) || 3000 });
```

If your application deploys successfully but still isn't reachable, take a look at the [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide.

## Install and compile during the build

By default, Cloud pre-fills a build command that installs your application's dependencies:

```sh theme={null}
npm ci --audit false
```

If your application has a compilation step, such as a TypeScript build, add it to your [build commands](https://laravel.com/cloud/docs/environments#build-commands):

```sh theme={null}
npm ci --audit false
npm run build
```

Prefer Yarn, pnpm, or Bun? You may swap these commands out by following the [Using Yarn, PNPM, or Bun](https://laravel.com/cloud/docs/knowledge-base/using-yarn-bun-pnpm) guide.

## Set the start command

Cloud also pre-fills a start command based on the `start` script or `main` entry in your `package.json`, such as `node server.js`. If neither of these points to a file, the start command falls back to `npm start`, `bun run start`, or `deno task start`, depending on your runtime.

Your start command should run your compiled output directly with `node`, such as `node dist/server.js`. When you keep compilation in your build commands, your application starts quickly when a new instance boots or when your environment wakes up after [scaling to zero](https://laravel.com/cloud/docs/compute#scale-to-zero), since there's nothing left to compile. Tools such as `nodemon`, `tsx watch`, and `ts-node` are great for development, but don't use them to run your application in production.

## Environment variables

Cloud sets your environment variables directly on your application's process, so you can read them from `process.env` just like you normally would. There's no need for a loader such as `dotenv`. Your build commands receive the same variables through a `.env` file in the build context.

In addition to your own variables, Cloud automatically sets `NODE_ENV=production` and `APP_URL`, which contains your application's URL, on every deployment. To add your own values, see the [environment variables](https://laravel.com/cloud/docs/environments#environment-variables) documentation.

A custom variable may refer to another variable with `${NAME}`, such as `CALLBACK_URL="${APP_URL}/auth/callback"`. Cloud resolves the reference before it sets the variable, so `process.env.CALLBACK_URL` holds the final URL. See [referencing other variables](https://laravel.com/cloud/docs/environments#referencing-other-variables) for which variables you can reference.

## Shut down gracefully

When an instance stops, whether during a deployment or while scaling down, Cloud sends a `SIGTERM` signal to your process. To avoid cutting off requests that are still in progress, your application should handle this signal and wait for those requests to finish before exiting:

```js theme={null}
const server = app.listen(process.env.PORT || 3000);

process.on("SIGTERM", () => {
  server.close(() => process.exit(0));

  setTimeout(() => process.exit(1), 25_000).unref();
});
```

Here, `server.close` stops accepting new connections and invokes its callback once all of the active connections have ended. The fallback timer makes sure your process exits even if a connection lingers. Keep this timer shorter than your environment's **graceful shutdown timeout** so the rest of the instance has time to stop cleanly. Once that timeout passes, Cloud terminates any process that is still running.

## Running behind the proxy

Cloud handles TLS for you before forwarding requests to your application, so your server only needs to speak plain HTTP. Cloud's proxy passes the original request scheme in the `X-Forwarded-Proto` header and the client's address chain in the `X-Forwarded-For` header.

Before relying on these headers to determine the request scheme or client IP address, you should configure your framework's trusted proxy settings. In Express, you may tell your application to trust the proxy running alongside it, which allows `req.protocol` and `req.secure` to reflect the original scheme:

```js theme={null}
app.set("trust proxy", 1);
```

Express's [proxy documentation](https://expressjs.com/en/guide/behind-proxies.html) describes the other available options. In general, you should avoid trusting forwarded headers from arbitrary sources, since clients can set them to any value they like.

## Databases and caches

When you attach a database or cache from the infrastructure canvas, Cloud injects a `DATABASE_URL` (`postgresql://...` or `mysql://...`) or `REDIS_URL` (`rediss://...`) variable into your application's environment. Most popular libraries accept these URLs directly, so connecting usually takes just a line or two of code.

For Postgres, you may pass the connection URL straight to [node-postgres](https://node-postgres.com/features/connecting):

```js theme={null}
import pg from "pg";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
```

For MySQL, [mysql2](https://sidorares.github.io/node-mysql2/docs) accepts the connection URL as well:

```js theme={null}
import mysql from "mysql2/promise";

const pool = mysql.createPool(process.env.DATABASE_URL);
```

For Redis, [node-redis](https://redis.io/docs/latest/develop/clients/nodejs/) will automatically configure TLS when it sees the `rediss://` scheme:

```js theme={null}
import { createClient } from "redis";

const client = createClient({ url: process.env.REDIS_URL });

await client.connect();
```

If you are using an ORM such as Prisma or Drizzle, you may point its configuration at `DATABASE_URL` as well.

## Object storage

When you attach a [bucket](https://laravel.com/cloud/docs/resources/object-storage) as your environment's default disk, Cloud injects the `AWS_BUCKET`, `AWS_ENDPOINT_URL`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` variables. When creating your S3 client with the AWS SDK for JavaScript, be sure to pass the endpoint explicitly:

```js theme={null}
import { S3Client } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  region: process.env.AWS_REGION,
  endpoint: process.env.AWS_ENDPOINT_URL,
});
```

You don't need to pass the access keys yourself, since the SDK reads them from the environment automatically.

## Migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live. If one of them fails, Cloud cancels the rollout. Keep in mind that deploy commands must finish within 15 minutes, and any changes they make to the filesystem will not be kept.

For example, if you are using Prisma, your deploy command might look like this:

```sh theme={null}
npx prisma migrate deploy
```

## Background processes

If your application needs a queue consumer or another long-running process alongside your web server, you may add it as a [custom background process](https://laravel.com/cloud/docs/workers#custom-background-processes):

```sh theme={null}
node worker.js
```

Cloud monitors your background processes and automatically restarts them if they exit unexpectedly.
