Source: https://docs.envoyer.io/accounts/source-control.md

# Source Control

> Connect to source control providers to deploy your projects.

## Overview

Project owners must connect their source control providers before they can deploy projects. You can manage source control providers from the [Integrations tab](https://envoyer.io/user/profile#/integrations) within your account dashboard.

## Supported Providers

Envoyer supports four source control providers:

* [ GitHub](https://github.com)
* [ Bitbucket](https://bitbucket.com)
* [ GitLab](https://gitlab.com)
* [ GitLab Self-Hosted](https://about.gitlab.com/install/)

Below we will discuss some issues that may arise when using each provider and how you can address them.

> [accordion] GitHub
>
> If your organization has third-party restrictions enabled, the organization's owner will need to approve the integration. This can be done using the following link: [https://github.com/settings/connections/applications/94f9ec2a8d84cbc725e2](https://github.com/settings/connections/applications/94f9ec2a8d84cbc725e2)

> [accordion] GitLab
>
> GitLab has [strict rate limits](https://docs.gitlab.com/ee/security/rate_limits.html) that can prevent a project from deploying to multiple servers at one time. If you need to deploy to more than one server at a time, you should consider switching to another source control provider.

> [accordion] GitLab Self-Hosted
>
> If you receive the "Invalid repository. Are you sure you have access to it?" error message when attempting to connect a repository to your project, you should try using the Repository ID instead of the name.

## Provider Management

### Connecting Providers

You can connect to any of the supported source control providers at any time through the [Integrations panel](https://envoyer.io/user/profile#/integrations) within your account dashboard.

### Unlinking Providers

You may unlink providers at any time by clicking the **Unlink** button next to the **Refresh Token** button.

> [!WARNING]
>
> If you unlink a source control provider, you will be unable to make new deployments for projects that are connected to that provider. Existing deployments will be unaffected.
