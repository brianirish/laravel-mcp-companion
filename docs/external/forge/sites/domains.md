# Forge - Sites/Domains

*Source: https://forge.laravel.com/docs/sites/domains*

---

- [Community](https://discord.gg/laravel)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)

##### Get Started

- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)

##### Basics

- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)

##### Servers

- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)

##### Sites

- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)

##### Resources

- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)

On this page

- [Introduction](#introduction)
- [Forge domains](#forge-domains)
- [Custom domains](#custom-domains)
- [www. redirect types](#www-redirect-types)
- [Wildcard subdomains](#wildcard-subdomains)
- [Primary domains](#primary-domains)
- [Protecting against unconfigured domains](#protecting-against-unconfigured-domains)
- [Certificates](#certificates)
- [Let’s Encrypt](#let%E2%80%99s-encrypt)
- [DNS-01 verification](#dns-01-verification)
- [HTTP-01 verification](#http-01-verification)
- [Custom certificates](#custom-certificates)
- [Cloudflare “Edge” certificates](#cloudflare-%E2%80%9Cedge%E2%80%9D-certificates)
- [Cloning certificates](#cloning-certificates)
- [Legacy sites (created prior to Oct 2025)](#legacy-sites-created-prior-to-oct-2025)
- [Let’s Encrypt](#let%E2%80%99s-encrypt-2)
- [Wildcard subdomain Let’s Encrypt certificates](#wildcard-subdomain-let%E2%80%99s-encrypt-certificates)
- [Cloudflare API token](#cloudflare-api-token)
- [Route53 user policy](#route53-user-policy)

Sites

# Domains

Configure and manage domains and SSL certificates for your sites.

## [​](#introduction) Introduction

Domains let you manage how your site is reached on the web. All Forge sites are assigned a free `on-forge.com` domain for development. But, you can also configure your own custom domains for your sites.

## [​](#forge-domains) Forge domains

Forge provides every site with a free `on-forge.com` domain. These vanity domains are automatically available as soon as a site is created and and receive free HTTPS encryption.
We do not recommend using `on-forge.com` domains in production. They’re best for quick previews, staging environments, or testing with zero DNS configuration.

## [​](#custom-domains) Custom domains

You can attach your own domain names to site in Forge, such as `example.com` or `app.example.com`.
Each custom domain is managed separately, allowing you to create domain-specific certificates, configure `www.` redirect behaviour, and choose one domain to serve as the primary domain.
Custom domains have their own Nginx configuration files and SSL certificates, so adding or removing a domain does not impact other domains on the same site.

### [​](#www-redirect-types) `www.` redirect types

When adding a custom domain to a site, you can decide how Forge should handle the `www.` version of that domain. Options include:

- Redirect from `www.` – traffic to `www.example.com` will permanently redirect to `example.com` (recommended).
- Redirect to `www.` – traffic to `example.com` will permanently redirect to `www.example.com`.
- No redirects – traffic will only be handled for the exact domain configured.

### [​](#wildcard-subdomains) Wildcard subdomains

Forge also supports wildcard domains such as `*.example.com`, which cover all subdomains of a given domain (e.g., `api.example.com`, `blog.example.com`). Wildcards are useful when you need dynamic or catch-all subdomains without adding each one individually.
Allowing wildcard subdomains will still serve traffic for the apex domain (e.g., `*.example.com` will still serve traffic for `example.com`).

### [​](#primary-domains) Primary domains

Each site can designate one domain as the **primary domain**.
Changing the primary domain does not impact your additional custom domains, it is used as the “name” of the site so that it’s easily recognisable inside of Forge and on your server.

Changing the primary domain updates the site’s directory name on the server. This may affect third-party integrations and custom scripts that reference the site directory.Be sure to use Forge’s pre-configured `$FORGE_SITE_PATH` and `$FORGE_RELEASE_DIRECTORY` variables inside of deploy scripts to mitigate these problems.

### [​](#protecting-against-unconfigured-domains) Protecting against unconfigured domains

When provisioning your server, Laravel Forge will automatically create a “catch-all” Nginx configuration for your server at `/etc/nginx/sites-available/000-catch-all`.
This is a special configuration file that is used to stop domains that are not configured on your server from being served. It will respond with a special `444` status code for any request that does not match an already configured domain.

## [​](#certificates) Certificates

Forge manages SSL/TLS certificates on a per-domain basis, allowing you to secure each domain individually without impacting existing domains.
Certificates are required to serve traffic over HTTPS and are automatically renewed where possible. You can choose between free, automated certificates from Let’s Encrypt or provide your own custom certificate.
When an SSL certificate is installed on a domain, Forge automatically configures your server to redirect all HTTP traffic to HTTPS, ensuring your site is always accessed securely.

### [​](#let’s-encrypt) Let’s Encrypt

[Let’s Encrypt](https://letsencrypt.org) provides free SSL certificates that are recognized across all major browsers.
Certificates will be configured to cover the `www.` subdomain and wildcard subdomains (if applicable) and will **automatically** renew within 21 days or less before expiration. Renewal will take place at a random day and time to avoid overwhelming the Let’s Encrypt servers.
If something goes wrong while renewing a certificate, Forge will notify the server owner via email.

You must have an **active Forge subscription** in order for your Let’s Encrypt certificates to automatically renew.

#### [​](#dns-01-verification) DNS-01 verification

The DNS-01 verification method validates domain ownership by creating a `TXT` record containing a temporary token. Let’s Encrypt then queries your domain’s DNS records to look for this token.
Forge simplifies this system through the use of CNAME forwarding. Instead of manually creating `TXT` records or providing API tokens for your chosen DNS provider, you instead create a single `CNAME` record that points to a unique target such as `verify-abcdef.ssl.on-forge.com`.
Let’s Encrypt will follow this `CNAME` and forward requests to the unique `ssl.on-forge.com` subdomain, allowing Forge to automatically manage the underlying `TXT` records. This means you can use DNS-01 verification regardless of your chosen DNS provider.
DNS-01 is our recommended choice because:

- It works for all domain types, including wildcard subdomains (`*.example.com`).
- It is more reliable than HTTP-01 if your site is behind a CDN, firewall, or proxy.
- Long-term maintenance is minimal: once the `CNAME` is created, it remains valid for future renewals – no DNS changes needed.

Removal of the `CNAME` verification record will cause future renewals to fail. This record must remain in place for as long as you wish to use Let’s Encrypt certificates on the domain.

#### [​](#http-01-verification) HTTP-01 verification

The HTTP-01 verification method validates domain ownership by serving a temporary file at `http://your-domain.com/.well-known/acme-challenge`. Let’s Encrypt then requests this file to verify control.

Your domain must resolve to your server and port 80 must be publicly accessible.

HTTP-01 is usually the best choice when:

- You don’t have access to the domain’s DNS records to configure additional records.
- You have strict restrictions around DNS record targets.
- The domain points directly to Forge and you know it won’t be placed behind a CDN, proxy, or firewall later.

While HTTP-01 can be more convenient to setup in limited cases, it is more fragile. **For most domains, we recommend using DNS-01 instead.**

### [​](#custom-certificates) Custom certificates

In addition to Let’s Encrypt, Forge also lets you install your own SSL certificates. This is useful if you use a commercial certificate authority, have an organization-validation (OV) or extended-validation (EV) certificate, or need to reuse an existing certificate across multiple systems.
To use a custom certificate, you’ll need to provide:

- The certificate file, including any intermediate certificates to form the full chain.
- The corresponding private key.

Custom certificates **are not renewed automatically** by Forge. You are responsible for monitoring their expiration and uploa

*[Content truncated for length]*