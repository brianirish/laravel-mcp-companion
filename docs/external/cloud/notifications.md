Source: https://laravel.com/cloud/docs/notifications.md

# Notifications

Configure notifications and alerts for Laravel Cloud events.

## Introduction

Laravel Cloud sends email and Slack notifications about events in your organization, applications, and environments. Email preferences are personal to each team member. Slack notifications go to your organization's connected workspace. Both delivery methods use the same notification categories.

## Notification categories

Laravel Cloud groups notifications by the scope they apply to. Each category belongs to one of three scopes: your organization, a specific application, or an individual environment within an application.

### Organization

The following categories apply to your organization as a whole:

* **Organization updates**: changes to your organization's settings
* **Members**: new and removed members of your organization
* **API tokens**: API tokens issued and revoked from your organization
* **Applications**: creation and deletion of applications in your organization
* **Resources**: creation, deletion, and changes to resources
* **Resource alerts**: usage, limits, and health alerts for caches, databases, compute, and WebSockets
* **Monthly spend alert**: alerts at 50%, 80%, 90%, and 100% of your [spending limit](https://laravel.com/cloud/docs/spending-limits)
* **Payments**: successful and failed payments, or only failed payments

### Application

The following categories apply to a specific application:

* **Application**: changes to this application
* **Environments**: creation and deletion of environments in this application
* **Automations**: creation, deletion, and changes to [automations](https://laravel.com/cloud/docs/scheduled-tasks)

### Environment

You may configure the following categories independently for each environment within an application:

* **Environment**: changes to this environment
* **Network**: creation, deletion, and changes to domains
* **Domain alerts**: SSL certificates that fail to renew and domains that no longer point to Laravel Cloud, as described in [domain health](https://laravel.com/cloud/docs/domains#domain-health)
* **Cluster alerts**: alerts when clusters have high CPU or RAM usage, or are crashing
* **Deployments**: successful and failed deployments, or only failed deployments
* **Commands**: successful and failed commands, or only failed commands

## Email notifications

Each user configures their own email notifications. Every team member can subscribe to the events they care about across the organizations, applications, and environments they have access to.

To configure your email preferences, click your profile picture in the top-right corner of the dashboard, select **Account**, and open the **Notifications** tab. From this page, you may enable email notifications globally, then choose the categories you wish to receive emails about for each of your organizations and applications.

### Organization notifications

After selecting an organization from the organization selector, you may enable any of the [organization categories](#organization) you wish to receive emails about. Cloud saves your preferences per organization, so you can subscribe to different categories for each organization you belong to.

### Application notifications

You manage application preferences independently for each application. After selecting an application, you may enable any of the [application categories](#application) for the application as a whole, as well as the [environment categories](#environment) for each individual environment within that application.

> [!NOTE]
>
> By default, you'll receive email notifications for members, API tokens, resource alerts, monthly spend alerts, failed deployments, failed commands, and failed payments. You may adjust these preferences at any time.

## Slack notifications

Slack notifications send Laravel Cloud events to channels in your connected Slack workspace as they happen. Unlike email preferences, Slack preferences are shared by your team and configured at the organization level.

### Connecting to Slack

To get started, open your organization's **Integrations** settings and click **Connect** next to Slack. A new window opens where you can complete the integration with your Slack workspace.

### Configuring Slack delivery

Once your Slack workspace is connected, open your organization's **Notifications** settings and enable Slack notifications. From there, you may control how and where Cloud sends notifications:

* **Default channel**: the channel that receives notifications unless a more specific override applies.
* **Overrides**: send notifications for a specific application to a different channel. You may add as many overrides as you need.
* **New environment behavior**: what happens automatically when you create a new environment within an application:
  * **Notify all**: enables every notification category for the new environment.
  * **Defaults**: applies your application's default notification settings.
  * **Mute all**: disables every notification category for the new environment.


### Organization notifications

From your organization's **Notifications** settings, you may select which [organization categories](#organization) are sent to your Slack workspace.

### Application notifications

Each application has its own Slack notification preferences, configured independently from your organization's notifications. Open your application's **Notifications** tab to select which [application categories](#application) and [environment categories](#environment) are sent to Slack.
