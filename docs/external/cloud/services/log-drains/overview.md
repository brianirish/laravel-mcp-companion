Source: https://laravel.com/cloud/docs/services/log-drains/overview.md

# Log drains

Forward your application logs to external destinations with log drains.

## Introduction

Log drains forward your application logs to an external destination in near real time. Draining logs lets you store your logs indefinitely to meet your own retention needs, archive them for compliance, or feed them into your preferred search and observability tooling.

> [!NOTE]
>
> Log drains are available for [Enterprise plan](https://laravel.com/cloud/docs/pricing) customers.

You can add log drains to an environment at any time from the **Environment > Settings > Log Drains** page. Each environment can run up to 5 drains.

## Supported destinations

Laravel Cloud currently supports draining to Amazon S3, with additional destinations planned.

### Amazon S3

Stream logs to an S3 bucket you own. Laravel Cloud authenticates with AWS by assuming an IAM role in your account. Configure the drain with the following properties:

| Property | Description |
| - | - |
| Name | The name of the log drain. |
| Bucket | The name of an existing S3 bucket you own. |
| Region | The AWS region your bucket resides in. |
| IAM role ARN | The ARN of an IAM role Laravel Cloud can assume to write to your bucket. |
| Path prefix (optional) | The prefix to use for the logs in the S3 bucket. |

> [!NOTE]
>
> Create an IAM role that trusts Laravel Cloud and grants write access to the
> specified S3 bucket, then paste the role ARN into the drain configuration. See
> [AWS IAM setup](#aws-iam-setup), or use **View AWS IAM setup** when you
> create or edit a drain on the **Environment > Settings > Log Drains** page
> for environment-specific policies.

#### Path structure

Laravel Cloud writes each log file to a time-partitioned path within your bucket, so logs are organized by environment, delivery time, and stream. By default, Laravel Cloud writes files from the root of the bucket under the environment's identifier:

```text theme={null}
{env-identifier}/{year}/{month}/{day}/{hh}/{mm}/{stream}/{timestamp}-{uuid}.log
```

If you set a path prefix, it replaces the environment identifier. For example, a drain with the path prefix `invoice-app` would write:

```text theme={null}
invoice-app/2026/08/17/05/23/app/1786944216-962d0179-cc98-49cd-8704-20b54f4abc32.log
```

#### AWS IAM setup

Create an IAM role in your AWS account with the **Custom trust policy** entity type. Attach the trust and permissions policies from the following sections, then paste the role ARN into Laravel Cloud. We recommend a dedicated role for each drain. You may reuse the same role across multiple applications and environments if you prefer to manage a single role.

#### Role trust policy

The trust policy allows Laravel Cloud to assume the role. It must include Laravel Cloud's writer role as the principal and your organization's external ID as a condition.

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<laravel-cloud-account-id>:role/laravel-cloud-log-drain-writer"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "laravel-cloud-organization:<organization-identifier>"
        }
      }
    }
  ]
}
```

Use **View AWS IAM setup** in the log drain configuration page for the exact external ID for your organization.

#### Permissions policy

The permissions policy grants the access a drain needs to write objects to your bucket:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLogDrainBucketCheck",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::my-log-bucket"
    },
    {
      "Sid": "AllowLogDrainObjectWrite",
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::my-log-bucket/optional-prefix/*"
    }
  ]
}
```

Use **View AWS IAM setup** on the log drain configuration page to copy a policy with your bucket, path prefix, and environment identifier already filled in.

If you reuse a single role across multiple applications and environments, paste the same role ARN into each drain.

If those drains share a bucket, replace the `PutObject` resource so it covers every prefix they write to. You may grant write access to the entire bucket:

```json theme={null}
{
  "Sid": "AllowLogDrainObjectWrite",
  "Effect": "Allow",
  "Action": ["s3:PutObject"],
  "Resource": "arn:aws:s3:::my-log-bucket/*"
}
```

Or list only the prefixes you want the role to write to:

```json theme={null}
{
  "Sid": "AllowLogDrainObjectWrite",
  "Effect": "Allow",
  "Action": ["s3:PutObject"],
  "Resource": [
    "arn:aws:s3:::my-log-bucket/invoice-app/*",
    "arn:aws:s3:::my-log-bucket/billing-app/*"
  ]
}
```

If a drain does not set a path prefix, use the environment identifier from that drain's IAM setup policy in the resource list.

If those drains write to different buckets, include each bucket in both the `ListBucket` and `PutObject` resources:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLogDrainBucketCheck",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::invoice-app-logs",
        "arn:aws:s3:::billing-app-logs"
      ]
    },
    {
      "Sid": "AllowLogDrainObjectWrite",
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": [
        "arn:aws:s3:::invoice-app-logs/*",
        "arn:aws:s3:::billing-app-logs/*"
      ]
    }
  ]
}
```

## Pricing

Laravel Cloud bills log drains for the time each drain runs and the volume of data it processes. For rates and a worked billing example, see [Log Drains Pricing](https://laravel.com/cloud/docs/services/log-drains/pricing).
