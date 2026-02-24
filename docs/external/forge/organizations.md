# Forge - Organizations

*Source: https://forge.laravel.com/docs/organizations*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Basics
Organizations
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
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
- [Storage Providers](/docs/storage-providers)
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
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [Introduction](#introduction)
- [Organization members](#organization-members)
- [Roles](#roles)
- [Inviting new members](#inviting-new-members)
- [Canceling invitations](#canceling-invitations)
- [Removing members](#removing-members)
- [Organization billing](#organization-billing)
- [Changing plans](#changing-plans)
- [Canceling subscriptions](#canceling-subscriptions)
- [Organization settings](#organization-settings)
- [Renaming organizations](#renaming-organizations)
- [Deleting organizations](#deleting-organizations)
Basics
# Organizations
Copy page
Learn how to create and manage organizations in Laravel Forge.
Copy page
## [​](#introduction) Introduction
After registering with Laravel Forge, you will be assigned to an organization. For new registrations, this will be a brand-new organization created for you; however, if you are invited by another Laravel Forge user, you will be added to the existing organization you were invited to.
In Laravel Forge, the organization is the top-level entity that owns all server provider credentials, servers, sites, and other resources.
Each organization’s member and billing plan configuration is unique, so each organization may configure its own payment method details and preferred pricing plan.
## [​](#organization-members) Organization members
As an owner or admin of an organization on the Business plan, you are able to manage organization members via the Members tab in your organization’s settings. Users can be assigned a default role, or you may create a custom role with specific permissions.
Organization members will always be able to view resources. To limit access to resources you should add members to [teams](/docs/teams).
### [​](#roles) Roles
Laravel Forge offers five default roles for organization members:
- **Owner** - Full access to all organization settings, servers, and team members.
- **Admin** - Full access to the organization, except managing or assigning owner roles.
- **Manager** - Manages servers and teams but not billing or organization settings.
- **Developer** - Full access to servers and sites, but can’t create new servers.
- **Viewer** - View all servers, sites, and sensitive data without making changes.
You may also create custom roles with specific permissions tailored to your organization’s needs. Roles can be assigned to members on an organization or team level.
### [​](#inviting-new-members) Inviting new members
To invite someone to an organization, navigate to the organization’s dashboard and click Settings > Members. Then, enter the email of the new user, select their role, and click “Send invite”. The invited user will receive an email and notification that will allow them to accept the invitation to join the organization.
### [​](#canceling-invitations) Canceling invitations
To cancel an invitation, an admin can navigate to your Organization dashboard and click Settings > Members. Pending invitations are listed under “Invited members”. Click the three dots next to the pending invitation you wish to cancel, then click “Cancel invite”.
### [​](#removing-members) Removing members
To remove a member from an organization, an admin can navigate to your Organization dashboard and click Settings > Members. Current members are listed under “Organization members”. Click the three dots next to the member you wish to remove, then click “Remove from organization”.
## [​](#organization-billing) Organization billing
Each organization’s billing plan configuration is unique, so each organization may configure its own payment method details and preferred pricing plan.
### [​](#changing-plans) Changing plans
Every Laravel Forge organization must have an active subscription. To upgrade or downgrade your plan, an admin can navigate to your Organization dashboard and click Settings > Billing.
From the billing page, you can view your current plan, change your plan, and update your payment method. For upgrades, you will be billed pro rata for the higher plan immediately. For downgrades, your plan will be changed at the end of your current billing cycle.
Downgrading plans will result in the loss of access to some features like teams, database backups and monitoring. Make sure your applications do not depend on these features before downgrading.
### [​](#canceling-subscriptions) Canceling subscriptions
If you wish to stop using Laravel Forge, you can cancel an organization’s subscription at any time.
To cancel an organization’s subscription, an admin can navigate to your Organization dashboard and click Settings > Billing. From the billing page, click the “Cancel plan” button.
## [​](#organization-settings) Organization settings
### [​](#renaming-organizations) Renaming organizations
To rename an organization, navigate to the organization’s dashboard and click Settings. On the General tab, edit the Organization Name field. After updating the name, click Save.
### [​](#deleting-organizations) Deleting organizations
To delete an organization, navigate to the organization’s dashboard and click Settings. Then, on the General tab, click the Delete Organization button.
Deleting an organization is permanently destructive and cannot be undone. All organization member, server, and resource data will be terminated immediately.
Was this page helpful?
YesNo
[Laravel Forge SDK](/docs/sdk)[Teams](/docs/teams)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.