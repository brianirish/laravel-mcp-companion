# Forge - Servers/Nginx-Templates

*Source: https://forge.laravel.com/docs/servers/nginx-templates*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Nginx Templates
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
- [Managing templates](#managing-templates)
- [Create template](#create-template)
- [Edit templates](#edit-templates)
- [Delete templates](#delete-templates)
- [Template variables](#template-variables)
- [Team permissions](#team-permissions)
Servers
# Nginx Templates
Copy page
Learn how to use Nginx templates to customize your site configurations.
Copy page
## [​](#introduction) Introduction
Nginx templates allow you to customize the Nginx site configuration that Laravel Forge uses when creating your new site.
Nginx templates that are not valid will prevent Nginx from properly working and your existing sites may stop responding. You should proceed with caution when creating and deploying custom Nginx templates.
## [​](#managing-templates) Managing templates
### [​](#create-template) Create template
You may create your own Nginx templates from within a server’s management dashboard. When creating a new template, you need to provide a template name and the template’s content. Laravel Forge will provide a default template that you may alter as required.
Although the default template does not show support for TLSv1.3, Laravel Forge will automatically update a site to support it if the server is able to do so.
### [​](#edit-templates) Edit templates
You may edit the name and content of your Nginx template at any time. Changes to a template will not affect existing sites that use the template.
### [​](#delete-templates) Delete templates
Deleting a template will not remove any sites which were configured to use it.
## [​](#template-variables) Template variables
Laravel Forge provides several variables that can be used within your templates to dynamically alter their content for new sites:
| Variable | Description |
| --- | --- |
| `{{DIRECTORY}}` | The site’s configured web directory, e.g., `/public` |
| `{{DOMAINS}}` | The site’s configured domains to respond to, e.g., `laravel.com alias.laravel.com` |
| `{{PATH}}` | The site’s web accessible directory, e.g., `/home/forge/laravel.com/public` |
| `{{PORT}}` | The IPv4 port the site should listen to (`:80`). If the site name is `default`, this variable will also contain `default_server` |
| `{{PORT_V6}}` | The IPV6 port to listen to (`[::]:80`). If the site name is `default`, this variable will also contain `default_server` |
| `{{PROXY_PASS}}` | The PHP socket to listen on, e.g., `unix:/var/run/php/php8.0-fpm.sock` |
| `{{ROOT_PATH}}` | The root of the configured site, e.g., `/home/forge/laravel.com` |
| `{{SERVER_PUBLIC_IP}}` | The public IP address of the server |
| `{{SERVER_PRIVATE_IP}}` | The private IP address of the server, if available |
| `{{SITE}}` | The site’s name, e.g., `laravel.com`. This differs from `{{DOMAINS}}` in that it does not include site aliases. |
| `{{SITE_ID}}` | The site’s ID, e.g., `12345` |
| `{{USER}}` | The site’s user, e.g., `forge` |
When using these variables, you should ensure that they exactly match the syntax shown above.
## [​](#team-permissions) Team permissions
The ability to manage Nginx Templates is determined by the `site:manage-nginx` permission. This permission is also used to restrict the ability to edit an existing site’s Nginx configuration file.
Was this page helpful?
YesNo
[Load Balancing](/docs/servers/load-balancing)[Security](/docs/servers/security)
⌘I