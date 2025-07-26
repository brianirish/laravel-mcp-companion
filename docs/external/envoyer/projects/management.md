# Envoyer - Projects/Management

*Source: https://docs.envoyer.io/projects/management*

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
- [Creating a Project](#creating-a-project)
- [Project Settings](#project-settings)
- [Health Checks](#health-checks)
- [Health Check IP Addresses](#health-check-ip-addresses)
- [Source Control](#source-control)
- [Transfer Project](#transfer-project)
- [Delete Project](#delete-project)

Projects

# Management

How to manage your Envoyer projects.

## [​](#overview) Overview

Within Envoyer, your application is represented by a “project”. Projects can be deployed to one or more servers at the same time.

## [​](#creating-a-project) Creating a Project

To create a project, click the **Add Project** button at the top of the Envoyer dashboard. You will be presented with a modal that asks you to provide a few details about the project.
If you don’t see the Source Control provider that you need, make sure that you’ve linked it in your account settings.
Once you’ve provided the details regarding your project, click **Save Project**.

To create new projects, you must be subscribed to one of Envoyer’s paid subscriptions.

## [​](#project-settings) Project Settings

To make changes to your project settings, click the **Settings** button at the top of the project’s dashboard.
From here, you can change the project settings, source control settings, and delete the project. In addition, you can edit the project’s name, type, health check URL, and how many deployments to retain for the project

### [​](#health-checks) Health Checks

When your site has finished deploying, Envoyer can ping it to ensure that it is still available. Health checks are performed from three locations:

- New York
- London
- Singapore

If you have configured notifications on your project, Envoyer will notify these channels of the result of the health check.

The configured URL must return a `2xx` status code. All other status codes will be considered a failure.

#### [​](#health-check-ip-addresses) Health Check IP Addresses

If your application firewall requires you to allow access from the health check monitors by IP address, you should allow the following IP addresses so that Envoyer can ping your URL:

- New York: `198.199.84.22`
- London: `167.71.140.19`
- Singapore: `167.71.208.72`

### [​](#source-control) Source Control

You can manage how the project is deployed via the project’s source control settings. Specifically, you may configure from which source control provider the project is deployed, the branch that is deployed, and you may also choose whether to install the project’s Composer dependencies.
You may also enable the project’s **Deploy When Code Is Pushed** setting. Enabling this setting will add a webhook to your source control provider. When code is pushed to the selected branch, Envoyer will automatically trigger a new deployment.

### [​](#transfer-project) Transfer Project

Projects may be transferred to other Envoyer accounts from the project’s Settings panel. To transfer the project, you must provide the email address of the Envoyer account you wish to transfer the project to. The Envoyer account that is receiving the project will receive an email asking them to confirm the transfer request.
You may only transfer projects to Envoyer accounts with an active subscription.

### [​](#delete-project) Delete Project

If you no longer need the project, you may delete it via the project settings dashboard. After confirming the name of the project, click the **Delete Project** button.

Deleting your project is an irreversible action, and we will be unable to recover the project’s settings for you.

Was this page helpful?

YesNo

[Your Account](/accounts/your-account)[Servers](/projects/servers)

Assistant

Responses are generated using AI and may contain mistakes.