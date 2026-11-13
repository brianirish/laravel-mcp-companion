Source: https://laravel.com/cloud/docs/preview-environments.md

# Preview Environments

Generate a fully isolated environment for every pull request to safely test changes, share previews, and catch issues before merging.

[Preview environments](https://www.youtube.com/embed/UB_zqrLE8Qw)

## Introduction

Preview environments generate fully isolated environments for every pull request so you can test changes, share previews, and catch issues before merging. By default, each preview environment scales to zero when idle and is automatically removed when the pull request is merged or closed.

> [!NOTE]
>
> Preview environments are available on all plans, with unlimited preview
> environments on the [Growth and Business plans](https://laravel.com/cloud/docs/pricing#plans). The Starter
> plan includes one preview automation per organization, which can generate multiple
> preview environments from a single target environment.

## What you can use them for

* Review every pull request in a live environment before merging.
* Share a live URL with team members, reviewers, and stakeholders.
* Run automated tests and QA against isolated infrastructure.
* Validate database migrations and infrastructure changes without impacting production.

## How preview environments work

**1. Trigger detected**

Laravel Cloud listens to your linked repository and generates a preview environment
when your trigger conditions are met.

**2. Resources provisioned**

Laravel Cloud builds each preview from isolated, inexpensive defaults that
scale to zero where available. You may change these defaults to customize
how Cloud provisions each resource.

**3. Preview deployed**

The preview deploys to a unique Cloud domain, which Cloud posts as a comment
on the pull request.

**4. Updates redeployed**

When push to deploy is enabled, new commits to the pull request rebuild and
redeploy the preview. Previews copy this setting from the target environment.

**5. Environment cleaned up**

When the pull request is merged or closed, auto-destroy removes the
environment and any resources it created.

## Configuring preview environments

To create a new automation or edit an existing one:

1. Open the environment you want to generate previews from.
2. Navigate to **Settings > Preview environments**.
3. Click **New automation** to create one, or select an existing automation to edit it.

### Automation rules

Automation rules control how Cloud creates, deploys, and cleans up previews. Each automation runs on pull requests opened or reopened against the target environment's branch. Pull requests from forks do not create previews.

> [!NOTE]
>
> Bitbucket preview environments require migrating to our new Git provider
> integration. On Bitbucket, Cloud creates previews when a pull request is opened,
> but not when a closed pull request is reopened.

* **Rule name**: A descriptive name for the automation.
* **Enable branch filtering**: Only run when the branch name matches a specific pattern.
* **Auto-deploy on creation**: Automatically deploy the new preview environment when created.
* **Delete on merge or close**: Automatically delete the preview environment and its resources when the pull request is merged or closed. When disabled, previews remain until you delete them manually.

### Replication settings

Replication settings control how Cloud provisions each resource for a preview environment. The defaults create fully isolated environments at the most economical setting and use scale to zero where available.

#### Compute

Compute settings apply to your App and worker clusters. Previews also receive isolated managed queues when the target environment uses them and managed queues are enabled for your framework.

* **Create new and scale to zero** (default): Isolated compute that matches your target configuration and sleeps when idle.
* **Create new with current settings**: Isolated compute that matches your target configuration.

> [!NOTE]
>
> If your target environment uses Pro tier compute and you select a scale-to-zero
> option, Cloud replicates it onto the largest Flex size with scale to zero
> enabled that has no more memory than your target compute.

#### Database

* **Create new and scale to zero** (default for Laravel MySQL and Laravel Serverless Postgres): Isolated database cluster that matches your target configuration and sleeps when idle.
* **Create new** (default for RDS): An isolated database on your existing cluster.
* **Share with the target environment**: Reuses your target database. Migrations and data changes affect the shared database, and data cannot be removed after a preview is deleted.
* **No database**: Previews run without a database.

> [!WARNING]
>
> Sharing existing resources with preview environments puts performance and data
> integrity at risk, so use this option with caution. A preview shares the same
> resource as your target environment, so its migrations or data changes can
> affect the target environment directly.

#### Cache

* **Create new and scale to zero** (default for Valkey): Isolated cache that matches your target configuration and sleeps when idle.
* **Create new and downsize** (default for caches that don't support scale to zero, such as Upstash): Isolated cache at a smaller size. Cloud creates Upstash caches at 250 MB and ElastiCache clusters at `r7g.large`.
* **Share with the target environment, namespaced by prefix**: Reuses your cache. Entries persist after a preview is deleted and cannot be selectively removed.
* **No cache**: Previews run without a cache.

> [!NOTE]
>
> Sharing a cache without a prefix is deprecated. If an existing automation
> still uses it, you can upgrade to a current option directly in the Cloud
> dashboard for improved isolation.

When you share a cache, Cloud adds a `REDIS_PREFIX` variable to the preview's environment variables, set to `application:environment:`, so its keys stay separate from other environments. If the preview runs Laravel Horizon, Cloud also sets `HORIZON_PREFIX`. Laravel applications use `REDIS_PREFIX` automatically. Other frameworks must configure their Redis client to use it.

#### Object storage

* **Create new bucket** (default): An isolated bucket for the preview environment.
* **Share with the target environment**: Reuses your existing bucket. Files persist after a preview is deleted and cannot be selectively removed.
* **No object storage**: Previews run without object storage.

#### WebSockets

WebSockets settings are available for frameworks that support Laravel Reverb.

* **Create new cluster and downsize** (default): Isolated WebSocket cluster at the lowest available size.
* **Use same WebSockets application**: Reuses your existing application and shares cluster capacity.
* **No WebSockets**: Previews run without WebSockets.

### Options

#### HTTP basic authentication

Enable HTTP basic authentication for every preview created by the automation. Visitors enter the username `admin` and the password you set before traffic reaches your application. HTTP basic authentication guards preview links shared in pull requests and keeps automated bots from waking sleeping previews. HTTP basic authentication is available on the [Growth plan](https://laravel.com/cloud/docs/pricing) or higher.

#### Environment variables

Preview environments do not inherit environment variables from the target environment. Each automation defines its own complete set of variables.

Laravel Cloud prefills a Laravel automation with a freshly generated `APP_KEY`, a Symfony automation with an `APP_SECRET`, a Django automation with a `SECRET_KEY`, and a Rails automation with a `SECRET_KEY_BASE`. For Django applications, Cloud also prefills `DJANGO_SETTINGS_MODULE` when it detects your settings module. Every preview the automation creates shares these values, so production secrets do not reach preview environments.

When you configure an automation, set any additional variables and secrets your previews need. JavaScript, Go, Flask, and generic Python applications may require framework-specific configuration. Subject to your role's permissions, you can view the target environment's variables to see which keys to set, but Cloud never copies their values automatically.

If your Rails application uses [encrypted credentials](https://laravel.com/cloud/docs/deploy-guides/ruby#encrypted-credentials), add the matching `RAILS_MASTER_KEY` to the automation's environment variables or linked [secrets](https://laravel.com/cloud/docs/secrets). The generated `SECRET_KEY_BASE` does not decrypt those credentials.

> [!NOTE]
>
> Automations created before July 13, 2026 may use a configuration that inherits
> environment variables from the target environment, which can carry its secrets
> into previews. Open the automation in the Cloud dashboard to upgrade it to the
> new, more secure model.

#### Injected variables

Cloud automatically injects variables into every preview, such as the credentials for its replicated resources. The variable names and connection settings depend on the attached resources and your application's runtime. These variables are read-only, but you can override any of them by defining a variable with the same name in the automation's environment variables.

## Managing automations

### Updating an automation

You can edit automation rules at any time. Updated rules take effect for new preview environments only. Previews that the rule already generated keep their existing configuration, so update them manually if needed. To modify an existing preview environment, edit it directly like any other environment, including resizing compute and provisioning additional resources.

In an individual preview environment's settings, you can override the password protection and automatic deletion settings inherited from its automation, and add or edit environment variables. These changes apply only to that preview environment.

### Deleting an automation

Delete an automation from **Settings > Preview environments**. Deleting an automation stops new previews from being generated. Any previews it already created remain active, so delete them individually if you no longer need them.

## Billing

Laravel Cloud meters and bills each preview environment's resources like any other environment. By default, Cloud enables scale to zero on the resources that support it, so you pay for previews only while you're actively previewing changes.
