Source: https://laravel.com/forge/docs/api-reference/introduction.md

# Introduction

> Introduction to the Laravel Forge API.

The Laravel Forge API allows you to programmatically interact with your Laravel Forge account and manage your organizations, servers, sites, and other resources.

## Base URL

The base URL for the Laravel Forge API is:

```
https://forge.laravel.com/api
```

## Authentication

The Laravel Forge API uses token-based authentication. You can generate an API token from your [Laravel Forge account settings](https://forge.laravel.com/profile/api). Once you have your token, include it in the `Authorization` header of your API requests as follows:

```http theme={null}
Authorization: Bearer YOUR_API_TOKEN
```

## Headers

All API requests must include the following headers:

```http theme={null}
Accept: application/json
Content-Type: application/json
```

## Errors

The Laravel Forge API uses standard HTTP status codes to indicate the success or failure of an API request. Common status codes include:

| Status Code | Description |
| -: | :- |
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
