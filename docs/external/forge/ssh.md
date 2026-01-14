# Forge - Ssh

*Source: https://forge.laravel.com/docs/ssh*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Basics

SSH Keys

[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)

- [Community](https://discord.gg/laravel)
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

##### Other

- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)

On this page

- [Introduction](#introduction)
- [Managing organization SSH keys](#managing-organization-ssh-keys)
- [Creating organization keys](#creating-organization-keys)
- [Deleting organization keys](#deleting-organization-keys)
- [Managing account SSH keys](#managing-account-ssh-keys)
- [Creating account keys](#creating-account-keys)
- [Deleting account keys](#deleting-account-keys)
- [Managing server SSH keys](#managing-server-ssh-keys)
- [Creating server keys](#creating-server-keys)
- [Deleting server keys](#deleting-server-keys)
- [Adding account keys](#adding-account-keys)
- [Server keys](#server-keys)
- [Server public key](#server-public-key)
- [Laravel Forge public key](#laravel-forge-public-key)
- [Deploy keys](#deploy-keys)

Basics

# SSH Keys

Copy page

SSH keys are used to authenticate with your server over the SSH protocol.

Copy page

## [​](#introduction) Introduction

SSH is a protocol that allows you to securely access your server via a command line terminal.
SSH keys are used to authenticate with your server over the SSH protocol.
If you are new to SSH keys, we recommend checking out the [GitHub documentation of generating SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to get started.
As part of the provisioning process, Laravel Forge will add all active organization SSH keys to the `forge` account. This will allow you to SSH into the server as the `forge` user.
After adding your SSH key to your server, you may SSH into the server without a password:

Copy

Ask AI

```
ssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS
```

If you have provisioned a custom server that configures a different SSH port, you will need to provide the port in the command.

Copy

Ask AI

```
ssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS -p YOUR_SERVERS_SSH_PORT_NUMBER
```

## [​](#managing-organization-ssh-keys) Managing organization SSH keys

Laravel Forge will automatically add all organization-level SSH keys to any server that is created within the organization.

### [​](#creating-organization-keys) Creating organization keys

To create an organization SSH key, navigate to the organization’s dashboard and click Settings. Then, navigate to the Security page, click the Add SSH key button. After providing a key name and the **Public key** click Add key.

### [​](#deleting-organization-keys) Deleting organization keys

To delete an organization SSH key, navigate to the organization’s dashboard and click Settings. Then, navigate to the Security tab and click the dropdown next to the key you want to delete. Click Delete and confirm that you want to delete the key.

Laravel Forge will not automatically remove organization SSH keys from servers. You must do this manually.

## [​](#managing-account-ssh-keys) Managing account SSH keys

Laravel Forge makes it easy to manage SSH keys on your own account, making it easy to quickly add your own keys to servers.

### [​](#creating-account-keys) Creating account keys

To create an account SSH key, navigate to your account dashboard and click the “SSH” tab. Then, click the “Add key” button. After providing a key name and the **Public key**, click “Add key”.

### [​](#deleting-account-keys) Deleting account keys

To delete an account SSH key, navigate to your account dashboard and click the “SSH” tab. Then, click the dropdown next to the key you want to delete. Click “Delete” and confirm that you want to delete the key.

When deleting an account key, Laravel Forge will also attempt to remove the key from servers.

## [​](#managing-server-ssh-keys) Managing server SSH keys

### [​](#creating-server-keys) Creating server keys

To create a server SSH key, navigate to the server and click “Settings”. Then, navigate to the “SSH” tab and click the “Add key” button. After providing a key name and the **Public key** click Add key. If your server has any sites configured with website isolation, you will also be able to select the user to add the key to. By default, this will be the `forge` user.

### [​](#deleting-server-keys) Deleting server keys

To delete a server SSH key, navigate to the server and click “Settings”. Then, navigate to the “SSH” tab and click the dropdown next to the key you want to delete. Click “Delete” and confirm that you want to delete the key.

### [​](#adding-account-keys) Adding account keys

To add your account’s SSH keys, navigate to the server and click “Settings”. Then, navigate to the “SSH” tab and click the “Add key” button. Click on the “Add from account” dropdown item, then select the key you want to add to the server and click “Add”.

## [​](#server-keys) Server keys

### [​](#server-public-key) Server public key

During the provisioning process, Laravel Forge will generate its own keypair so that it may access the server. It will add the public key from this keypair to the `~/.ssh/authorized_keys` file of both the `root` and `forge` users.

### [​](#laravel-forge-public-key) Laravel Forge public key

During the provisioning process, Laravel Forge will generate a public key for the `forge` user. This is used by Git to clone the projects to your server. The key will be added to the source control provider. This key is located at `/home/forge/.ssh/id_rsa.pub`.
Alternatively, you may opt out of having this key added to your source control providers by un-checking the **Add server’s SSH key to source control providers** option when creating a server. When opting-out, you will need to use site-level [deploy keys](#deploy-keys) in order to grant your server access to specific repositories on a source control provider such as GitHub, GitLab, or Bitbucket.

### [​](#deploy-keys) Deploy keys

Sometimes you may wish to only grant the Laravel Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository’s “Deploy Keys” on the repository’s GitHub, GitLab, or Bitbucket dashboard.
When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider’s dashboard - allowing the server to clone that specific repository.

Deploy keys can be used on servers that have their SSH key attached to your source control provider accounts, allowing you to grant the server access to clone a repository that the source control account connected to your Laravel Forge account does not have collaborator access to.

Was this page helpful?

YesNo

[Source Control](/docs/source-control)[Recipes](/docs/recipes)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)