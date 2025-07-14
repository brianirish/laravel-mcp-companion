# Forge - Accounts/Ssh

*Source: https://forge.laravel.com/docs/accounts/ssh*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#7c1a130e1b193c101d0e1d0a1910521f1311)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationAccountsSSH Keys[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Accounts# SSH Keys

SSH keys are used to authenticate with your server over the SSH protocol. Learn how to add your SSH keys to your Forge account and servers.

## [​](#introduction)Introduction

SSH is a protocol that allows you to access your server via a command line terminal. SSH keys are used to authenticate with your server over the SSH protocol. If you are new to SSH keys, we recommend checking out the [GitHub documentation of generating SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to get started.

After adding your SSH key to your server, you may SSH into the server without a password:

CopyAsk AI```
ssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS

```

## [​](#adding-your-ssh-key-to-new-servers)Adding Your SSH Key To New Servers

Before you provision a server for the first time, you should add your SSH keys to your account. You can do this from the your accounts [SSH Keys page](https://forge.laravel.com/user-profile/ssh-keys) in the Forge dashboard.

As part of the provisioning process, Forge will add all your active SSH keys to the `forge` account. This will allow you to SSH into the server as the `forge` user.

If any of your sites are using User Isolation, you will be asked to select the user you want to add the key to. You will then be able to SSH into the server as that user.

## [​](#adding-ssh-key-to-existing-servers)Adding SSH Key To Existing Servers

If you already have servers provisioned and want to add a new SSH key to several servers at once, then first add your key to your account via the [SSH Keys page](https://forge.laravel.com/user-profile/ssh-keys). Once it is listed in the “Active Keys”, you may use the “Add To Servers” action and select which servers you would like the key added to.

You can also [add SSH keys directly to a server](/docs/servers/ssh) without adding them to your account.

## [​](#server-public-key)Server Public Key

During the provisioning process, Forge will generate its own keypair so that it may access the server. It will add the public key from this keypair to the `authorized_keys` file of both the `root` and `forge` users.

## [​](#forge-public-key)Forge Public Key

During the provisioning process, Forge will generate a public key for the `forge` user. This is used by Git to clone the projects to your server. The key will be added to the source control provider. This key is located at `/home/forge/.ssh/id_rsa.pub`.

Was this page helpful?

YesNo[Source Control](/docs/accounts/source-control)[API](/docs/accounts/api)On this page
- [Introduction](#introduction)
- [Adding Your SSH Key To New Servers](#adding-your-ssh-key-to-new-servers)
- [Adding SSH Key To Existing Servers](#adding-ssh-key-to-existing-servers)
- [Server Public Key](#server-public-key)
- [Forge Public Key](#forge-public-key)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.