Source: https://laravel.com/forge/docs/integrations/openclaw.md

# OpenClaw

> Deploy OpenClaw AI agent servers on Laravel Forge.

## Introduction

[OpenClaw](https://openclaw.ai) is an open-source AI agent platform that allows you to run AI assistants on your own infrastructure while integrating with popular messaging applications such as WhatsApp, Telegram, Discord, Slack, Microsoft Teams, Twitch, and Google Chat. By hosting OpenClaw on your own server, you maintain complete control over your data, API keys, and infrastructure.

Laravel Forge makes it simple to provision and manage OpenClaw servers, allowing you to deploy your own private AI assistant in minutes.

## Creating an OpenClaw Server

To create an OpenClaw server, navigate to your organization's overview or "Servers" tab and click "New server". When selecting your server type, choose "OpenClaw" from the available options.

Next, configure your server by selecting the region closest to you and choosing an appropriate server size based on your expected usage. OpenClaw servers are powered by Laravel VPS infrastructure, ensuring reliable performance and quick provisioning times.

> [!NOTE]
>
> OpenClaw servers created in the "Laravel managed" private network are available for instant provisioning. Servers in Small, Medium, Large, and X Large sizes provision instantly, while other sizes may take longer.

## Server Requirements

OpenClaw servers are provisioned with all the necessary dependencies to run the OpenClaw platform.

## Configuring OpenClaw

After your server is provisioned, you will be dropped into the OpenClaw configuration wizard terminal interface. Laravel VPS servers include a built-in web-based terminal for convenient management of your OpenClaw installation.

## Managing Your OpenClaw Server

### Resizing Your Server

If your OpenClaw deployment requires more resources, you can resize your server from the Settings tab. Select a new server size from the "Size" dropdown and confirm the change.

> [!WARNING]
>
> When resizing an OpenClaw server, the server will be temporarily unavailable during the resize process. You cannot downsize to a smaller specification.

### Backups

We recommend enabling regular backups for your OpenClaw server to protect your configuration and conversation data. Navigate to the Backups tab to configure automated backup schedules.

## Deleting an OpenClaw Server

To delete an OpenClaw server, navigate to the server's Settings tab, locate the Danger zone, and click "Delete server". Enter the server name to confirm.

> [!CAUTION]
>
> Deleting a server will permanently destroy all data, including your OpenClaw configuration and any stored conversation history. This action cannot be undone.
