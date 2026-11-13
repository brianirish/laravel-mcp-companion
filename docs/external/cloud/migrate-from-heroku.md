Source: https://laravel.com/cloud/docs/migrate-from-heroku.md

# Migrate from Heroku

Migrate your Laravel application from Heroku to Laravel Cloud with step-by-step deployment guidance.

> [!NOTE]
>
> This guide is for Laravel applications. For Ruby on Rails, see [Migrate Rails to Cloud](https://laravel.com/cloud/docs/knowledge-base/migrating-rails-to-cloud#move-from-heroku).

Learn how to migrate your application from Heroku to Laravel Cloud.

Heroku is a general-purpose platform as a service (PaaS) that many Laravel teams have relied on over the years. However, it requires manual PHP configuration, buildpack management, and Procfiles, which add complexity your application doesn't need. Laravel Cloud offers a simpler operational model with framework-aware defaults, more predictable costs, and no boilerplate setup.

### How to migrate

Migrating from Heroku means replacing Heroku-specific concepts, such as Procfiles, buildpacks, dynos, and add-ons, with their Laravel Cloud equivalents.

The [migration guide](https://laravel.com/cloud/migrate-heroku-cloud) walks you through exporting your Postgres database, provisioning your Laravel Cloud infrastructure, and switching your DNS without any downtime to your existing application.
