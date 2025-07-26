# Forge - Sites/Deployments

*Source: https://forge.laravel.com/docs/sites/deployments*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)

##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

On this page

- [Overview](#overview)
- [Environments](#environments)
- [Environment Circle Permission](#environment-circle-permission)
- [Encrypted Environment Files](#encrypted-environment-files)
- [Quick Deploy](#quick-deploy)
- [Deploy Script](#deploy-script)
- [PHP Versions](#php-versions)
- [Restarting Daemons During Deployment](#restarting-daemons-during-deployment)
- [Environment Variables](#environment-variables)
- [Deploying From CI](#deploying-from-ci)
- [Using Deployment Triggers](#using-deployment-triggers)
- [Using Forge CLI](#using-forge-cli)
- [Example With GitHub Actions](#example-with-github-actions)
- [Example With Chipper CI](#example-with-chipper-ci)
- [Deployment Branch](#deployment-branch)
- [Git Remote](#git-remote)
- [Deployment Notifications](#deployment-notifications)
- [Slack](#slack)
- [Telegram](#telegram)
- [Discord](#discord)
- [Webhooks](#webhooks)
- [Circle Permissions](#circle-permissions)

Sites

# Deployments

Manage code deployments with scripts, queues, and CI tools

## [​](#overview) Overview

A deployment is the process in which your code is downloaded from your source control provider on to your server, ready for the world to access. Forge tracks the latest 10 deployments so that you can see what was deployed, when it was deployed, how long it took to be deployed, and also view the output of your [deploy script](/docs/sites/deployments#deploy-script).

## [​](#environments) Environments

Some applications, such as those created with the Laravel framework, may require a `.env` file to configure settings such as databases and caches. You can create and edit your Environment file within the Forge site’s management dashboard.

If your project contains a `.env.example` file, Forge will automatically copy this and replace some of the settings to match your server’s database settings. An empty `.env.example` could result in an empty environment file on the first deploy.

### [​](#environment-circle-permission) Environment Circle Permission

You may grant a circle member authority to view and edit a site’s environment file (or WordPress configuration) using the `site:manage-environment` permission. Without this permission, Forge will **not** display the contents of the environment file to circle members.

### [​](#encrypted-environment-files) Encrypted Environment Files

Forge provides support for Laravel’s [encrypted environment files](https://laravel.com/docs/configuration#encrypting-environment-files) without requiring you to include your encryption key within your deployment script.
To leverage this feature, add your encryption key to the “Environment Encryption Key” section of your site’s management dashboard. Once added, Forge will inject the value into the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable during deployment, allowing you to add the `env:decrypt` Artisan command to your deployment script without explicitly setting the `--key` option:

Copy

Ask AI

```
php artisan env:decrypt --force

```

## [​](#quick-deploy) Quick Deploy

Forge’s “Quick Deploy” feature allows you to easily deploy your projects when you push to your source control provider. When you push to your configured quick deploy branch, Forge will pull your latest code from source control and run your application’s configured deployment script.
You can enable Forge’s quick deploy feature by clicking the “Enable Quick Deploy” button within the *Apps* tab of your site’s management dashboard.
For sites using a [custom source control provider](/docs/accounts/source-control#using-a-custom-git-provider) you will need to manually set up a [Deployment Trigger](/docs/sites/deployments#deploying-from-ci) to have your code deployed when you push to your source provider. Click the “Manage Quick Deploy” button within the *Apps* tab of your site’s management dashboard for instructions.

## [​](#deploy-script) Deploy Script

The commands that are executed on your server when your project is deployed are determined by your site’s deployment script. Of course, this deployment script can be edited directly within the Forge UI. By default, your site’s deployment script will:

- Navigate into the site’s directory
- Execute the `git pull` command
- Installs your application’s Composer dependencies
- Execute the `php artisan migrate` command (if your application contains an `artisan` file)

You can make your `.env` variables available to your deploy script by checking the “Make .env variables to deploy script” checkbox below the Deploy Script panel. When enabled, Forge will automatically inject the variables in your site’s `.env` file into the deploy script, allowing them to be accessed like any normal Bash variable:

Copy

Ask AI

```
echo "${APP_NAME} is deploying..."

```

Deployments may make your site unavailable for a brief moment. If you need absolutely zero downtime during deployments, check out [Envoyer](https://envoyer.io).

### [​](#php-versions) PHP Versions

If you have installed [multiple versions of PHP](/docs/servers/php) on your server, your deploy script may need to be updated to use the correct version of PHP.
By default, `php` will always point to the active version of PHP used on the CLI. If you need to use a different version of PHP, you must use `phpx.x` where `x.x` reflects on the version used (e.g. `php8.4`) when invoking PHP commands.
The deployment script for newly created sites uses the `$FORGE_PHP` [environment variable](#environment-variables). This environment variable will always contain the current PHP binary configured for the site, so no additional changes are needed to your deployment script when using this variable and switching your site’s PHP version.

### [​](#restarting-daemons-during-deployment) Restarting Daemons During Deployment

When deploying applications that use [daemons](/docs/resources/daemons) (such as Next.js applications), you may need to restart the daemon to ensure it picks up your code changes. You can do this by adding the restart command to your deployment script:

Copy

Ask AI

```
# Restart your daemon (replace 12345 with your daemon's ID)...
sudo supervisorctl restart daemon-12345:*

```

You can find your daemon’s ID in the Forge dashboard under your server’s **Daemons** tab.

### [​](#environment-variables) Environment Variables

Forge will automatically inject the following environment variables into your deployment script at runtime:

| Key | Description |
| --- | --- |
| `FORGE_COMPOSER` | The path to the Composer installation. |
| `FORGE_CUSTOM_DEPLOY` | Whether the deployment was triggered with a custom deployment trigger request. |
| `FORGE_DEPLOY_AUTHOR` | The author of the commit. |
| `FORGE_DEPLOY_COMMIT` | The Git hash of the commit being deployed. |
| `FORGE_DEPLOY_MESSAGE` | The Git commit message. |
| `FORGE_DEPLOYMENT_ID` | The Forge assigned ID of this deployment. |
| `FORGE_MANUAL_DEPLOY` | Whether the deploy was triggered by clicking “Deploy Now”. |
| `FORGE_PHP_FPM` | The PHP-FPM process name that is being used by Forge. |
| `FORGE_PHP` | The `php` binary that is being used by the Forge site or server. |
| `FORGE_QUICK_DEPLOY` | Whether the deploy was triggered by a source control provider webhook. |
| `FORGE_REDEPLOY` | Whether this is a re-deployed commit. |
| `FORGE_SERVER_ID` | The ID of the Forge server that is being deployed to. |
| `FORGE_SITE_BRANCH` | The name of the branch that is being deployed. |
| `FORGE_SITE_ID` | The ID of the Forge site that is being deployed to. |
| `FORGE_SITE_PATH` | The root of the deployment path, e.g. `/home/forge/mysite.com` |
| `FORGE_SITE_USER` | The name of the user deploying the site. |

You may use these variables as you would any other Bash variable:

Copy

Ask AI

```
if [[ $FORGE_MANUAL_DEPLOY -eq 1 ]]; then
    echo "This deploy was triggered manually."
fi

```

For example, you may wish to prevent deployments if the commit message contains “wip”:

Copy

Ask AI

```
if [[ $FORGE_DEPLOY_MESSAGE =~ "wip" ]]; then
    echo "WORK IN PROGRESS, DO NOT CONTINUE."
    exit 1
fi

```

*[Content truncated for length]*