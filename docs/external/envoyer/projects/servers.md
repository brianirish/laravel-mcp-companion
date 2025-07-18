# Envoyer - Projects/Servers

*Source: https://docs.envoyer.io/projects/servers*

---

- [Documentation](/introduction)
- [Community](https://discord.com/invite/laravel)

##### Get Started

- [Introduction](/introduction)
- [Quick Start](/quick-start)

##### Accounts

- [Source Control](/accounts/source-control)
- [Your Account](/accounts/your-account)

##### Projects

- [Management](/projects/management)
- [Servers](/projects/servers)
- [Deployment Hooks](/projects/deployment-hooks)
- [Heartbeats](/projects/heartbeats)
- [Notifications](/projects/notifications)
- [Collaborators](/projects/collaborators)

On this page

- [Overview](#overview)
- [Server Configuration](#server-configuration)
- [Configuring Multiple PHP Versions](#configuring-multiple-php-versions)
- [Non-Standard PHP Services](#non-standard-php-services)
- [Importing Laravel Forge Servers](#importing-laravel-forge-servers)
- [Managing Uploaded Files](#managing-uploaded-files)

Projects

# Servers

Learn how Envoyer deploys your projects to servers.

## [​](#overview) Overview

After creating a project, you may add as many servers as you like to the project. After adding a server, you will be given an SSH key to add to your server. You should add the SSH key to the `~/.ssh/authorized_keys` file for the users Envoyer should connect to the server as.

After you have added the SSH key to the server, click the “refresh” icon next to the server’s “Connection Status” indicator. Envoyer will attempt to connect to your server and run a few health checks on the server, such as attempting to restart PHP FPM (if it is installed on the server).

If Envoyer was unable to restart PHP FPM, you will receive an alert on your project overview. The information modal for the alert will provide the command needed to allow Envoyer to restart FPM without a password.

## [​](#server-configuration) Server Configuration

There are several options you may configure when managing a server:

| **Field** | Description |
| --- | --- |
| **Name** | Give your server a name that you can identify easily. |
| **Hostname / IP Address** | The IPv4 address of your server. |
| **Port** | The port Envoyer should use to connect to your server. |
| **Connect As** | The user that Envoyer should use to connect to your server. |
| **Receives Code Deployments** | Determines whether the server should receive code deployments. |
| **Project Path** | The absolute path to the project’s root directory on your server. |
| **Reload FPM After Deployments** | Determines whether the PHP-FPM service will be reloaded after each deployment. |
| **FreeBSD** | Indicates whether the server is running the FreeBSD operating system. |
| **PHP Version** | The version of PHP being used (also determines the version of the PHP-FPM service that will be reloaded). |
| **PHP Path** | The absolute path to the PHP binary on your system. |
| **Composer Path** | The absolute path to the Composer binary on your system. |

### [​](#configuring-multiple-php-versions) Configuring Multiple PHP Versions

If your server is configured to run multiple versions of PHP, you may find that the **Install Composer Dependencies** step uses the wrong version. To resolve this, you should define a custom Composer path configuration setting, such as `php8.0 /usr/local/bin/composer`. This setting will instruct Composer to run using PHP 8.0 instead of the system default.

### [​](#non-standard-php-services) Non-Standard PHP Services

Some VPS providers run custom versions of Ubuntu that manage PHP services in a variety of ways that are not typical. If Envoyer is not able to correctly identify and reload the correct PHP service, you will need to disable the **Reload FPM After Deployments** setting and create a custom [Deployment Hook](/projects/deployment-hooks) that reloads the correct service.

## [​](#importing-laravel-forge-servers) Importing Laravel Forge Servers

If you have provisioned your server with [Laravel Forge](https://forge.laravel.com), you may import it into your Envoyer project. You’ll need to create an API token on your Forge account and then connect it to your Envoyer account from the [Integrations](https://envoyer.io/user/profile#/integrations) dashboard.

When adding a server to your project, click the **Import Forge Server** button. Envoyer will display a modal asking you to select the server from your account and the site from the server.

Once selected, Envoyer will add the required SSH key to the connected site’s user (typically `forge`, unless using a Forge configured isolated user). Envoyer will use this SSH key to connect to your server and deploy your site.

## [​](#managing-uploaded-files) Managing Uploaded Files

When storing user uploaded files in an Envoyer deployed Laravel application, you should store them in the application’s `storage` directory. Then, you may use the “Manage Linked Folders” feature of Envoyer to create a symbolic link from your public directory to the `storage` directory. The “Manage Linked Folders” button can be found on the “Deployment Hooks” tab of your project.

If you are not using Laravel, you will essentially follow the same process. However, you will need to manually create a `storage` directory in the deployment path of your application (the same directory level as the `current` symbolic link).

Was this page helpful?

YesNo

[Management](/projects/management)[Deployment Hooks](/projects/deployment-hooks)

Assistant

Responses are generated using AI and may contain mistakes.