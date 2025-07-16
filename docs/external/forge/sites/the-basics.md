# Forge - Sites/The-Basics

*Source: https://forge.laravel.com/docs/sites/the-basics*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#e2848d908587a28e83908394878ecc818d8f)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesThe Basics[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Sites# The Basics

Creating sites, installing applications, and managing your server.

## [​](#creating-sites)Creating Sites

When creating a new site on your Forge server, a variety of configuration options are available to you:

- **Root Domain:** The domain name that the server should respond to.

- **Aliases:** Additional domains that the site should respond to.

- **Project Type:** This configuration setting indicates if the project installed for your site will be a General PHP / Laravel / Symfony project or a static HTML site. This setting is used to determine the structure of the Nginx configuration file that is created for your site.

- **Web Directory:** The directory that should be publicly accessible via the Internet. For Laravel applications, this is typically the `/public` directory.

- **PHP Version:** If you have multiple versions of PHP installed on your server, you can select which one should be used to serve the site.

- **Nginx Template**: If you have configured any [Nginx Templates](/docs/servers/nginx-templates) for you server, you will have the option to select one as the site’s Nginx configuration, otherwise Forge will utilise its default Nginx configuration for you new site.

- **Wildcard Sub-Domains:** This configuration setting will enable the site to respond to any subdomain under its configured root domain.

- **Website Isolation:** This configuration setting indicates whether the PHP-FPM process should run under its own user account. You may learn more about website isolation by consulting the [full documentation regarding this feature](/docs/sites/user-isolation).

- **Create Database:** This setting indicates if you would like a new database to be created for your site.

### [​](#automatic-redirects)Automatic Redirects

When creating your site, Forge will automatically create a redirect from the `www` subdomain to the root domain. For example, if you create a site with the root domain `example.com`, Forge will automatically create a redirect from `www.example.com` to `example.com`. Likewise, if your site’s domain is `www.example.com`, Forge will automatically create a redirect from `example.com` to `www.example.com`.

### [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and delete sites by granting the `site:create` and `site:delete` permissions.

## [​](#apps-%2F-projects)Apps / Projects

Once the site has been created in Forge, you can then install an application or project. Projects contain the actual source code of your application. Forge can install three types of applications: an application that exists within a [Git repository](/docs/sites/the-basics#git-repository), [WordPress](/docs/sites/the-basics#wordpress), or [phpMyAdmin](/docs/sites/the-basics#phpmyadmin).

### [​](#git-repository)Git Repository

Before you can install a Git repository, you must first ensure that you have [connected your source control provider](/docs/accounts/source-control) to your Forge account.

Once you have connected your source control provider accounts, you may choose the provider from one of the available options. If you’re self-hosting your own code or using a provider that Forge doesn’t include first-party support for, you may select the **Custom** option. When using either the Bitbucket or Custom provider option, you will need to manually add the Forge SSH key to the provider.

You will also need to provide the repository name. For GitHub, GitLab, and Bitbucket providers, you should provide the name in `user/repository` format, e.g. `laravel/laravel`. Self-hosted projects should use the full SSH URL, e.g. `[[email protected]](/cdn-cgi/l/email-protection):laravel/laravel.git`.

Before you install the repository, you can also decide whether or not to install Composer dependencies. If your project does not contain a `composer.json` file, you should uncheck this option.

#### [​](#deploy-keys)Deploy Keys

Sometimes you may wish to only grant the Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository’s “Deploy Keys” on the repository’s GitHub, GitLab, or Bitbucket dashboard.

When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider’s dashboard - allowing the server to clone that specific repository.

### [​](#wordpress)WordPress

Forge can also install [WordPress](https://wordpress.org) for you, so you can get right into writing your next blog post.

If you haven’t done so already, you should [create a new database](/docs/resources/databases#creating-databases) and database user. This is used by WordPress to store all of your blog posts.

Once WordPress has been installed, you can visit your site’s domain name and continue the WordPress installation from your browser.

When installing WordPress for your site, Forge will also install the [WordPress CLI](https://wp-cli.org/) so that you can manage your installation with the `wp` terminal command.

You should continue installing WordPress as soon as Forge has installed it for you, so that it’s made secure with your username and password. You could also choose to create a new [Security Rule](/docs/sites/security-rules) before you install WordPress so that your installation is password protected.

Forge provides access to the `wp-config.php` file through the WordPress tab on your site’s management dashboard. You can use this to add authentication keys, define constants like `DISALLOW_FILE_EDIT`, or modify the database table prefix.

Editing some variables such as `$table_prefix` will invoke the WordPress installer and you will need to reinstall your WordPress site after making this change. The following variables will trigger the WordPress installer if they are changed:

- `$table_prefix`

- `AUTH_KEY`

- `AUTH_SALT`

- `DB_HOST`

- `DB_NAME`

- `DB_PASSWORD`

- `DB_USER`

- `LOGGED_IN_SALT`

- `NONCE_KEY`

- `NONCE_SALT`

- `SECURE_AUTH_KEY`

- `SECURE_AUTH_SALT`

### [​](#phpmyadmin)phpMyAdmin

Forge also supports installing [phpMyAdmin](https://phpmyadmin.net), so you can manage your databases from anywhere.

If you haven’t done so already, you should [create a new database](/docs/resources/databases#creating-databases) and database user. This is used by phpMyAdmin to store the configuration of your databases and users.

Once Forge has installed phpMyAdmin, you can then log in to your installation using any of your database username and password combinations.

Some very small server sizes, such as `t2.nano` on AWS, do not have enough resources to run an application like phpMyAdmin.

## [​](#default-sites)Default Sites

When you initially provision a Forge server, Forge creates a single site on the server named `default`. This site may be accessed by visiting the IP address of your server in your web browser. This is convenient because sometimes you may not have a particular domain you want to associate with a given server immediately after provisioning.

When you are ready to transition your application to an official domain name, you may rename the site in the **Settings** tab of the site’s management panel. After renaming the site, you will no longer be able to access it using the server’s IP address. After renaming the site, you should add a DNS `A` record for the domain that points to your server’s IP address.

### [​](#nginx-configuration)Nginx Configuration

Below is an example of the default Nginx site configuration that is used by Laravel Forge. [Additional Nginx templates](/docs/servers/nginx-templates) may be created in Forge using

*[Content truncated for length]*