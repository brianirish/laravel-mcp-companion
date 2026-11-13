Source: https://herd.laravel.com/docs/macos/advanced-usage/social-auth.md

# Social Authentication

# Implementing Social Authentication

When implementing social authentication in your Laravel application, you may face the issue that Herd's `.test`
domain is not recognized by the social authentication providers. This is because they often require a public top-level
domain (TLD) for their callback URLs. Herd does not support changing the `.test` domain to a public TLD, because
that would introduce serious security issues to your machine – but we can work around this.

## Using the fwd.host Webservice

We've created a web service that acts as a proxy for your redirects and does not store any data. You can use this service
to handle social authentication callbacks by setting your callback URLs to `https://fwd.host/http://your-herd-site.test/auth/callback`.

This way, the social authentication provider will redirect to `fwd.host`, which will then forward the request to your Herd site.

You can see the setup in the following screenshot:


The `fwd.host` service will forward the request to your Herd site, allowing you to handle the social authentication as usual.
For security reasons, the redirects are limited to Herd sites with `.test` domains only, so you cannot use this service to redirect to any other site.
