# Vapor - Introduction

*Source: https://docs.vapor.build/introduction*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)

[Laravel Vapor home page![light logo](https://mintcdn.com/vapor/xzCd7jrV_PrTp5n0/logo/light.svg?fit=max&auto=format&n=xzCd7jrV_PrTp5n0&q=85&s=b75f22b35cd4eb8d659a33a7efe9a317)![dark logo](https://mintcdn.com/vapor/xzCd7jrV_PrTp5n0/logo/dark.svg?fit=max&auto=format&n=xzCd7jrV_PrTp5n0&q=85&s=bbbfac3aab3d7a07d5382ee8fa9a669e)](https://vapor.laravel.com)

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...

Navigation

Get Started

Introduction

[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com)

##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

On this page

- [What Is Vapor?](#what-is-vapor)
- [Requirements](#requirements)
- [Account Creation](#account-creation)
- [Installing The Vapor CLI](#installing-the-vapor-cli)
- [Logging In](#logging-in)
- [Installing The Vapor Core](#installing-the-vapor-core)
- [Sandbox Accounts](#sandbox-accounts)
- [Teams](#teams)
- [Current Team & Switching Teams](#current-team-%26-switching-teams)
- [Collaborators](#collaborators)
- [Linking With AWS](#linking-with-aws)
- [Creating An IAM Role](#creating-an-iam-role)
- [Permissions](#permissions)
- [Defining Your AWS Budget](#defining-your-aws-budget)
- [AWS Service Limits](#aws-service-limits)
- [Notification Methods](#notification-methods)
- [Slack](#slack)
- [Legal and Compliance](#legal-and-compliance)

Get Started

# Introduction

Manage your Laravel infrastructure on Vapor and fall in love with the scalability and simplicity of serverless.

[## Create An Account

Create your Vapor account today](https://vapor.laravel.com/register)[## Watch More

Watch the free Vapor series on Laracasts](https://laracasts.com/series/serverless-laravel)

## [​](#what-is-vapor) What Is Vapor?

Laravel Vapor is an auto-scaling, serverless deployment platform for Laravel, powered by AWS Lambda. Manage your Laravel infrastructure on Vapor and fall in love with the scalability and simplicity of serverless.
Vapor abstracts the complexity of managing Laravel applications on AWS Lambda, as well as interfacing those applications with SQS queues, databases, Redis clusters, networks, CloudFront CDN, and more. Some highlights of Vapor’s features include:

- Auto-scaling web / queue infrastructure fine tuned for Laravel
- Zero-downtime deployments and rollbacks
- Environment variable / secret management
- Database management, including point-in-time restores and scaling
- Redis Cache management, including cluster scaling
- Database and cache tunnels, allowing for easy local inspection
- Automatic uploading of assets to Cloudfront CDN during deployment
- Unique, Vapor assigned vanity URLs for each environment, allowing immediate inspection
- Custom application domains
- DNS management
- Certificate management and renewal
- Application, database, and cache metrics
- CI friendly

**In short, you can think of Vapor as** [Laravel Forge](https://forge.laravel.com) **for serverless technology.**

## [​](#requirements) Requirements

Vapor requires that your application be compatible with PHP 7.3+ and Laravel 6.0+.

## [​](#account-creation) Account Creation

Before integrating Vapor into your application, you should create a Vapor account. If you are just collaborating with others on their projects, you are not required to have a Vapor subscription. To create and manage your own projects, you will need a Vapor subscription.

## [​](#installing-the-vapor-cli) Installing The Vapor CLI

You will deploy your Laravel Vapor applications using the [Vapor CLI](https://github.com/laravel/vapor-cli). This CLI may be installed globally or on a per-project basis using Composer:

Copy

Ask AI

```
composer require laravel/vapor-cli --update-with-dependencies

composer global require laravel/vapor-cli --update-with-dependencies
```

When the CLI is installed per project, you will likely need to execute it via the `vendor/bin` directory of your project, which is where Composer installs executables. For example, to view all of the available Vapor CLI commands, you may use the `list` command:

Copy

Ask AI

```
php vendor/bin/vapor list
```

To save keystrokes when interacting with per-project installations of the Vapor CLI, you may add a shell alias to your operating system that aliases the `vapor` command to `php vendor/bin/vapor`.

To learn more about a command and its arguments, execute the `help` command with the name of the command you wish to explore:

Copy

Ask AI

```
php vendor/bin/vapor help deploy
```

### [​](#logging-in) Logging In

After you have installed the Vapor CLI, you should authenticate with your Vapor account using the `login` command:

Copy

Ask AI

```
vapor login
```

## [​](#installing-the-vapor-core) Installing The Vapor Core

The `laravel/vapor-core` [package](https://github.com/laravel/vapor-core) must be installed as a dependency of every Laravel application that is deployed using Vapor. This package contains various Vapor runtime files and a service provider to allow your application to run on Vapor. You may install the Vapor Core into your project using Composer:

Copy

Ask AI

```
composer require laravel/vapor-core --update-with-dependencies
```

## [​](#sandbox-accounts) Sandbox Accounts

After creating a Vapor account, your account will be on our free “sandbox” plan, which allows you to experience the power of Vapor without the upfront commitment of subscribing to a paid plan. A sandbox account allows you to provision services such as networks, databases, and caches. You may add a single project which, once deployed, will be accessible via an [AWS Lambda function URL](https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html).

Sandbox projects may not utilize API Gateway versions, load balancers, firewalls, or custom domains. To utilize these features, you will need to choose a subscription plan.

## [​](#teams) Teams

When you create your Vapor account, a “Personal” team is automatically created for you. You can rename this team in your team settings. All projects, databases, caches, and other Vapor resources belong to a team. You are free to create as many teams as you wish via the Vapor UI or the `team` CLI command. There is no additional charge for creating teams, and they serve as a great way to organize your projects by client or topic.

### [​](#current-team-&-switching-teams) Current Team & Switching Teams

When managing Vapor resources via the CLI, you will need to be aware of your currently active team. You may view your current team using the `team:current` command:

Copy

Ask AI

```
vapor team:current
```

To change your active team, you may use the `team:switch` command:

Copy

Ask AI

```
vapor team:switch
```

### [​](#collaborators) Collaborators

You can invite more people to your team via the “Team Settings” menu in the Vapor UI, or using the `team:add` CLI command. When you add a new collaborator to your team via the Vapor UI, you may select the permissions to assign to that person. For example, you can prevent a given team member from deleting databases or caches.
You may remove collaborators from your team using the Vapor UI or `team:remove` CLI command.

## [​](#linking-with-aws) Linking With AWS

In order to deploy projects or create other resources using Vapor, you will need to link an active AWS account on your team’s settings management page.

### [​](#creating-an-iam-role) Creating An IAM Role

To create a new IAM role, navigate to the IAM service on your AWS dashboard. Once you are in the IAM dashboard, you may select “Roles” from the left-side navigation panel and click the “Create Role” button.
The process for creating the role is outlined in these steps:

1. Choose “AWS account” as the trusted entity type, and select “Another AWS account”.
2. Enter the “Vapor Account ID” from the Vapor dashboard.
3. Under “Options”, enable the “Require external ID” checkbox, enter the “Team External ID” shown in the Vapor dashboard, and then click “Next”.
4. In the “Permissions policies” section, either grant full administrator access by selecting the `AdministratorAccess` policy or create a custom policy with the [specific permissions](/introduction#permissions) required by Vapor. After selecting a policy, click “Next”.
5. In the “Name, review, and create” section, provide a name and description for the role.
6. Complete the process by creating the role.
7. Copy the role ARN displayed in the AWS dashboard and add it to your AWS credentials in Vapor.

#### [​](#permissions) Permissions

Since Vapor manages many types of resources across more than a dozen AWS services, it may be convenient to create a role with the `AdministratorAccess` policy. If desired, you may create a separate AWS account to house this role and contain all of your Vapor resources.

On the permissions management screen, you may grant full administrator access to the IAM role by selecting the “AdministratorAccess” policy. Or, you would prefer to not provide administrator access to Vapor, you may instead create a custom permission policy with the specific permissions needed by Vapor.
It is necessary to create two policies due to the policy size limit set by AWS. To do so, select “Create policy” from the “Permissions policies” panel. Choose the JSON option an

*[Content truncated for length]*