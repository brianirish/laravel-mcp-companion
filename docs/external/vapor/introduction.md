# Vapor - Introduction

*Source: https://docs.vapor.build/introduction*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)
[Laravel Vapor home page](https://vapor.laravel.com)
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)
Search...
Navigation
Get Started
Introduction
[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)
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
- [Migrate to Cloud](/resources/migrate-to-cloud)
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
[Laravel Cloud](https://cloud.laravel.com) builds on the ideas behind Vapor while removing much of the operational complexity. [This migration guide](https://cloud.laravel.com/migration-vapor-cloud) explains why teams are migrating from Vapor to Cloud and what changes when moving an application.
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
It is necessary to create two policies due to the policy size limit set by AWS. To do so, select “Create policy” from the “Permissions policies” panel. Choose the JSON option and provide the first permission definition below. Then, follow the same process to create another policy using the second definition listed below. Once the policies have been defined, you may attach them to your new IAM role:
Copy
Ask AI
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VaporPolicy",
            "Effect": "Allow",
            "Action": [
                "acm:AddTagsToCertificate",
                "acm:DeleteCertificate",
                "acm:DescribeCertificate",
                "acm:ImportCertificate",
                "acm:RequestCertificate",
                "apigateway:DELETE",
                "apigateway:GET",
                "apigateway:PATCH",
                "apigateway:POST",
                "apigateway:PUT",
                "apigateway:SetWebACL",
                "budgets:ModifyBudget",
                "budgets:ViewBudget",
                "cloudformation:CreateStack",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeStacks",
                "cloudformation:UpdateStack",
                "cloudfront:CreateOriginAccessControl",
                "cloudfront:CreateDistribution",
                "cloudfront:DeleteDistribution",
                "cloudfront:GetDistribution",
                "cloudfront:GetDistributionConfig",
                "cloudfront:UpdateDistribution",
                "cloudwatch:DeleteAlarms",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:PutMetricAlarm",
                "dynamodb:CreateTable",
                "dynamodb:DescribeTable",
                "dynamodb:DescribeTimeToLive",
                "dynamodb:TagResource",
                "dynamodb:UpdateTimeToLive",
                "ec2:AllocateAddress",
                "ec2:AssociateAddress",
                "ec2:AssociateRouteTable",
                "ec2:AttachInternetGateway",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateInternetGateway",
                "ec2:CreateNatGateway",
                "ec2:CreateRoute",
                "ec2:CreateRouteTable",
                "ec2:CreateSubnet",
                "ec2:CreateTags",
                "ec2:CreateVpc",
                "ec2:CreateVpcEndpoint",
                "ec2:DeleteInternetGateway",
                "ec2:DeleteKeyPair",
                "ec2:DeleteNatGateway",
                "ec2:DeleteRoute",
                "ec2:DeleteRouteTable",
                "ec2:DeleteSubnet",
                "ec2:DeleteVolume",
                "ec2:DeleteVpc",
                "ec2:DeleteVpcEndpoints",
                "ec2:DescribeAddresses",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeImages",
                "ec2:DescribeInstanceAttribute",
                "ec2:DescribeInstances",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeNatGateways",
                "ec2:DescribeNetworkAcls",
                "ec2:DescribeRegions",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroupRules",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSnapshots",
                "ec2:DescribeSubnets",
                "ec2:DescribeTransitGatewayRouteTables",
                "ec2:DescribeTransitGatewayVpcAttachments",
                "ec2:DescribeTransitGateways",
                "ec2:DescribeVolumes",
                "ec2:DescribeVpcEndpoints",
                "ec2:DescribeVpcs",
                "ec2:DetachInternetGateway",
                "ec2:DisassociateRouteTable",
                "ec2:ImportKeyPair",
                "ec2:ModifySubnetAttribute",
                "ec2:ModifyVpcAttribute",
                "ec2:ReleaseAddress",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:RunInstances",
                "ec2:TerminateInstances",
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchDeleteImage",
                "ecr:BatchGetImage",
                "ecr:CompleteLayerUpload",
                "ecr:CreateRepository",
                "ecr:DeleteRepository",
                "ecr:GetAuthorizationToken",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:SetRepositoryPolicy",
                "ecr:UploadLayerPart",
                "elasticache:AddTagsToResource",
                "elasticache:CreateCacheSubnetGroup",
                "elasticache:CreateReplicationGroup",
                "elasticache:CreateServerlessCache",
                "elasticache:DeleteCacheSubnetGroup",
                "elasticache:DeleteReplicationGroup",
                "elasticache:DeleteServerlessCache",
                "elasticache:DescribeCacheSubnetGroups",
                "elasticache:DescribeReplicationGroups",
                "elasticache:DescribeServerlessCaches",
                "elasticache:ListTagsForResource",
                "elasticache:ModifyReplicationGroupShardConfiguration",
                "elasticache:ModifyServerlessCache",
                "elasticloadbalancing:AddListenerCertificates",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyRule",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:SetWebAcl",
                "events:DeleteRule",
                "events:DescribeRule",
                "events:ListTargetsByRule",
                "events:PutRule",
                "events:PutTargets",
                "events:RemoveTargets",
                "iam:CreateRole",
                "iam:CreateServiceLinkedRole",
                "iam:GetRole",
                "iam:GetUser",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:UpdateAssumeRolePolicy",
                "kms:CreateGrant",
                "kms:Decrypt",
                "kms:DescribeKey",
                "kms:Encrypt",
                "kms:GenerateDataKey",
                "lambda:AddPermission",
                "lambda:CreateAlias",
                "lambda:CreateEventSourceMapping",
                "lambda:CreateFunction",
                "lambda:CreateFunctionUrlConfig",
                "lambda:DeleteFunction",
                "lambda:DeleteFunctionConcurrency",
                "lambda:DeleteProvisionedConcurrencyConfig",
                "lambda:GetAccountSettings",
                "lambda:GetAlias",
                "lambda:GetFunction",
                "lambda:GetFunctionUrlConfig",
                "lambda:GetLayerVersion",
                "lambda:GetPolicy",
                "lambda:InvokeFunction",
                "lambda:ListEventSourceMappings",
                "lambda:ListVersionsByFunction",
                "lambda:PublishVersion",
                "lambda:PutFunctionConcurrency",
                "lambda:PutFunctionEventInvokeConfig",
                "lambda:PutProvisionedConcurrencyConfig",
                "lambda:TagResource",
                "lambda:UpdateAlias",
                "lambda:UpdateEventSourceMapping",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "logs:FilterLogEvents",
                "rds:AddTagsToResource",
                "rds:CreateDBCluster",
                "rds:CreateDBInstance",
                "rds:CreateDBProxy",
                "rds:CreateDBSubnetGroup",
                "rds:DeleteDBCluster",
                "rds:DeleteDBInstance",
                "rds:DeleteDBProxy",
                "rds:DeleteDBSubnetGroup",
                "rds:DescribeDBClusters",
                "rds:DescribeDBEngineVersions",
                "rds:DescribeDBInstances",
                "rds:DescribeDBProxies",
                "rds:DescribeDBSubnetGroups",
                "rds:ListTagsForResource",
                "rds:ModifyDBCluster",
                "rds:ModifyDBInstance",
                "rds:RegisterDBProxyTargets",
                "rds:RestoreDBInstanceToPointInTime",
                "route53:ChangeResourceRecordSets",
                "route53:CreateHostedZone",
                "route53:GetHostedZone",
                "route53:ListHostedZonesByName",
                "route53:ListResourceRecordSets",
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:DeleteBucketPolicy",
                "s3:DeleteObject",
                "s3:GetBucketCORS",
                "s3:GetBucketLocation",
                "s3:GetBucketTagging",
                "s3:GetBucketVersioning",
                "s3:GetObject",
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:PutBucketCORS",
                "s3:PutBucketOwnershipControls",
                "s3:PutBucketPublicAccessBlock",
                "s3:PutLifecycleConfiguration",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutBucketPolicy",
                "secretsmanager:CreateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:GetSecretValue",
                "secretsmanager:TagResource",
                "servicequotas:GetServiceQuota",
                "ses:VerifyDomainDkim",
                "ses:VerifyDomainIdentity",
                "sns:ConfirmSubscription",
                "sns:CreateTopic",
                "sns:GetTopicAttributes",
                "sns:ListSubscriptionsByTopic",
                "sns:SetTopicAttributes",
                "sns:Subscribe",
                "sns:TagResource"
            ],
            "Resource": "*"
        }
    ]
}
```
Copy
Ask AI
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VaporPolicy",
            "Effect": "Allow",
            "Action": [
                "sqs:CreateQueue",
                "sqs:DeleteQueue",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl",
                "sqs:SetQueueAttributes",
                "ssm:DeleteParameter",
                "ssm:DeleteParameters",
                "ssm:PutParameter",
                "ssm:UpdateServiceSetting",
                "wafv2:AssociateWebACL",
                "wafv2:CreateWebACL",
                "wafv2:DeleteWebACL",
                "wafv2:GetWebACL",
                "wafv2:ListResourcesForWebACL",
                "wafv2:TagResource",
                "wafv2:UpdateWebACL"
            ],
            "Resource": "*"
        }
    ]
}
```
It’s probable this list of permissions will change as we add new features to Vapor, which may result in unexpected errors if your policy is not kept up to date.
#### [​](#defining-your-aws-budget) Defining Your AWS Budget
When linking your AWS account to Vapor, it is important to stay informed about your AWS costs. This can be done directly in the AWS Console using the AWS Budgets service. In addition, you can use Vapor’s managed budgets to define your monthly AWS budget in USD, while also configuring multiple alarms directly on the “Team Settings > AWS Accounts” screen of the Vapor UI. At this time, up to five alarms can be configured:
- Actual cost > 85%
- Actual cost > 100%
- Actual cost > 200%
- Actual cost > 500%
- Forecasted cost > 100%
Each alarm can be triggered once per monthly billing period. When an alarm is triggered, the team owner will receive an email, allowing them to act quickly and avoid unexpected charges.
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
## [​](#notification-methods) Notification Methods
### [​](#slack) Slack
In order to receive notifications via Slack, you will need to [create a Slack App](https://api.slack.com/apps) and select the workspace to which the Slack App should be installed.
Once the Slack App has been created, visit the **Incoming Webhooks** settings pane of your App under the “Features” sidebar. Then, activate the Incoming Webhooks feature using the activation switch.
Once activated, you can create a new Incoming Webhook using the **Add New Webhook to Workspace** button. Finally, you should copy the Webhook URL provided by Slack and insert into your team’s [Notifications Settings](https://vapor.laravel.com/app/team/settings/notification-methods). 
## [​](#legal-and-compliance) Legal and Compliance
Our [Terms of Service](https://vapor.laravel.com/terms) and [Privacy Policy](https://vapor.laravel.com/privacy) provide details on the terms, conditions, and privacy practices for using Laravel Vapor.
Was this page helpful?
YesNo
[The Basics](/projects/the-basics)
⌘I
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)