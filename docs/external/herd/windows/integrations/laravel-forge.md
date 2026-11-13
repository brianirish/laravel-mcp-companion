Source: https://herd.laravel.com/docs/windows/integrations/laravel-forge.md

# Laravel Forge

# Laravel Forge

Herd has a seamless integration with [Laravel Forge](https://forge.laravel.com) and allows you to interact and deploy your Herd site directly on Forge. After connecting your site, you are able to deploy the site, open an SSH connection, grab your environment variables or open the site within Forge with a single click.

## Connect Herd with your Laravel Forge account

To use the Forge integration, you need to set up at least one Forge account. Open the settings, go to "General" and select "Integrations". Click "Connect Service" and select Laravel Forge. Herd supports multiple Forge accounts in case you have separate accounts for your personal sites and sites that you manage at work.


During the setup process, Herd connects to your Laravel Forge account and obtains an OAuth token during the authorization.


When Forge and Herd are connected, it shows up in the list of connected services next to your [Laravel Cloud](https://herd.laravel.com/docs/windows/integrations/laravel-cloud.md) and Expose connections. This means that you are ready to link local sites with sites on Forge now.


## Link a Herd site with Laravel Forge

When the integration is set up, select a site in the [Applications window](https://herd.laravel.com/docs/windows/sites/managing-sites.md). The inspector shows the deploy button below the quick actions. If you're connected to Laravel Cloud and Laravel Forge, use the icons next to the button to switch between both. With Forge selected, click "Deploy to Laravel Forge" to link the site.


Click "Detect automatically" and Herd finds the matching Forge site based on the git remote of your project. This can take a moment on large accounts. If Herd can't find the site or you want to link a different one, click "Link manually" and select the organization, server and site.


After you've selected a site, you can deploy the site with the icon in the main toolbar or use the other functions on the right side of the panel.


### Deployments

Deploying a site is as easy as clicking on the deployment button.


If you click on this button, you can select the deployment target and confirm your action. After that, the deployment is triggered on Forge. You can follow the deployment status in the status bar at the bottom of the window.


### Forge

The Forge button open your site in Forge and gives you access to all Forge features.

### SSH

You can directly open an SSH connection in your favorite terminal from the site menu.

### `.env`

If you want to copy some environment variables from a Forge site to recreate the same setup locally, you can open your `.env` file with the .env button.

## CLI

The Herd integration with the Forge CLI allows you to omit servers and sites from commands which makes it super easy to interact with your sites via the command line. Just run `forge` to see all available commands or go through the list below.

```bash theme={null}
  command          Execute a CLI command
  deploy           Deploy a site
  open             Open a site in forge.laravel.com
  ssh              Start an SSH session
  tinker           Tinker with a site

  daemon:list      List the daemons
  daemon:logs      Retrieve the latest daemon log messages
  daemon:restart   Restart a daemon
  daemon:status    Get the current status of a daemon

  database:logs    Retrieve the latest database log messages
  database:restart Restart the database
  database:shell   Start a database shell
  database:status  Get the current status of the database

  deploy:logs      Retrieve the latest deployment log messages

  env:pull         Download the environment file for the given site
  env:push         Upload the environment file for the given site

  nginx:logs       Retrieve the latest Nginx log messages
  nginx:restart    Restart Nginx
  nginx:status     Get the current status of Nginx

  php:logs         Retrieve the latest PHP log messages
  php:restart      Restart PHP
  php:status       Get the current status of PHP

  server:current   [current] Determine your current server
  server:list      List the servers
  server:switch    [switch] Switch to a different server

  site:list        List the sites
  site:logs        Retrieve the latest site log messages

  ssh:configure    Configure SSH key based secure authentication
  ssh:test         Test the SSH key based secure authentication connection
```

If the CLI detects more than one linked site, it asks you which one you want to use before running the command:

```bash theme={null}
 ┌ Select the Forge integration to use: ────────────────────────┐
 │ › ● herd.laravel.com                                         │
 │   ○ latest.herdphp.com                                       │
 └──────────────────────────────────────────────────────────────┘
```

## Version Control

Herd stores the server and site ids in a `herd.yml` within the root of your project. This way, everyone on your team can directly access the site if they have access to the site in Forge. If you want to fully leverage the `herd.yml`, read more [here](https://herd.laravel.com/docs/windows/sites/herd-yaml.md).

```yaml theme={null}
integrations:
  forge:
    herd.laravel.com:
      server-id: 12345
      site-id: 67890

```
