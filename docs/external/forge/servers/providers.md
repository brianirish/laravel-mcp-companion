# Forge - Servers/Providers

*Source: https://forge.laravel.com/docs/servers/providers*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)

##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

On this page

- [Supported Server Providers](#supported-server-providers)
- [Linking Server Providers](#linking-server-providers)
- [Amazon AWS API Access](#amazon-aws-api-access)
- [AWS Service Limits](#aws-service-limits)
- [Akamai / Linode API Access](#akamai-%2F-linode-api-access)
- [DigitalOcean OAuth Access](#digitalocean-oauth-access)
- [DigitalOcean API Access](#digitalocean-api-access)
- [Vultr API Access](#vultr-api-access)
- [Hetzner Cloud API Access](#hetzner-cloud-api-access)
- [Bring Your Own Server](#bring-your-own-server)

Servers

# Server Providers

Learn about the server providers supported by Forge.

## [​](#supported-server-providers) Supported Server Providers

Forge can create and manage servers on the following cloud server providers:

- [DigitalOcean](https://www.digitalocean.com/)
- [Vultr](https://www.vultr.com/)
- [Akamai / Linode Cloud](https://www.linode.com/)
- [Amazon AWS](https://aws.amazon.com/)
  - Forge supports provisioning servers in all non-Gov regions that are active in the connected AWS account.
- [Hetzner Cloud](https://www.hetzner.com/cloud)
- [Bring Your Own Server](#bring-your-own-server)

If your preferred server provider is not supported by Forge, you may use Forge’s “Custom VPS” option to create your server. Custom VPS servers receive all of the same functionality as first-party supported server providers. [Learn more](/docs/servers/providers#bring-your-own-server)

## [​](#linking-server-providers) Linking Server Providers

You can link server providers from your [Server Providers dashboard](https://forge.laravel.com/user-profile/server-providers). It is possible to link any number of supported provider accounts, including multiple accounts for one provider.

### [​](#amazon-aws-api-access) Amazon AWS API Access

In order to provision servers on AWS, you need to create a new IAM role. To get started, navigate to the IAM service on your AWS dashboard. Once you are in the IAM dashboard, you may select “Roles” from the left-side navigation panel and click the “Create Role” button.
The process for creating the role is outlined in these steps:

1. Choose “AWS account” as the trusted entity type, and select “Another AWS account.”
2. Enter the “Forge AWS Account” from the Forge dashboard, then click “Next.”
3. In the “Permissions policies” section, select the `AmazonEC2FullAccess` and `AmazonVPCFullAccess` policies. Then, click “Next.”
4. In the “Name, review, and create” section, provide a name and description for the role.
5. Update the “Trust policy” under “Select trusted entities” by enabling the “Require external ID” checkbox and entering the “AWS External ID” shown in the Forge dashboard.
6. Complete the process by creating the role.
7. Copy the role ARN displayed in the AWS dashboard and add it to your AWS credentials in Forge.

There are a few requirements you should review to ensure Forge works correctly with your linked AWS account:

- If you are using an existing VPC, the subnet must be configured to **auto-assign public IP addresses**.
- If you are using an existing VPC, the default security group **must allow Forge to SSH into the server**. Here is an example:

| Type | Protocol | Port Range | Source |  | Description |
| --- | --- | --- | --- | --- | --- |
| HTTP | TCP | 80 | Custom | 0.0.0.0/0 |  |
| HTTP | TCP | 80 | Custom | ::/0 |  |
| SSH | TCP | 22 | Custom | YOUR_IP_ADDRESS/32 | SSH from your IP |
| SSH | TCP | 22 | Custom | 159.203.150.232/32 | SSH from Forge |
| SSH | TCP | 22 | Custom | 159.203.150.216/32 | SSH from Forge |
| SSH | TCP | 22 | Custom | 45.55.124.124/32 | SSH from Forge |
| SSH | TCP | 22 | Custom | 165.227.248.218/32 | SSH from Forge |
| HTTPS | TCP | 443 | Custom | 0.0.0.0/0 |  |
| HTTPS | TCP | 443 | Custom | ::/0 |  |

#### [​](#aws-service-limits) AWS Service Limits

AWS Service Limits can be increased through the following options:

From the AWS console

1. Open the Service Quotas console.
2. In the navigation pane, choose AWS services.
3. Select a service.
4. Select a quota.
5. Follow the directions to request a quota increase.

From the AWS CLI

1. Use the [request-service-quota-increase](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/request-service-quota-increase.html) AWS CLI command.

From a support case

- If a service is not yet available in Service Quotas, use the AWS Support Center Console to create a [service quota increase case](https://support.console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase).
- If the service is available in Service Quotas, AWS recommends that you use the [Service Quotas console](https://console.aws.amazon.com/servicequotas/home) instead of creating a support case.

For additional information, refer to the following AWS documentation:

- [Requesting a quota increase](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html) in the *Service Quotas User Guide*.
- [AWS Service Quotas reference](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).

### [​](#akamai-%2F-linode-api-access) Akamai / Linode API Access

When creating a [new Akamai Cloud API token](https://cloud.linode.com/profile/tokens) for your Akamai account, Akamai will ask you to select which permissions are needed by the token. You will need to select the following permissions:

- **Linodes** - Read/Write
- **IPs** - Read/Write

In addition, you may wish to set the token to never expire.

### [​](#digitalocean-oauth-access) DigitalOcean OAuth Access

The easiest way to allow Forge to communicate with your DigitalOcean account is by using the “Login with DigitalOcean” button. This option can be found on the [Server Providers](https://forge.laravel.com/user-profile/server-providers) page within your Forge account.
Clicking the “Login with DigitalOcean” button will redirect you to DigitalOcean’s Authorize Application page, where you’ll be asked to approve the required permissions requested by Forge.
Once approved, Forge will create an OAuth credential, allowing it access to the necessary permissions needed in provisioning and managing your servers on your behalf.

### [​](#digitalocean-api-access) DigitalOcean API Access

In addition to granting Forge access via OAuth, you can also use a [Personal Access Token](https://cloud.digitalocean.com/account/api/tokens) to enable Forge to communicate with your DigitalOcean account. When creating a new Personal Access Token for your DigitalOcean account, you will need to select which scopes will be granted on the token. You must select either:

1. **Full Access**: Grants access to all scopes based on the account’s current role permissions
2. **Custom Scopes**: Grants granular permissions on specific scopes. The following are **required** by Forge to successfully provision a server:
   - **Droplet** - Create / Read / Update / Delete
   - **Reserved IP** - Create / Read / Update / Delete
   - **SSH Key** - Create / Read / Update / Delete
   - **VPC Key** - Create / Read / Update / Delete

### [​](#vultr-api-access) Vultr API Access

The Vultr server provider requires you to add the [Forge IP addresses](/docs/introduction#forge-ip-addresses) to an [IP address allow list](https://docs.vultr.com/platform/other/api/manage-api-access-control) so that Forge can communicate with your servers. You should ensure that you do this before provisioning a Vultr server via Forge.

### [​](#hetzner-cloud-api-access) Hetzner Cloud API Access

Hetzner API tokens are specific to a Hetzner Project. If you utilize Hetzner Projects, you should ensure that Forge has an API token for each Hetzner Project.

## [​](#bring-your-own-server) Bring Your Own Server

Alongside supporting several first-party server providers, Forge also supports the ability to use your own custom server. To do so, select the **Custom VPS** option when creating a new server. When provisioning a Custom VPS, Forge can only provision and manage an existing server — it cannot create servers on that custom provider.
In addition, you should 

*[Content truncated for length]*