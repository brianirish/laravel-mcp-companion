# Forge - Sites/Ssl

*Source: https://forge.laravel.com/docs/sites/ssl*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationSitesSSL[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)
##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

Sites# SSL

Configure SSL certificates for your sites.

## [​](#overview)Overview

Forge supports installing custom SSL certificates and using Let’s Encrypt to generate free certificates for your websites.

## [​](#let%E2%80%99s-encrypt)Let’s Encrypt

[Let’s Encrypt](https://letsencrypt.org) provides free SSL certificates that are recognized across all major browsers.

If you need to install Let’s Encrypt for multiple domains, you may separate multiple domains using commas.

Because of the Let’s Encrypt renewal process, it is not possible to clone Let’s Encrypt certificates to other sites. You should simply issue a new Let’s Encrypt certificate for that site.

### [​](#renewing-let%E2%80%99s-encrypt-certificates)Renewing Let’s Encrypt Certificates

Forge will **automatically** renew your Let’s Encrypt certificates within 21 days or less before expiration. Renewal will take place at a random day and time to avoid overwhelming the Let’s Encrypt servers.

If something goes wrong while renewing a certificate, Forge will notify the server owner via email.

You must have an active Laravel Forge subscription in order for your Let’s Encrypt certificates to automatically renew.

### [​](#wildcard-subdomain-let%E2%80%99s-encrypt-certificates)Wildcard Subdomain Let’s Encrypt Certificates

To install a Let’s Encrypt certificate with support for wildcard subdomains, you will need to list both the wildcard subdomain and the root domain in your domain list: `*.domain.com, domain.com`. Let’s Encrypt only supports the `dns-01` challenge type when issuing wildcard certificates, so you will need to provide API credentials for your DNS provider.

Forge currently supports the following Let’s Encrypt wildcard DNS providers:

- Cloudflare

- DNSimple

- DigitalOcean

- Linode

- OVH

- Route53

#### [​](#cloudflare-api-token)Cloudflare API Token

If you are using [Cloudflare](https://cloudflare.com) to manage your DNS, your Cloudflare API token must have the `Zone.Zone.Read` and `Zone.DNS.Edit` permissions. In addition, the token must have permissions on **all** zones attached to your Cloudflare account.

#### [​](#cloudflare-universal-ssl-certificates)Cloudflare Universal SSL Certificates

Cloudflare provides [free SSL certificates](https://developers.cloudflare.com/ssl/edge-certificates/universal-ssl/enable-universal-ssl/) to all connected domains and all their first-level subdomains. These certificates are automatically enabled on all domains and subdomains that have Cloudflare’s proxy functionality enabled. However, if you have multiple nested subdomains (e.g. `staging.api.example.com`), this universal certificate will not cover those domains and may cause an `ERR_SSL_VERSION_OR_CIPHER_MISMATCH` error. If your application requires multiple nested subdomains, we recommend you disable Cloudflare proxying and use a traditional SSL certificate for your Forge site.

#### [​](#route53-user-policy)Route53 User Policy

If you are using [Route53](https://docs.aws.amazon.com/Route53/latest/APIReference/Welcome) to manage your DNS, your IAM user must have the `route53:ChangeResourceRecordSets` permission on your domain’s hosted zone. In addition, the user must have the `route53:GetChange` and `route53:ListHostedZones` permissions.

## [​](#circle-permissions)Circle Permissions

You may grant a circle member authority to create and manage SSL certificates by granting the `site:manage-ssl` permission.

Was this page helpful?

YesNo[Redirects](/docs/sites/redirects)[User Isolation](/docs/sites/user-isolation)On this page
- [Overview](#overview)
- [Let’s Encrypt](#let%E2%80%99s-encrypt)
- [Renewing Let’s Encrypt Certificates](#renewing-let%E2%80%99s-encrypt-certificates)
- [Wildcard Subdomain Let’s Encrypt Certificates](#wildcard-subdomain-let%E2%80%99s-encrypt-certificates)
- [Cloudflare API Token](#cloudflare-api-token)
- [Cloudflare Universal SSL Certificates](#cloudflare-universal-ssl-certificates)
- [Route53 User Policy](#route53-user-policy)
- [Circle Permissions](#circle-permissions)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.