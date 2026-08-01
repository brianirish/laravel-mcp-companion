# Forge - Api

*Source: https://forge.laravel.com/docs/api*

---

## On this page
- [Introduction](#introduction)
- [Managing API tokens](#managing-api-tokens)
  - [Create a new API token](#create-a-new-api-token)
  - [Delete an API token](#delete-an-api-token)
Basics
# API
Copy pageCopy page
Learn how to get started and interact with the Laravel Forge API.
Copy pageCopy page
## [​](#introduction) Introduction
Laravel Forge provides a comprehensive JSON API that allows you to programmatically manage your Forge servers and sites. To learn more, please review the [Forge API documentation](/docs/api-reference/introduction).
The official Laravel Forge [PHP SDK](/docs/sdk) provides an expressive interface for interacting with Forge’s API and managing Laravel Forge servers.
## [​](#managing-api-tokens) Managing API tokens
### [​](#create-a-new-api-token) Create a new API token
To create an API token, navigate to your account dashboard and click “API”. Click “Create token”, provide a name for the token, an optional expiration date, and select the scopes you wish to assign to the token. Finally, click “Add token”.
### [​](#delete-an-api-token) Delete an API token
To delete an API token, navigate to your account dashboard and click “API”. Locate the token you wish to delete, click the action dropdown next to the token, and select “Delete”.
Deleting an API token is permanent and cannot be undone. Any applications or services using the deleted token will no longer be able to access the Laravel Forge API.
Was this page helpful?
YesNo
[Recipes](/docs/recipes)[Managing Servers](/docs/servers/the-basics)
⌘I