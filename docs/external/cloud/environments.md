Source: https://laravel.com/cloud/docs/environments.md

# Environments

Manage Laravel Cloud environments, deployment settings, variables, domains, commands, and runtime configuration.

## Introduction

A Laravel Cloud application can have many environments, such as "production", "staging", or even short-lived environments for trying out new features you're developing.

Each environment has its own compute infrastructure, resources, and deployment settings, so you can tune each environment for its purpose.

For example, you might give your staging environment small Flex compute instances that scale to zero, and give your production environment larger, always-on compute instances.

## Build and deploy commands

You may define how your application is built during deployment from the **Deployments** section of your environment settings.

### Build commands

Build commands let you customize how Laravel Cloud builds your application during deployment.

> [tab] Laravel
>
> Typically, your Laravel build command will install your Composer and npm dependencies and compile your application's assets:
>
> ```shell theme={null}
> composer install --no-dev && npm run build
> ```
>
> > [!TIP]
> >
> > Run `php artisan optimize` or `php artisan config:cache` during the build process, not during the deploy process.
>
> #### Private Composer packages
>
> To install private Composer packages, configure your application's Composer HTTP authentication credentials for each package using the `composer config` command. Add this command to your build commands before `composer install`:
>
> ```shell theme={null}
> composer config http-basic.composer.fluxui.dev your-username your-license-key
>
> composer install --no-dev
> ```

> [tab] Symfony
>
> Typically, your Symfony build command will install Composer dependencies and compile your application's assets:
>
> ```shell theme={null}
> composer install --no-dev && php bin/console asset-map:compile
> ```
>
> #### Private Composer packages
>
> To install private Composer packages, configure your application's Composer HTTP authentication credentials for each package using the `composer config` command. Add this command to your build commands before `composer install`:
>
> ```shell theme={null}
> composer config http-basic.example.com your-username your-license-key
>
> composer install --no-dev
> ```

> [tab] Next.js
>
> Typically, your Next.js build command will install Node dependencies and compile your application:
>
> ```shell theme={null}
> npm ci && npm run build
> ```

> [tab] Nuxt
>
> Typically, your Nuxt build command will install Node dependencies and compile your application:
>
> ```shell theme={null}
> npm ci && npm run build
> ```

> [tab] JavaScript
>
> Typically, your Node.js build command will install dependencies and compile your application:
>
> ```shell theme={null}
> npm ci && npm run build
> ```

> [tab] Go
>
> Laravel Cloud pre-fills your Go build command for the detected entrypoint. An application with its `main` package at the repository root and no detected cgo requirements uses:
>
> ```shell theme={null}
> CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o app .
> ```
>
> Cloud adjusts the package path for entrypoints such as `cmd/server` and sets `CGO_ENABLED=1` when it detects cgo requirements. The default start command, `./app`, runs the resulting binary. If you change the output path or binary name, update the start command to match.

