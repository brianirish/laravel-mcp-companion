# Forge - Servers/Management

*Source: https://forge.laravel.com/docs/servers/management*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#7c1a130e1b193c101d0e1d0a1910521f1311)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersManagement[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# Management

Learn how to manage your servers in Forge.

## [​](#server-settings)Server Settings

The server dashboard’s **Settings** tab can be used to update important details of a server including its name, SSH connection details, timezone, and tags.

### [​](#ip-addresses)IP Addresses

If your server’s IP address changes, you should inform Forge so that it can remain connected and continue to manage your server. To update the IP address of a server, navigate to the **Settings** tab and update the **IP Address** field under the Server Settings section.

When rebooting an AWS server, AWS will allocate a new IP address to the server. Therefore, you will need to update the IP address after a server reboot.

### [​](#timezone)Timezone

By default, all Forge servers are provisioned and configured to use the UTC timezone. If you need to change the timezone used by the server, you can do so by selecting one of the timezones from the list. Forge uses the `timedatectl` command to modify the system’s timezone.

## [​](#archiving-servers)Archiving Servers

You may archive a server from the Forge UI by clicking the **Archive** button at the bottom of the server’s detail page. Archiving a server will remove Forge’s access to the server. If necessary, you may reconnect an archived server to Forge via your Forge account profile.

Archiving a server **will not** delete your server from the server provider and **will not** cause any data loss on your server.

### [​](#archive-circle-permission)Archive Circle Permission

You may grant a circle member authority to archive a server from your account by granting the `server:archive` permission.

## [​](#transferring-servers-to-other-users)Transferring Servers To Other Users

Servers may be transferred to other Forge accounts from the server’s **Settings** tab by providing the email address of the Forge account you wish to transfer the server to.

The Forge account that is receiving the server will receive an email asking them to confirm the request. They must also have set up the [server provider](/docs/servers/providers) that the server exists in before the transfer request can be sent. For example, if the server is a DigitalOcean server, the recipient must have DigitalOcean set up as a server provider within their own account.

You may only transfer servers to a Forge accounts with an active subscription that have not reached their server quota.

### [​](#transfer-circle-permission)Transfer Circle Permission

You may grant a circle member authority to transfer a server from your account by granting the `server:transfer` permission.

## [​](#deleting-servers)Deleting Servers

You may delete a server from the Forge UI by clicking the **Destroy Server** button at the bottom of the server’s detail page. Forge requires you to confirm the name of the server before deleting it.

Deleting a server will **permanently destroy the server** from the connected provider, resulting in data loss.

### [​](#deleting-custom-servers)Deleting Custom Servers

When deleting a custom server, the server will only be removed from Forge. The server itself will continue to run.

### [​](#delete-circle-permission)Delete Circle Permission

You may grant a circle member authority to delete a server from your account by granting the `server:delete` permission.

Was this page helpful?

YesNo[Server Types](/docs/servers/types)[Root Access / Security](/docs/servers/provisioning-process)On this page
- [Server Settings](#server-settings)
- [IP Addresses](#ip-addresses)
- [Timezone](#timezone)
- [Archiving Servers](#archiving-servers)
- [Archive Circle Permission](#archive-circle-permission)
- [Transferring Servers To Other Users](#transferring-servers-to-other-users)
- [Transfer Circle Permission](#transfer-circle-permission)
- [Deleting Servers](#deleting-servers)
- [Deleting Custom Servers](#deleting-custom-servers)
- [Delete Circle Permission](#delete-circle-permission)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.