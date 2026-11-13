Source: https://laravel.com/cloud/docs/knowledge-base/managing-robots.md

# Manage robots.txt

Learn how to customize the robots.txt file in Laravel Cloud and manage crawler access for better SEO.

The `robots.txt` file controls which pages and sections of your site search engine crawlers may visit.

To customize the contents of `robots.txt` when your application deploys, add a command to the **Build Commands** section of your environment's deployment settings.

For example, to disallow crawling of any part of your website:

1. Visit your application environment.
2. Open its **Settings** page.
3. In the **Deployments** section of the **Settings** page, add the following to the **Build commands** section:

```shell theme={null}
echo -e "User-agent: *\nDisallow: /" > public/robots.txt
```

## Cloudflare reserved paths and SEO

Laravel Cloud uses Cloudflare's CDN service, which automatically reserves the `/cdn-cgi` path on all hosted domains. This path appears on your domain as `https://www.example.com/cdn-cgi/l/email-protection` and similar endpoints.

Cloudflare generates and manages these `/cdn-cgi` endpoints. You can't modify or customize them.

To exclude these paths from search engine crawling, consider adding the following directive to your `robots.txt` file:

```
Disallow: /cdn-cgi/
```

For more technical details about Cloudflare's CDN endpoints, refer to [Cloudflare's developer documentation](https://developers.cloudflare.com/fundamentals/reference/cdn-cgi-endpoint).
