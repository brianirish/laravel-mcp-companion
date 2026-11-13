Source: https://laravel.com/cloud/docs/deploy-guides/nextjs.md

# Next.js deploy guide

Configure your Next.js application for production on Laravel Cloud.

The [Next.js quickstart](https://laravel.com/cloud/docs/quickstart#next-js) walks you through your first deployment to Laravel Cloud. Cloud already knows how to build and start a Next.js application. This guide focuses on the handful of things that are still yours to decide, such as how your environment variables reach the browser, where your data lives, and how you migrate your database. Each section links to the full documentation if you would like to dig deeper.

## Choose a runtime version

Cloud can run your Next.js application on Node.js, Bun, or Deno, and it detects the right runtime from the files in your repository. A `package-lock.json` file selects Node.js, a `bun.lock`, `bun.lockb`, or `bunfig.toml` file selects Bun, and a `deno.json` or `deno.lock` file selects Deno.

You may choose your Node.js, Bun, or Deno version from the Runtime section of your environment's General Settings page. After changing it, redeploy your environment so the new version takes effect. You can find the supported versions in the [Runtimes](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno) documentation.

## Build your application

Your environment's [build commands](https://laravel.com/cloud/docs/environments#build-commands) run each time you deploy. Typically, they install your dependencies and compile your application:

```sh theme={null}
npm ci --audit false
npm run build
```

If you prefer Yarn, pnpm, or Bun over npm, take a look at [Using Yarn, PNPM, or Bun](https://laravel.com/cloud/docs/knowledge-base/using-yarn-bun-pnpm).

## Start your application

Cloud starts your application by running the `start` script defined in your `package.json` file, which is usually `next start`. If you are using the Deno runtime, Cloud runs `deno task start` instead. You may override the start command from your environment's deployment settings if needed.

Cloud routes traffic to your application on the port set by the `PORT` environment variable. The `next start` command reads this variable automatically, so most applications work without any changes. However, if you have replaced `next start` with a custom server, such as an Express server in a `server.js` file, make sure that server reads `PORT` rather than listening on a hardcoded port. Otherwise, your deployment succeeds but doesn't receive any traffic. The [deployment troubleshooting](https://laravel.com/cloud/docs/deployments#deployment-succeeds-but-serves-no-traffic) guide has more details.

## Environment variables

You may add your environment variables from your environment's [settings](https://laravel.com/cloud/docs/environments#environment-variables). Cloud sets them directly on your application's process, so your server code can read them from `process.env` just like it does locally.

Variables prefixed with `NEXT_PUBLIC_` are also available in the browser, while all other variables stay on the server. Keep in mind that Next.js inlines `NEXT_PUBLIC_` values into your JavaScript when your application is built. Your build commands receive your environment variables through a `.env` file, so these values are available during the build. Whenever you change one, redeploy so Next.js compiles the new value into your application.

In addition to your own variables, Cloud automatically sets `NODE_ENV=production` and `NEXT_PUBLIC_SITE_URL`, which contains your application's URL, on every deployment.

## Attach a database or cache

When you attach a [database](https://laravel.com/cloud/docs/resources/databases/postgres) or [cache](https://laravel.com/cloud/docs/resources/caches/valkey) from your environment's infrastructure canvas, Cloud injects a `DATABASE_URL` or `REDIS_URL` connection string into your environment. Most database libraries and ORMs, including Prisma and Drizzle, accept these URLs directly. The [Node.js deploy guide](https://laravel.com/cloud/docs/deploy-guides/nodejs#databases-and-caches) includes examples for several popular clients.

Cloud resets your environment's [filesystem](https://laravel.com/cloud/docs/environments#filesystem) each time you deploy, and each replica of your application has its own disk. Because of this, anything your application needs to share or keep, such as sessions or cached data, should live in an attached database or cache rather than on disk.

The same applies to Next.js's own data cache and incremental static regeneration. By default, Next.js stores these on the local filesystem, so each replica keeps its own copy and every deployment clears the cache. If your application relies on revalidated pages staying consistent across replicas, configure a [custom cache handler](https://nextjs.org/docs/app/api-reference/config/next-config-js/incrementalCacheHandlerPath) backed by your cache.

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
