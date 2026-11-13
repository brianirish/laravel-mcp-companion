Source: https://herd.laravel.com/docs/macos/guides/laravel.md

# Laravel

# How to set up a Laravel application

Herd's main purpose is serving Laravel developers by providing a fully integrated development stack with PHP and nginx at its core. Both services are complemented with all tools that you need to work on almost any Laravel application. This means that Herd is the right tool, no matter if you are just starting as a beginner or work with Laravel for a decade.

This guide covers all steps that you need to follow to get up and running with a new Laravel application but also works if you replace the application creation step with checking out an existing git repository.

## Code Directory

Herd uses the concept of *parked paths* for serving sites via `.test` domains. By default, Herd creates and parks the `~/Herd` directory and every folder that you create in this directory is reachable via its own domain.

Let's open your terminal and go into the directory:

```bash theme={null}
cd ~/Herd
```

## Database Choices

Laravel ships with an SQLite database for your application by default but if you are familiar with MySQL or PostgreSQL, you should get a database instance up and running before you create or check our your application.

> [!NOTE]
>
> [Herd Pro]() allows you to install database instances and other complementary services directly from Herd – but you can also download and run the database of your choice separately.

## Installing Laravel

If you prefer a graphical interface, you can also create applications in Herd's new application window, or describe your idea and let a coding agent [build it for you](https://herd.laravel.com/docs/macos/herd-studio/build-with-ai.md).

The easiest way to download and install a fresh Laravel application is the command line. Herd ships with the Laravel installer, and it's already available in your CLI, so switch back to the terminal and run the following command. The first line creates the application, the second line switches in your application directory for further commands.

```bash theme={null}
laravel new my-first-application
cd my-first-application
```

If you have an existing Laravel application and git is available on your terminal, simply clone the repository and follow the setup guide for the application's readme file. It's usually something like this:

```bash theme={null}
git clone path-to-your-repository
cd repository-name
cp .env.example .env
composer install
herd php artisan key:generate
herd php artisan migrate
```

## Visit your application in the browser

Your application is now up and running, and you can visit it via it's `.test` domain. Herd provides a command to open your browser directly from your terminal.

```bash theme={null}
herd open
```

You can now start working on your application, if you've set up a favorite editor, in the Herd settings, you can open the editor via the command `herd edit`.

[Herd Pro](https://herd.laravel.com/docs/#features) users can set up additional services and start using the integrated dump debugging feature, work with emails and check our their logs, so if you are using Herd Pro, this is how they work.

## Set up Services

You can set up and manage [services](https://herd.laravel.com/docs/macos/herd-pro-services/services.md) directly in Herd with a convenient interface. Simply head over to the services tab in the settings and add the service that you need. Herd supports many widely used services like databases, caches, and search-, and storage engines.

### Databases

* [MySQL](https://herd.laravel.com/docs/macos/herd-pro-services/mysql.md)
* [MariaDB](https://herd.laravel.com/docs/macos/herd-pro-services/mariadb.md)
* [PostgreSQL](https://herd.laravel.com/docs/macos/herd-pro-services/postgresql.md)
* [MongoDB](https://herd.laravel.com/docs/macos/herd-pro-services/mongodb.md)

### Caches and Queues

* [Redis](https://herd.laravel.com/docs/macos/herd-pro-services/redis.md)
* [Valkey](https://herd.laravel.com/docs/macos/herd-pro-services/valkey.md)

### Broadcasting and Realtime

* [Laravel Reverb](https://herd.laravel.com/docs/macos/herd-pro-services/laravel-reverb.md)

### Search

* [Meilisearch](https://herd.laravel.com/docs/macos/herd-pro-services/meilisearch.md)
* [Typesense](https://herd.laravel.com/docs/macos/herd-pro-services/typesense.md)

### Storage

* [MinIO](https://herd.laravel.com/docs/macos/herd-pro-services/minio.md)
* [RustFS](https://herd.laravel.com/docs/macos/herd-pro-services/rustfs.md)

You can install all these services with a few clicks and decide if you want to start them with Herd automatically or only on demand.

To use a service in your application, select the application in the Applications window and pick the service in the "Services" section of the inspector. Herd updates your `.env` file accordingly. Learn more in [Per-Site Services](https://herd.laravel.com/docs/macos/herd-pro-services/per-site-services.md).


## Debug with Insights

The most common debugging method in Laravel is using the helpers for `dump()` or `dd()`. While `dd` stands for `dump and die` and stops your application, `dump` simply displays some output. Herd Pro has a separate [Insights](https://herd.laravel.com/docs/macos/debugging/insights.md) window that displays this information in a great way and also shows Eloquent queries, logs and more. As a first test, you can invoke the dump function and print out the simple string `hello from your app`.

Go to your terminal and start a tinker session by running the tinker command of the Herd command line interface. It proxies the tinker command of Laravel but always uses the application PHP:

```bash theme={null}
herd tinker
```

Once tinker has started, you can use the dump helper to output the string:

```bash theme={null}
dump("hello from your app");
```

When running this simple command, the string appears in the Insights window. Herd only captures CLI commands like tinker if you turn on "Include `php` CLI commands" in the AI tab of the settings. You can use the `dump` and `dd` helper anywhere in your application to debug browser requests and CLI commands.


## Test Emails

Testing emails can be cumbersome and even result in sending emails to your users when you're connected to a real mail service. Herd solves this by running a local email server that catches your mails and sends them to an internal email client that you can use for testing the email.

To enable the email server for your application, go to the `env` file in the root of your application directory and make sure to update the mail settings according to the following configuration.

```bash theme={null}
MAIL_MAILER=smtp
MAIL_HOST=127.0.0.1
MAIL_PORT=2525
MAIL_USERNAME=${APP_NAME}
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="hello@example.com"
MAIL_FROM_NAME="${APP_NAME}"
```

Every time when your application sends an email, it uses Herd's integrated mail service. If it's the first email from this application, it creates an inbox for this application based on the name of the application so that you can easily identify emails and where they are from.

Please make sure that your application name does not include any special characters or if it does, simply change the `MAIL_USERNAME` in the configuration above to something easily identifiable.

So after you've setup up the mail service, let's test the configuration by creating a test email and sending it via tinker.

```bash theme={null}
herd php artisan make:mail TestMail --markdown
herd tinker
```

Send the email in your tinker session via the mail facade.

```php theme={null}
Mail::to('sebastian@beyondcode.com')->send(new \App\Mail\TestMail());
```


After setting up your first Laravel application in Herd, you can now follow the docs to learn more about all features in more detail and fully leverage Herd when using it every day.
