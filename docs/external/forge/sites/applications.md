# Forge - Sites/Applications

*Source: https://forge.laravel.com/docs/sites/applications*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#9ef8f1ecf9fbdef2ffecffe8fbf2b0fdf1f3)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesApplications[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# Applications

Learn how to create and manage your applications on Laravel Forge.

## [​](#overview)Overview

Forge provides first-class support for applications running [Laravel](https://laravel.com), allowing you to quickly toggle and configure:

- Laravel’s Task Scheduler

- Laravel’s Maintenance Mode

- Laravel Horizon Daemon

- Laravel Octane Daemon

- Laravel Reverb Daemon

- Inertia.js Server Side Rendering (SSR) Daemon

To accomplish this, Forge parses the `composer.json` and `composer.lock` files from your application and inspects for the presence and version of the packages above.

### [​](#requirements)Requirements

Forge will only show the application panel for Laravel framework installations of version `5.0` or later. In addition, the panel’s supported packages must meet the following version requirements:

DependencyMinimum Version`laravel/framework``5.0``laravel/horizon``1.0``laravel/octane``1.0``laravel/pulse``1.0``laravel/reverb``*``inertiajs/inertia-laravel``0.6.6`
## [​](#laravel-scheduler)Laravel Scheduler

You may quickly enable or disable the Laravel scheduler via the “Laravel Scheduler” toggle. Forge will create the required [Scheduler](/docs/resources/scheduler) for you.

Forge will automatically configure the scheduler to run every minute using the site’s configured PHP version.

## [​](#maintenance-mode)Maintenance Mode

If you have deployed a Laravel application, Forge allows you to make use of Laravel’s maintenance mode feature. Clicking the **Laravel Maintenance Mode** toggle within the site’s **Application** tab will run the `php artisan down` Artisan command within your application, which will make your site unavailable. When the site is in maintenance mode, you can then toggle it off to make your site available again.

### [​](#maintenance-mode-%E2%80%9Csecret%E2%80%9D)Maintenance Mode “Secret”

Laravel 8.0+ applications can make use of the “secret” option to bypass maintenance mode. Using this option with older versions of Laravel is not supported.

## [​](#laravel-horizon)Laravel Horizon

You may quickly enable or disable the Laravel Horizon daemon via the “Laravel Horizon” toggle. Forge will create the required Horizon daemon for you.

If the site’s deploy script does not contain the `horizon:terminate` command, Forge will automatically append it for you.

### [​](#converting-existing-daemons)Converting Existing Daemons

If your server is already configured with a daemon that runs Laravel Horizon, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.

## [​](#laravel-octane)Laravel Octane

You may quickly enable or disable the Laravel Octane daemon via the “Laravel Octane” toggle. Forge will create the required Octane daemon and install Octane dependencies for you.

When enabling the Octane daemon, Forge will ask you to provide the port number you would like to use for the Octane server as well as your Octane server of choice.

If the site’s deploy script does not contain the `octane:reload` command, Forge will automatically append it for you.

Before enabling Laravel Octane, you must set the `OCTANE_SERVER` environment variable to the Octane server you choose.

### [​](#converting-existing-daemons-2)Converting Existing Daemons

If your server is already configured with a daemon that runs Laravel Octane, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.

## [​](#laravel-reverb)Laravel Reverb

Determining the correct server type for hosting Laravel Reverb depends on your configuration requirements. You may use the table below to help inform your decision:

ConfigurationApp ServerWeb ServerReverb server alongside Laravel application⊙Dedicated Reverb server⊙Dedicated Reverb server with Pulse⊙Dedicated Reverb server with Pulse (seperate ingest and / or database)⊙
Once your preferred server has been provisioned, you should [add a new site](/docs/sites/the-basics.html#creating-sites) and [install your Reverb-enabled Laravel application](/docs/sites/the-basics#apps-projects) from your version control provider of choice.

Now, you may quickly enable or disable Laravel Reverb via the “Laravel Reverb” toggle within Forge’s application panel. When enabling Reverb, Forge will create the Reverb daemon, install the required dependencies, and configure the server for optimum performance.

Additionally, Forge will prompt for additional information required to setup the server per your requirements.

- **Public Hostname:** Used to update the Nginx configuration of the site, allowing Reverb connections to be accepted by the server on the given hostname. Forge will default to a subdomain of the site’s current hostname, but you are free to customize this value. For example, if the site’s hostname is `example.com`, Forge will default Reverb’s hostname to `ws.example.com`.

- **Port:** Used to instruct the Reverb daemon which server port it should run on. Forge will proxy requests for the given public hostname to this port.

- **Maximum Concurrent Connections:** The number of connections your Reverb server can handle will depend on a combination of the resources available on the server and the amount of connections and messages being processed. You should enter the number of connections the server can manage before it should prevent new connections. This option will update the server’s allowed open file limit, Nginx’s allowed open file and connection limit, and install the `ev` event loop if required.

Forge ensures the hostname provided during Reverb’s installation process is publicly accessible by adding a new server block to your existing site’s Nginx configuration. This server block is contained within a new file and is not available to edit from the Forge UI dashboard.

If the site’s deploy script does not contain the `reverb:restart` command, Forge will automatically append it for you.

### [​](#ssl)SSL

If an SSL certificate exists for your site which protects Reverb’s configured hostname, Forge will automatically install it when enabling Reverb, ensuring your Reverb server is accessible via secure WebSockets (`wss`).

If Reverb is installed before a valid certificate is available, you may request a new certificate for Reverb’s configured hostname from your site’s “SSL” tab. Forge will automatically configure secure WebSockets for Reverb as soon as the certificate is activated. Forge will also pre-populate the “Domains” SSL form input with Reverb’s hostname when requesting a certificate.

After activating SSL on a Reverb-enabled site, you should ensure the following environment variables are properly defined before redeploying your site:

CopyAsk AI```
REVERB_PORT=443
REVERB_SCHEME=https

VITE_REVERB_PORT="${REVERB_PORT}"
VITE_REVERB_SCHEME="${REVERB_SCHEME}"

MIX_REVERB_PORT="${REVERB_PORT}"
MIX_REVERB_SCHEME="${REVERB_SCHEME}"

```

### [​](#converting-existing-daemons-3)Converting Existing Daemons

If your server is already configured with a daemon that runs Laravel Reverb, Forge will manage the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon on your behalf.

When disabling Reverb, Forge will remove the daemon and ensure the public hostname is no longer accessible. However, any settings Forge updated when enabling Reverb, such as open file and connection limits, will not be reset and any PHP extensions installed will not be removed.

## [​](#inertia-server-side-rendering)Inertia Server Side Rendering

You may quickly enable or disable the Inertia SSR daemon via the

*[Content truncated for length]*