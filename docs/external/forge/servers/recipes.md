# Forge - Servers/Recipes

*Source: https://forge.laravel.com/docs/servers/recipes*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersRecipes[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# Recipes

Save and run common Bash scripts across your servers.

## [​](#overview)Overview

Recipes allow you to save common Bash scripts and run them across any of your servers. For example, you could save a recipe to install MongoDB so you can conveniently run it on future servers. The output of the recipe will be emailed to you.

## [​](#creating-recipes)Creating Recipes

You can create your own recipe from the [Recipes dashboard](https://forge.laravel.com/recipes). When creating a new recipe you will be asked to supply:

- The name of the recipe

- The operating system user that the script should be run as

- The recipe script contents

### [​](#variables)Variables

Forge provides a few variables that can be used to make your recipe more dynamic. You are free to use any of these variables within your recipe’s script:

- `{{server_id}}` - The ID of the server that the recipe is running on

- `{{server_name}}` - The name of the server that the recipe is running on

- `{{ip_address}}` - The public IP address of the server

- `{{private_ip_address}}` - The private IP address of the server

- `{{username}}` - The server user who is running the script

- `{{db_password}}` - The database password for the server the script is running on

- `{{server_type}}` - The type of the server that the recipe is running on, i.e. one of the following…

`"app"`

- `"cache"`

- `"database"`

- `"loadbalancer"`

- `"meilisearch"`

- `"web"`

- `"worker"`

When using these variables, you should ensure that they exactly match the syntax shown above.

## [​](#running-recipes)Running Recipes

When running a recipe, you will be presented with options that allow you to have the output of the recipe emailed to you and allow you to configure which servers the recipe will run on.

Was this page helpful?

YesNo[Packages](/docs/servers/packages)[Load Balancing](/docs/servers/load-balancing)On this page
- [Overview](#overview)
- [Creating Recipes](#creating-recipes)
- [Variables](#variables)
- [Running Recipes](#running-recipes)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.