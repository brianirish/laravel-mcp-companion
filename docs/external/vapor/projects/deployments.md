# Vapor - Projects/Deployments

*Source: https://docs.vapor.build/projects/deployments*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)
[Laravel Vapor home page](https://vapor.laravel.com)
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)
Search...
Navigation
Projects
Deployments
[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)
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
- [Migrate to Cloud](/resources/migrate-to-cloud)
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
To assist with this, Vapor will attempt to load variables first from `.env.[environment]` (e.g. `.env.staging`). If that file does not exist, Vapor will attempt to load variables from the `.env` file. You should ensure one of these file contains all of the environment variables needed by that environment’s build script.
When using CI platforms, you may not have access to the environment files as these are typically omitted from version control. In this scenario, your CI provider will typically provide a mechanism for injecting variables into the build pipeline. For instance, with GitHub Actions, your GitHub Action configuration might look like the following:
Copy
Ask AI
```
- name: Deploy Environment
    run: vapor deploy production
    env:
      VITE_PUSHER_APP_KEY: ${{ secrets.VITE_PUSHER_APP_KEY }}
```
When using Vite and running `npm run build`, Vite will always use the `.env.production` file if it is present, even if you are deploying a different environment. If you maintain multiple environment files in your deployment environment, you should set the Vite build mode explicitly:
Copy
Ask AI
```
npm run build -- --mode staging
```
### [​](#code-splitting-/-dynamic-imports-with-mix) Code Splitting / Dynamic Imports With Mix
If you are taking advantage of JavaScript dynamic imports and code splitting in your project via Laravel Mix, you will need to let Webpack know where the child chunks will be loaded from for each deployment. To accomplish this, you can take advantage of the `ASSET_URL` variable that Laravel Vapor injects into your environment during your build step:
Copy
Ask AI
```
const mix = require("laravel-mix");

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

mix
    .js("resources/js/app.js", "public/js")
    .sass("resources/sass/app.scss", "public/css");

if (mix.inProduction()) {
    const ASSET_URL = process.env.ASSET_URL + "/";

    mix.webpackConfig(webpack => {
        return {
            plugins: [
                new webpack.DefinePlugin({
                    "process.env.ASSET_PATH": JSON.stringify(ASSET_URL)
                })
            ],
            output: {
                publicPath: ASSET_URL
            }
        };
    });
}
```
### [​](#hot-module-replacement-with-mix) Hot Module Replacement With Mix
If you are using code splitting and “hot module replacement” with Laravel Mix during local development, you will need to use the `mix` helper locally and the `asset` helper when deploying to Vapor:
Copy
Ask AI
```
@if (app()->environment('local'))
    <link href="{{ mix('css/admin/app.css') }}" rel="stylesheet">
    <script src="{{ mix('js/admin/app.js') }}"></script>
@else
    <link href="{{ asset('css/admin/app.css') }}" rel="stylesheet">
    <script src="{{ asset('js/admin/app.js') }}" defer></script>
@endif
```
### [​](#urls-within-css) URLs Within CSS
Sometimes, your CSS may need to reference asset URLs, such as a `background-image` property that references an image via URL. Obviously, you are not able to use the PHP `asset` helper within your CSS. For this reason, Vapor will automatically prepend the correct asset base URL to all relative URLs in your CSS during the build process. After your build steps have executed, Vapor performs this action against any CSS files in your application’s `public` directory (including directories nested under `public`).
### [​](#root-domain-assets) Root Domain Assets
Some applications, such as PWAs, may need to serve certain assets from the root domain. If your application has this need, you can define an array of assets that should be served from your application’s root domain via the `serve_assets` configuration option within your `vapor` configuration file:
Copy
Ask AI
```
/*
|--------------------------------------------------------------------------
| Servable Assets
|--------------------------------------------------------------------------
|
| Here you can configure list of public assets that should be servable
| from your application's domain instead of only being servable via
| the public S3 "asset" bucket or the AWS CloudFront CDN network.
|
*/

'serve_assets' => [
    'serviceWorker.js',
],
```
If your application doesn’t contain a `vapor` configuration file, you can publish it using the `vendor:publish` Artisan command:
Copy
Ask AI
```
php artisan vendor:publish --tag=vapor-config
```
Due to the serverless nature of applications powered by Vapor, assets served from the root domain are not cacheable at the client-side and they are served using Laravel routes. Therefore, you should only serve assets that absolutely must be served from the root domain as there is a slight performance penalty for doing so.
### [​](#dot-files-as-assets) Dot Files As Assets
Typically, “dot” files are not uploaded to the AWS CloudFront CDN by Vapor. However, if you need the public directory’s dot files to be uploaded as assets, you should set the `dot-files-as-assets` key to `true` in your `vapor.yml` file:
Copy
Ask AI
```
id: 1
name: app-test
dot-files-as-assets: true
```
You may also choose to serve asset dot files from the application’s root domain:
Copy
Ask AI
```
'serve_assets' => [
    'serviceWorker.js',
    '.well-known/assetlinks.json',
],
```
### [​](#root-domain-robots-txt) Root Domain robots.txt
By default, Vapor will redirect requests to your application’s `robots.txt` file to the S3 asset bucket or CloudFront’s asset URL. If you would like the `robots.txt` file to be served directly from your application, you may set the `redirect_robots_txt` configuration value to `false` within your application’s `config/vapor.php` configuration file:
Copy
Ask AI
```
'redirect_robots_txt' => false,
```
If your application doesn’t contain a `vapor` configuration file, you can publish it using the `vendor:publish` Artisan command:
Copy
Ask AI
```
php artisan vendor:publish --tag=vapor-config
```
## [​](#redeploying) Redeploying
Sometimes you may need to simply redeploy a given environment without rebuilding it. For example, you may wish to do this after updating an environment variable. To accomplish this, you may use the Vapor UI or the `redeploy` CLI command:
Copy
Ask AI
```
vapor redeploy production
```
## [​](#rollbacks) Rollbacks
To rollback to a previous deployment, you may select the deployment in the Vapor UI and click the “Rollback To” button, or you may use the `rollback` CLI command. The `rollback` command’s “—select” option will allow you to select which deployment to rollback to from a list of recent deployments. If the `rollback` command is executed without this option, it will simply rollback to the most previous successful deployment:
Copy
Ask AI
```
vapor rollback production

vapor rollback production --select
```
When rolling back to a previous deployment, Vapor will use the environment’s variables and secrets as they existed at the time the deployment you’re rolling back to was originally deployed.
## [​](#deploying-from-ci) Deploying From CI
So far, we have discussed deploying Vapor projects from your local command line. However, you may also deploy them from a CI platform of your choice. Since the Vapor CLI client is part of your Composer dependencies, you may simply execute the `vapor deploy` command in your CI platform’s deployment pipeline.
In order to authenticate with Vapor from your CI platform, you will need to add a `VAPOR_API_TOKEN` environment variable to your CI build environment. You may generate an API token in your [Vapor API settings dashboard](https://vapor.laravel.com/app/account/api-tokens).
### [​](#git-commit-information) Git Commit Information
Some CI platforms expose the Git commit information as environment variables during your build. You may pass this information to the `vapor deploy` command. For example, if using CodeShip:
Copy
Ask AI
```
vapor deploy production --commit="${CI_COMMIT_ID}" --message="${CI_MESSAGE}"
```
The commit hash will be injected into your application’s environment variables as `VAPOR_COMMIT_HASH`.
### [​](#example-with-github-actions) Example With GitHub Actions
If your application uses [GitHub Actions](https://github.com/features/actions) as its CI platform, the following guidelines will assist you in configuring Vapor deployments so that your application is automatically deployed when someone pushes a commit to the `master` branch:
1. First, add the `VAPOR_API_TOKEN` environment variable to your “GitHub > Project Settings > Secrets” settings so that GitHub can authenticate with Vapor while running actions.
2. Next, create a `deploy.yml` file within the `your-project/.github/workflows` directory. The file should have the following contents:
Copy
Ask AI
```
name: Deploy

on:
  push:
    branches: [ master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.5
          tools: composer:v2
          coverage: none
      - name: Require Vapor CLI
        run: composer global require laravel/vapor-cli
      - name: Install Project Dependencies
        run: composer install --no-interaction --prefer-dist --optimize-autoloader
      - name: Deploy Environment
        run: vapor deploy production --commit="${{ github.sha }}" --message="${{ github.event.head_commit.message }}"
        env:
          VAPOR_API_TOKEN: ${{ secrets.VAPOR_API_TOKEN }}
```
3. Finally, you can edit the `deploy.yml` file to fit your application’s deployment needs, as it may require a different PHP version or a library like `npm`. Once you are done, commit and push the `deploy.yml` file to `master` so GitHub Actions can run the first deployment job.
#### [​](#docker-arm-runtime) Docker Arm Runtime
Since GitHub actions run on the `x86_64` architecture, they are unable to natively compile `arm64` based images. In order to compile the `docker-arm` runtime, the `arm64` platform can be emulated using QEMU. To get started, add the following to your `deploy.yml`, directly after the “Checkout Code” step:
Copy
Ask AI
```
- name: Setup QEMU
  uses: docker/setup-qemu-action@v2
  with:
    platforms: arm64
```
When building a `docker-arm` image via GitHub Actions or other CI environments that emulate the `arm64` architecture using QEMU, you should disable Docker’s build provenance attestations by setting `provenance=false`. Without this option, the build may produce a manifest list instead of a single image, which can cause deployment failures.
You may specify Docker build options via the `docker-build-options` configuration option within your application’s `vapor.yml` file. The `docker-build-options` option accepts an array of strings, where each string corresponds to a flag passed to the `docker build` command:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        runtime: docker-arm
        docker-build-options:
            - provenance=false
        build:
            - 'composer install --no-dev'
```
### [​](#example-with-chipper-ci) Example With Chipper CI
If your application uses [Chipper CI](https://chipperci.com/) as its CI platform, the following guidelines will assist you in configuring Vapor deployments so that your application is automatically deployed when someone pushes a commit to the `master` branch:
1. First, add the `VAPOR_API_TOKEN` environment variable to your “Chipper CI > Project Settings > Project Environment Variables” settings so that Chipper CI can authenticate with Vapor while running your build pipeline.
2. Then, on the “Build Pipeline” dashboard, add a step with the name `Deploy` and the following content:
Copy
Ask AI
```
if [[ $CI_COMMIT_BRANCH == 'master' ]]; then
    composer install --no-interaction --prefer-dist --optimize-autoloader

    composer global require laravel/vapor-cli

    vapor deploy
fi
```
3. Next, commit and push any change to the `master` branch so that Chipper CI will deploy your application.
If you plan to use Docker based runtimes to run your Vapor application, you must purchase a Chipper CI paid plan and enable Docker in each project that contains a Docker based Vapor application.
Was this page helpful?
YesNo
[Environments](/projects/environments)[Development](/projects/development)
⌘I
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)