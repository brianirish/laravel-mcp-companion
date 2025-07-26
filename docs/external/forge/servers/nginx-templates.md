# Forge - Servers/Nginx-Templates

*Source: https://forge.laravel.com/docs/servers/nginx-templates*

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
- [Managing Templates](#managing-templates)
- [Create Template](#create-template)
- [Edit Templates](#edit-templates)
- [Delete Templates](#delete-templates)
- [Template Variables](#template-variables)
- [Circle Permissions](#circle-permissions)

Servers

# Nginx Templates

Learn how to use Nginx templates to customize your site configurations.

## [​](#overview) Overview

Nginx templates allow you to customize the Nginx site configuration that Forge uses when creating your new site.

Nginx templates that are not valid will prevent Nginx from properly working and your existing sites may stop responding. You should proceed with caution when creating and deploying custom Nginx templates.

## [​](#managing-templates) Managing Templates

### [​](#create-template) Create Template

You may create your own Nginx templates from within a server’s management dashboard. When creating a new template, you need to provide a template name and the template’s content. Forge will provide a default template that you may alter as required.

Although the default template does not show support for TLSv1.3, Forge will automatically update a site to support it if the server is able to do so.

### [​](#edit-templates) Edit Templates

You may edit the name and content of your Nginx template at any time. Changes to a template will not affect existing sites that use the template.

### [​](#delete-templates) Delete Templates

Deleting a template will not remove any sites which were configured to use it.

## [​](#template-variables) Template Variables

Forge provides several variables that can be used within your templates to dynamically alter their content for new sites:

| Variable | Description |
| --- | --- |
| `{{DIRECTORY}}` | The site’s configured web directory, e.g. `/public` |
| `{{DOMAINS}}` | The site’s configured domains to respond to, e.g. `laravel.com alias.laravel.com` |
| `{{PATH}}` | The site’s web accessible directory, e.g. `/home/forge/laravel.com/public` |
| `{{PORT}}` | The IPv4 port the site should listen to (`:80`). If the site name is `default`, this variable will also contain `default_server` |
| `{{PORT_V6}}` | The IPV6 port to listen to (`[::]:80`). If the site name is `default`, this variable will also contain `default_server` |
| `{{PROXY_PASS}}` | The PHP socket to listen on, e.g. `unix:/var/run/php/php8.0-fpm.sock` |
| `{{ROOT_PATH}}` | The root of the configured site, e.g. `/home/forge/laravel.com` |
| `{{SERVER_PUBLIC_IP}}` | The public IP address of the server |
| `{{SERVER_PRIVATE_IP}}` | The private IP address of the server, if available |
| `{{SITE}}` | The site’s name, e.g. `laravel.com`. This differs from `{{DOMAINS}}` in that it does not include site aliases. |
| `{{SITE_ID}}` | The site’s ID, e.g. `12345` |
| `{{USER}}` | The site’s user, e.g. `forge` |

When using these variables, you should ensure that they exactly match the syntax shown above.

## [​](#circle-permissions) Circle Permissions

The ability to manage Nginx Templates is determined by the `site:manage-nginx` permission. This permission is also used to restrict the ability to edit an existing site’s Nginx configuration file.

Was this page helpful?

YesNo

[Load Balancing](/docs/servers/load-balancing)[Database Backups](/docs/servers/backups)

Assistant

Responses are generated using AI and may contain mistakes.