> [tab] Python
>
> Laravel Cloud installs Python dependencies automatically, using `uv.lock`, `poetry.lock`, `Pipfile.lock`, `requirements.txt`, or `pyproject.toml`, in that order. Lockfile tools export dependencies for pip to install into the shared Python user directory.
>
> Cloud pre-fills additional build steps when needed. Django projects with a `STATIC_ROOT` setting or WhiteNoise dependency receive `python manage.py collectstatic --noinput`. Projects missing a compatible application server receive `pip install --user gunicorn` for WSGI or `pip install --user uvicorn` for ASGI. You may edit or remove these commands to suit your project. See the [Python deploy guide](https://laravel.com/cloud/docs/deploy-guides/python) for server and static-file configuration.

> [tab] Ruby and Rails
>
> Laravel Cloud installs gems automatically using `Gemfile.lock`. Rails applications with detected assets receive an asset compilation command, preceded by JavaScript dependency installation when needed:
>
> ```shell theme={null}
> SECRET_KEY_BASE_DUMMY=1 bundle exec rails assets:precompile
> ```
>
> Review your asset pipeline and any additional build steps in the [Ruby and Rails deploy guide](https://laravel.com/cloud/docs/deploy-guides/ruby#build-and-serve-assets). Generic Ruby and API-only Rails applications do not receive this default asset build.

> [tab] Rust
>
> Laravel Cloud downloads your crates automatically and pre-fills the following build command:
>
> ```shell theme={null}
> cargo build --release
> ```
>
> Cloud copies the executables from your release output to `/var/www/bin`, which is on your `PATH`, and detects which binary the default start command should run. See the [Rust deploy guide](https://laravel.com/cloud/docs/deploy-guides/rust#compile-during-the-build) to learn how Cloud chooses between several binaries.

> [!WARNING]
>
> Build commands time out if they do not complete within 15 minutes.

#### Dynamic environment variables

For Laravel and Symfony applications, Laravel Cloud writes your environment's variables to a `.env` file in the build context. You may append a derived value for your application to read:

```shell theme={null}
# Adding a dynamic environment variable
echo "MY_DYNAMIC_VAR=value" >> .env
```

> [!NOTE]
>
> JavaScript, Go, Python, Ruby, and Rust applications receive variables through the process environment during builds and at runtime. Appending to a `.env` file does not configure their runtime variables. Add persistent values under your environment's [environment variables](#environment-variables) instead.

#### Exposing variables to scripts

For Laravel and Symfony applications, your build and deploy commands can read your environment's variables directly, but the scripts and tools those commands run cannot. To pass a variable to a script, `export` it first:

```shell theme={null}
export SENTRY_AUTH_TOKEN
npm run build
```

You may export several variables at once:

```shell theme={null}
export SENTRY_AUTH_TOKEN SENTRY_ORG SENTRY_PROJECT
./scripts/upload-sourcemaps.sh
```

### Deploy commands

Laravel Cloud runs your environment's "Deploy Commands" on your infrastructure just before a new deployment goes "live". Typically, you use these commands to migrate your environment's database.

Unlike build commands, deploy commands do not persist their filesystem changes to your application. As with build commands, you must [export variables](#exposing-variables-to-scripts) before scripts your deploy commands run can read them.


> [!WARNING]
>
> Deploy commands time out if they do not complete within 15 minutes.

For Rails applications using a database, run `bin/rails db:prepare` as a deploy command. If you have kept the default deploy command, attaching a database uncomments it. See [Rails database preparation](https://laravel.com/cloud/docs/deploy-guides/ruby#prepare-the-databases).

#### Unnecessary build and deploy commands

> [!NOTE]
>
> This section applies to Laravel applications.

Laravel Cloud either handles the following commands automatically, or they should not run during deployment:

* `php artisan queue:restart`: Laravel Cloud restarts queue workers automatically after each deployment.
* `php artisan horizon:terminate`: Laravel Cloud manages Horizon processes automatically during deployments.
* `php artisan optimize:clear`: This command clears the cache and can cause unexpected behavior, especially with the queue.
* `php artisan storage:link`: The symbolic link won't persist, because Laravel Cloud does not save changes that deploy commands make. Use [Laravel Object Storage](https://laravel.com/cloud/docs/resources/object-storage) for persistent file storage instead.

Typically, your deploy commands should only include database migrations and other essential post-deployment tasks.

## Environment settings

### Environment variables

The environment variables section of your environment's settings lets you customize the variables available to your environment.


In addition to your custom environment variables, Laravel Cloud automatically injects a variety of environment variables for you. These include any credentials needed to connect to Laravel Cloud resources like databases, caches, or object storage.


For sensitive values that should be shared across multiple environments, use [Secrets Manager](https://laravel.com/cloud/docs/secrets) to create encrypted organization-level secrets and link them to the environments that need them.

> [!NOTE]
>
> Custom environment variables take priority and override any automatically injected environment variables.

After you change an environment's variables, redeploy the environment for the changes to take effect.

#### How variables reach your application

Laravel Cloud delivers your environment's variables differently depending on the runtime:

> [tab] Laravel, Symfony
>
> Laravel Cloud writes your variables to a `.env` file in your application's root directory before your application starts, so the framework reads them the same way it does locally.

> [tab] JavaScript
>
> Laravel Cloud sets your variables on the application process, the way `export` does in a shell. Read them from `process.env`.

> [tab] Go
>
> Laravel Cloud sets your variables on the application process, the way `export` does in a shell. Read them with `os.Getenv`. No `.env` file is written at runtime, so your application does not need a loader such as `godotenv`.

> [tab] Python
>
> Laravel Cloud sets your variables on the application process, the way `export` does in a shell. Read them from `os.environ`, or, in a Django application, through your settings module as usual. No `.env` file is written at runtime, so your application does not need a loader such as `python-dotenv`.

> [tab] Ruby and Rails
>
> Laravel Cloud sets variables on your application process. Read them from `ENV`. Rails reads `DATABASE_URL` automatically, while custom application settings require you to read the corresponding variables in your configuration.

> [tab] Rust
>
> Laravel Cloud sets your variables on the application process, the way `export` does in a shell. Read them with `std::env::var`. No `.env` file is written at runtime, so your application does not need a loader such as `dotenvy`.

Laravel Cloud also makes your environment's variables available during builds. Laravel and Symfony builds include a `.env` file for the framework to read. JavaScript, Go, Python, Ruby, and Rust build commands receive exported process variables.

#### Referencing other variables

A custom variable's value may refer to another variable with `${NAME}`:

```bash theme={null}
API_HOST=api.example.com
API_BASE_URL="https://${API_HOST}/v1"
CALLBACK_URL="${APP_URL}/auth/callback"
```

In Laravel and Symfony applications, the framework's `.env` loader resolves these references when your application boots, the same way it does locally.

For JavaScript, Go, Python, Ruby, and Rust applications, Laravel Cloud resolves references before it sets the variables, so your application and your build commands receive the final value. In the example above, `API_BASE_URL` contains `https://api.example.com/v1`, not the text `https://${API_HOST}/v1`. A reference resolves to:

* A variable Laravel Cloud injects for your environment, such as `APP_URL`, `DATABASE_URL`, or `REDIS_URL`.
* A custom variable defined **above** it in your environment's variables.

Any other reference resolves to an empty string. This includes a variable defined below the one that references it, a variable that doesn't exist, and a [secret](https://laravel.com/cloud/docs/secrets) linked to the environment. Only the variables shown in your environment's injected variables can be referenced. For example, JavaScript applications receive `DATABASE_URL` but not `DB_HOST` or `DB_PASSWORD`, so `${DB_HOST}` resolves to an empty string.

Variable names in references must use uppercase letters, digits, and underscores. A `$` followed by an uppercase letter is also treated as a reference without braces: `$API_HOST` works like `${API_HOST}`, and in a value such as `pa$Sw0rd`, `$S` is replaced with an empty string. A `$` followed by a lowercase letter is left as is.

To keep a literal `$` in a value, such as a password, wrap the value in single quotes in the custom environment variables editor:

```bash theme={null}
SMTP_PASSWORD='pa$Sw0rd'
```

When you set a variable through the [API](https://laravel.com/cloud/docs/api/introduction) or the [CLI](https://laravel.com/cloud/docs/api/cli), send the value without quotes, because quotes become part of the value. Laravel Cloud keeps any `$` in the value as literal text unless it starts a `${NAME}` reference, so `pa$Sw0rd` reaches your application unchanged. The same applies to [secrets](https://laravel.com/cloud/docs/secrets).

When a variable that a reference depends on changes, such as `REDIS_URL` after you attach a cache, the staged changes banner lists the referencing variable as changed until you deploy again.

### HTTP basic authentication

HTTP basic authentication lets you protect an environment with a username and password before traffic reaches your application. Basic authentication is useful for staging environments, private demos, preview environments, or sleeping environments that should not wake up because of unauthorized requests or automated bot traffic.

You may enable HTTP basic authentication in the Security section of your environment's General Settings page. Once you enable it, users can access the environment with the username `admin` and the password you set. Passwords must be between 5 and 32 characters and cannot contain the `:` character.


HTTP basic authentication is available on the [Growth plan](https://laravel.com/cloud/docs/pricing) or higher. After you enable it, disable it, or change the password, redeploy the environment for the changes to take effect.

### Runtime

#### PHP runtime

You may select an environment's PHP version on the environment's General Settings page. After you change the PHP version, redeploy the environment for the change to take effect. See [Runtimes](https://laravel.com/cloud/docs/runtimes#php) for the supported PHP versions.


#### Node.js, Bun, and Deno runtimes

Next.js, Nuxt, TanStack Start, Express, and Hono applications run on the Node.js, Bun, or Deno runtime. Laravel Cloud detects the runtime automatically from the configuration files in your repository. See [Runtimes](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno) for detection rules and supported versions.

You may select the Node.js, Bun, or Deno version on the environment's General Settings page. After you change it, redeploy the environment for the change to take effect.


#### Go and Python runtimes

Laravel Cloud detects Go and Python applications automatically from your repository: a `go.mod` file for Go, or a `pyproject.toml`, `requirements.txt`, `Pipfile`, or `setup.py` file for Python. Rather than using a dashboard setting, Laravel Cloud reads the language version straight from your repository. For Go, it reads the `go` directive in `go.mod`. For Python, it reads a `.python-version` file or the `requires-python` constraint in `pyproject.toml`. See [Runtimes](https://laravel.com/cloud/docs/runtimes) for supported versions and what happens when a detected version isn't one Laravel Cloud publishes.

#### Ruby runtime

Laravel Cloud reads Ruby version declarations from your deployment's commit. When the repository does not declare a version, you may select one in **General Settings**. See [Ruby versions](https://laravel.com/cloud/docs/runtimes#ruby) for the supported release lines and declaration order.

#### Rust runtime

Laravel Cloud detects Rust applications automatically from a `Cargo.toml` file at the root of your repository. Rather than using a dashboard setting, Laravel Cloud builds with a recent stable Rust release, or with the toolchain pinned by your `rust-toolchain.toml` file. See [Rust versions](https://laravel.com/cloud/docs/runtimes#rust) for details.

### PHP extensions

> [!NOTE]
>
> PHP extensions are only available for PHP runtime environments (Laravel and Symfony).

Laravel Cloud currently supports the following PHP extensions:

```
apcu, bcmath, calendar, Core, ctype, curl, date, dom, ev, excimer, exif,
fileinfo, filter, ftp, gd, gettext, gmp, grpc, hash, iconv, igbinary, imagick,
imap, intl, json, ldap, libxml, mbstring, mongodb, msgpack, mysqli,
mysqlnd, openssl, pcntl, pcre, PDO, pdo_mysql, pdo_pgsql, pdo_sqlite, pdo_sqlsrv,
Phar, posix, pspell, random, readline, redis, Reflection, session, shmop,
SimpleXML, soap, sockets, sodium, SPL, sqlite3, sqlsrv, standard, tokenizer, xml,
xmlreader, xmlwriter, xsl, Zend OPcache, zip, zlib.
```

You can also list the loaded extensions by running `php -m` with Laravel Cloud's "Command" feature in your environment dashboard.

### PHP memory limit

> [!NOTE]
>
> This section applies to PHP runtime environments (Laravel and Symfony).

Laravel Cloud allocates PHP memory dynamically based on a percentage of your instance's total memory. If your application needs a specific amount, you can override the default by defining a new `memory_limit`.

You can override the default memory limit by adding configuration directly in your application code. The most common method is to update your `public/index.php` and your `artisan` file:

```php theme={null}
<?php

// Set memory limit to 512 MB...
ini_set('memory_limit', '512M');

// Or, remove memory limits entirely...
ini_set('memory_limit', -1);
```

Or, you can set the memory limit in your build commands to avoid modifying your project's source code:

```bash theme={null}
# Add memory_limit to the top of the public/index.php file...
sed -i 's/<?php/<?php\nini_set('\''memory_limit'\'', '\''512M'\'');/g' public/index.php

# Add memory_limit to the top of the artisan file...
sed -i 's/<?php/<?php\nini_set('\''memory_limit'\'', '\''512M'\'');/g' artisan
```

Adjust memory early in your application's lifecycle. Excessive memory usage can slow your whole application. Setting the memory limit to -1 removes all memory restrictions, but it can lead to unpredictable behavior, so use it with caution, especially in production environments.

For more information about PHP memory configuration, consult the [official PHP documentation](https://www.php.net/manual/en/ini.core.php#ini.memory-limit).

## Cloud domains

Laravel Cloud assigns each environment a free `laravel.cloud` domain the first time it deploys successfully. You can use this domain to test and build your application before attaching a custom domain.

Laravel Cloud builds these domains from your application and environment names. If you change either name, Laravel Cloud updates the domain to match. Redeploy the environment for the new domain to take effect.


## Custom domains

Of course, before shipping your application to the world, you will likely want to assign your own custom domain name to your production environment.

Laravel Cloud guides you through DNS configuration, verifies domain ownership, and issues an SSL certificate automatically.

For DNS records, verification paths, wildcards, provider-specific guides, and plan limits, see [Domains](https://laravel.com/cloud/docs/domains).

> [!TIP]
>
> If your domain verification is taking longer than expected, check out our docs on [verifying domains](https://laravel.com/cloud/docs/knowledge-base/domain-verification).

## Stop and restart

To stop an environment, click the "..." button next to the environment's "Deploy" button. Then, click "Stop". When you stop an environment, Laravel Cloud shuts down all App and worker clusters in the environment. All web traffic, background processes, and scheduled tasks stop. You are not charged for the environment's compute, but you are still charged for any attached resources.

You can restart the environment from the same dropdown menu. Restarting an environment runs a full deployment.


## Replicate

Environments in the same application often have similar or identical resources and settings. So when you create a new environment, it is often more convenient to clone an existing one and make changes than to start from scratch.

To replicate an environment, click the "..." button next to the environment's "Deploy" button. Then, click "Replicate". Confirm you are replicating the correct environment and Git branch, then enter a name for your new environment. By default, Laravel Cloud duplicates all General, Environment, and Deployment settings. You can optionally edit the default replication settings for compute and resources. The default replication behavior is:

* Compute: duplicate all clusters at a smaller size, with scale to zero enabled
* Database: create a new database cluster that scales to zero, or a new database within the same cluster if your database does not support scale-to-zero replication
* Cache: create a new cache that scales to zero, or a new cache at the smallest available size if your cache does not support scale to zero
* Object storage: create a new bucket
* WebSockets: create a new WebSocket cluster

If you choose to share the cache instead, Cloud adds a `REDIS_PREFIX` environment variable set to `application:environment:` so each environment's keys stay separate. If the environment runs Laravel Horizon, Cloud also sets `HORIZON_PREFIX`.


> [!WARNING]
>
> Review and edit the "Replication options" as needed **before** deploying your new environment. The defaults balance cost and performance, but they may not be right for your application. Take extra care when you replicate a production environment. Reusing its resources can hurt performance or interfere with queued jobs, sessions, or other application data.

To generate an isolated environment automatically for every pull request, use [preview environments](https://laravel.com/cloud/docs/preview-environments) instead.

## Commands

Laravel Cloud's console gives you an interactive terminal in your environment. Navigate to your environment's **Commands** tab and click **Open console** to start a session. You can run shell commands for any supported framework or runtime, such as `php artisan cache:clear` in a Laravel application or `node script.js` in a Node.js application. The console also supports interactive tools such as `php artisan tinker` and `python manage.py shell`.

If your environment has worker clusters, you can choose to run the console session on your app cluster or a worker cluster when starting the session.

Console sessions end automatically after 15 minutes without any input from you or output from a command.

You can review console session history from the **Commands** tab. Select a session to view its transcript and replay interactive commands.

### One-off commands

One-off commands are available only through the [API](https://laravel.com/cloud/docs/api/introduction) and [CLI](https://laravel.com/cloud/docs/api/cli#commands). For example, use `cloud command:run` to run a one-off command from the CLI. Laravel Cloud runs these commands on any available cluster in your environment.

> [!WARNING]
>
> One-off commands run through the API or CLI must be non-interactive and may not run for more than 30 minutes. These limitations apply only to API and CLI commands, not console sessions.

## Filesystem

Environment filesystems are **ephemeral**, meaning files may not persist across requests or jobs. New deployments and redeployments reset the filesystem. In addition, each replica of your compute cluster has its own filesystem. Treat the filesystem as temporary, unshared disk space that stays consistent only during a single request or job.

The total disk space available on each replica is proportional to the cluster's RAM. Every 1GB of RAM gives 512MB of disk space. For example, a cluster with 2GB of RAM will have 1GB of ephemeral disk space available to it. If you exceed the available disk space, your application may crash and the deployment may need to restart.

For persistent cache and session storage, PHP applications should use the `redis` or `database` drivers with a [cache](./resources/caches) or [database](./resources/databases/laravel-mysql) resource. JavaScript applications should use their framework's equivalent persistent session and cache adapter backed by one of these resources. Go, Python, and Rust applications should connect directly to a cache or database resource using the injected `REDIS_URL` or `DATABASE_URL` connection string. For persistent file storage, use [Laravel Cloud Object Storage](./resources/object-storage).

## Nightwatch integration

> [!NOTE]
>
> Nightwatch integration is currently available for Laravel applications only.

Laravel Cloud environments have built-in support for [Laravel Nightwatch](https://nightwatch.laravel.com) monitoring. Nightwatch shows your environment's performance, exceptions, logs, and overall health.


**1. Install Nightwatch package**

Install the Laravel Nightwatch package in your application locally using [Composer](https://packagist.org/packages/laravel/nightwatch):

```bash theme={null}
composer require laravel/nightwatch
```

> [!NOTE]
>
> Run `composer require laravel/nightwatch` on your local machine to update your `composer.json` and `composer.lock` files before deploying.

**2. Connect Nightwatch**

Click the **Connect Nightwatch** button in your environment dashboard.

**3. Enable monitoring**

Toggle **Enable monitoring** to activate Nightwatch for your environment.

**4. Enter your Nightwatch token**

Enter your Nightwatch token, which you can find in your Nightwatch application settings.

> [!NOTE]
>
> When you enable Nightwatch, Laravel Cloud runs the agent on all App and worker clusters in the environment. You can [set up Nightwatch manually](https://laravel.com/cloud/docs/knowledge-base/nightwatch-on-cloud) if you want the agent to run on specific instances.

When you enable Nightwatch, Laravel Cloud automatically injects the following environment variables into your environment:

```
NIGHTWATCH_TOKEN=
NIGHTWATCH_REQUEST_SAMPLE_RATE=0.1
LOG_CHANNEL=stack
LOG_STACK=laravel-cloud-socket,nightwatch
```

You can override these variables in your environment variable settings if needed.

> [!WARNING]
>
> If you have previously [configured Nightwatch manually](https://laravel.com/cloud/docs/knowledge-base/nightwatch-on-cloud) with a background process, remove that process from every cluster before you enable the built-in integration. Otherwise, your environment may run into issues.
