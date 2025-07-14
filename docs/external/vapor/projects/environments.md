# Vapor - Projects/Environments

*Source: https://docs.vapor.build/projects/environments*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#e29483928d90a28e83908394878ecc818d8f)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationProjectsEnvironments[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/vapor)
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

Projects# Environments

Learn how to manage environments in Laravel Vapor.

## [​](#introduction)Introduction

As you may have noticed, projects do not contain much information or resources themselves. All of your deployments and invoked commands are stored within environments. Each project may have as many environments as needed.

Typically, you will have an environment for “production”, and a “staging” environment for testing your application. However, don’t be afraid to create more environments for testing new features without interrupting your main staging environment.

## [​](#creating-environments)Creating Environments

Environments may be created using the `env` Vapor CLI command:

CopyAsk AI```
vapor env my-environment

```

This command will add a new environment entry to your project’s `vapor.yml` file that you may deploy when ready:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        build:
            - 'composer install --no-dev'
    my-environment:
        build:
            - 'composer install --no-dev'

```

In addition to our native runtimes, Vapor supports Docker image deployments. If you would like an environment to use a Docker image runtime instead of the default Vapor runtime, use the `--docker` option when creating your environment:

CopyAsk AI```
vapor env my-environment --docker

```

This command will create a `my-environment.Dockerfile` file in your application’s root directory.

## [​](#opening-environments)Opening Environments

Environments may be opened in your default browser using the Vapor CLI’s `open` command:

CopyAsk AI```
vapor open my-environment

```

## [​](#default-environment)Default Environment

When executing a Vapor CLI command, Vapor CLI uses the `staging` environment by default:

CopyAsk AI```
vapor open // Opens the `staging` environment in your default browser...

vapor open production // Opens the `production` environment in your default browser...

```

However, within your application’s `vapor.yml` file, you may define a `default-environment` option to change the default environment for your project:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
default-environment: production
environments:
    production:
        build:
            - 'composer install --no-dev'
    my-environment:
        build:
            - 'composer install --no-dev'

```

## [​](#environment-variables)Environment Variables

Each environment contains a set of environment variables that provide crucial information to your application during execution, just like the variables present in your application’s local `.env` file.

### [​](#vapor%E2%80%99s-default-environment-variables)Vapor’s Default Environment Variables

Vapor automatically injects a variety of environment variables based on your environment’s configured cache, database, etc. As an example, by adding a `cache` or `database` key to your `vapor.yml` file, Vapor will inject the necessary `CACHE_*` and `DB_*` environment variables.

Here is the full list of environment variables injected by Vapor on your environment:

`.env` Value`env()` Value`APP_ENV`Environment name`APP_DEBUG`False`APP_LOG_LEVEL`Debug`APP_URL`Vanity domain, or custom domain if exists`ASSET_URL`CloudFront`AWS_BUCKET`Storage resource if exists`BROADCAST_DRIVER`Pusher`CACHE_DRIVER`DynamoDB, or cache (Redis) resource if exists`DB_*`Database (MySQL, Postgresql, etc) resource if exists`DYNAMODB_CACHE_TABLE``vapor_cache``FILESYSTEM_DISK`S3`FILESYSTEM_DRIVER`S3`FILESYSTEM_CLOUD`S3`LOG_CHANNEL`Stderr`MAIL_DRIVER`LOG, but SES for environments with the name `production``MAIL_MAILER`LOG, but SES for environments with the name `production``MAIL_FROM_ADDRESS``[[email protected]](/cdn-cgi/l/email-protection)` or `[[email protected]](/cdn-cgi/l/email-protection)` if exists`MAIL_FROM_NAME``your_project_name``MIX_URL`CloudFront`QUEUE_CONNECTION`SQS`SCHEDULE_CACHE_DRIVER`DynamoDB`SESSION_DRIVER`Cookie
You will not see these environment variables when you manage your environment via Vapor CLI or Vapor UI, and any variables you manually define will override Vapor’s automatically injected variables.

### [​](#updating-environment-variables)Updating Environment Variables

You may update an environment’s variables via the Vapor UI or using the `env:pull` and `env:push` CLI commands. The `env:pull` command may be used to pull down an environment file for a given environment:

