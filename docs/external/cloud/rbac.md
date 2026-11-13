Source: https://laravel.com/cloud/docs/rbac.md

# Roles and permissions

Control what your team members can do in Laravel Cloud with roles and granular permissions.

## Introduction

Laravel Cloud uses role-based access control (RBAC) to manage what each member of your organization can do. Every member has a role, and that role determines which actions they can perform, such as deploying environments or managing billing.

As your team grows, RBAC helps you give everyone the right level of access without exposing sensitive settings or destructive actions.

## Plan availability

Laravel Cloud offers two tiers of RBAC, and the tier available to your organization depends on your [plan](https://laravel.com/cloud/docs/pricing):

| | Starter | Growth | Business & Enterprise |
| - | - | - | - |
| **Basic RBAC** | | | |
| Team roles | Admin, Developer | All team roles | All team roles |
| **Advanced RBAC** | | | |
| Custom roles | — | — | |
| Application and environment-level access | — | — | |
| Restricted role | — | — | |

Basic RBAC uses a fixed set of predefined team roles applied across your entire organization. Advanced RBAC adds custom roles, application and environment-level access, and the Restricted role.

## Team roles

Laravel Cloud ships with predefined team roles that cover the most common team structures. You can't modify these roles, but each one has a carefully chosen set of permissions.

### Admin

Full access to everything in the organization, including member management, billing, integrations, and all resources. Every organization has at least one Admin.

### Manager

Broad operational access for day-to-day work. Managers can do nearly everything an Admin can, except delete the organization or edit billing settings.

### Developer

Build and operate applications, environments, databases, caches, and other resources. Developers cannot manage organization settings such as members, invitations, integrations, API tokens, or billing.

### Finance

Focused access for billing and usage visibility. Finance users can edit billing settings and view usage data, but don't have access to technical resources or organization management.

### Viewer

Read-only access across the organization. Viewers can see applications, environments, instances, databases, caches, object storage, WebSocket clusters, edge networks, private connections, logs, metrics, and usage. Viewers cannot create, edit, or delete anything, and cannot view environment variables or resource credentials.

### Restricted

Restricted members have no access by default. You grant them explicit access to individual applications or environments. The Restricted role is useful for contractors, auditors, or teammates who should only see part of your organization.

The Restricted role is available with Advanced RBAC on the Business and Enterprise plans and is meant to be paired with [application and environment-level access](#application-and-environment-level-access). Restricted members also inherit access to [preview environments](#preview-environments) based on the scope they're granted.

## Permissions

Each role is made up of individual permissions that control specific actions, such as creating a database, viewing environment variables, or managing domains. Laravel Cloud organizes permissions into groups that match its sections:

| Group | Controls |
| - | - |
| **Organization** | Organization settings, members, invitations, roles, billing, integrations, API tokens, notifications, and usage |
| **Applications** | Viewing, creating, editing, and deleting applications, application notifications, and merging similar exceptions |
| **Environments** | Creating and managing environments, instances, domains, environment variables, linked secrets, deploy hooks, commands, console, logs, metrics, exceptions, automations, and deployments |
| **Databases** | Creating, editing, archiving, and deleting database clusters, databases, database users, snapshots, credentials, and restores, and viewing database contents |
| **Caches** | Creating, editing, and deleting caches and cache credentials |
| **Queues** | Viewing queues, and viewing, retrying, and deleting failed jobs |
| **Object storage** | Creating, editing, and deleting buckets, objects, credentials, and access keys |
| **WebSocket clusters** | Creating, editing, and deleting WebSocket clusters and applications |
| **Edge networks** | Viewing edge networks, managing network rules, and managing private connections |
| **Secrets** | Creating, editing, and deleting secrets |
| **Log drains** | Viewing, creating, editing, and deleting log drains |
| **Email** | Viewing, creating, verifying, and deleting sending domains |

The permissions for each predefined role are fixed.

## Custom roles

> [!NOTE]
>
> Custom roles are available with Advanced RBAC on the Business and Enterprise plans.

If the predefined roles don't match the way your team is structured, you can create custom roles with any combination of permissions. Custom roles are scoped to your organization, and you assign them to members the same way as predefined roles.

To manage custom roles, navigate to your organization's **Settings > Access** page. From there you can:

* Create a new role with a name, description, and selected permissions
* Edit an existing custom role's name, description, or permissions
* Delete a custom role, provided no members are currently assigned to it

Custom roles require at least one permission.

## Application and environment-level access

> [!NOTE]
>
> Application and environment-level access is available with Advanced RBAC on the Business and Enterprise plans.

By default, a member's role applies across every application and environment in the organization. With Advanced RBAC, you can scope a member's access to a specific set of applications, or even to specific environments within an application.

You can grant access at two levels:

* **Application-level**: the member has access to every environment within the selected applications.
* **Environment-level**: the member has access only to the specific environments you choose, even if the parent application has other environments.

> [!TIP]
>
> Use application-level access for teammates who work across an entire application, and environment-level access for contractors or reviewers who should only see staging, preview, or a single production environment.

### Preview environments

Laravel Cloud creates [preview environments](https://laravel.com/cloud/docs/preview-environments) automatically from a parent environment when someone opens a pull request. Preview environments inherit the access you've already granted:

* Members with **application-level** access automatically have access to every preview environment created within that application.
* Members with **environment-level** access automatically have access to any preview environments replicated from the environments they've been granted access to.

You don't need to grant access to each preview environment individually. Access follows the same scope you originally configured.

## Managing organization members and roles

Admins can manage members and assign roles from **Settings > Access** in the organization dashboard. From this page you can:

* Invite new members and assign them a role
* Change an existing member's role
* Remove members from the organization
* Revoke pending invitations

When you change a member's role, their permissions update immediately.

For basic member management, see [Organizations](https://laravel.com/cloud/docs/organizations).
