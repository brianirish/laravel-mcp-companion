Source: https://laravel.com/forge/docs/storage-providers.md

# Storage Providers

> Learn about the storage providers supported by Laravel Forge for database backups.

## Introduction

Storage providers allow Laravel Forge to store your database backups on external object storage services. Once configured, a storage provider can be reused across multiple servers and backup configurations within your organization.

Storage providers are configured and managed within the [organization's](https://forge.laravel.com/docs/organizations.md) settings.

## Supported providers

Laravel Forge supports the following storage providers:

* [Amazon S3](https://aws.amazon.com/s3/)
* [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces)
* [Hetzner](https://www.hetzner.com/storage/object-storage/)
* [Scaleway](https://www.scaleway.com/en/object-storage/)
* [OVH Cloud](https://www.ovhcloud.com/en/public-cloud/object-storage/)
* Custom (S3 Compatible)

> [!NOTE]
>
> Not all providers are 100% compatible with Amazon S3's API. Some providers, such as OVH and Scaleway, require a custom configuration to work correctly, typically through the use of `awscli-plugin-endpoint`.

## Managing storage providers

### Adding a storage provider

To add a storage provider, navigate to the organization's settings. Then, on the "Storage providers" page, click "Add provider". Select the provider you wish to configure and provide the required credentials.

For Amazon S3, DigitalOcean Spaces, Hetzner, Scaleway, and OVH Cloud, you need to provide:

* A name for the storage provider
* The region your backups should be stored in (`eu-west-2`, `nyc3`, etc.)
* The access and secret keys that should be used to connect to the storage service

When using a custom, S3 compatible provider, you must supply:

* The service endpoint or URL
* The access and secret keys that should be used to connect to the storage service

You may also provide a default bucket and storage directory. These values can be overridden when creating a [backup configuration](https://forge.laravel.com/docs/resources/database-backups.md).

### Using EC2 assumed roles

When using Amazon S3 in combination with an EC2 server, you can choose to use the identity of the EC2 server to stream the backup to S3 without providing credentials. To use this option, enable the "Use EC2 Assumed Role" toggle when creating the storage provider.

> [!WARNING]
>
> When using Amazon S3 to store your database backups, your AWS IAM user must have the following permissions for S3:
>
> * `s3:PutObject`
> * `s3:GetObject`
> * `s3:ListBucket`
> * `s3:DeleteObject`

### Editing storage providers

To edit a storage provider, navigate to the organization's settings. Then, on the "Storage providers" page, click the dropdown menu on the provider and click "Edit". You can update any of the configuration options, including credentials.

### Deleting storage providers

To delete a storage provider, navigate to the organization's settings. Then, on the "Storage providers" page, click the dropdown menu on the provider and click "Delete".

> [!WARNING]
>
> Storage providers cannot be deleted while they are in use by one or more backup configurations. You must first update or delete those backup configurations before removing the storage provider.

## Team permissions

The ability to manage storage providers is controlled by the `storage:manage` permission.
