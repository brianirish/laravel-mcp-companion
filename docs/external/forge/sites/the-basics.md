# Forge - Sites/The-Basics

*Source: https://forge.laravel.com/docs/sites/the-basics*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Sites
Creating and Managing Sites
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
- [Creating sites](#creating-sites)
- [Source control provider](#source-control-provider)
- [Deploy keys](#deploy-keys)
- [Forge domain](#forge-domain)
- [Installing Composer dependencies](#installing-composer-dependencies)
- [Advanced settings](#advanced-settings)
- [Pre-configured applications](#pre-configured-applications)
- [Statamic](#statamic)
- [WordPress](#wordpress)
- [Customizing wp-config.php](#customizing-wp-config-php)
- [phpMyAdmin](#phpmyadmin)
- [PHP versions](#php-versions)
- [Team permissions](#team-permissions)
Sites
# Creating and Managing Sites
Copy page
Learn how to create sites and install applications.
Copy page
## [​](#introduction) Introduction
Laravel Forge provides a simple and intuitive interface for managing and deploying your web applications.
## [​](#creating-sites) Creating sites
When you create a new site in Forge, you’re presented with a variety of configuration options to tailor the site to your needs. These options vary depending on the type of site you’re creating, but generally include settings for the Forge domain, web directory, PHP version, and more.
### [​](#source-control-provider) Source control provider
Laravel Forge allows you to install applications directly from your source control provider.
If you’re using a hosted Git service (GitHub, Bitbucket, GitLab) then Laravel Forge will provide you with a list of repositories that you have access to. You can choose one of these repositories, as well as the branch, that you wish to install.
When using a custom Git repository, you will need to provide the full SSH URL of the repository and manually enter the branch you wish to install.
Laravel Forge must be able to access your repository via SSH. You will be prompted to add your server’s public SSH key to the source control provider during the site creation process.
#### [​](#deploy-keys) Deploy keys
Sometimes you may wish to only grant Laravel Forge access to a specific Git repository. If that is the case, you can generate a unique SSH key during the site creation process and add it to your source control provider’s “Deploy Keys” section in the GitHub, GitLab, or Bitbucket dashboard.
### [​](#forge-domain) Forge domain
Every site created in Laravel Forge is provided with a free `on-forge.com` domain. These vanity domains are automatically available as soon as a site is created and proxied through Cloudflare which provides HTTPS encryption.
You can customize the subdomain used for your site during the site creation process, or use the automatically generated one and configure a custom domain later.
### [​](#installing-composer-dependencies) Installing Composer dependencies
When creating a new PHP site (Laravel, Statamic, Symfony, vanilla PHP), you can choose to have Laravel Forge automatically install Composer dependencies for you.
This is done after the site has been created, but will also update your site’s default deploy script to include the `composer install` command for future deployments.
Laravel Forge will run the following command to install your Composer dependencies:
Copy
Ask AI
```
composer install --no-dev --no-interaction --prefer-dist --optimize-autoloader
```
If your project does not contain a `composer.lock` file, you should uncheck this option.
### [​](#advanced-settings) Advanced settings
If you need more control over how your site is created, you can open the “Advanced settings” modal during the site creation process.
This allows you to:
- **Customize the web directory** used by your site – this defaults to `/public` for the majority of site types.
- **Choose the PHP version** used by your site – this defaults to the server’s default PHP version.
- **Configure [website isolation](/docs/sites/user-isolation)** – configures a dedicated PHP-FPM process for the site.
- Enable or disable **push to deploy** – this is enabled by default and will automatically deploy your site when you push to the configured Git branch.
- Enable or disable [**zero downtime deployments**](/docs/sites/deployments#zero-downtime-deployments) – this is enabled by default for new sites and can only be configured during site creation.
Laravel Forge provides a set of sensible defaults for these settings based on the type of site you’re creating, but you can customize them as needed.
## [​](#pre-configured-applications) Pre-configured applications
Laravel Forge makes it incredibly easy to install popular applications such as Statamic, WordPress, and phpMyAdmin. These applications are pre-configured with sensible defaults so you can get started quickly.
### [​](#statamic) Statamic
Whilst it is possible to create a Statamic site from a Git repository, Laravel Forge also provides a simple way to create a new Statamic site from a [“starter kit”](https://statamic.com/starter-kits).
When creating a new Statamic site, you will need to choose a starter kit and provide an email address for the created “super user”.
If the “Super user password” field is left blank, the default password of `password` will be used for the created user.We recommend using the “Generate password” action, entering a strong password for the super user, or changing it immediately after installation.
Once Statamic has been installed, you can visit your site using the provided Forge domain and log in to the control panel using the email address you provided during installation.
### [​](#wordpress) WordPress
When creating a new WordPress site, Laravel Forge will automatically install the latest version of WordPress for you, as well as the WordPress CLI so that you can manage your installation with the `wp` command.
You will need to choose an existing database for WordPress to use, or create a new one, to proceed.
Once WordPress has been installed, you can visit your site using the provided Forge domain and complete the WordPress installation from your browser.
You should continue installing WordPress as soon as Laravel Forge has installed it for you, so that it’s made secure with your username and password.You could also choose to create a new [“security rule”](/docs/sites/network#security-rules) before you install WordPress so that your installation is password protected.
#### [​](#customizing-wp-config-php) Customizing `wp-config.php`
If you need to customize your site’s `wp-config.php` file, you can do so from the “WordPress” tab in your site’s settings. You can use this to add authentication keys, define constants like `DISALLOW_FILE_EDIT`, or modify the database table prefix.
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
### [​](#phpmyadmin) phpMyAdmin
Laravel Forge also supports installing [phpMyAdmin](https://phpmyadmin.net), allowing you to manage your server’s databases from anywhere.
You will need to choose an existing database, or create a new one, to proceed. This database is used by phpMyAdmin to store the configuration of your databases and users.
Once Laravel Forge has installed phpMyAdmin, you can visit your site using the provided Forge domain and log in using any of your database username and password combinations.
Some very small server sizes, such as `t2.nano` on AWS, do not have enough resources to run an application like phpMyAdmin.
## [​](#php-versions) PHP versions
If your server has [multiple versions of PHP](/docs/servers/php) installed, you can switch the version used by your site at any time by using the site’s “Settings” tab in the Laravel Forge dashboard.
When switching the version used by your site, you should ensure that your server has any additional PHP extensions / modules installed for that version.Failure to install additional modules may make your site unresponsive.
Laravel Forge will automatically update your site’s Nginx configuration files to use the correct PHP-FPM socket and reload the required services for you.
## [​](#team-permissions) Team permissions
You may grant a team member authority to create and delete sites by granting the `site:create` and `site:delete` permissions.
Was this page helpful?
YesNo
[Real-Time Metrics](/docs/servers/real-time-metrics)[Domains](/docs/sites/domains)
Assistant
Responses are generated using AI and may contain mistakes.