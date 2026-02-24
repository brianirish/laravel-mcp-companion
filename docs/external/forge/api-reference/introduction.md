# Forge - Api-Reference/Introduction

*Source: https://forge.laravel.com/docs/api-reference/introduction*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Introduction
Introduction
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)
##### Introduction
- [Introduction](/docs/api-reference/introduction)
- [Pagination](/docs/api-reference/pagination)
- [Rate Limiting](/docs/api-reference/rate-limiting)
- [Filtering & Sorting](/docs/api-reference/filtering)
- [Relationships](/docs/api-reference/relationships)
##### Reference
- Background Processes
- Backups
- Commands
- Databases
- Deployments
- Firewall Rules
- Integrations
- Logs
- Monitors
- Nginx
- Organizations
- Providers
- Recipes
- Redirect Rules
- Roles
- SSH Keys
- Scheduled Jobs
- Security Rules
- Server Credentials
- Servers
- Sites
- Storage Providers
- Teams
- User
On this page
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Headers](#headers)
- [Errors](#errors)
Introduction
# Introduction
Copy page
Introduction to the Laravel Forge API.
Copy page
This documentation is for the new Laravel Forge API. For the legacy API, please refer to the [legacy API documentation](https://forge.laravel.com/api-documentation).
The Laravel Forge API allows you to programmatically interact with your Laravel Forge account and manage your organizations, servers, sites, and other resources.
## [​](#base-url) Base URL
The base URL for the Laravel Forge API is:
Copy
Ask AI
```
https://forge.laravel.com/api
```
## [​](#authentication) Authentication
The Laravel Forge API uses token-based authentication. You can generate an API token from your [Laravel Forge account settings](https://forge.laravel.com/profile/api). Once you have your token, include it in the `Authorization` header of your API requests as follows:
Copy
Ask AI
```
Authorization: Bearer YOUR_API_TOKEN
```
## [​](#headers) Headers
All API requests must include the following headers:
Copy
Ask AI
```
Accept: application/json
Content-Type: application/json
```
## [​](#errors) Errors
The Laravel Forge API uses standard HTTP status codes to indicate the success or failure of an API request. Common status codes include:
| Status Code | Description |
| --- | --- |
| `200` | Success |
| `201` | Created |
| `204` | No content |
| `400` | Bad request |
| `401` | No valid API key was provided. |
| `403` | Forbidden |
| `404` | Not found |
| `422` | Unprocessable entity |
| `429` | Too many requests |
| `500` | Internal server error |
| `503` | Forge is offline for maintenance. |
Was this page helpful?
YesNo
[Pagination](/docs/api-reference/pagination)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.