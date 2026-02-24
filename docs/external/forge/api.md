# Forge - Api

*Source: https://forge.laravel.com/docs/api*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Basics
API
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
- [Managing API tokens](#managing-api-tokens)
- [Create a new API token](#create-a-new-api-token)
- [Delete an API token](#delete-an-api-token)
Basics
# API
Copy page
Learn how to get started and interact with the Laravel Forge API.
Copy page
## [​](#introduction) Introduction
Laravel Forge provides a comprehensive JSON API that allows you to programmatically manage your Forge servers and sites. To learn more, please review the [Forge API documentation](/docs/api-reference/introduction).
The official Laravel Forge [PHP SDK](/docs/sdk) provides an expressive interface for interacting with Forge’s API and managing Laravel Forge servers.
## [​](#managing-api-tokens) Managing API tokens
### [​](#create-a-new-api-token) Create a new API token
To create an API token, navigate to your account dashboard and click “API”. Click “Create token”, provide a name for the token, an optional expiration date, and select the scopes you wish to assign to the token. Finally, click “Add token”.
### [​](#delete-an-api-token) Delete an API token
To delete an API token, navigate to your account dashboard and click “API”. Locate the token you wish to delete, click the action dropdown next to the token, and select “Delete”.
Deleting an API token is permanent and cannot be undone. Any applications or services using the deleted token will no longer be able to access the Laravel Forge API.
Was this page helpful?
YesNo
[Recipes](/docs/recipes)[Managing Servers](/docs/servers/the-basics)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.