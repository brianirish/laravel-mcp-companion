Source: https://laravel.com/forge/docs/api.md

# API

> Learn how to get started and interact with the Laravel Forge API.

## Introduction

Laravel Forge provides a comprehensive JSON API that allows you to programmatically manage your Forge servers and sites. To learn more, please review the [Forge API documentation](https://forge.laravel.com/docs/api-reference/introduction.md).

The official Laravel Forge [PHP SDK](https://forge.laravel.com/docs/sdk.md) provides an expressive interface for interacting with Forge's API and managing Laravel Forge servers.

## Managing API tokens

### Create a new API token

To create an API token, navigate to your account dashboard and click "API". Click "Create token", provide a name for the token, an optional expiration date, and select the scopes you wish to assign to the token. Finally, click "Add token".

### Delete an API token

To delete an API token, navigate to your account dashboard and click "API". Locate the token you wish to delete, click the action dropdown next to the token, and select "Delete".

> [!WARNING]
>
> Deleting an API token is permanent and cannot be undone. Any applications or services using the deleted token will no longer be able to access the Laravel Forge API.
