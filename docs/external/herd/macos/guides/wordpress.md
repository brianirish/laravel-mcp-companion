Source: https://herd.laravel.com/docs/macos/guides/wordpress.md

# WordPress

# How to set up a WordPress site

While Herd was mainly developed with Laravel in mind, most concepts apply to working with WordPress, too. Herd supports standard WordPress setups as well as Bedrock with its different folder structure. This guide covers the installation of a standard WordPress site via a zip file but you can apply the same concepts when using the WordPress CLI or cloning a git repository.

## Code Directory

Herd uses the concept of *parked paths* for serving sites via `.test` domains. By default, Herd creates and parks the `~/Herd` directory and every folder that you create in this directory is reachable via its own domain.

This means that you can simply move or install a site to this directory and don't have to create it via the Applications window in Herd – it just works.

## Database Setup

While Laravel uses SQLite as default, WordPress requires either MySQL or MariaDB as database service for your site. You can set up this database via a free tool like [dbngin](https://dbngin.com) or set up a database instance via a [Herd service](https://herd.laravel.com/docs/macos/herd-pro-services/services.md).

> [!NOTE]
>
> [Herd Pro]() allows you to install database instances and other complementary services directly from Herd – but you can also download and run the database of your choice separately.

## Local Domains

As described above, Herd serves all directories in your parked paths via local `.test` domains. This means that you can move a site into the directory `my-wordpress-site` and access it via [http://my-wordpress-site.test](http://my-wordpress-site.test).

If you are running a multisite and want to point multiple domains to a single WordPress installation, you can use Herd links to create more local domains. You can either do that via the Applications window as described in the chapter [linking sites](https://herd.laravel.com/docs/macos/getting-started/applications.md#linking-an-existing-application) or use the terminal with the commands below.

```bash theme={null}
cd ~/Herd/my-wordpress-site
herd link my-second-domain
```

These commands go into your site directory and create the local domain [http://my-second-domain.test](http://my-second-domain.test) to your site. It's now accessible via both domains and you can proceed with your normal configuration.

## Drivers

Herd uses drivers to detect frameworks and serve sites to your browser. These drivers support standard WordPress installations and Bedrock but you can write [custom drivers](https://herd.laravel.com/docs/macos/extending-herd/custom-drivers.md) if you are using a different setup for your site. So if your setup is supported by default, you can skip this step but it's important to know that customized installations might need a custom driver or there will simply be a 404 error.

## Installation

The installation of a new WordPress site is straight forward. At first, you need to set up a database. Herd Pro users can go to `Settings > Services` and select their MySQL instance and then open TablePlus or AdminerEvo in the menu on the right to create the database. If you are familiar with MySQL on the command line, you can do that as well.

After that, simply follow these steps:

1. Download the latest version of WordPress from the [official site](https://wordpress.org/download/)
2. Extract the zip file into a parked Herd directory, for example `~/Herd`
3. Rename the directory to your domain, in this guide, we're using the local domain `wordpress-guide.test`, so the directory name is `wordpress-guide`.
4. Go to [http://wordpress-guide.test](http://wordpress-guide.test) and follow the installation process.

If you are using a different port for your database instance, make sure to add this port to the database host during the installation. When using Herd, the database username is `root` and has no password.


Your WordPress site is now running via Herd and you can start working on it.

## Debugging with Insights

[Herd Pro](https://herd.laravel.com/docs/#plans) allows you to debug your site with a convenient `dump` helper. So if you're working on plugins and need to output data for debugging purposes, this is super powerful. In this example, we\`re creating a very basic plugin and dumping a string and all existing posts of the fresh WordPress install.

```php theme={null}
/*
Plugin Name: My Herd Plugin
Plugin URI: https://example.com/my-herd-plugin
Description: A simple plugin to demonstrate WordPress plugin development.
Version: 1.0
Author: Your Name
Author URI: https://example.com
License: GPL2
*/

// Hook into an action
add_action('wp_head', 'my_custom_function');

function my_custom_function() {
    dump("Hello from Herd 👋");
    dump(get_posts());
}
```

When opening any page of your site, the function runs and sends the debug output to the [Insights](https://herd.laravel.com/docs/macos/debugging/insights.md) window where it looks like this example.


## Test Emails

Testing emails can be cumbersome and even result in sending emails to your users when you're connected to a real mail service. Herd solves this by running a local email server that catches your mails and sends them to an internal email client that you can use for testing the email.

The quickest way to set up mails in Herd Pro is by defining a mailer in the `functions.php`. Simply paste the following snippet to the end of your `functions.php` to receive emails in Herd.

```php theme={null}
function herd_mailer($phpmailer) {
    $phpmailer->isSMTP();
    $phpmailer->Host = '127.0.0.1';
    $phpmailer->SMTPAuth = true;
    $phpmailer->Port = 2525;
    $phpmailer->Username = 'WordPress';
    $phpmailer->Password = '';
}

add_action('phpmailer_init', 'herd_mailer');
```

Every time when your application sends an email, it uses Herd's integrated mail service. If it's the first email from this application, it creates an inbox for this application based on the username of the configuration so that you can easily identify emails and where they are from.

You can test this feature by logging out of your site and using the password reset form to trigger an email.


After setting up your first WordPress site in Herd, you can now follow the docs to learn more about all features in more detail and fully leverage Herd when using it every day.
