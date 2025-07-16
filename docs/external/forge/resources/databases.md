# Forge - Resources/Databases

*Source: https://forge.laravel.com/docs/resources/databases*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#75131a07121035191407140310195b161a18)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationResourcesDatabases[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Resources# Databases

Learn how to manage databases on your Forge server.

## [​](#overview)Overview

When provisioning a new Forge server you may choose to install an [App Server](/docs/servers/types#app-servers) or a [Database Server](/docs/servers/types#database-servers). You can then use the Forge dashboard to manage databases, users, and permissions.

## [​](#creating-servers-with-databases)Creating Servers With Databases

When creating a new server, you can select to install a supported database server:

- MySQL (8.0)

- MariaDB (10.6)

- MariaDB (10.11)

- PostgreSQL (12)

- PostgreSQL (13)

- PostgreSQL (14)

- PostgreSQL (15)

- PostgreSQL (16)

As part of the provisioning process, Forge will automatically install the selected database server and create a default `forge` database, `forge` user, and a secure, randomly-generated password. The database password will be shown upon creating the server alongside the root password. These passwords will also be emailed to you.

### [​](#installing-databases-later)Installing Databases Later

If you later decide to that you need to install a database on your server, you can do so through the server’s **Databases** management tab. Once installed, you will then be able to manage your database via Forge.

If you created a “Web Server”, you will not be able to install a database on that server at any point. Web servers are provisioned with the minimum amount of software needed to serve your PHP application only. If you need a database and web server on the same server, you should provision an “App Server”.

## [​](#changing-the-root-%2F-forge-database-password)Changing the Root / Forge Database Password

To reset the `root` and `forge` database user passwords, you may use the password reset functionality provided by Forge’s **Databases** management tab.

You should not change the `root` or `forge` database user passwords manually or outside of the Forge dashboard. Doing so will prevent Forge from being able to connect to or manage your database.

## [​](#connecting-to-databases-via-a-gui-client)Connecting To Databases Via A GUI Client

By default, database connections require SSH key authentication and are not able to be accessed using passwords. Therefore, when using a GUI database client to connect to your Forge database, you will need to use SSH authentication.

When selecting the SSH key to use during authentication, **ensure that you select your private SSH key**. For example, when using the [TablePlus](https://tableplus.com) database client:

### [​](#using-the-database-connection-url)Using The Database Connection URL

Some clients, such as TablePlus, allow you to connect to a database via a connection URL. Forge automatically generates this connection URL for you and you can use it to connect to your database. Note that the password is not included in this URL, so you should provide your password manually within your database client’s GUI.

## [​](#connecting-to-a-database-on-another-forge-server)Connecting To A Database On Another Forge Server

You can utilize [Forge’s server network feature](/docs/resources/network#server-network) to connect one server’s application to a database on another server within the same network.

If both the server hosting your application and the server hosting the external database [meet the requirements](/docs/resources/network#server-network) for internal network connections, you may follow these steps to establish the database connection:

- Allow access from your application’s web server to the database server:

Navigate to the Network settings of your application’s web server: `https://forge.laravel.com/servers/<serverID>/networks`.

- Under the Server Network section of the page, enable the connection to the server of the external database.

- Next, update your application’s environment configuration:

Visit your site’s environment page at `https://forge.laravel.com/servers/<serverID>/sites/<siteID>/environment`

- Set the database host to the external server’s private IP address.

- Update the database credential variables to match those of the external database.

## [​](#managing-your-databases-within-forge)Managing Your Databases Within Forge

For servers running MySQL, MariaDB, and PostgreSQL, Forge offers some advanced features which allows it to manage your databases and database users easily. We’ll discuss these features below.

### [​](#creating-databases)Creating Databases

You can create a new database through the server’s **Database** tab within Forge. At a minimum, you must supply the name of your new database. The `forge` user will be able to access the database automatically.

### [​](#syncing-databases)Syncing Databases

For consistency, you should use Forge to manage your databases and database users. However, if you created databases outside of the Forge dashboard, you can manually sync them into the Forge dashboard using the **Sync Databases** button on your Forge database management panel.

When syncing databases, some database names that are reserved by the database engine will not be synced, including:

- `mysql`

- `information_schema`

- `peformance_schema`

- `sys`

- `postgres`

- `template0`

- `template1`

### [​](#creating-database-users)Creating Database Users

You can create extra database users through the Forge dashboard’s database panel. To do so, you’ll need to provide the username, password, and select the databases that the new user can access.

## [​](#upgrading-databases)Upgrading Databases

Forge does not provide the ability to upgrade your database server software automatically. If you wish to upgrade your database server, you will need to complete this manually.

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage databases **and** database users by granting the `server:create-databases` and `server:delete-databases` permissions.

Was this page helpful?

YesNo[Daemons](/docs/resources/daemons)[Caches](/docs/resources/caches)On this page
- [Overview](#overview)
- [Creating Servers With Databases](#creating-servers-with-databases)
- [Installing Databases Later](#installing-databases-later)
- [Changing the Root / Forge Database Password](#changing-the-root-%2F-forge-database-password)
- [Connecting To Databases Via A GUI Client](#connecting-to-databases-via-a-gui-client)
- [Using The Database Connection URL](#using-the-database-connection-url)
- [Connecting To A Database On Another Forge Server](#connecting-to-a-database-on-another-forge-server)
- [Managing Your Databases Within Forge](#managing-your-databases-within-forge)
- [Creating Databases](#creating-databases)
- [Syncing Databases](#syncing-databases)
- [Creating Database Users](#creating-database-users)
- [Upgrading Databases](#upgrading-databases)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.