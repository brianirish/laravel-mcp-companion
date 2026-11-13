Source: https://laravel.com/cloud/docs/knowledge-base/logs.md

# Understanding logs

Learn about common application logs when using Laravel Cloud.

## \[error] Access forbidden by rule

Like most websites on the internet, your site will often see bots scanning it for vulnerabilities. When a bot requests a page that does not exist, or a page that Laravel Cloud blocks for security purposes, you may see related `[error]` logs. You can safely ignore these logs.

```shell theme={null}
Example logs:

2025-03-26 17:26:05 UTC
2025/03/26 17:26:05 [error] 148#148: *35409 access forbidden by rule, client: 2600:1f16:e0:8506:ea9f::8, server: _, request: "GET /config/php.ini HTTP/1.1", host: "yourWebsite.com"

2025-03-26 17:26:18 UTC
2025/03/26 17:26:18 [error] 150#150: *35439 access forbidden by rule, client: 2600:1f16:e0:8506:b40f::6, server: _, request: "GET /.aws/credentials HTTP/1.1", host: "yourWebsite.com"

2025-03-26 17:26:24 UTC
2025/03/26 17:26:24 [error] 150#150: *35455 access forbidden by rule, client: 2600:1f16:e0:8506:ea9f::8, server: _, request: "GET /config.ini HTTP/1.1", host: "yourWebsite.com"
```

***

## fatal: not a git repository

Some packages may attempt to access your `.git` directory while your application is running. Laravel Cloud removes the `.git` folder during the deploy process, so the directory is unavailable at runtime. Packages that depend on the `.git` directory can then trigger this error. For example, Sentry gives you the option to run Git to grab the current commit hash, which triggers these errors.

If a package depends on your deployment's Git hash being available, you can inject it as an environment variable by adding the following to your build commands:

```bash theme={null}
# Install production dependencies...
composer install --no-dev

# Add the Git commit hash to an environment variable...
echo -e "\nSENTRY_RELEASE=`git log --pretty="%h" -n1 HEAD`" >> .env

# Cache the configuration to make SENTRY_RELEASE available at runtime...
php artisan config:cache
```

***

## \[truncated due size]

The `[truncated due size...]` message means that a log message exceeded a size limit and was cut off. Long logs and error messages cause this, and it is common during deployments. To reduce the output of your deploy commands, add flags that make the commands less verbose:

```
composer install --no-dev --quiet

npm ci --quiet --no-progress
```

If your application has `APP_DEBUG=true`, errors produce a full stack trace, which can also be truncated.
