Source: https://herd.laravel.com/docs/windows/sites/herd-yaml.md

# Herd.yml

# Sharing project configurations

When working in a team, it's important to ensure that everyone uses the same PHP version, certificate settings, and service versions. You can use the `herd.yml` file to manage these configurations within your repository.

## Creating the `herd.yml` file

The easiest way to create the `herd.yml` file is by running the `herd init` command in your project directory.

```powershell theme={null}
herd init
```

This command starts a wizard to guide you through the setup process of the `herd.yml` file. If you run `herd init` in a project that already has this file, it configures your site accordingly. Re-running the command after a change, applies all additional configurations but does not remove existing ones.

The setup allows you to configure the following settings:

* Project Name
* Aliases (aka multiple domains)
* PHP Version
* TLS/SSL Certificates

[Herd Pro](https://herd.laravel.com/checkout) users can also specify [services](https://herd.laravel.com/docs/windows/herd-pro-services/service-versions.md) in their `herd.yml` and to install them automatically. By default, Herd preselects the services that are present in your `.env` file, but you can add more if needed.

The list contains the latest versions of these services and if you need other versions, check the section about [editing the `herd.yml` file](#editing-the-codeherdymlcode-file).

```bash theme={null}
 ~ herd-website  (main)
› herd init --fresh

 ┌ What is the name of your project? ───────────────────────────┐
 │ herd-website                                                 │
 └──────────────────────────────────────────────────────────────┘

...

 ┌ Do you want to add additional services? ─────────────────────┐
 │ › ◻ Meilisearch (1.6.2)                                    ┃ │
 │   ◻ MinIO (RELEASE.2024-03-05)                             │ │
 │   ◼ MySQL (8.0.36)                                         │ │
 │   ◻ PostgreSQL (16)                                        │ │
 │   ◼ Redis (7.0.0)                                          │ │
 └────────────────────────────────────────────────── 2 selected ┘
  Use the space bar to select options.
```

After running the wizard, a `herd.yml` file will be created in your project root. To overwrite an existing file, you can use the `herd init --fresh` command and generate a new file.

## Setting up a project via `herd.yml`

If a `herd.yml` file exists in your project, Herd can automatically apply the necessary configuration via the `herd init` command.

```bash theme={null}
herd init
```

Running `herd init` checks for the presence of an `.env` file and if not, asks if the `.env.example` file should be copied. After that, this command applies the configurations, including installing and isolating the specific PHP version, aliases, services and more:

```bash theme={null}
 ~ herd-website  (main)
› herd init

   INFO  Setting up your project…

   INFO  PHP 8.3 is installed.

   INFO  Site is secured.

   INFO  Mysql is running on port 3346

   INFO  Installing service Redis
   INFO  Redis is running on port 6379

   DONE  Your application is ready to go!
```

If the `herd.yml` file contains a service that isn't available on your machine, Herd skips this service with a warning and continues with the setup. Run `herd services:available` to see which services Herd supports.

## Editing the `herd.yml` file

Here is an example of a `herd.yml` file using all possible customizations:

```yaml theme={null}
name: herd-website
php: '8.3'
secured: true
aliases:
    - herd-laravel
services:
    mysql:
        version: 8.0.36
        port: '${DB_PORT}'
    redis:
        version: 7.0.0
        port: '${REDIS_PORT}'
```

Instead of referencing your applications' `.env` file with the placeholder (e.g. `${REDIS_PORT}`) you can set a fixed port as well - just keep in mind that your team members may use these ports already.

You can check out a list of available services and versions [here](https://herd.laravel.com/docs/windows/herd-pro-services/service-versions.md).

## Configuring workspaces

The `workspaces` section of the `herd.yml` file configures how Herd sets up [workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) for your project. You can define the default database mode, files that Herd copies into every workspace, environment variables and hooks that run after creating or before deleting a workspace.

```yaml theme={null}
workspaces:
  database: clone
  copy:
    - storage/app/public
  env:
    MAIL_FROM_NAME: "{{branch}}"
  hooks:
    after_create:
      - composer install
      - npm run build
```

See [Configuring workspaces in herd.yml](https://herd.laravel.com/docs/windows/sites/workspaces.md#configuring-workspaces-in-herdyml) for all options.
