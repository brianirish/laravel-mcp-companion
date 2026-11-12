Source: https://laravel.com/forge/docs/sites/repository-access.md

# Repository Access

> How Laravel Forge authenticates to your source control provider when cloning and deploying, and how to resolve access errors, especially with Bitbucket.

## Introduction

When Forge installs or deploys a site, it clones your repository from your source control provider. This page explains **which credential Forge uses** for that clone, why the answer differs between zero-downtime and standard deployments, and how to fix the most common access error:

```
git@bitbucket.org: Permission denied (publickey).
fatal: Could not read from remote repository.
```

## How Forge authenticates

Depending on how a site is configured, Forge clones using one of three identities:

* **The connection's OAuth token**: used only by zero-downtime deployments, over HTTPS. No SSH key is involved.
* **A deploy key**: an SSH key unique to a single site, which you add to that repository. See [deploy keys](https://forge.laravel.com/docs/ssh.md#deploy-keys).
* **The server's SSH key**: a key registered on your source control account that allows the server to clone repositories the account can access. See [server keys](https://forge.laravel.com/docs/ssh.md#server-keys).

Which one applies depends mostly on whether the site uses zero-downtime deployments.

## Deployment strategies

The deployment strategy determines which credential Forge uses to clone the repository.

> [tab] Zero-downtime deployments (default)
>
> Clones over **HTTPS using the connection's OAuth token**. No SSH key is required, and the site authenticates as the connected account. A GitHub, GitLab, or Bitbucket site with zero-downtime deployments enabled generally requires no additional SSH key configuration.

> [tab] Standard deployments
>
> Clones over **SSH**, which requires a key that is registered with your source control provider and can read the repository: a [deploy key](https://forge.laravel.com/docs/ssh.md#deploy-keys) on the repository, or the [server's SSH key](https://forge.laravel.com/docs/ssh.md#server-keys) on the account. Without a registered key, the clone fails with `Permission denied (publickey)`.

> [!NOTE]
>
> The same repository can deploy successfully as a zero-downtime site (HTTPS token) while failing as a standard site (SSH) if no SSH key is registered. If you disable zero-downtime deployments on a Bitbucket site, make sure a deploy key or the server key is registered first.

## Bitbucket specifics

Bitbucket behaves differently from GitHub and GitLab because **Bitbucket does not offer an API for managing SSH keys**. Forge can register the server's key on GitHub and GitLab automatically, but for Bitbucket you must add keys yourself.

When you create a **standard** (non-zero-downtime) Bitbucket site in the Forge dashboard, Forge checks whether the server can already reach the repository and, if it cannot, shows you the exact SSH key to add to your Bitbucket account before the site can be installed. Add the displayed key to your Bitbucket account (or use a deploy key), click **Verify SSH connection**, and continue once it turns green.

> [!WARNING]
>
> Because Bitbucket has no key-management API, Forge cannot register keys for you. For Bitbucket standard-deployment sites (and especially for sites created via the [API or SDK](#creating-sites-via-the-api), where there is no dashboard prompt), [deploy keys](https://forge.laravel.com/docs/ssh.md#deploy-keys) are the most reliable option.

## Isolated sites

When [user isolation](https://forge.laravel.com/docs/sites/user-isolation.md) is enabled, a site's deployment runs as that site's dedicated system user, **not** the default `forge` user. That isolated user does not have the server's SSH key in its home directory, so it cannot rely on the server key to clone.

Isolated standard-deployment sites therefore need their own credential:

* A [deploy key](https://forge.laravel.com/docs/ssh.md#deploy-keys) generated for the site and added to the repository (recommended), or
* Zero-downtime deployments enabled, so the clone uses the OAuth token instead of SSH.

## Creating sites via the API

Unlike the Forge dashboard, the API and SDK cannot prompt you to add a key while creating a site. For **standard Bitbucket sites created via the API** (particularly [isolated](https://forge.laravel.com/docs/sites/user-isolation.md) ones), use a deploy key you register *before* creating the site:

**1. Generate a keypair**

Generate an SSH keypair locally (for example, `ssh-keygen -t ed25519 -f ./deploy_key -N ""`).

**2. Add the public key to the repository**

Add the **public** key to the repository's access keys in Bitbucket. Doing this first avoids a failed clone and the automatic site rollback that follows it.

**3. Create the site with the deploy key**

Include `generate_deploy_key: true` along with the `public_deploy_key` and `private_deploy_key` you generated. The clone will use the already-registered deploy key and succeed.

> [!NOTE]
>
> If a site's initial clone fails, Forge automatically rolls the site back, removing the Nginx configuration, domain, and isolated user. Registering the deploy key before creating the site avoids this. Note that `generate_deploy_key: true` means "use the keypair I am supplying", not "generate one for me", so you must still pass `public_deploy_key` and `private_deploy_key`.

## Managing a site deploy key via the API

You do not have to recreate a site to move it onto a deploy key. Once a site exists, you can generate, inspect, or remove its deploy key through the API, which is the cleanest way to convert an existing OAuth or server-key site to per-repository access. The endpoints live in the **Deployments** group of the [API reference](https://forge.laravel.com/docs/api-reference/introduction.md):

* `GET` on `.../sites/{site}/deploy-key` returns the site's current public deploy key.
* `POST` on `.../sites/{site}/deploy-key` generates a deploy key for the site.
* `DELETE` on `.../sites/{site}/deploy-key` removes the site's deploy key.

Unlike the create-time flow, where you supply your own keypair, the `POST` endpoint generates the keypair **on the server** and returns the public key in the response's `key` attribute. Add that key to the repository's deploy keys on your provider so the server can clone. Once a site has a deploy key, Forge deploys using it and stops managing account- or server-level keys for that site.

> [!NOTE]
>
> If the site already has a deploy key, `POST` returns the existing key unchanged rather than rotating it; to replace a key, delete it first and then generate a new one. Forge never registers the key on your provider for you, so remember to add the returned public key to the repository yourself.

## Troubleshooting access errors

Most repository access failures fall into one of two categories, and the error in the deployment output tells you which:

* **`Permission denied (publickey)`** means an SSH clone could not authenticate. The site is deploying over SSH (a standard, non-zero-downtime deployment) and no SSH key that can read the repository is registered. This is a **key** problem.
* **`Authentication failed`, `Repository not found`, or an HTTP `403`/`404`** means a zero-downtime clone could not use the connection's OAuth token. This is a **token or permission** problem, and no SSH key is involved.

> [accordion] Permission denied (publickey) on a standard deployment
>
> No SSH key that can read the repository is registered for this site.
> Add a [deploy key](https://forge.laravel.com/docs/ssh.md#deploy-keys) to the repository (recommended), or register the [server's key](https://forge.laravel.com/docs/ssh.md#server-keys) on your GitHub, GitLab, or Bitbucket account, then redeploy.
> Alternatively, enable zero-downtime deployments so the site clones over HTTPS with the OAuth token and skips SSH entirely.
> On GitHub and GitLab, Forge can register the server key for you; on Bitbucket you must add it manually, since Bitbucket has no key-management API.

> [accordion] A new site fails to clone from a repository that already deploys elsewhere
>
> An existing site usually already has a registered deploy key, or was created while a working key was in place, whereas a brand-new site has no credential of its own until you add one.
> This is common after moving a project from a custom or deploy-key setup to an OAuth provider, because the new OAuth sites start without a registered key. Add a deploy key to the new site, or confirm the server key is registered on the account.

> [accordion] Authentication failed on a zero-downtime site
>
> The connection's OAuth token is expired, revoked, or was reset on the provider.
> Open the organization's [source control](https://forge.laravel.com/docs/source-control.md) settings, use **Verify connection** to confirm, then **Reconnect** to refresh the token.
> If an expired token is stored in an older site's Git remote, redeploying after reconnecting updates it.

> [accordion] The token is valid but the repository is missing or inaccessible
>
> The provider may restrict visibility of a repository even when the token is valid.
> On GitHub, the Forge OAuth app may not be approved for the organization that owns the repository. On GitLab, group or project access may be restricted. On Bitbucket, a **workspace IP allowlist** or app-access policy can hide repositories even while deploys from an allowlisted server still succeed.
> **Reconnect** the connection and explicitly grant access to the organization or workspace, or adjust the provider's access controls, then try again.

> [accordion] The SSH key is registered but the provider still rejects it
>
> An SSH key can be registered on only **one** account per provider.
> If the same public key is already attached to a different account (most commonly on Bitbucket), the provider refuses to add it again.
> Use a per-site [deploy key](https://forge.laravel.com/docs/ssh.md#deploy-keys) on the repository instead of a shared account key, so each site has a unique key.

## Choosing an approach

Use **zero-downtime deployments** when you want the simplest setup and do not need SSH key management. Forge clones over HTTPS using the connection's OAuth token, which authenticates as the connected account.

Use a **deploy key** for standard deployments, [isolated sites](https://forge.laravel.com/docs/sites/user-isolation.md), or per-repository access. A deploy key is a dedicated SSH key that grants a site access to one repository.

Use the **server key** when you want a server to clone every repository available to the associated source control account. This reduces per-site key management, but grants broader access than a deploy key.
