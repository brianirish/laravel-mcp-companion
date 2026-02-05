# Forge - Sites/Deployments

*Source: https://forge.laravel.com/docs/sites/deployments*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Sites
Deployments
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)
##### Get Started
- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)
##### Basics
- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Storage Providers](/docs/storage-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)
##### Servers
- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)
##### Sites
- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)
##### Resources
- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)
##### Integrations
- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [Introduction](#introduction)
- [Deployment strategies](#deployment-strategies)
- [Zero-downtime deployments](#zero-downtime-deployments)
- [Release creation and activation](#release-creation-and-activation)
- [Running tasks during deployments](#running-tasks-during-deployments)
- [Configuring deployment retention](#configuring-deployment-retention)
- [Shared paths](#shared-paths)
- [Laravel Octane](#laravel-octane)
- [Standard deployments](#standard-deployments)
- [Push to deploy](#push-to-deploy)
- [Deploy script](#deploy-script)
- [Environment variables](#environment-variables)
- [Making .env variables available](#making-env-variables-available)
- [PHP versions](#php-versions)
- [Restarting background processes](#restarting-background-processes)
- [Deploying from CI](#deploying-from-ci)
- [Deployment hooks](#deployment-hooks)
- [Refreshing the deployment token](#refreshing-the-deployment-token)
- [Using query parameters](#using-query-parameters)
- [Forge CLI](#forge-cli)
- [GitHub Actions example](#github-actions-example)
- [Deployment branch](#deployment-branch)
- [Deployment health checks](#deployment-health-checks)
- [Health check service IP addresses](#health-check-service-ip-addresses)
- [Deployment notifications](#deployment-notifications)
- [Slack](#slack)
- [Telegram](#telegram)
- [Discord](#discord)
- [Webhooks](#webhooks)
Sites
# Deployments
Copy page
Manage code deployments with scripts, queues, and CI tools
Copy page
## [​](#introduction) Introduction
Laravel Forge makes it easy to deploy your applications on demand, whether that be manually, automatically when pushing new code to your source control provider, or via a webhook from your CI platform of choice.
You can see a list of your site’s deployments by navigating to the “Deployments” tab within your site’s management dashboard. Laravel Forge provides a paginated list of your site’s deployments, including what was deployed, when it was deployed, how long it took to be deployed, and also the output of your deploy script.
Deployments are limited to 10 minutes. If a deployment takes longer, it will fail automatically. If your site is integrated with [Envoyer](/docs/integrations/envoyer), Envoyer’s deployment limits apply instead.
## [​](#deployment-strategies) Deployment strategies
Laravel Forge supports two deployment strategies, letting you choose the one that best fits your workflow.
### [​](#zero-downtime-deployments) Zero-downtime deployments
Zero-downtime deployments use a strategy where your new code is cloned into a special `releases` directory, and then a symbolic link is used to “activate” the new code once deployment is completed.
This strategy greatly reduces the risk of your site going down during deployments, as the new code is only activated once all deployment steps have completed successfully. If any step in the deployment process fails, your site will continue to use the previous release.
Zero-downtime deployments are exclusively available for new sites and must be configured at the time of creation — they cannot be added to existing sites later.Laravel Forge automatically enables zero-downtime deployments for all new sites by default. If you prefer not to use this feature, you can disable it by toggling the “Zero-downtime deployments” option in the “Advanced settings” modal during site creation.
#### [​](#release-creation-and-activation) Release creation and activation
If you create a new site with zero-downtime deployments enabled, Laravel Forge will configure your site’s deployment script to include three special “macros”:
- `$CREATE_RELEASE()` – creates the new release directory and clones your site’s code into it.
- `$ACTIVATE_RELEASE()` – activates the new release by creating a symbolic link from the `current` directory to the new release directory.
- `$RESTART_QUEUES()` - restarts any Laravel queues that are running for the site. Additionally, if your site is using Horizon, it will also restart the Horizon process.
It’s important that these commands are included in your deployment script as they are responsible for handling zero-downtime deployments. Failure to include these commands will result in your site not being deployed correctly.
#### [​](#running-tasks-during-deployments) Running tasks during deployments
Forge adds the `cd $FORGE_RELEASE_DIRECTORY` command after the `$CREATE_RELEASE()` macro in the deployment script to make sure all commands located after this code block will be executed in the context of the new release directory. This means that if you need to run any tasks that depend on your new code, you should place those commands after the `cd $FORGE_RELEASE_DIRECTORY` command.
If you need to run any tasks after a new release has been activated, you should place those commands after the `$ACTIVATE_RELEASE()` macro.
For zero-downtime deployments, it is unnecessary to reload the PHP-FPM service because every deployment is deployed to a new, uncached directory.
#### [​](#configuring-deployment-retention) Configuring deployment retention
By default, Laravel Forge retains the last 4 deployments when using zero-downtime deployments. This allows you to quickly rollback to a previous release if needed.
You can change the number of deployments to retain by navigating to your site’s **Settings** tab and clicking **Deployments**. From there, you can adjust the number of deployments that Forge will keep on your server.
#### [​](#shared-paths) Shared paths
When using zero-downtime deployments, shared paths allow you to specify files or directories that should remain consistent across all releases. These paths are automatically symlinked from a shared storage location into each new release directory, ensuring that important data persists between deployments.
Common use cases for shared paths include:
- **Storage directories** – User uploads, generated files, and other application storage
- **Cache directories** – Application caches that should persist between releases
- **Log files** – Application logs that should be preserved across deployments
- **Environment files** – The `.env` file (automatically shared by default)
- **SQLite databases** – SQLite databases that should persist between releases
For example, if you want to share the `storage` directory, you would add `storage` as a shared path. During each deployment, Laravel Forge will create a symbolic link from `/home/forge/example.com/current/storage` to the shared storage directory at `/home/forge/example.com/storage`.
If your application uses an SQLite database, you should add a shared path from `database.sqlite` to `database/database.sqlite`. This ensures that your database persists between deployments, as Forge will symlink `/home/forge/example.com/current/database/database.sqlite` to `/home/forge/example.com/database.sqlite`.
By default, Laravel Forge automatically configures the `.env` file as a shared path for all sites using zero-downtime deployments.
#### [​](#laravel-octane) Laravel Octane
You should not use zero-downtime deployments when using Laravel Octane, as Octane already handles graceful, zero-downtime restarts internally. Enabling Forge’s zero-downtime feature alongside Octane will interfere with this process and cause deployments to behave incorrectly.
### [​](#standard-deployments) Standard deployments
The standard deployment strategy uses a simpler approach where your site’s code is kept in a single directory and updated in place during deployment.
This strategy *can* be faster than zero-downtime deployments, but it does come with the risk of your site going down if a deployment step fails midway through the deployment process.
## [​](#push-to-deploy) Push to deploy
Laravel Forge’s “Push to deploy” feature allows you to easily deploy your projects when you push new code to your source control provider.
When code is pushed to your site’s configured branch, Laravel Forge will automatically trigger a new deployment and run your site’s deployment script.
Push to deploy is **enabled by default for new sites** created with GitHub, GitLab, or Bitbucket. If you wish to disable this feature, you may do so by toggling the “Push to deploy” toggle inside of the [“Advanced settings” modal](/docs/sites/the-basics#advanced-settings).
To enable push to deploy for existing sites, you may do so by enabling the “Push to deploy” toggle on the “Deployments” tab of your site’s settings.
For sites using a [custom source control provider](/docs/source-control#using-custom-git-providers) you will need to manually set up a [“Deployment hook”](/docs/sites/deployments#deploying-from-ci) to have your code deployed when you push to your source provider.
## [​](#deploy-script) Deploy script
When a deployment is triggered, Laravel Forge will execute the commands defined in your site’s deploy script.
At a minimum, your deploy script should contain the commands needed to update your site’s codebase (such as a `git pull` or `$CREATE_RELEASE()` macro), install any dependencies (such as `composer install` or `npm ci`), and perform any other tasks needed to get your application up and running (such as `php artisan migrate --force`).
### [​](#environment-variables) Environment variables
Laravel Forge will automatically inject a number of environment variables into your deployment script at runtime. These variables are configured to provide information about the deployment itself, the site, and the server.
| Key | Description |
| --- | --- |
| `FORGE_COMPOSER` | The path to the Composer installation. |
| `FORGE_CUSTOM_DEPLOY` | Whether the deployment was triggered with a custom deployment trigger request. |
| `FORGE_DEPLOY_AUTHOR` | The author of the commit. |
| `FORGE_DEPLOY_COMMIT` | The Git hash of the commit being deployed, used for display purposes. |
| `FORGE_DEPLOY_MESSAGE` | The Git commit message. |
| `FORGE_DEPLOYMENT_ID` | The Laravel Forge assigned ID of this deployment. |
| `FORGE_MANUAL_DEPLOY` | Whether the deploy was triggered by clicking “Deploy Now”. |
| `FORGE_PHP_FPM` | The PHP-FPM process name that is being used by Laravel Forge. |
| `FORGE_PHP` | The `php` binary that is being used by the Laravel Forge site or server. |
| `FORGE_QUICK_DEPLOY` | Whether the deploy was triggered by a source control provider webhook. |
| `FORGE_REDEPLOY` | Whether this is a re-deployed commit. |
| `FORGE_RELEASE_DIRECTORY` | The path of the current release when zero-downtime deployment is enabled. |
| `FORGE_SERVER_ID` | The ID of the Laravel Forge server that is being deployed to. |
| `FORGE_SITE_BRANCH` | The name of the branch that is being deployed. |
| `FORGE_SITE_ID` | The ID of the Laravel Forge site that is being deployed to. |
| `FORGE_SITE_PATH` | The root of the deployment path, e.g., `/home/forge/mysite.com/current` |
| `FORGE_SITE_ROOT` | The site’s root directory, e.g., `/home/forge/mysite.com` |
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
Laravel Forge prefixes injected variables with `FORGE_`.We do not recommend using this “namespace” when defining your own variables to avoid potential conflicts.
#### [​](#making-env-variables-available) Making .env variables available
Laravel Forge makes it easy to include your site’s `.env` variables in your deploy script.
You may enable this feature by navigating to the “Deployments” tab of your site’s settings and checking the “Make .env variables available to deployment script” checkbox.
When enabled, Laravel Forge will automatically inject the variables in your site’s `.env` file into the deploy script, allowing them to be accessed like any normal Bash variable:
Copy
Ask AI
```
echo "${APP_NAME} is deploying..."
```
### [​](#php-versions) PHP versions
Sites use the `$FORGE_PHP` environment variable when invoking PHP commands in the deployment script. This variable will always point to the configured PHP version for the site. If you need to use a specific version of PHP, you must use the `phpx.x` command where `x.x` reflects on the version required (e.g., `php8.5`).
During a deployment, Forge also configures the `php` binary to be the PHP version configured on your site. This ensures that `composer` and `npm` scripts which invoke PHP will use the site’s PHP version.
### [​](#restarting-background-processes) Restarting background processes
When deploying applications that use [background processes](/docs/resources/background-processes) such as daemons, you may need to restart the process to ensure it picks up your code changes. You can do this by adding the restart command to your deployment script:
Copy
Ask AI
```
# Restart your daemon (replace 12345 with your daemon's ID)...
sudo supervisorctl restart daemon-12345:*
```
If your site is using zero-downtime deployments, you should place the restart command after the `$ACTIVATE_RELEASE()` macro to ensure the new code is activated before the process is restarted.
## [​](#deploying-from-ci) Deploying from CI
If you wish to trigger deployments from CI, or from a source control provider that is not currently supported by Laravel Forge, you may do so by using “deployment hooks” or the [Forge CLI](/docs/cli).
### [​](#deployment-hooks) Deployment hooks
Deployment hooks are special webhooks that Laravel Forge provides for each site. You may trigger a deployment by making a `GET` or `POST` request to the deployment trigger URI provided.
To find your site’s deployment hook URI, navigate to the “Deployments” tab of your site’s settings. You will find a “Deploy hook” section with the URI that you can quickly copy to your clipboard.
#### [​](#refreshing-the-deployment-token) Refreshing the deployment token
Each deploy hook contains a unique token that is used to authenticate the request.
If you wish to regenerate this token, you may do so by clicking the “Refresh” icon button next to the deploy hook URI.
Refreshing the deployment token will immediately invalidate the previous token. Any services that are using the previous token will need to be updated to use the new token.
#### [​](#using-query-parameters) Using query parameters
You may pass additional data when triggering a deployment using query parameters.
Laravel Forge will detect the following “reserved” query parameters and use them to populate specific information about the deployment:
| Parameter | Environment variable | Description |
| --- | --- | --- |
| `forge_deploy_branch` | – | The branch that contains the commit. The deployment is only triggered if the branch matches the site’s configured deployment branch. |
| `forge_deploy_commit` | `FORGE_DEPLOY_COMMIT` | The commit hash label displayed in the deployment history. This does not affect which commit is deployed. |
| `forge_deploy_author` | `FORGE_DEPLOY_AUTHOR` | The author of the commit. |
| `forge_deploy_message` | `FORGE_DEPLOY_MESSAGE` | The commit message. |
In addition to the reserved parameters, you may also pass custom parameters that will be injected into your deployment script.
For example, if you pass the query parameter `&env=staging` to the deployment hook URL, Laravel Forge will inject a `FORGE_VAR_ENV` variable into your deployment script that will evaluate to `"staging"`.
### [​](#forge-cli) Forge CLI
If you need to have access to the deployment output or execute additional deployment actions such as restarting services, you should use the [Forge CLI](/docs/cli).
Once you have installed and configured the Forge CLI on your CI platform, you may execute the `forge deploy` command.
To authenticate with Laravel Forge from your CI platform, you will need to add a `FORGE_API_TOKEN` environment variable to your CI build environment.You may generate an API token from your Laravel Forge [API settings dashboard](https://forge.laravel.com/profile/api). Your CI platform will also require SSH access to your server.
#### [​](#github-actions-example) GitHub Actions example
If your site uses [GitHub Actions](https://github.com/features/actions) as its CI platform, the following guidelines will assist you in configuring Laravel Forge deployments so that your application is automatically deployed when someone pushes a commit to the `main` branch:
1. First, add the `FORGE_API_TOKEN` environment variable to your “GitHub > Project Settings > Secrets” settings so that GitHub can authenticate with Laravel Forge while running actions.
2. Next, add the `SSH_PRIVATE_KEY` environment variable to your “GitHub > Project Settings > Secrets” settings so that GitHub can have SSH Access to your site’s server.
3. Then, create a `deploy.yml` file within the `your-project/.github/workflows` directory. The file should have the following contents:
.github/workflows/deploy.yml
Copy
Ask AI
```
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup SSH
        uses: webfactory/[email protected]
        with:
          ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.5
          tools: composer:v2
          coverage: none
      - name: Require Laravel Forge CLI
        run: composer global require laravel/forge-cli
      - name: Deploy Site
        run: |
          forge server:switch your-server-name
          forge deploy your-site-name.com
        env:
          FORGE_API_TOKEN: ${{ secrets.FORGE_API_TOKEN }}
```
4. Finally, you can edit the `deploy.yml` file to fit your site’s deployment needs, as it may require a different PHP version or a library like `npm`. Once you are done, commit and push the `deploy.yml` file to the `main` branch so GitHub Actions can run the first deployment job.
## [​](#deployment-branch) Deployment branch
It is possible to change which branch is deployed on the “General” tab of your site’s settings.
If your site uses the zero-downtime deployment strategy, Laravel Forge will automatically use the newly configured branch on the next deployment.
For standard deployments, ensure that your deployment script uses the `$FORGE_SITE_BRANCH` environment variable when pulling new code, or update any manual references to the branch in your deployment script.
## [​](#deployment-health-checks) Deployment health checks
After enabling deployment health checks, Forge will ping your application from several regions around the world to make sure the application is still accessible and returns a successful HTTP status code. If the site is not accessible after a deployment, Forge will notify you.
To enable health checks, navigate to your site’s “Settings” tab, then click “Deployments”. Then, enable the “Health check” toggle. After enabling health checks, you can optionally configure the URL that Forge will ping after each deployment.
### [​](#health-check-service-ip-addresses) Health check service IP addresses
Health check requests are made from the following IP addresses, which should be added to your HTTP and HTTPS firewall allow rules. These IPs will **not make** SSH connections to the server.
- 209.38.170.132
- 206.189.255.228
- 139.59.222.70
Alternatively, you can allow the health check service by its `User-Agent` header value: `Laravel-Healthcheck/1.0`.
## [​](#deployment-notifications) Deployment notifications
You can enable deployment notifications for your site from the site management dashboard’s “Notifications” tab. Laravel Forge supports several notification channels:
- Email
- Slack
- Telegram
- Discord
By default, Laravel Forge will automatically notify you by email for failed deployments.
### [​](#slack) Slack
To enable Slack notifications, first enter the Channel name that you wish to send messages to, and then click “Enable Slack Notifications”. You will be redirected to the Slack application authorization page, where you need to click “Allow”.
If you wish to modify the channel that Laravel Forge messages, you should first disable Slack notifications and then re-enable them for your site.
### [​](#telegram) Telegram
To enable Telegram notifications, open Telegram and create or select a group chat that you want Laravel Forge to send deployment notifications to. Next, you should add the Laravel Forge bot to the chat by searching for the user `laravel_forge_telegram_bot`. Finally, copy the `/start` command, provided by Forge under the Telegram Deployment Notifications section, and paste it into the chat.
If you wish to change the group that Laravel Forge messages, you should disable Telegram notifications and then follow the above steps again to reactivate notifications.
### [​](#discord) Discord
To enable Discord notifications, you first need to create a new “Incoming Webhook” integration on your Discord server. Once Discord has generated a webhook, you need to copy the URL into the “Webhook URL” field, then click “Enable Discord Notifications”. Laravel Forge will now notify the configured channel for both successful and failed deployments.
If you wish to change the webhook URL, you first need to disable Discord notifications and then re-enable the notifications.
### [​](#webhooks) Webhooks
Laravel Forge can also send an HTTP POST request to arbitrary URLs after each deployment. The payload of the request will contain the server ID, site ID, deployment status, and the relevant commit information:
Copy
Ask AI
```
{
  "status": "success",
  "server": {
    "id": 123,
    "name": "my-awesome-server"
  },
  "site": {
    "id": 456,
    "name": "my-awesome-site.dev"
  },
  "commit_hash": "382b0f5185773fa0f67a8ed8056c7759",
  "commit_url": "https://github.com/johndoe/my-awesome-site/commit/382b0f5185773fa0f67a8ed8056c7759",
  "commit_author": "John Doe",
  "commit_message": "deploying!"
}
```
Was this page helpful?
YesNo
[Domains](/docs/sites/domains)[Environment Variables](/docs/sites/environment-variables)
⌘I