Source: https://laravel.com/cloud/docs/deployments.md

# Deployments

Learn how deployments work in Laravel Cloud, including builds, push to deploy, deploy hooks, and zero-downtime releases.

## Introduction

You deploy in Laravel Cloud whenever you have new code to release, new resources to attach, or environment settings to update.

When a new deployment starts, Laravel Cloud takes your code and environment settings and builds an image for your application's runtime and version. Then it runs your build and deploy commands.

Once your build succeeds, Laravel Cloud brings the new deployment online with zero downtime. It gracefully terminates the existing deployment and lets any running processes complete.


## Deploy options

### Push to deploy

Every time you push new code to your remote Git branch, Laravel Cloud automatically starts a new deploy. **Push to deploy is enabled by default** on all environments. To change this setting, go to **Settings > Deployments**.

### Deploy hooks

To trigger a deployment through an HTTP endpoint, enable the **Deploy hook** option in **Settings > Deployments**. Laravel Cloud then gives you a URL that your CI pipeline can send a POST request to. You can refresh the URL anytime from the **Deployments** settings.

You can also deploy a specific commit by passing a `commit_hash` query parameter to the deploy hook URL. The commit must belong to the branch configured for the environment.

```shell theme={null}
curl -X POST "https://your-deploy-hook-url?commit_hash=abc123def456"
```

If you don't provide a commit hash, Laravel Cloud deploys the latest commit from the environment's branch.

#### Example using GitHub Actions

Deploy hooks let you trigger Laravel Cloud deployments from your CI pipeline. Here's a complete example using GitHub Actions:

1. First, add your deploy hook URL as a secret in your GitHub repository:
   * Go to your GitHub repository settings.
   * Navigate to **Secrets and variables > Actions**.
   * Add a new secret named `LARAVEL_CLOUD_DEPLOY_HOOK` with your deploy hook URL.

2. Create a `.github/workflows/deploy.yml` file in your repository:

```yaml theme={null}
name: Deploy to Laravel Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Laravel Cloud
        run: |
          curl -X POST "${{ secrets.LARAVEL_CLOUD_DEPLOY_HOOK }}?commit_hash=${{ github.sha }}"
```

3. Commit and push the workflow file to trigger your first deployment.

You don't need to install dependencies or run build commands in CI. Laravel Cloud handles those steps for you. The deploy hook tells Laravel Cloud to:

* Pull your code from the specified commit
* Run your configured build commands
* Run your configured deploy commands
* Deploy your application with zero downtime

### Manual

You can trigger a deployment from the Laravel Cloud dashboard anytime by clicking the **Deploy** button on the environment overview page or the **Deployments** page. When you update environment settings, Cloud stages your changes until you deploy them. Review the pending changes and deploy them together from the staged changes banner, or click **Deploy** at any time.

## Troubleshooting

### Health check failed

