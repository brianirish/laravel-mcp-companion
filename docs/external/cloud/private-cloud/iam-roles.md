Source: https://laravel.com/cloud/docs/private-cloud/iam-roles.md

# IAM roles

Give your Private Cloud environments temporary, auto-rotating credentials for an IAM role in your own AWS account.

## Introduction

Laravel Cloud lets you attach an AWS Identity and Access Management (IAM) role from your own AWS account to a Private Cloud environment. Every workload in that environment then receives temporary credentials for that role, including your web instances, queue workers, scheduled tasks, and deployment commands.

You own the role. You control which permissions it grants, and your trust policy controls which Cloud environments may assume it. Cloud never stores or sees a long-lived credential.

This replaces the practice of pasting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` into your environment variables. Static access keys never expire, so you have to rotate them by hand everywhere you have stored a copy, including developer machines and continuous integration pipelines. An IAM role gives your application credentials that expire and rotate automatically.

> [!NOTE]
>
> IAM roles are available only with [Private Cloud](https://laravel.com/cloud/docs/private-cloud). If you don't see the **Integrations** tab in your environment settings, [contact us](https://laravel.com/enterprise).

## Why use an IAM role

Attaching a role changes how your application authenticates with AWS:

* **Nothing static to store.** You keep no long-lived credentials in your environment variables, so there is no key to leak or rotate.
* **Credentials rotate automatically.** AWS issues short-lived credentials to each instance and refreshes them before they expire.
* **You keep control of permissions.** The role lives in your AWS account, so you grant and revoke access without involving Laravel.
* **Scoped to a single environment.** Your trust policy names the exact environment allowed to assume the role, so staging cannot reach production resources.
* **Works with your existing code.** The AWS SDK resolves the role through its default credential chain, so packages such as `league/flysystem-aws-s3-v3` need no changes.

Common uses include reading and writing your own Amazon S3 buckets, querying DynamoDB tables, invoking Amazon Bedrock models, publishing to Amazon SNS topics, and reaching any other AWS service your application depends on.

## Configuring an IAM role

You configure the AWS Role ARN per environment under **Environment > Settings > Integrations**.

**1. Create a role in your AWS account**

In the AWS console, create an IAM role with the **Custom trust policy** option. You will paste the trust policy from Cloud in the next step.

**2. Copy the trust policy from Cloud**

Open **Environment > Settings > Integrations** in Cloud. The **Trust policy** section shows the exact policy your role requires, already populated for this environment. Copy it and use it as the role's trust policy.

**3. Attach the permissions your application needs**

Attach your own permission policies to the role, granting only the AWS actions your application uses. If your environment uses managed queues, also attach the queue policy shown in the **Permissions** section of the same page.

**4. Save the role ARN in Cloud**

Paste the role ARN into the **AWS Role ARN** field and save. Cloud validates the format, so the value must look like `arn:aws:iam::123456789012:role/laravel-cloud`.

**5. Remove any static AWS keys**

Delete `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` from your environment variables. The AWS SDK checks these before it checks the credentials Cloud provides. If you leave them in place, they take precedence and your role never takes effect. You can keep `AWS_REGION` and `AWS_DEFAULT_REGION`, which Cloud honors as usual.

**6. Deploy the environment**

The role takes effect on your next deployment.

For reference, a trust policy for a Private Cloud environment looks like the following. Always copy the version Cloud generates rather than adapting this example, because the principal and external ID are specific to your cluster and environment:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/<cluster-name>-cstmr-wrkld"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<region>/<account-id>/<cluster-name>/env-<uuid>/sa-env-<uuid>"
        }
      }
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/<cluster-name>-cstmr-wrkld"
      },
      "Action": "sts:TagSession"
    }
  ]
}
```

Both statements are required. The `sts:TagSession` statement lets Cloud pass your environment's identity through to your account. That identity is what allows your permission policies to scope themselves to a single environment.

The `sts:ExternalId` value is what limits the role to one environment. Cloud builds it from your region, account, cluster, and environment, and AWS rejects any request that does not carry the exact value you allowed.

### Managed queues

