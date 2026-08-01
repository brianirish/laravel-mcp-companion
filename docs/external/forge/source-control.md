# Forge - Source-Control

*Source: https://forge.laravel.com/docs/source-control*

---

## On this page
- [Introduction](#introduction)
- [Supported providers](#supported-providers)
- [Managing source control providers](#managing-source-control-providers)
  - [Connecting to a source control provider](#connecting-to-a-source-control-provider)
  - [Removing source control providers](#removing-source-control-providers)
  - [Refreshing tokens](#refreshing-tokens)
  - [Updating source control access and permissions](#updating-source-control-access-and-permissions)
  - [Using custom Git providers](#using-custom-git-providers)
Basics
# Source Control
Copy pageCopy page
Source control providers allow Laravel Forge to access your project’s codebase and easily deploy your applications.
Copy pageCopy page
## [​](#introduction) Introduction
Source control providers allow Laravel Forge to access your project’s codebase and easily deploy your applications. Forge supports most popular Git providers as well as custom / self-hosted options.
Source control providers are configured and managed within the [organization’s](/docs/organizations) settings.
## [​](#supported-providers) Supported providers
Laravel Forge supports the following source control providers:
- [GitHub](https://github.com/)
- [GitLab](https://about.gitlab.com/) (hosted and self-hosted)
- [Bitbucket](https://bitbucket.org/)
- Custom Git Repositories
## [​](#managing-source-control-providers) Managing source control providers
### [​](#connecting-to-a-source-control-provider) Connecting to a source control provider
To connect a source control provider, navigate to the organization’s settings. Then, on the “Source control” page, click “Add provider”. Select the provider you wish to connect to and authenticate your chosen account.
You may only configure one account from each provider at a time. If you need to connect a different account from the same provider, you must first remove the existing connection.
When you connect a source control provider via OAuth, the API token grants Forge access to all repositories accessible by your authenticated account. If a server is compromised, an attacker could potentially use this token to discover and access other repositories. For enhanced security, consider using [deploy keys](/docs/ssh#deploy-keys) instead, which limit access to only specific repositories.
### [​](#removing-source-control-providers) Removing source control providers
To unlink a source control provider, navigate to the organization’s settings. Then, on the “Source control” page, click the dropdown menu on the provider and click “Delete”.
Source control providers cannot be unlinked if an active site is using that provider.
### [​](#refreshing-tokens) Refreshing tokens
To refresh a source control provider token, navigate to the organization’s settings. Then, on the “Source control” page, click the dropdown menu on the provider and click “Refresh token”.
### [​](#updating-source-control-access-and-permissions) Updating source control access and permissions
To update your source control provider connection for accessing different organizations, repositories, or modifying token permissions:
1. Navigate to your source control provider’s settings
2. Locate and uninstall the Laravel Forge application
3. Return to Laravel Forge
4. Click the **Refresh Token** button to initiate a new OAuth authentication flow
When you need access to different organizations or repositories, refreshing the token may not grant the necessary permissions.
Following the complete OAuth authentication flow allows you to explicitly authorize access to your desired organizations and repositories with the appropriate permission scope.
### [​](#using-custom-git-providers) Using custom Git providers
If your Git Provider is not a first-party provider, then you may use the **Custom** option when creating a new site on your server.
First, choose the `Custom` option when creating your Git based site. Next, add the generated SSH key to your source control provider and provide the full repository path (`git@provider.com:user/repository.git`).
Was this page helpful?
YesNo
[Storage Providers](/docs/storage-providers)[SSH Keys](/docs/ssh)
⌘I