If a [health check](https://laravel.com/cloud/docs/health-checks) fails during your deployment, the deployment page names the failed check and the request Laravel Cloud made. It also shows the cause, such as an HTTP 404 response or a refused connection. To fix the failure, follow the [health checks troubleshooting guide](https://laravel.com/cloud/docs/health-checks#troubleshooting-health-check-failures) and review your environment's health check settings under **Settings > Deployments**.

### Framework or runtime version not supported

> [tab] Laravel
>
> Laravel Cloud requires Laravel 9 or greater. You should also use the latest minor version of the `laravel/framework` Composer package. The minimum minor versions required are:
>
> * Laravel 11: `v11.41.3`
>
> * Laravel 10: `v10.48.28`
>
> * Laravel 9: `v9.52.20`
>
> > [!TIP]
> >
> > Watch [this video](https://youtu.be/95iC9L-3CxY) to learn more about fixing this framework error.
>
> If you receive an error during a deployment that *"The \[laravel/framework] package was found in the \[composer.lock] file, but the version is not supported. Upgrade Laravel to the latest minor version"* update by running the following command:
>
> ```shell theme={null}
> composer update laravel/framework
> ```

> [tab] Symfony
>
> Laravel Cloud requires Symfony 7.4 LTS or 8.x. Make sure your `composer.json` specifies a compatible version and that your `composer.lock` is up to date:
>
> ```shell theme={null}
> composer update symfony/framework-bundle
> ```

> [tab] Next.js
>
> Next.js applications can run on any [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno). If you're using Node.js, make sure your `package.json` specifies a compatible engine:
>
> ```json theme={null}
> {
>   "engines": {
>     "node": ">=22"
>   }
> }
> ```
>
> If you're using Bun or Deno, you don't need an `engines` configuration. Choose your version in your environment's **General Settings** instead.

> [tab] Nuxt
>
> Nuxt applications can run on any [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno). If you're using Node.js, make sure your `package.json` specifies a compatible engine:
>
> ```json theme={null}
> {
>   "engines": {
>     "node": ">=22"
>   }
> }
> ```
>
> If you're using Bun or Deno, you don't need an `engines` configuration. Choose your version in your environment's **General Settings** instead.

> [tab] JavaScript
>
> JavaScript applications, including Express and Hono, can run on any [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno). If you're using Node.js, make sure your `package.json` specifies a compatible engine:
>
> ```json theme={null}
> {
>   "engines": {
>     "node": ">=22"
>   }
> }
> ```
>
> If you're using Bun or Deno, you don't need an `engines` configuration. Choose your version in your environment's **General Settings** instead.

> [tab] Go
>
> Laravel Cloud reads the `go` directive in your `go.mod` file and uses the lowest supported version that satisfies it. If no supported version satisfies the directive, the deployment fails before building. Update the `go` directive to a version listed in [Runtimes](https://laravel.com/cloud/docs/runtimes#go):
>
> ```text theme={null}
> go 1.25
> ```

> [tab] Python
>
> Laravel Cloud reads your Python version from a `.python-version` file or, when that file does not declare a version, the `requires-python` constraint in `pyproject.toml`. If the pinned version is unsupported, or no supported version satisfies the constraint, the deployment fails before building. Update your declaration to a version listed in [Runtimes](https://laravel.com/cloud/docs/runtimes#python):
>
> ```toml theme={null}
> [project]
> requires-python = ">=3.12"
> ```
>
> A version declared in your repository takes precedence over the version selected in your environment settings.

### Deployment succeeds but serves no traffic

> [tab] JavaScript
>
> Laravel Cloud's proxy, which runs alongside your application in each instance, routes traffic to your application on the port set by the `PORT` environment variable (`3000` by default, or the port you chose when creating the application). Make sure your Express, Hono, or other JavaScript application reads `PORT` rather than listening on a hardcoded port.

> [tab] Next.js
>
> Laravel Cloud's proxy, which runs alongside your application in each instance, routes traffic to your application on the port set by the `PORT` environment variable (`3000` by default, or the port you chose when creating the application). The default start command, `next start`, reads `PORT` automatically, so this works out of the box for most applications.
>
> If you've overridden the start command with a custom server (for example, a `server.js` file using Express), the build can succeed even if that server listens on a different, hardcoded port. Laravel Cloud can't detect the mismatch, so the deployment goes live without routing any traffic to your application.
>
> Make sure your custom server reads the `PORT` environment variable rather than hardcoding a port number.

> [tab] Nuxt
>
> Laravel Cloud starts Nuxt applications with Nitro's default `node-server` preset (`.output/server/index.mjs`). If your `nuxt.config` still sets a host-specific `nitro.preset` (for example, `vercel`, `netlify`, or `cloudflare`) left over from a previous provider, or a `NITRO_PRESET` environment variable is set, Nitro builds output for that host instead (such as `.vercel/output`). The build completes without error, but Laravel Cloud has no way to serve that output, so the deployment goes live without routing any traffic to your application.
>
> Remove the `nitro.preset` option and any `NITRO_PRESET` environment variable so Nitro can auto-detect the `node-server` preset.

> [tab] Go
>
> Laravel Cloud's proxy, which runs alongside your application in each instance, routes traffic to your application on the port set by the `PORT` environment variable (`3000` by default). If your application binds to a hardcoded port instead of reading `PORT`, the build and deployment can both succeed, but the deployment goes live without routing any traffic to your application.
>
> Make sure your application reads the `PORT` environment variable rather than hardcoding a port number.

> [tab] Python
>
> Laravel Cloud's proxy, which runs alongside your application in each instance, routes traffic to your application on the port set by the `PORT` environment variable (`3000` by default). The default start commands for Django, FastAPI, and Flask all read `$PORT`, so this works out of the box unless you've overridden the start command with something that hardcodes a port.
>
> Make sure your start command reads the `PORT` environment variable rather than hardcoding a port number.

> [tab] Rust
>
> Laravel Cloud's proxy, which runs alongside your application in each instance, routes traffic to your application on the port set by the `PORT` environment variable (`3000` by default). If your application binds to a hardcoded port, or to `0.0.0.0` or `127.0.0.1` instead of `::`, the proxy can't reach it.
>
> Make sure your application reads the `PORT` environment variable and binds to `::`. Rocket reads its own `ROCKET_PORT` and `ROCKET_ADDRESS` variables, which Laravel Cloud sets for you.

### Build or start command not configured

Go applications require an explicit build command because Laravel Cloud has no default way to compile a Go module for you. Go, Python, and JavaScript applications require an explicit start command because no framework tells Laravel Cloud how to run them.

Laravel Cloud pre-fills a default for each command when it first detects your application, so you usually see this error only if you've cleared the field. If a required command is blank, the deployment fails immediately with *"The environment has no build command configured"* or *"The environment has no start command configured."* For a Go application, restore a build command such as:

```shell theme={null}
CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o app .
```

### Django start command still has the `<project>` placeholder

Laravel Cloud discovers your Django project's WSGI module from your repository and pre-fills the start command with it. When the module can't be discovered, the start command falls back to a `<project>` placeholder:

```shell theme={null}
gunicorn <project>.wsgi --bind [::]:$PORT
```

Replace `<project>` with your Django project's settings module name (the directory containing `wsgi.py`) before deploying. If the placeholder is still there when you deploy, the deployment fails with *"The start command still contains the `<project>` placeholder. Replace `<project>` with your Django project's module name."*
