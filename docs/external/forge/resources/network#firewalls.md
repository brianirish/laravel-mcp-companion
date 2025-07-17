# Forge - Resources/Network#Firewalls

*Source: https://forge.laravel.com/docs/resources/network#firewalls*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationResourcesNetwork[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Resources# Network

Learn how to manage your server network and firewall.

## [​](#overview)Overview

Forge allows you to manage your server’s firewall as well as configure which servers can connect to other servers via the **Network** management panel within your server’s management dashboard.

If you manually create a `ufw` rule on your server, this will not be reflected in the Forge dashboard. Forge is only aware of rules created via the Forge dashboard.

## [​](#server-network)Server Network

Server networks make it painless to use a connected server as a separate database, cache, or queue server. For a server to be connected to an internal network, it must:

- Be created by the same provider.

- Be using the same server provider credentials.

- Be owned by the same user.

- Be within the same region.

Once you have granted access from one server to another, you may access the other server via its private IP address.

## [​](#firewalls)Firewalls

You can configure and manage your firewall from within the Forge dashboard via the **Network** tab on the server’s management dashboard. Firewalls are used to open ports on your server to the Internet. For example, when using FTP you may need to open port `21`.

For added security, you can restrict opened ports to specific IP addresses.

In the “From IP Address” field, you can provide multiple IP addresses by entering a list of comma separated IP addresses. For example: `192.168.1.1,192.168.1.2,192.168.1.3`.

### [​](#port-ranges)Port Ranges

When creating new firewall rules, you may supply a range of ports to open (`8000:8010`), which will open every port from `8000` to `8010`.

### [​](#allow-%2F-deny-rules)Allow / Deny Rules

You may select whether to allow or deny the traffic that matches a given rule. By creating a `deny` rule, you will be preventing traffic from reaching the service.

To make `deny` rules work correctly, they are added at a higher priority than `allow` rules. Each new `deny` rule for IPv4 addresses will be added above any existing `deny` rules. UFW does not currently support IPv6 rules at first priority.

## [​](#default-firewall-rules)Default Firewall Rules

As part of the provisioning process, Forge will automatically configure three rules:

- SSH - Allow port 22 traffic from any IP Address

- HTTP - Allow port 80 traffic from any IP Address

- HTTPS - Allow port 443 traffic from any IP Address

You should note that although incoming traffic is allowed on port 22 for SSH connections, SSH connections that do not use an SSH key are not accepted. Therefore, it is not possible to brute force an SSH connection to your server. **You should never delete the rule that allows SSH traffic to your server; otherwise, Forge will be unable to connect to or manage your server.**

#### [​](#deleted-ssh-firewall-rule)Deleted SSH Firewall Rule

If you have deleted the firewall rule (typically port 22) from the Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.

To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.

Forge uses `ufw` for the firewall, so once you’ve connected to the server you need to run the following as `root`:

CopyAsk AI```
ufw allow 22

```

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to manage the server’s network by granting the `server:manage-network` permission.

Was this page helpful?

YesNo[Caches](/docs/resources/caches)[Scheduler](/docs/resources/scheduler)On this page
- [Overview](#overview)
- [Server Network](#server-network)
- [Firewalls](#firewalls)
- [Port Ranges](#port-ranges)
- [Allow / Deny Rules](#allow-%2F-deny-rules)
- [Default Firewall Rules](#default-firewall-rules)
- [Deleted SSH Firewall Rule](#deleted-ssh-firewall-rule)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.