# Envoyer - Accounts/Source-Control

*Source: https://docs.envoyer.io/accounts/source-control*

---

- [Documentation](/introduction)
- [Community](https://discord.com/invite/laravel)

##### Get Started

- [Introduction](/introduction)
- [Quick Start](/quick-start)

##### Accounts

- [Source Control](/accounts/source-control)
- [Your Account](/accounts/your-account)

##### Projects

- [Management](/projects/management)
- [Servers](/projects/servers)
- [Deployment Hooks](/projects/deployment-hooks)
- [Heartbeats](/projects/heartbeats)
- [Notifications](/projects/notifications)
- [Collaborators](/projects/collaborators)

On this page

- [Overview](#overview)
- [Supported Providers](#supported-providers)
- [Provider Management](#provider-management)
- [Connecting Providers](#connecting-providers)
- [Unlinking Providers](#unlinking-providers)

Accounts

# Source Control

Connect to source control providers to deploy your projects.

## [​](#overview) Overview

Project owners must connect their source control providers before they can deploy projects. You can manage source control providers from the [Integrations tab](https://envoyer.io/user/profile#/integrations) within your account dashboard.

## [​](#supported-providers) Supported Providers

Envoyer supports four source control providers:

- [GitHub](https://github.com)
- [Bitbucket](https://bitbucket.com)
- [GitLab](https://gitlab.com)
- [GitLab Self-Hosted](https://about.gitlab.com/install/)

Below we will discuss some issues that may arise when using each provider and how you can address them.

GitHub

If your organization has third-party restrictions enabled, the organization’s owner will need to approve the integration. This can be done using the following link: <https://github.com/settings/connections/applications/94f9ec2a8d84cbc725e2>

GitLab

GitLab has [strict rate limits](https://docs.gitlab.com/ee/security/rate_limits.html) that can prevent a project from deploying to multiple servers at one time. If you need to deploy to more than one server at a time, you should consider switching to another source control provider.

GitLab Self-Hosted

If you receive the “Invalid repository. Are you sure you have access to it?” error message when attempting to connect a repository to your project, you should try using the Repository ID instead of the name.

## [​](#provider-management) Provider Management

### [​](#connecting-providers) Connecting Providers

You can connect to any of the supported source control providers at any time through the [Integrations panel](https://envoyer.io/user/profile#/integrations) within your account dashboard.

### [​](#unlinking-providers) Unlinking Providers

You may unlink providers at any time by clicking the **Unlink** button next to the **Refresh Token** button.

If you unlink a source control provider, you will be unable to make new deployments for projects that are connected to that provider. Existing deployments will be unaffected.

Was this page helpful?

YesNo

[Quick Start](/quick-start)[Your Account](/accounts/your-account)

Assistant

Responses are generated using AI and may contain mistakes.