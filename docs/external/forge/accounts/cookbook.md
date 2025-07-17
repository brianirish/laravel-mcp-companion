# Forge - Accounts/Cookbook

*Source: https://forge.laravel.com/docs/accounts/cookbook*

---

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

Search...

⌘KAsk AI

- Support
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...

Navigation

Accounts

Troubleshooting

[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)

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

Accounts

# Troubleshooting

Account Troubleshooting

## [​](#forge-is-unable-to-access-git-repository) Forge Is Unable To Access Git Repository

There are several reasons Forge may not be able to access your GitHub, GitLab, or Bitbucket repository. First, you should try refreshing the source control API token that is linked to Forge via your account profile’s “Source Control” tab.

Forge attempts to access your repository using your source control provider’s API. The API credentials that will be used are the credentials tied to the account of the person who **owns** the Forge server. If a Forge server is shared with you via a circle, it will use the circle **owner’s** API credentials. You should ensure this person has full access to the repository on GitHub.

### [​](#github-organization-repositories) GitHub Organization Repositories

Sometimes, if the repository is an organization repository, you will need to grant Forge access to that organization. You may do that using the following link: <https://github.com/settings/connections/applications/fdb28071bd05daebc122>

Was this page helpful?

YesNo

[Tags](/docs/accounts/tags)[Server Providers](/docs/servers/providers)

On this page

- [Forge Is Unable To Access Git Repository](#forge-is-unable-to-access-git-repository)
- [GitHub Organization Repositories](#github-organization-repositories)

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Assistant

Responses are generated using AI and may contain mistakes.