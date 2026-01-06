# Vapor - Projects/Deployments

*Source: https://docs.vapor.build/projects/deployments*

---

[Laravel Vapor home page![light logo](https://mintcdn.com/vapor/xzCd7jrV_PrTp5n0/logo/light.svg?fit=max&auto=format&n=xzCd7jrV_PrTp5n0&q=85&s=b75f22b35cd4eb8d659a33a7efe9a317)![dark logo](https://mintcdn.com/vapor/xzCd7jrV_PrTp5n0/logo/dark.svg?fit=max&auto=format&n=xzCd7jrV_PrTp5n0&q=85&s=bbbfac3aab3d7a07d5382ee8fa9a669e)](https://vapor.laravel.com)

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...

Navigation

Projects

Deployments

[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com)

##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

On this page

- [Introduction](#introduction)
- [Initiating Deployments](#initiating-deployments)
- [Build Hooks](#build-hooks)
- [Deploy Hooks](#deploy-hooks)
- [Reviewing Output / Logs](#reviewing-output-%2F-logs)
- [Assets](#assets)
- [Custom Asset Domains](#custom-asset-domains)
- [Referencing Assets From JavaScript](#referencing-assets-from-javascript)
- [Asset Compilation](#asset-compilation)
- [Code Splitting / Dynamic Imports With Mix](#code-splitting-%2F-dynamic-imports-with-mix)
- [Hot Module Replacement With Mix](#hot-module-replacement-with-mix)
- [URLs Within CSS](#urls-within-css)
- [Root Domain Assets](#root-domain-assets)
- [Dot Files As Assets](#dot-files-as-assets)
- [Root Domain robots.txt](#root-domain-robots-txt)
- [Redeploying](#redeploying)
- [Rollbacks](#rollbacks)
- [Deploying From CI](#deploying-from-ci)
- [Git Commit Information](#git-commit-information)
- [Example With GitHub Actions](#example-with-github-actions)
- [Docker Arm Runtime](#docker-arm-runtime)
- [Example With Chipper CI](#example-with-chipper-ci)

Projects

# Deployments

Learn how to deploy your Laravel applications to Laravel Vapor.

## [​](#introduction) Introduction

Of course, one of the primary features of Laravel Vapor is atomic, zero-downtime deployments. Unlike many other features of Vapor, deployments are **only initiated via the Vapor CLI**. During deployment, Vapor will run the `build` steps of your `vapor.yml` file on the local machine that the deployment is running on. This might be your personal machine or a continuous integration platform.

## [​](#initiating-deployments) Initiating Deployments

To initiate a deployment, execute the `deploy` CLI command from the root of your application:

Copy

Ask AI

```
vapor deploy production
```

By default, when you run `vapor deploy production`, Vapor will look for a `vapor.yml` manifest file. However, you can specify a custom manifest using the `--manifest` option:

Copy

Ask AI

```
vapor deploy production --manifest vapor-eu-west-1.yml
```

AWS Lambda has strict limitations on the size of applications running within the environment. If your application exceeds this limit, you may take advantage of Vapor’s [Docker based deployments](/projects/environments#building-custom-docker-images). Docker based deployments allow you to package and deploy applications up to 10GB in size.

## [​](#build-hooks) Build Hooks

You may define build hooks for an environment using the `build` key within your `vapor.yml` file. These commands are executed on the local machine that the deployment is running on and may be used to prepare your application for deployment. During deployment, your application is built within a temporary `.vapor` directory that is created by the CLI and all of your `build` commands will run within that temporary directory:

vapor.yml

Copy

Ask AI

```
id: 3
name: vapor-app
environments:
  production:
    memory: 1024
    database: vapor-app
    cache: vapor-cache
    build:
      - 'composer install --no-dev'
      - 'php artisan event:cache'
    deploy:
      - 'php artisan migrate --force'
```

## [​](#deploy-hooks) Deploy Hooks

You may define deployment hooks for an environment using the `deploy` key within your `vapor.yml` file. These commands are executed against the deployed environment **before it is activated for general availability**. If any of these commands fail, the deployment will not be activated.

vapor.yml

Copy

Ask AI

```
id: 3
name: vapor-app
environments:
  production:
    memory: 1024
    database: vapor-app
    cache: vapor-cache
    build:
      - 'composer install --no-dev'
      - 'php artisan event:cache'
    deploy:
      - 'php artisan migrate --force'
```

### [​](#reviewing-output-/-logs) Reviewing Output / Logs

When a deployment hook fails, you may review the output / logs via the Vapor UI’s deployment detail screen.
Also, if you are deploying your application using the `vapor deploy` command, the CLI output will contain the failing hook output. Of course, you may review the output at any time using the `hook:output` command:

Copy

Ask AI

```
vapor hook:output {DEPLOYMENT_HOOK_ID}
```

You can review the logs associated with the failing hook using the `hook:log` command:

Copy

Ask AI

```
vapor hook:log {DEPLOYMENT_HOOK_ID}
```

[Native Vapor runtimes](/projects/environments#runtime) do not support [squashed migrations](https://laravel.com/docs/migrations#squashing-migrations). If you wish to utilize this feature of Laravel, you may take advantage of Vapor’s [Docker based deployments](/projects/environments#docker-runtimes)

## [​](#assets) Assets

During deployment, Vapor will automatically extract all of the assets in your Laravel project’s `public` directory and upload them to S3. In addition, Vapor will create a AWS CloudFront (CDN) distribution to distribute these assets efficiently around the world.
Because all of your assets will be served via S3 / CloudFront, you should always generate URLs to these assets using Laravel’s `asset` helper. Vapor injects an `ASSET_URL` environment variable which Laravel’s `asset` helper will use when constructing your URLs:

Copy

Ask AI

```
<img src="{{ asset('img.jpg') }}">
```

On subsequent deployments, only the assets that have changed will be uploaded to S3, while unchanged assets will be copied over from the previous deployment.

### [​](#custom-asset-domains) Custom Asset Domains

If you would like to use your own domain to serve your assets, you may do so by attaching a custom asset domain to your project. First, you should [ensure a DNS zone exists](/projects/domains.html#adding-domains) for the domain and that a [certificate is issued](/projects/domains.html#requesting-ssl-certificates) for the domain in the `us-east-1` region.
Next, set the `asset-domain` option of your `vapor.yml` file to your chosen domain:

Copy

Ask AI

```
id: 3
name: vapor-app
asset-domain: assets.laravel.rocks
environments:
  production:
    ...
```

During a subsequent deployment of any environment associated with your project, Vapor will add the custom domain as an alias to your CloudFront distribution. Vapor will also inject the relevant environment variables for the [asset helper](/projects/deployments#assets) and Vite asset compilation process to ensure your assets are served from your custom asset domain.

### [​](#referencing-assets-from-javascript) Referencing Assets From JavaScript

If you are referencing your project’s public assets in your JavaScript code, you may generate URLs to these assets using Vapor’s NPM package. This package includes a `Vapor.asset` helper that will behave like Laravel’s `asset` helper but on the client. To get started, install the `laravel-vapor` NPM package:

Copy

Ask AI

```
npm install --save-dev laravel-vapor
```

Next, within your application’s `app.js` file, initialize the global Vapor JavaScript object:

Copy

Ask AI

```
// Vite
import Vapor from 'laravel-vapor'
window.Vapor = Vapor

// Mix
window.Vapor = require('laravel-vapor');
```

Finally, you may call the `Vapor.asset` helper in your JavaScript code:

Copy

Ask AI

```
$('#container').prepend($('<img>', { src: Vapor.asset('avatar.png') }))
```

Or, if you are using Vue, you may find it convenient to add the following mixin to your Vue application:

Copy

Ask AI

```
Vue.mixin({
    methods: {
        asset: window.Vapor.asset
    },
});

// Within your Vue components...
<img :src="asset('img/global/logo.svg')"/>
```

If you are using Laravel Vite with your project, you only need to utilize the `asset` helper when you are referencing assets you don’t want bundled, such as those that already live in your public directory.If you want to use the `asset` helper with your Vite project, you will also need to specify the base URL for assets in your application’s entry point, for example in your `resources/js/app.js`, like so: `Vapor.withBaseAssetUrl(import.meta.env.VITE_VAPOR_ASSET_URL)`

### [​](#asset-compilation) Asset Compilation

If you are compiling your application’s assets in one of the build steps listed in your `vapor.yml` configuration file, you may need your build script to be able to access your environment variables. An excellent example of this requirement is instantiating a frontend SDK such as Pusher.
Build steps are executed in the environment where a deployment is initiated - typically, this will be your local machine or your CI pipeline. As such, you must ensure the required environment variables are available in that environment.
To assist with this, Vapor will attempt to load variables first from `.env.[environment]` (e.g. `.env.staging`). If that file does not exist, Vapor will attempt to load variables from the `.env` file. You should 

*[Content truncated for length]*