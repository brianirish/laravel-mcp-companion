# Forge - Resources/Cookbook

*Source: https://forge.laravel.com/docs/resources/cookbook*

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

- [Scheduled Jobs Not Running](#scheduled-jobs-not-running)
- [Deleted SSH Firewall Rule](#deleted-ssh-firewall-rule)

Resources

# Cookbook

Common issues and solutions for Laravel Forge.

## [​](#scheduled-jobs-not-running) Scheduled Jobs Not Running

It’s important to be aware that one single misconfigured scheduled job will break **all jobs** in the scheduler. You should verify that your frequency and commands are correct using a tool such as [Crontab.guru](https://crontab.guru).

## [​](#deleted-ssh-firewall-rule) Deleted SSH Firewall Rule

If you have deleted the firewall rule (typically port 22) from the Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.
To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.
Forge uses `ufw` for the firewall, so once you’ve connected to the server you need to run the following as `root`:

Copy

Ask AI

```
ufw allow 22

```

Was this page helpful?

YesNo

[Integrations](/docs/resources/integrations)[Envoyer](/docs/integrations/envoyer)

Assistant

Responses are generated using AI and may contain mistakes.