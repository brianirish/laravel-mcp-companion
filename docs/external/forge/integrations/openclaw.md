# Forge - Integrations/Openclaw

*Source: https://forge.laravel.com/docs/integrations/openclaw*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Integrations
OpenClaw
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
- [Creating an OpenClaw Server](#creating-an-openclaw-server)
- [Server Requirements](#server-requirements)
- [Configuring OpenClaw](#configuring-openclaw)
- [Managing Your OpenClaw Server](#managing-your-openclaw-server)
- [Resizing Your Server](#resizing-your-server)
- [Backups](#backups)
- [Deleting an OpenClaw Server](#deleting-an-openclaw-server)
Integrations
# OpenClaw
Copy page
Deploy OpenClaw AI agent servers on Laravel Forge.
Copy page
## [​](#introduction) Introduction
[OpenClaw](https://openclaw.ai) is an open-source AI agent platform that allows you to run AI assistants on your own infrastructure while integrating with popular messaging applications such as WhatsApp, Telegram, Discord, Slack, Microsoft Teams, Twitch, and Google Chat. By hosting OpenClaw on your own server, you maintain complete control over your data, API keys, and infrastructure.
Laravel Forge makes it simple to provision and manage OpenClaw servers, allowing you to deploy your own private AI assistant in minutes.
## [​](#creating-an-openclaw-server) Creating an OpenClaw Server
To create an OpenClaw server, navigate to your organization’s overview or “Servers” tab and click “New server”. When selecting your server type, choose “OpenClaw” from the available options.
Next, configure your server by selecting the region closest to you and choosing an appropriate server size based on your expected usage. OpenClaw servers are powered by Laravel VPS infrastructure, ensuring reliable performance and quick provisioning times.
OpenClaw servers created in the “Laravel managed” private network are available for instant provisioning. Servers in Small, Medium, Large, and X Large sizes provision instantly, while other sizes may take longer.
## [​](#server-requirements) Server Requirements
OpenClaw servers are provisioned with all the necessary dependencies to run the OpenClaw platform.
## [​](#configuring-openclaw) Configuring OpenClaw
After your server is provisioned, you will be dropped into the OpenClaw configuration wizard terminal interface. Laravel VPS servers include a built-in web-based terminal for convenient management of your OpenClaw installation.
## [​](#managing-your-openclaw-server) Managing Your OpenClaw Server
### [​](#resizing-your-server) Resizing Your Server
If your OpenClaw deployment requires more resources, you can resize your server from the Settings tab. Select a new server size from the “Size” dropdown and confirm the change.
When resizing an OpenClaw server, the server will be temporarily unavailable during the resize process. You cannot downsize to a smaller specification.
### [​](#backups) Backups
We recommend enabling regular backups for your OpenClaw server to protect your configuration and conversation data. Navigate to the Backups tab to configure automated backup schedules.
## [​](#deleting-an-openclaw-server) Deleting an OpenClaw Server
To delete an OpenClaw server, navigate to the server’s Settings tab, locate the Danger zone, and click “Delete server”. Enter the server name to confirm.
Deleting a server will permanently destroy all data, including your OpenClaw configuration and any stored conversation history. This action cannot be undone.
Was this page helpful?
YesNo
[Aikido](/docs/integrations/aikido)[Support](/docs/support)
⌘I