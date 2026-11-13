Source: https://laravel.com/cloud/docs/organizations.md

# Organizations

Manage Laravel Cloud organizations, members, permissions, billing, and shared application resources.

## Introduction

When you register with Laravel Cloud, Cloud assigns you to an organization. For new registrations, Cloud creates a brand new organization just for you. If another Laravel Cloud user invites you, Cloud adds you to their existing organization instead.

In Laravel Cloud, the organization is the top-level entity that owns all applications, environments, and resources
such as databases and custom domains.

Each organization's member and billing plan configuration is unique, so each organization may configure its own payment method details and preferred pricing plan.

## Organization members

You can manage your organization's members from **Settings > Access**. Each member has a role that controls what they can view and manage. See [Roles and permissions](https://laravel.com/cloud/docs/rbac) for the available roles.

### Inviting new members

To invite someone to an organization, navigate to the organization's dashboard and click **Settings > Access**.
Then, enter the email of the new user and click **Invite**. Cloud sends the invited user an email they can use to accept the invitation and join the organization.

#### Revoking invitations

Admins can revoke pending invitations. To revoke an invite, navigate to your organization's dashboard and click **Settings > Access**.
On any row that shows the **Invite pending** status, click the **...** button and select **Revoke invite**.

### Removing members

To remove a member from an organization, navigate to your organization's dashboard and click **Settings > Access**. On a member row, click the **...** button and select **Remove member**.

## Organization billing

Each organization's billing plan configuration is unique, so each organization may configure its own payment method details and preferred pricing plan.

### Changing plans

Every Laravel Cloud organization must have an active subscription. To upgrade or downgrade your plan,
an Admin can navigate to your organization's dashboard and click **Settings > Billing**.

Then, click **Change plan**, select
a new plan, and then click **Update plan**. For upgrades, we immediately issue a one-off invoice for any usage accrued in the current billing period. The invoice also includes the new subscription fee, prorated based on the days remaining in the current billing period. We then continue to issue monthly invoices on the regular anniversary billing date.

For downgrades, you keep access to the higher plan and its features for the rest of the billing period.

> [!WARNING]
>
> When you downgrade, you lose access to some features, such as custom domains and autoscaling.
> Before downgrading, make sure your applications do not depend on these features.

### Canceling subscriptions

If you wish to stop using Laravel Cloud, you can cancel an organization's subscription at any time.

To cancel an organization's subscription, an Admin can navigate to the organization's dashboard, click **Settings > Billing**, and click **Cancel subscription**.

Your subscription continues on the current plan for the rest of your current billing period. At the end of the billing period, Cloud terminates any environment
compute, resources, or custom domains that are still active. Two days later, we process your final invoice.

After your subscription ends, you still have access to your organization's basic data, such as invoices and members. To deploy or manage additional applications for that organization, resubscribe to a billing plan.

### Billing details

To change an organization's billing details, an Admin can navigate to the organization's dashboard and click **Settings > Billing**.
Scroll to the **Billing details** section, and make any necessary changes to your **Bill as** type (**Individual** or **Company**),
**Billing name**, **Billing email**, **Billing address**, or **Payment method**.

### Usage and invoices

To view information about your organization's current compute, bandwidth, or other resource usage, navigate to
your organization's dashboard and click **Usage** in the navigation bar. From the usage dashboard, you can review your
current spend, your plan allowances, usage by application and environment, and resource usage across your organization.

## General settings

### Renaming organizations

To rename an organization, navigate to the organization's dashboard and click **Settings**. On the **General** tab,
edit the **Organization name** field. After updating the name, click **Save**.

### Deleting organizations

To delete an organization, navigate to the organization's dashboard and click **Settings**. Then, on the **General** tab, click the **Delete organization** button.

> [!WARNING]
>
> Before you can delete an organization, it must be current on all outstanding invoices and have no additional usage charges for the current
> billing period. Deleting an organization is permanent and cannot be undone. Cloud immediately terminates all organization member, application, and resource data.

## Notifications

Connect Laravel Cloud to your Slack workspace to receive notifications about your organization, applications, resources, and more.

See [Notifications](https://laravel.com/cloud/docs/notifications) for detailed setup of organization notifications.
