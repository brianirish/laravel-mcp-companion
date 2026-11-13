Source: https://laravel.com/cloud/docs/deploy-guides/nuxt.md

# Nuxt deploy guide

Configure your Nuxt application for production on Laravel Cloud.

The [Nuxt quickstart](https://laravel.com/cloud/docs/quickstart#nuxt) walks you through your first deployment to Laravel Cloud. Cloud already knows how to build and start a Nuxt application. This guide focuses on the handful of things that are still yours to decide, such as how Nuxt renders your application, how your configuration reaches the browser, and where your data lives. Each section links to the full documentation if you would like to dig deeper.

## Choose a runtime version

Cloud can run your Nuxt application on Node.js, Bun, or Deno, and it detects the right runtime from the files in your repository. A `package-lock.json` file selects Node.js, a `bun.lock`, `bun.lockb`, or `bunfig.toml` file selects Bun, and a `deno.json` or `deno.lock` file selects Deno.

You may choose your Node.js, Bun, or Deno version from the Runtime section of your environment's General Settings page. After changing it, redeploy your environment so the new version takes effect. You can find the supported versions in the [Runtimes](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno) documentation.

## Build your application

When you create your application, you choose whether Nuxt should run as a server or be generated as a static site. Your environment's [build commands](https://laravel.com/cloud/docs/environments#build-commands) should match that choice. For a server-rendered application, install your dependencies and build:

```sh theme={null}
npm ci --audit false
npm run build
```

For static site generation, use `npx nuxt generate` in place of `npm run build`. If you prefer Yarn, pnpm, or Bun over npm, take a look at [Using Yarn, PNPM, or Bun](https://laravel.com/cloud/docs/knowledge-base/using-yarn-bun-pnpm).

## Use the default Nitro preset

Cloud serves Nuxt applications using Nitro's default `node-server` preset, which builds your server to `.output/server/index.mjs`. Nitro detects this preset automatically, so you usually don't need to configure anything.

However, if your application was previously deployed to another host, your `nuxt.config` file may still set a host-specific `nitro.preset`, such as `vercel`, `netlify`, or `cloudflare`. The same is true if a `NITRO_PRESET` environment variable is set. In either case, the build still succeeds, but it produces output that Cloud can't serve. Your deployment then goes live without receiving any traffic. Remove both before you deploy.

## Start your application

Cloud starts your application by running `.output/server/index.mjs` with `node`, `bun run`, or `deno run -A`, depending on your runtime. You may override the start command from your environment's deployment settings if needed.

Cloud routes traffic to your application on the port set by the `PORT` environment variable, and Nitro's server reads this variable automatically. Nitro also listens on all available network interfaces unless you set a `HOST` or `NITRO_HOST` variable. Cloud's startup probes reach your application over IPv6, so leave these variables unset rather than pointing them at an IPv4-only address such as `0.0.0.0`. If your application deploys successfully but still isn't reachable, take a look at the [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide.

## Environment variables

You may add your environment variables from your environment's [settings](https://laravel.com/cloud/docs/environments#environment-variables). Cloud sets them directly on your application's process, so your server code can read them just like it does locally.

Variables prefixed with `NUXT_PUBLIC_` are available on the client, while all other variables stay on the server. Nuxt uses these variables to override the matching keys in your application's [runtime config](https://nuxt.com/docs/guide/going-further/runtime-config) when it starts, so you can change them without rebuilding your application. Redeploy so the new values reach your instances.

In addition to your own variables, Cloud automatically sets `NODE_ENV=production` and `NUXT_PUBLIC_SITE_URL`, which contains your application's URL, on every deployment.

## Attach a database or cache

When you attach a [database](https://laravel.com/cloud/docs/resources/databases/postgres) or [cache](https://laravel.com/cloud/docs/resources/caches/valkey) from your environment's infrastructure canvas, Cloud injects a `DATABASE_URL` or `REDIS_URL` connection string into your environment. Most database libraries and ORMs, including Prisma and Drizzle, accept these URLs directly. The [Node.js deploy guide](https://laravel.com/cloud/docs/deploy-guides/nodejs#databases-and-caches) includes examples for several popular clients.

Cloud resets your environment's [filesystem](https://laravel.com/cloud/docs/environments#filesystem) each time you deploy, and each replica of your application has its own disk. Because of this, anything your application needs to share or keep, such as sessions or cached data, should live in an attached database or cache rather than on disk. If you use Nitro's storage layer, you may configure it with a [Redis driver](https://nitro.build/docs/storage) that points at your cache.

## Store files in object storage

For user uploads and any other files your application needs to keep, attach a [bucket](https://laravel.com/cloud/docs/resources/object-storage) to your environment as its default disk. Cloud injects the `AWS_BUCKET`, `AWS_ENDPOINT_URL`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` variables. When you create your S3 client with the AWS SDK for JavaScript, pass the endpoint explicitly:

```js theme={null}
import { S3Client } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  region: process.env.AWS_REGION,
  endpoint: process.env.AWS_ENDPOINT_URL,
});
```

## Run migrations

Database migrations belong in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands). Cloud runs these commands just before your new deployment goes live. If one of them fails, Cloud cancels the rollout. For example, if you are using Prisma, your deploy command might look like this:

```sh theme={null}
npx prisma migrate deploy
```

Keep in mind that deploy commands must finish within 15 minutes, and Cloud does not keep any changes they make to the filesystem.
