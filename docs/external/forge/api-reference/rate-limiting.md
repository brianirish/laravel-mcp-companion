Source: https://laravel.com/forge/docs/api-reference/rate-limiting.md

# Rate Limiting

> Learn about rate limiting in the Laravel Forge API.

The Laravel Forge API implements rate limiting to ensure fair usage and protect against abuse.
The default rate limit is set to **60 requests per minute** per authenticated user.

API responses include the `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` headers to provide information about the rate limit.

## Requesting a higher rate limit

If the default rate limit is insufficient for your workflow, you can request an adjustment by contacting our support team at [forge@laravel.com](mailto:forge@laravel.com). Please include a description of your use-case so we can properly review your request.
