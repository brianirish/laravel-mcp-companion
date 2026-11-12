Source: https://laravel.com/forge/docs/integrations/sentry.md

# Sentry

> Sentry provides error monitoring and tracing for your apps with Laravel Forge integration for creating Sentry organizations.

## Introduction

[Sentry](https://sentry.io) delivers comprehensive error monitoring and application tracing for your applications. Through Laravel Forge's partnership with Sentry, you can seamlessly create new Sentry organizations and projects directly from the Forge dashboard, eliminating the need to switch between platforms.

This integration streamlines error tracking implementation for applications hosted on Forge-managed servers while maintaining a unified development workflow.

## Connecting with Sentry

To begin using Sentry with Laravel Forge, you'll need to enable the integration at the organization level. Navigate to your organization's settings, select the **Integrations** tab, and toggle the Sentry integration on. Complete the setup by providing the required information and clicking Save to create your new Sentry organization.

> [!NOTE]
>
> The Laravel Forge integration requires creating a new Sentry organization. Existing Sentry organizations cannot be connected to this integration—all Forge-created projects will be added to your new organization.

## Creating Sentry projects

Once your organization is connected to Sentry, you can create projects for individual sites. Navigate to your site's **Settings / Integrations** panel and toggle the Sentry integration on. Select your target platform from the available options and follow the provided configuration instructions.

Click Enable Sentry to create the project, then follow the additional setup instructions to properly configure error monitoring for your specific application requirements.

> [!WARNING]
>
> Laravel Forge doesn't automatically install Sentry into your application. You must manually install the [Sentry SDK for Laravel](https://github.com/getsentry/sentry-laravel) via Composer and configure the `SENTRY_DSN` environment variable with your provided DSN key.