Managed queue workers run inside the same environment and use the same identity as your web instances, so they assume your role too. Cloud's built-in permission to reach your managed queue belongs to Cloud's own role, and your role does not inherit it.

If you configure an IAM role on an environment that uses [managed queues](https://laravel.com/cloud/docs/queues) without granting the role queue access, your queue scales up, but the workers can't receive or delete messages. Jobs accumulate in the queue instead of returning an error.

To avoid this, open the **Permissions** section under **Environment > Settings > Integrations**, expand **Managed queues**, and attach the policy shown there to your role as an inline policy. The policy targets your environment's queue automatically, so you do not need to look up a queue ARN.

### Preview environments

[Preview environments](https://laravel.com/cloud/docs/preview-environments) inherit their settings from the target environment configured on your automation, including the AWS Role ARN. If that target environment has a role configured, every preview environment created from it attempts to assume the same role.

Each preview environment receives its own UUID, and the external ID contains that UUID. A trust policy pinned to a single external ID will therefore reject every preview environment, and your preview instances will fail their AWS calls at runtime rather than at deployment time.

The fix is to widen the trust policy so it accepts any environment on your Private Cloud. Do that on a role built for previews, not on your production role.

Create a second IAM role in your AWS account and give it access only to non-production resources. A preview environment runs the code on an open pull request, so anyone who can open a pull request against your repository can reach whatever that role can reach. Keep production buckets and tables out of it.

Set the preview role on the target environment your automation points at, such as staging. Every preview environment created from that automation inherits the role. Your production environment keeps its own role, with its external ID still pinned to production alone.

On the preview role, remove the `sts:ExternalId` condition from the `sts:AssumeRole` statement:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/<cluster-name>-cstmr-wrkld"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<account-id>:role/<cluster-name>-cstmr-wrkld"
      },
      "Action": "sts:TagSession"
    }
  ]
}
```

Keep the `sts:TagSession` statement, and keep the principal pinned to Cloud's role for your cluster. That principal is unique to your Private Cloud, so only your own dedicated infrastructure can assume the role.

> [!WARNING]
>
> Do not remove the external ID condition from a role your production environment uses. Once that condition is gone, any environment on your Private Cloud can assume the role. That is acceptable for a role scoped to non-production resources, and a poor trade for a role that can reach live customer data.
>
> Only remove the external ID condition on a Private Cloud. On shared infrastructure, the external ID is the only thing that separates your environment from another organization's.

## Verifying your configuration

Deploy the environment, then use whatever part of your application talks to AWS, such as uploading a file to Amazon S3 or dispatching a queued job. If that works, your role is working.

If it fails, your application logs show the AWS error, and the error tells you where to look.
`AccessDenied` on `sts:AssumeRole` means the trust policy is wrong. `AccessDenied` on the service itself, such as `s3:PutObject`, means your role was assumed correctly but is missing that permission.

To rule out the most common problem, open your [environment variables](https://laravel.com/cloud/docs/environments#environment-variables) and confirm that `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` are not defined. Any one of them left in place will shadow your role. Remove them and deploy again. For anything else, review [Troubleshooting](#troubleshooting).

## Troubleshooting

AWS does not validate your trust policy when you configure the role, so a misconfigured role does not fail the deployment. It fails the first time your application calls AWS.

| Symptom | Resolution |
| - | - |
| `AccessDenied` on `sts:AssumeRole` or `sts:TagSession` | Your trust policy is missing a statement or carries the wrong external ID. Copy it from **Environment > Settings > Integrations** again and apply it verbatim |
| The role appears to have no effect | Static AWS keys are still shadowing it. Remove `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`, then deploy |
| Preview environments fail while the target environment works | The trust policy pins a single external ID. Remove that condition, as described in [Preview environments](#preview-environments) |
| Queues scale up but jobs are never processed | Your role is missing the managed queue permissions. Attach the managed queues policy to it |
| Deployment fails with a missing `aws/aws-sdk-php` package error | Your environment uses managed queues but the AWS SDK is not installed. Run `composer require aws/aws-sdk-php` and deploy |

For anything not covered here, [contact us](https://laravel.com/enterprise) with your environment name and the error your application is reporting.
