Source: https://laravel.com/forge/docs/source-control.md

# Source Control

> Source control providers allow Laravel Forge to access your project's codebase and easily deploy your applications.

## Introduction

Source control providers allow Laravel Forge to access your project's codebase and easily deploy your applications. Forge supports most popular Git providers as well as custom / self-hosted options.

Source control providers are configured and managed within the [organization's](https://forge.laravel.com/docs/organizations.md) settings. Each account you authenticate is stored as an independent **connection**, and a single organization may hold many connections at once, including multiple connections for the same provider.

## Supported providers

Laravel Forge supports the following source control providers:

* [GitHub](https://github.com/)
* [GitLab](https://about.gitlab.com/) (hosted and self-hosted)
* [Bitbucket](https://bitbucket.org/)
* Custom Git Repositories

## Managing source control providers

### Connecting to a source control provider

To connect a source control provider, navigate to the organization's settings. Then, on the "Source control" page, click "Add provider". Select the provider you wish to connect to and authenticate your chosen account.

You may connect the same provider more than once. For example, you can add a personal GitHub account alongside a work account, or connect GitLab accounts with access to different groups. Each authenticated account becomes its own connection and is managed independently. When you keep several connections for the same provider, use the "Rename" action to give each one a memorable label so you can tell them apart when creating a site.

> [!WARNING]
>
> When you connect a source control provider via OAuth, the API token grants Forge access to all repositories accessible by your authenticated account. If a server is compromised, an attacker could potentially use this token to discover and access other repositories. For enhanced security, consider using [deploy keys](https://forge.laravel.com/docs/ssh.md#deploy-keys) instead, which limit access to only specific repositories.

### Managing a connection

Each connection has a dropdown menu on the "Source control" page. The available actions depend on the provider, and may include:

* **View sites**: list the sites that are currently deploying from this connection.
* **Verify connection**: confirm the connection's token is still valid and can reach your repositories.
* **Reconnect**: re-run the OAuth flow to refresh the token or grant access to additional organizations and repositories.
* **Manage GitHub access**: open GitHub to adjust which repositories the Forge application can access.
* **Rename**: give the connection a custom label. This is especially useful when you have several connections for the same provider.
* **Edit**: update connection settings (available for connection types such as self-hosted GitLab).
* **Copy ID**: copy the connection's ID.
* **Delete**: remove the connection.

### Removing a connection

To unlink a connection, navigate to the organization's settings. Then, on the "Source control" page, click the dropdown menu on the connection and click "Delete".

> [!WARNING]
>
> A connection cannot be deleted while an active site is using it. Move or delete the affected sites first, or switch them to a different connection.

### Reconnecting and updating access

To refresh a connection's token, or to grant Forge access to different organizations, repositories, or permission scopes, use the **Reconnect** action on the connection's dropdown menu. This re-runs the full OAuth authentication flow so you can explicitly authorize the access you need.

If reconnecting does not surface the organizations or repositories you expect, the underlying provider authorization may need to be reset first:

1. Navigate to your source control provider's settings.
2. Locate and uninstall (or revoke access for) the Laravel Forge application.
3. Return to Laravel Forge.
4. Click **Reconnect** to initiate a fresh OAuth authentication flow, then authorize the desired organizations and repositories.

### Using custom Git providers

If your Git Provider is not a first-party provider, then you may use the **Custom** option when creating a new site on your server.

First, choose the `Custom` option when creating your Git based site. Next, add the generated SSH key to your source control provider and provide the full repository path (`git@provider.com:user/repository.git`).

> [!NOTE]
>
> Custom Git sites cannot use [push to deploy](https://forge.laravel.com/docs/sites/deployments.md#push-to-deploy), because Forge cannot register a deployment webhook on an arbitrary Git host. If your repository is hosted on a first-party provider you later connect, you can switch the site over from its **Git** settings to enable push to deploy and the other provider-aware features.
