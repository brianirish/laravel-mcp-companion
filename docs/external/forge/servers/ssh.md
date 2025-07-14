# Forge - Servers/Ssh

*Source: https://forge.laravel.com/docs/servers/ssh*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#95f3fae7f2f0d5f9f4e7f4e3f0f9bbf6faf8)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersSSH Keys / Git Access[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# SSH Keys / Git Access

Learn how to manage SSH keys on your Forge servers.

## [​](#account-ssh-keys)Account SSH Keys

When provisioning a new server Forge will automatically add any of your [account’s SSH keys](/docs/accounts/ssh) to the server. This means that you can SSH onto your server without using a password:

CopyAsk AI```
ssh forge@IP_ADDRESS

```

## [​](#server-ssh-key-%2F-git-project-access)Server SSH Key / Git Project Access

When a server is provisioned, an SSH key is generated for the server. This key is stored at `~/.ssh/id_rsa` and its public key counterpart is stored at `~/.ssh/id_rsa.pub`. When creating a server, you will have the option to add this key to your connected source control providers. By doing so, the server will be able to clone any repository that your source control account has access to.

Alternatively, you may opt-out of having this key added to your source control providers by un-checking the **Add Server’s SSH Key To Source Control Providers** option when creating a server. When opting-out, you will need to use site-level [Deploy Keys](/docs/_sites/forge-laravel/servers/ssh#deploy-keys) in order to grant your server access to specific repositories on a source control provider such as GitHub, GitLab, or Bitbucket.

### [​](#deploy-keys)Deploy Keys

Sometimes you may wish to only grant the Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository’s “Deploy Keys” on the repository’s GitHub, GitLab, or Bitbucket dashboard.

When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider’s dashboard - allowing the server to clone that specific repository.

You are also free to use Deploy Keys even on servers that have their SSH key attached to your source control provider accounts, allowing you to grant the server access to clone a repository that the source control account connected to your Forge account does not have collaborator access to.

Was this page helpful?

YesNo[Root Access / Security](/docs/servers/provisioning-process)[PHP](/docs/servers/php)On this page
- [Account SSH Keys](#account-ssh-keys)
- [Server SSH Key / Git Project Access](#server-ssh-key-%2F-git-project-access)
- [Deploy Keys](#deploy-keys)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.