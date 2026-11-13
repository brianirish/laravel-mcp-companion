Source: https://laravel.com/cloud/docs/quickstart.md

# Quickstart

Get started with Laravel Cloud and deploy your first application in minutes.

Select your framework to get started:

> [tab] Laravel
>
> ## Prerequisites
>
> * A [supported PHP version](https://laravel.com/cloud/docs/runtimes#php)
> * Laravel 9.x or greater
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Connect to GitHub (or GitLab or Bitbucket). A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> **4. Select the PHP runtime**
>
> In your environment settings, confirm the runtime is set to **PHP** and select the PHP version that matches your application's requirements.
>
> **5. Set build and deploy commands**
>
> Set your **build command** to install dependencies and compile assets:
>
> ```sh theme={null}
> composer install --no-dev && npm run build
> ```
>
> Set your **deploy command** to run database migrations on each deployment:
>
> ```sh theme={null}
> php artisan migrate --force
> ```
>
> **6. Add environment variables**
>
> At minimum, set your `APP_KEY`. You can generate one locally and paste the value into the Laravel Cloud dashboard:
>
> ```sh theme={null}
> php artisan key:generate --show
> ```
>
> If your application uses a database, connect a [MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) or [Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) resource from the infrastructure canvas. Laravel Cloud automatically injects the connection environment variables.
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application, runs your deploy command, and routes traffic to the new instance.
>
> Congratulations! Your Laravel application is live on Laravel Cloud! Continue with the [Laravel deploy guide](https://laravel.com/cloud/docs/deploy-guides/laravel) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), [managed queues](https://laravel.com/cloud/docs/queues), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Symfony
>
> ## Prerequisites
>
> * A [supported PHP version](https://laravel.com/cloud/docs/runtimes#php)
> * Symfony 7.4 LTS or 8.x
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> Laravel Cloud automatically detects Symfony applications and configures `php bin/console` as the command runner.
>
> **4. Select the PHP runtime**
>
> In your environment settings, confirm the runtime is set to **PHP** and select the PHP version that matches your application's requirements.
>
> **5. Set build and deploy commands**
>
> Set your **build command** to install dependencies and compile assets:
>
> ```sh theme={null}
> composer install --no-dev && php bin/console asset-map:compile
> ```
>
> Set your **deploy command** to run database migrations on each deployment:
>
> ```sh theme={null}
> php bin/console doctrine:migrations:migrate --no-interaction
> ```
>
> **6. Add environment variables**
>
> At minimum, set `APP_ENV` and `APP_SECRET` in the Laravel Cloud dashboard:
>
> | Variable | Value |
> | - | - |
> | `APP_ENV` | `prod` |
> | `APP_SECRET` | A securely generated secret string |
>
> If your application uses a database, connect a [MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) or [Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` environment variable.
>
> > [!NOTE]
> >
> > If your application defines `DATABASE_URL` or other Cloud-injected variables in `.env.prod`, those values take precedence over Cloud's runtime injection. Keep Cloud-managed variables out of `.env.prod` to avoid unexpected overrides.
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application, runs your deploy command, and routes traffic to the new instance.
>
> Congratulations! Your Symfony application is live on Laravel Cloud! Continue reading to learn about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), [managed queues](https://laravel.com/cloud/docs/queues), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Next.js
>
> ## Prerequisites
>
> * A [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno)
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. You can also choose the Port to serve on. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> **4. Adjust the runtime version**
>
> In your environment settings, set the Node.js, Bun, or Deno version your application requires.
>
> **5. Set the build command**
>
> Set your **build command** to install dependencies and compile your application:
>
> ```sh theme={null}
> npm ci --audit false
> npm run build
> ```
>
> Laravel Cloud sets a default start command for Next.js applications that runs the `start` script defined in your `package.json` (or the `deno task start` command, if you're using the Deno runtime). You can override it from your deployment settings if needed.
>
> **6. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. Variables prefixed with `NEXT_PUBLIC_` are available in the browser. All other variables are server-only.
>
> Laravel Cloud automatically sets `NODE_ENV=production` and `NEXT_PUBLIC_SITE_URL` (your application's URL) on every deployment. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Next.js application is live on Laravel Cloud! Continue with the [Next.js deploy guide](https://laravel.com/cloud/docs/deploy-guides/nextjs) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Nuxt
>
> ## Prerequisites
>
> * A [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno)
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. You can also choose the Mode (server or static site generation) and the Port to serve on. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> **4. Adjust the runtime version**
>
> In your environment settings, set the Node.js, Bun, or Deno version your application requires.
>
> **5. Set the build command**
>
> Set your **build command** to install dependencies and compile your application:
>
> ```sh theme={null}
> npm ci --audit false
> npm run build
>
> # alternatively for static site generation
> # npx nuxt generate
> ```
>
> Laravel Cloud sets a default start command for Nuxt applications that runs `.output/server/index.mjs` with `node`, `bun run`, or `deno run -A` depending on your runtime. You can override it from your deployment settings if needed.
>
> > [!NOTE]
> >
> > Laravel Cloud runs Nitro's default `node-server` preset, which outputs to `.output/server/index.mjs`. If your `nuxt.config` was previously deployed to another host, remove any `nitro.preset` option (for example, `vercel`, `netlify`, or `cloudflare`) and any `NITRO_PRESET` environment variable. A leftover preset still builds successfully, but it produces output Laravel Cloud can't serve. Your deployment then completes without routing any traffic to your application.
>
> **6. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. Variables prefixed with `NUXT_PUBLIC_` are available client-side. All other variables are server-only.
>
> Laravel Cloud automatically sets `NODE_ENV=production` and `NUXT_PUBLIC_SITE_URL` (your application's URL) on every deployment. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Nuxt application is live on Laravel Cloud! Continue with the [Nuxt deploy guide](https://laravel.com/cloud/docs/deploy-guides/nuxt) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Node.js
>
> ## Prerequisites
>
> * A [supported Node.js, Bun, or Deno version](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno)
> * An Express, Hono, or other Node.js application with a `package.json` file at the root of your repository
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. You can also choose the Port to serve on from the Advanced settings. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> Laravel Cloud detects Express and Hono applications automatically from the dependencies in your `package.json` file. Laravel Cloud still supports applications that don't use a recognized framework as generic Node.js applications.
>
> **4. Adjust the runtime version**
>
> In your environment settings, set the Node.js, Bun, or Deno version your application requires.
>
> **5. Set the build and start commands**
>
> Laravel Cloud pre-fills your **build command** to install your application's dependencies:
>
> ```sh theme={null}
> npm ci --audit false
> ```
>
> If your application has a compilation step, such as a TypeScript build, append `npm run build` to your build command.
>
> Laravel Cloud also pre-fills a **start command** based on the `start` script or `main` entry in your `package.json` file, such as `node server.js`. When Laravel Cloud can't resolve either one to a file, the start command falls back to `npm start` (or `bun run start` or `deno task start`, depending on your runtime). You can override it from your deployment settings if needed.
>
> **6. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. Laravel Cloud sets these variables on your application process rather than writing a `.env` file, so read them from `process.env`. Your application doesn't need a loader such as `dotenv`.
>
> Laravel Cloud automatically sets `NODE_ENV=production` and `APP_URL` (your application's URL) on every deployment. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> Your application must listen on the port Laravel Cloud provides through the `PORT` environment variable (`3000` by default):
>
> ```js theme={null}
> app.listen(process.env.PORT || 3000);
> ```
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Node.js application is live on Laravel Cloud! Continue with the [Node.js deploy guide](https://laravel.com/cloud/docs/deploy-guides/nodejs) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Go
>
> ## Prerequisites
>
> * A [supported Go version](https://laravel.com/cloud/docs/runtimes#go)
> * A `go.mod` file at the root of your repository
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> Laravel Cloud detects your application as a Go application from its `go.mod` file and reads your Go version from the `go` directive at the top of that file.
>
> **4. Set the build command**
>
> Cloud pre-fills your **build command** for the detected entrypoint. An application with its `main` package at the repository root and no detected cgo requirements uses:
>
> ```sh theme={null}
> CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o app .
> ```
>
> Cloud adjusts the package path for entrypoints such as `cmd/server` and sets `CGO_ENABLED=1` when it detects cgo requirements. The default **start command**, `./app`, runs the resulting binary. If you change the output path or binary name, update the start command to match.
>
> **5. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> Cloud supplies these variables through the process environment. Read them with `os.Getenv`.
>
> Your application must listen on the port Laravel Cloud provides through the `PORT` environment variable (`3000` by default).
>
> **6. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Go application is live on Laravel Cloud! Continue with the [Go deploy guide](https://laravel.com/cloud/docs/deploy-guides/go) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Python
>
> ## Prerequisites
>
> * A [supported Python version](https://laravel.com/cloud/docs/runtimes#python)
> * A `pyproject.toml`, `requirements.txt`, `Pipfile`, or `setup.py` file
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. Then, click Create Application.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> Laravel Cloud detects Django, FastAPI, and Flask applications automatically from your dependencies. Laravel Cloud still supports applications that don't use a recognized framework as generic Python applications.
>
> **4. Set the build command (optional)**
>
> During the build, Cloud automatically installs your dependencies from your lockfile or dependency manifest. It pre-fills additional steps when needed, such as installing a missing application server or collecting Django static files. You may edit these commands or add your own steps:
>
> ```sh theme={null}
> python manage.py collectstatic --noinput
> ```
>
> **5. Set the start command**
>
> Cloud pre-fills a **start command** using your detected framework, entrypoint, and a compatible server from your dependencies. Django and Flask default to Gunicorn. FastAPI defaults to Uvicorn. If you need to set the command yourself, these examples use the default servers:
>
> | Framework | Example start command |
> | - | - |
> | Django | `gunicorn <project>.wsgi --bind [::]:$PORT` |
> | FastAPI | `uvicorn main:app --host :: --port $PORT` |
> | Flask | `gunicorn app:app --bind [::]:$PORT` |
> | Generic Python | `python main.py` |
>
> > [!NOTE]
> >
> > Replace the example entrypoint with your application's module or callable. If your Django start command still contains `<project>`, Cloud requires you to replace it before deploying. Keep the server in your dependencies to control its version. For Uvicorn, use `--host ::` even if the pre-filled command uses `--host ''`. See the [Python deploy guide](https://laravel.com/cloud/docs/deploy-guides/python#bind-to-the-right-interface).
>
> **6. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> Cloud supplies these variables through the process environment. Read them from `os.environ`. For Django, configure the [environment and proxy settings](https://laravel.com/cloud/docs/deploy-guides/python#django-environment-variables) before deploying.
>
> **7. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Python application is live on Laravel Cloud! Continue with the [Python deploy guide](https://laravel.com/cloud/docs/deploy-guides/python) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Ruby and Rails
>
> ## Prerequisites
>
> * A [supported Ruby version](https://laravel.com/cloud/docs/runtimes#ruby)
> * A committed `Gemfile` and `Gemfile.lock` in your application directory
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Create an application**
>
> From your Laravel Cloud dashboard, select **New application**, connect your Git provider, and choose your repository and deployment region. For a monorepo, select the directory containing your `Gemfile`.
>
> Laravel Cloud detects Ruby applications and recognizes Rails from its application configuration and framework files. If the repository scan reports a missing lockfile platform, run `bundle lock --add-platform aarch64-linux` locally, commit the lockfile, and refresh the scan.
>
> **2. Review the Ruby version**
>
> Declare your version in `.ruby-version`, or review the other [supported version declarations](https://laravel.com/cloud/docs/runtimes#ruby). When your repository does not declare a version, you may choose one in your environment's **General Settings**.
>
> **3. Review build and start commands**
>
> Laravel Cloud installs gems automatically from your lockfile. For Rails applications with detected assets, it pre-fills asset compilation and any detected JavaScript dependency installation:
>
> ```sh theme={null}
> SECRET_KEY_BASE_DUMMY=1 bundle exec rails assets:precompile
> ```
>
> The default Rails start command uses your binstub when available:
>
> ```sh theme={null}
> bundle exec bin/rails server -b '::' -p $PORT
> ```
>
> Laravel Cloud uses a Procfile `web` command when one exists. Keep your server in the foreground, listening on `PORT` and accepting IPv6 connections. See the [Ruby and Rails deploy guide](https://laravel.com/cloud/docs/deploy-guides/ruby) for Puma, Rack, and generic Ruby commands.
>
> **4. Configure Rails secrets and resources**
>
> New Rails environments include a generated `SECRET_KEY_BASE`. Preserve your existing value when migrating an application, and add `RAILS_MASTER_KEY` if production uses encrypted credentials.
>
> Connect a Postgres or MySQL database from the infrastructure canvas and include its `pg` or `mysql2` adapter in your production bundle. Laravel Cloud supplies `DATABASE_URL`. Review any separate [Solid Cache, Solid Queue, or Solid Cable connections](https://laravel.com/cloud/docs/deploy-guides/ruby#solid-cache-solid-queue-and-solid-cable) before attaching the database.
>
> **5. Review the deploy command**
>
> For Rails applications using a database, set your deploy command to:
>
> ```sh theme={null}
> bin/rails db:prepare
> ```
>
> Attaching a database enables this command if you have kept the default deploy command. Add it yourself if you have customized that command.
>
> **6. Deploy**
>
> Click **Deploy**. Laravel Cloud builds your application, runs the deploy command, and routes traffic to the new deployment. Configure any job workers as [background processes](https://laravel.com/cloud/docs/workers).
>
> Congratulations! Your Ruby application is live on Laravel Cloud! Continue with the [Ruby and Rails deploy guide](https://laravel.com/cloud/docs/deploy-guides/ruby) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).

> [tab] Rust
>
> ## Prerequisites
>
> * A `Cargo.toml` file at the root of your repository
> * A GitHub, GitLab, or Bitbucket account
>
> **1. Go to your main Laravel Cloud dashboard page and select + New application.**
>
> 
>
> **2. Connect your Git provider**
>
> Select Continue with GitHub, GitLab, or Bitbucket. A new tab or window opens. Sign in to your Git provider and select the user or organization and the repositories you want to give Laravel Cloud access to.
>
> 
>
> After you complete the Git provider authentication flow, your Git provider redirects you back to Laravel Cloud.
>
> **3. Create a new application**
>
> Select the repository you want to use, name your Laravel Cloud application, and select a Region where your application will deploy. Then, click **Create application**.
>
> 
>
> Laravel Cloud creates your application along with a default environment. It then takes you to your application's default environment overview page.
>
> 
>
> Laravel Cloud detects your application as a Rust application from its `Cargo.toml` file, and recognizes axum, Actix Web, Rocket, or warp from your dependencies. Cloud builds with a recent stable Rust release, or with the toolchain pinned in your `rust-toolchain.toml` file.
>
> **4. Set the build command**
>
> Cloud pre-fills your **build command** with:
>
> ```sh theme={null}
> cargo build --release
> ```
>
> Cloud copies the executables from your release output to `/var/www/bin`, adds that directory to your `PATH`, and detects the binary your **start command** should run. If your package contains several binaries and you didn't set `default-run` in your `Cargo.toml` before creating the application, update the start command to name the binary you want. See the [Rust deploy guide](https://laravel.com/cloud/docs/deploy-guides/rust#compile-during-the-build) for details.
>
> **5. Add environment variables**
>
> Add any environment variables your application requires in the Laravel Cloud dashboard. If your application uses a database or cache, connect a resource from the infrastructure canvas. Laravel Cloud automatically injects the `DATABASE_URL` or `REDIS_URL` connection string.
>
> Cloud supplies these variables through the process environment. Read them with `std::env::var`.
>
> Your application must listen on the port Laravel Cloud provides through the `PORT` environment variable (`3000` by default), and it must accept IPv6 connections by binding to `::` rather than `0.0.0.0`. Rocket applications need no change, since Cloud configures Rocket's address and port for you.
>
> **6. Deploy**
>
> Click the **Deploy** button. Laravel Cloud builds your application and routes traffic to the new instance.
>
> Congratulations! Your Rust application is live on Laravel Cloud! Continue with the [Rust deploy guide](https://laravel.com/cloud/docs/deploy-guides/rust) to make it production-ready, or read about [environments](https://laravel.com/cloud/docs/environments), [databases](https://laravel.com/cloud/docs/resources/databases/laravel-mysql), and [more](https://laravel.com/cloud/docs/organizations).
