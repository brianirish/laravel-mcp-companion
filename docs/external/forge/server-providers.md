# Forge - Server-Providers

*Source: https://forge.laravel.com/docs/server-providers*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Basics

Server Providers

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
- [Supported providers](#supported-providers)
- [Managing server providers](#managing-server-providers)
- [Connecting server providers](#connecting-server-providers)
- [DigitalOcean](#digitalocean)
- [AWS](#aws)
- [AWS service limits](#aws-service-limits)
- [Akamai](#akamai)
- [Vultr API access](#vultr-api-access)
- [Hetzner Cloud API access](#hetzner-cloud-api-access)
- [Bring your own server](#bring-your-own-server)

Basics

# Server Providers

Copy page

Learn about the server providers supported by Laravel Forge.

Copy page

## [​](#introduction) Introduction

All servers provisioned on Laravel Forge are powered by an underlying server provider. The fastest way to get started is by using Laravel VPS as your server provider, which are Laravel managed servers. After subscribing to a Forge plan, you can immediately start provisioning Laravel VPS servers with zero additional configuration.
Forge also allows you to link external server providers such as AWS or Hetzner so that you may create servers on those platforms. Server providers are configured and managed within the [organization’s](/docs/organizations) settings.

## [​](#supported-providers) Supported providers

Laravel Forge supports the following cloud server providers:

- [Laravel VPS](/docs/servers/laravel-vps)
- [DigitalOcean](https://www.digitalocean.com/)
- [Akamai / Linode Cloud](https://www.linode.com/)
- [Vultr](https://www.vultr.com/)
- [Amazon AWS](https://aws.amazon.com/) (Non-Gov)
- [Hetzner Cloud](https://www.hetzner.com/cloud)
- [Bring your own server](#bring-your-own-server)

If your preferred server provider is not supported by Laravel Forge, you may use Forge’s “Custom VPS” option to create your server. Custom VPS servers receive all of the same functionality as first-party supported server providers. [Learn more](#bring-your-own-server)

## [​](#managing-server-providers) Managing server providers

### [​](#connecting-server-providers) Connecting server providers

To connect a server provider, navigate to the organization’s settings. Then, on the “Server providers” page, click “Add provider”. Select the provider you wish to connect to and authenticate your chosen account.
It is possible to link any number of supported server provider accounts, including multiple accounts for the same provider.

### [​](#digitalocean) DigitalOcean

To connect your DigitalOcean account, navigate to the Server providers page under the organization’s settings. Then, click Add provider. Select DigitalOcean, click Add provider, then click Login with DigitalOcean. Authenticate your account by following instructions provided by DigitalOcean.
Once approved, Laravel Forge will create an OAuth credential, allowing it to access the necessary permissions needed in provisioning and managing your servers on your behalf.

### [​](#aws) AWS

In order to provision servers on AWS, you need to create a new IAM role. To get started, navigate to the IAM service on your AWS dashboard. Once you are in the IAM dashboard, you may select “Roles” from the left-side navigation panel and click the “Create Role” button.
The process for creating the role is outlined in these steps:

1. Choose “AWS account” as the trusted entity type, and select “Another AWS account.”
2. Enter the “Laravel Forge AWS Account” from the Forge dashboard, then click “Next.”
3. In the “Permissions policies” section, select the `AmazonEC2FullAccess` and `AmazonVPCFullAccess` policies. Then, click “Next.”
4. In the “Name, review, and create” section, provide a name and description for the role.
5. Update the “Trust policy” under “Select trusted entities” by enabling the “Require external ID” checkbox and entering the “AWS External ID” shown in the Laravel Forge dashboard.
6. Complete the process by creating the role.
7. Copy the role ARN displayed in the AWS dashboard and add it to your AWS credentials in Laravel Forge.

There are a few requirements you should review to ensure Laravel Forge works correctly with your linked AWS account:

- If you are using an existing VPC, the subnet must be configured to **auto-assign public IP addresses**.
- If you are using an existing VPC, the default security group **must allow Laravel Forge to SSH into the server**. Here is an example:

| Type | Protocol | Port Range | Source |  | Description |
| --- | --- | --- | --- | --- | --- |
| HTTP | TCP | 80 | Custom | 0.0.0.0/0 |  |
| HTTP | TCP | 80 | Custom | ::/0 |  |
| SSH | TCP | 22 | Custom | YOUR_IP_ADDRESS/32 | SSH from your IP |
| SSH | TCP | 22 | Custom | 159.203.150.232/32 | SSH from Laravel Forge |
| SSH | TCP | 22 | Custom | 159.203.150.216/32 | SSH from Laravel Forge |
| SSH | TCP | 22 | Custom | 45.55.124.124/32 | SSH from Laravel Forge |
| SSH | TCP | 22 | Custom | 165.227.248.218/32 | SSH from Laravel Forge |
| HTTPS | TCP | 443 | Custom | 0.0.0.0/0 |  |
| HTTPS | TCP | 443 | Custom | ::/0 |  |

#### [​](#aws-service-limits) AWS service limits

AWS Service Limits can be increased through the following options:

From the AWS console

1. Open the Service Quotas console.
2. In the navigation pane, choose AWS services.
3. Select a service.
4. Select a quota.
5. Follow the directions to request a quota increase.

From the AWS CLI

- Use the [request-service-quota-increase](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html) AWS CLI command.

From a support case

- If a service is not yet available in Service Quotas, use the AWS Support Center Console to create a [service quota increase case](https://support.console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase).
- If the service is available in Service Quotas, AWS recommends that you use the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home) instead of creating a support case.

For additional information, refer to the following AWS documentation:

- [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*.
- [AWS Service Quotas reference](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).

### [​](#akamai) Akamai

To connect your Akamai account, navigate to the Server providers page under the organization’s settings. Then, click Add provider. Select Akamai, click Add provider. Once you have provided a Profile name and API key, click Add provider. Laravel Forge will verify that it is able to access your account.
When creating a [new Akamai Cloud API token](https://cloud.linode.com/profile/tokens) for your Akamai account, Akamai will ask you to select which permissions are needed by the token. You will need to select the following permissions:

- **Linodes** - Read/Write
- **IPs** - Read/Write

In addition, you may wish to set the token to never expire.

### [​](#vultr-api-access) Vultr API access

The Vultr server provider requires you to add the [Laravel Forge IP addresses](/docs/introduction#forge-ip-addresses) to an [IP address allow list](https://docs.vultr.com/platform/other/api/manage-api-access-control) so that Forge can communicate with your servers. You should ensure that you do this before provisioning a Vultr server via Forge.

### [​](#hetzner-cloud-api-access) Hetzner Cloud API access

Hetzner API tokens are specific to a Hetzner Project. If you utilize Hetzner Projects, you should ensure that Laravel Forge has an API token for each Hetzner Project.

#

*[Content truncated for length]*