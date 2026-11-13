Source: https://laravel.com/cloud/docs/knowledge-base/command-failed-prod-app.md

# Fix production command failures

Resolve production command failures in Laravel Cloud when commands prompt for confirmation in non-interactive environments.

Some migration operations are destructive, which means they may cause you to lose data. All Laravel Cloud environments default to `APP_ENV=production`, so you may run into issues when you run one-off migrations from the **Commands** tab of your environment panel. These commands are not interactive, so a command fails if it tries to prompt you for input. This failure happens most often when you run migrations in a production environment.

```shell theme={null}

                           APPLICATION IN PRODUCTION.

   WARN  Command cancelled.

```

If you accept the risks of running migrations in a production environment, pass a flag to bypass the production environment warning.

> [tab] Laravel
>
> Append the `--force` flag to bypass the production prompt:
>
> ```bash theme={null}
> php artisan migrate --force
> ```
>
> Related commands that may also require the `--force` flag include:
>
> ```bash theme={null}
> php artisan migrate:fresh --force
> php artisan migrate:refresh --force
> php artisan db:seed --force
> ```

> [tab] Symfony
>
> Append the `--no-interaction` flag to bypass the production prompt:
>
> ```bash theme={null}
> php bin/console doctrine:migrations:migrate --no-interaction
> ```
>
> Related commands that may also require the `--no-interaction` flag include:
>
> ```bash theme={null}
> php bin/console doctrine:migrations:migrate --no-interaction --allow-no-migration
> php bin/console doctrine:schema:update --no-interaction --force
> ```

### Customizing your `APP_ENV`

If you are working on a non-production environment, consider overriding the `APP_ENV` variable in your environment's [custom environment variables](https://laravel.com/cloud/docs/environments#environment-variables) to match the environment's purpose. Non-production environments do not trigger the production warning.

```
APP_ENV=development
```
