# Forge - Servers/The-Basics

*Source: https://forge.laravel.com/docs/servers/the-basics*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Servers
Creating and Managing Servers
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
- [Creating servers](#creating-servers)
- [Laravel VPS](#laravel-vps)
- [Server settings](#server-settings)
- [IP addresses](#ip-addresses)
- [Resizing Laravel VPS servers](#resizing-laravel-vps-servers)
- [Timezone](#timezone)
- [Managing servers](#managing-servers)
- [Archiving servers](#archiving-servers)
- [Unarchiving servers](#unarchiving-servers)
- [Transferring servers](#transferring-servers)
- [Deleting servers](#deleting-servers)
- [Preserving servers at the provider](#preserving-servers-at-the-provider)
Servers
# Creating and Managing Servers
Copy page
Learn how to create and manage your servers in Laravel Forge.
Copy page
## [​](#introduction) Introduction
Laravel Forge can provision new servers for you in seconds, allowing you to quickly deploy web applications built in PHP or other stacks. We also offer you the ability to provision multiple server types (e.g., web servers, database servers, load balancers) with the option of having a variety of services configured for you to hit the ground running.
## [​](#creating-servers) Creating servers
To create a new server, navigate to your organization’s overview or “Servers” tab and click “New server”. Provide a name for your server and choose the provider to create the server with, then click “Continue”. Next, you need to configure the [type of server](/docs/servers/types) you want to create, which region to create the server in, and the size of the server.
When creating a custom VPS, you must provide additional information including the server’s IP address and the SSH port to connect to.
### [​](#laravel-vps) Laravel VPS
There are a couple of important differences when creating a Laravel VPS server:
1. Only servers created in the “Laravel managed” private network are available for instant provisioning. Private networks can be created, but may take longer to provision.
2. Only servers in the Small, Medium, Large, and X Large sizes are available for instant provisioning. Other sizes can be selected, but may take longer to provision.
## [​](#server-settings) Server settings
The server’s Settings tab can be used to update important details of a server, including its name, SSH connection details, timezone, and tags.
### [​](#ip-addresses) IP addresses
If your server’s IP address changes, you should inform Laravel Forge so that it can remain connected and continue to manage your server. To update the IP address of a server, navigate to the Settings tab and update the IP Address field under the Server Settings section.
When rebooting an AWS server, AWS will allocate a new IP address to the server. Therefore, you will need to update the IP address after a server reboot.
### [​](#resizing-laravel-vps-servers) Resizing Laravel VPS servers
Laravel VPS servers can be resized to a different specification. To resize a Laravel VPS server, navigate to your server’s settings page. Then, select a new server size from the “Size” dropdown. Click “Save” to save the new settings. When resizing a server, you will be prompted to confirm the action. Once confirmed, the server will be resized, which may take a few minutes to complete.
You cannot downsize Laravel VPS servers to a smaller specification. You can only resize to a larger server size.
When resizing a Laravel VPS server, the server will be temporarily unavailable during the resize process.
### [​](#timezone) Timezone
By default, all Laravel Forge servers are provisioned and configured to use the UTC timezone. If you need to change the timezone used by the server, you can do so by selecting one of the timezones from the list. Forge uses the `timedatectl` command to modify the system’s timezone.
## [​](#managing-servers) Managing servers
### [​](#archiving-servers) Archiving servers
Archiving a server will remove Laravel Forge’s access to the server while retaining all sites, configurations, and resources. You will still be charged for the server by your provider.
To archive a server, navigate to the server’s overview and click the Settings tab. Locate the Danger zone and click Archive server. Enter the name of the server and click confirm.
Archiving a server will not delete your server from the server provider and will not cause any data loss on your server.
Laravel VPS servers cannot be archived.
### [​](#unarchiving-servers) Unarchiving servers
To archive a server, navigate to the server’s overview. Click the Unarchive button to generate the unique reconnection script. Once you have executed the script on your server, click Unarchive.
### [​](#transferring-servers) Transferring servers
Servers may be transferred between organizations that you are part of. The receiving organization must also have a [server provider](/docs/server-providers) configured for the server you are transferring. You must have the `server:transfer` permission in both organizations to transfer a server. Laravel VPS servers cannot currently be transferred between organizations.
To transfer a server, navigate to the server’s overview and click the Settings tab. Locate the Danger zone and click Transfer server. Confirm the organization you wish to transfer the server to. Server transfers are immediate.
You may only transfer servers to a Laravel Forge organization with an active subscription that have not reached their server quota.
Laravel Forge will not transfer a server on a server-provider level. You must do this manually.
### [​](#deleting-servers) Deleting servers
To delete a server, navigate to the server and click the Settings tab. Locate the Danger zone and click Delete server. Enter the name of the server and click confirm.
By default, deleting a server will permanently destroy the server from the connected provider, resulting in data loss that cannot be undone by the Laravel Forge team.
#### [​](#preserving-servers-at-the-provider) Preserving servers at the provider
When deleting a server, you can choose to preserve the server at your server provider by enabling the “Preserve this server at [provider]” option in the deletion confirmation dialog. When this option is enabled, the server will only be removed from Laravel Forge and will not be deleted from your server provider’s infrastructure.
This is useful in scenarios where:
- You no longer have access to the server provider credentials
- You want to remove the server from Forge management but keep it running
- You’re transferring server management to another tool or team
This option is not available for custom servers or Laravel VPS servers. Custom servers are not managed by Forge at the provider level, and Laravel VPS servers are always deleted from the underlying infrastructure when removed from Forge.
Was this page helpful?
YesNo
[API](/docs/api)[Server Types](/docs/servers/types)
Assistant
Responses are generated using AI and may contain mistakes.