CopyAsk AI```
vapor env:pull production

```

Once this command has been executed, a `.env.{environment}` file will be placed in your application’s root directory. To update the environment’s variables, simply open and edit this file. When you are done editing the variables, use the `env:push` command to push the variables back to Vapor:

CopyAsk AI```
vapor env:push production

```

If you are using the DotEnv library’s [variable nesting](https://github.com/vlucas/phpdotenv#nesting-variables) feature to reference default environment variables that Vapor is injecting, you should replace these references with literal values instead. Since Vapor’s injected environment variables do not belong to the environment file, they can not be referenced using the nesting feature.

After updating an environment’s variables, the new variables will not be utilized until the application is deployed again. In addition, when rolling back to a previous deployment, Vapor will use the variables as they existed at the time the deployment you’re rolling back to was originally deployed.

Due to AWS Lambda limitations, your environment variables may only be 4kb in total. To accommodate Vapor’s own injection of environment variables, users are limited to 2,000 characters of environment variables. You should use encrypted environment files in place of or in addition to environment variables if you exceed this limit.

### [​](#reserved-environment-variables)Reserved Environment Variables

The following environment variables are reserved and may not be added to your environment:

- `_HANDLER`

- `AWS_ACCESS_KEY_ID`

- `AWS_DEFAULT_REGION`

- `AWS_EXECUTION_ENV`

- `AWS_LAMBDA_FUNCTION_MEMORY_SIZE`

- `AWS_LAMBDA_FUNCTION_NAME`

- `AWS_LAMBDA_FUNCTION_VERSION`

- `AWS_LAMBDA_LOG_GROUP_NAME`

- `AWS_LAMBDA_LOG_STREAM_NAME`

- `AWS_LAMBDA_RUNTIME_API`

- `AWS_REGION`

- `AWS_SECRET_ACCESS_KEY`

- `AWS_SESSION_TOKEN`

- `LAMBDA_RUNTIME_DIR`

- `LAMBDA_TASK_ROOT`

- `TZ`

In addition, environment variables should not contain `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, or `AWS_SESSION_TOKEN` in their names. For example: `MY_SERVICE_AWS_SECRET_ACCESS_KEY`.

## [​](#encrypted-environment-files)Encrypted Environment Files

Vapor provides built-in support for Laravel’s [encrypted environment files](https://laravel.com/docs/configuration#encrypting-environment-files). If Vapor discovers an encrypted environment file while booting your application, it will automatically attempt to decrypt it and inject the resulting variables into the runtime.

To leverage this feature, you must first ensure an encrypted environment file is present at the root of your application during deployment. For example, deploying the `production` environment requires a file called `.env.production.encrypted` to be present at the root of your application.

Additionally, you should ensure the decryption key is available in the runtime by defining it as the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable via the Vapor UI or [CLI](/_sites/docs.vapor.build/projects/environments#environment-variables).

Utilizing encrypted environment files requires your application to be running Laravel >= v9.37 and Vapor Core >= v2.26.

### [​](#passport-keys)Passport Keys

You may easily add your project’s Passport keys to your encrypted environment file using the `env:passport` CLI command:

CopyAsk AI```
vapor env:passport production

```

The `env:passport` command will append the contents of your local Passport keys to your `.env.production` file. When the command completes, you should re-encrypt the environment file using Laravel’s `env:encrypt` command and redeploy your project in order for the changes to take effect.

## [​](#maintenance-mode)Maintenance Mode

When deploying a Laravel application using a traditional VPS like those managed by [Laravel Forge](https://forge.laravel.com), you may have used the `php artisan down` command to place your application in “maintenance mode”. To place a Vapor environment in maintenance mode, you may use the Vapor UI or the `down` CLI command:

CopyAsk AI```
vapor down production

```

To remove an environment from maintenance mode, you may use the `up` command:

CopyAsk AI```
vapor up production

```

When an environment is in maintenance mode, the environment’s custom domain will display a maintenance mode splash screen; however, you may still access the environment via its “vanity URL”

### [​](#customizing-the-maintenance-mode-screen)Customizing The Maintenance Mode Screen

You may customize the m

*[Content truncated for length]*