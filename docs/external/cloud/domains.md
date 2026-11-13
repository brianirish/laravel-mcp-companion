Source: https://laravel.com/cloud/docs/domains.md

# Domains

Configure Laravel Cloud domains, connect custom domains, set up DNS, and troubleshoot verification.

Laravel Cloud provides two types of domains for each environment: an automatically assigned `laravel.cloud` domain and any custom domains you connect.

> [!WARNING]
>
> Domain stuck verifying? Read our docs on [verifying domains](https://laravel.com/cloud/docs/knowledge-base/domain-verification).

## Cloud domains

Laravel Cloud assigns each environment a free `laravel.cloud` domain after its first successful deployment. This domain is ideal for testing and staging before switching to your own domain.

Laravel Cloud builds Cloud domains from your application and environment name. If you rename either, the Cloud domain changes, and you need to redeploy for the change to take effect.

Because teams often use Cloud domains for non-production environments, Laravel Cloud automatically sets an `X-Robots-Tag: noindex, nofollow` header on all `*.laravel.cloud` domains so search engines do not index them. Laravel Cloud does not set this header for custom domains.

The [edge network rules](https://laravel.com/cloud/docs/network#cloud-edge-network) you configure for an environment, such as response rules, rate limiting, and firewall settings, apply only to custom domains. Laravel Cloud does not evaluate these rules for requests to Cloud domains.

## Custom domains

A custom domain lets visitors reach your application at your own address (for example, `example.com`) instead of the default `laravel.cloud` domain. Laravel Cloud automatically provisions and renews SSL certificates for each custom domain so visitors reach your site over HTTPS.

### Add a custom domain

In the dashboard, open your environment's **Network settings** and click **Add domain**. Laravel Cloud asks you to choose:

* **Wildcard support**: Whether to accept traffic on all subdomains (for example, `*.example.com`).
* **Redirect behavior**: Whether Cloud should redirect `www.example.com` to `example.com` (or the reverse).
* **Downtime preference**: Whether brief downtime is acceptable during setup, or whether you need an uninterrupted transition with no gaps in service.
* **Cloudflare DNS settings**: Whether Cloudflare manages your DNS and whether the hostname is already proxied (routed through Cloudflare's network).

These choices determine which DNS records Laravel Cloud asks you to add and in what order.

**1. Add the domain in Laravel Cloud**

Enter the domain and choose your options.

**2. (Optional) Pre-verify ownership and SSL**

If you selected the uninterrupted path, add the ownership and SSL validation records first. These records let Laravel Cloud confirm you own the domain and issue an SSL certificate before you switch any traffic over. This option is available only if the hostname is not already proxied through Cloudflare's network.

**3. Point the domain to Laravel Cloud**

Add the origin records shown in the UI. Origin records are the DNS entries that direct your domain's traffic to Laravel Cloud's servers.

**4. Refresh until connected**

Use the Refresh action in the dashboard until the domain status shows as connected. Most domains connect within 15 minutes, but DNS propagation can occasionally take longer.

### Verification paths

Laravel Cloud supports two verification approaches. The right choice depends on whether you can tolerate a brief gap in service while DNS changes take effect:

* **Real-time verification (flexible)**: Point the domain to Laravel Cloud first, and Laravel Cloud then verifies ownership and issues an SSL certificate. This is the simplest path, but there may be a short window where the domain is not yet serving over HTTPS.
* **Pre-verification (uninterrupted)**: Prove ownership and issue the SSL certificate before switching traffic. This path avoids any downtime or insecure window, but requires additional DNS records up front. This path is available only if the hostname is not already proxied through Cloudflare's network.

## DNS records you will see in Cloud

When you open a domain's configuration, Laravel Cloud shows the exact DNS records required for your setup. Copy each record's type, name, and value exactly as shown into your DNS provider.

### Origin records

Origin records are the primary DNS entries that tell the internet to send traffic for your domain to Laravel Cloud:

* An **A** record maps your domain to an IP address and is common when you are not using Cloudflare DNS.
* A **CNAME** record maps your domain to another hostname and is common when you are using Cloudflare DNS (Cloudflare supports CNAME flattening at the apex, which allows a CNAME on the root domain).

### Ownership verification record

During pre-verification, Laravel Cloud may require a temporary TXT record to confirm that you control the domain. This record looks like:

`TXT _cf-custom-hostname.<your-domain> -> <value>`

After Laravel Cloud confirms ownership, you no longer need this record, though leaving it in place does not cause any issues.

### SSL validation records

To issue an SSL certificate for your domain (so your site can use HTTPS), Laravel Cloud may require one or more validation records:

`TXT _acme-challenge.<your-domain> -> <value>`

`CNAME _acme-challenge.<your-domain> -> <value>` (common for wildcard domains or DCV delegation)

If you are using wildcard support, keep the DCV delegation CNAME record in place permanently. This record lets Laravel Cloud automatically renew your wildcard SSL certificate. Removing it prevents future renewals.

## Understanding verification status

A domain is fully connected once Laravel Cloud verifies three components:

* **Hostname**: Ownership of the domain is confirmed.
* **SSL**: An SSL certificate has been issued and is active, so HTTPS works.
* **Origin**: DNS is correctly routing traffic to Laravel Cloud.

As verification progresses, the dashboard shows one of the following statuses:

* **Verifying ownership**: Laravel Cloud is waiting for your ownership and SSL validation DNS records to become visible. This is the propagation stage.
* **Verifying**: Ownership and SSL are confirmed, but origin routing has not been detected yet. Your origin DNS record may still be propagating.
* **Connected**: All three components are verified and your domain is live.
* **Timed out**: Verification did not complete within the allowed window. Review your DNS records for errors and retry.

Laravel Cloud retries verification checks for approximately 12 hours before timing out, so you do not need to re-trigger verification manually during this period.

If you are using real-time verification, visiting your domain in a browser can help Laravel Cloud detect traffic flowing through the network and speed up the final verification step.

## Domain health

After a domain connects, Laravel Cloud keeps checking that the domain still points to Cloud and that its SSL certificate renews. When Cloud finds a problem, it shows an alert on your environment's canvas, marks the domain in your environment's **Network settings**, and sends a [domain alert](#domain-alerts) to your team.

Cloud reads your DNS records but never changes them. Fix any problem at your DNS provider.

### Disconnected domains

Cloud checks the origin record of every connected domain once an hour. Cloud marks a domain as **Disconnected** when it cannot find the domain's A or CNAME record, or when the record resolves somewhere other than Laravel Cloud. The most common causes are a record that was deleted or overwritten at your DNS provider, and a move to new nameservers that did not copy the existing records.

To fix a disconnected domain, restore the origin record shown in the domain's details, then click **Check again**. To re-check every disconnected domain in the environment, click **Check all** in the canvas alert. Cloud also clears the status on its next hourly check once the record resolves correctly. DNS changes can take up to 48 hours to propagate.

### Certificate renewal failures

Cloud renews your SSL certificates automatically. If a renewal fails, Cloud marks the domain with a **Certificate issue**. When Cloud can identify the cause, the alert explains it. Common causes include:

* A CAA record that does not authorize Google Trust Services and Let's Encrypt
* A DNS provider that does not answer CAA lookups from every region
* A missing or proxied `_acme-challenge` delegation record on a [wildcard domain](#wildcard-domains)
* A temporary rate limit from the certificate authority

Once you fix the cause, click **Retry renewal** on the domain. To retry every failed renewal in the environment, click **Retry all** in the canvas alert. Renewal can take a few minutes. If Cloud cannot identify the cause, the alert asks you to [contact support](https://laravel.com/cloud/docs/support).

Your existing certificate keeps serving traffic until it expires. Fix the cause before then so visitors do not see a security warning.

### Domain alerts

When a domain disconnects or a certificate fails to renew, Cloud sends a notification by email and Slack. Each alert includes the affected domain and environment, a link to the domain in the dashboard, and either the record Cloud expects or the certificate's expiry date.

Domain alerts have their own notification category, which you configure for each environment in your [notification settings](https://laravel.com/cloud/docs/notifications#environment).

## Wildcard domains

A wildcard domain (for example, `*.example.com`) lets any subdomain, such as `app.example.com` or `api.example.com`, route to your environment without configuring each one individually. Wildcard domains follow the same verification path as any other domain, determined by your downtime preference.

When you configure a wildcard domain:

* Also configure the root domain `example.com`, so both `example.com` and its subdomains are covered.
* Add the DCV delegation record shown in the UI. This record lets Laravel Cloud continue issuing and renewing wildcard SSL certificates on your behalf.

If Cloudflare manages your DNS, make sure the DCV delegation records under `_acme-challenge` are set to **DNS only** (gray cloud, not proxied). Proxying these records blocks certificate issuance.

## Managing domains

From your environment's domain settings, you can detach and reassign domains between environments in the same organization. You can also set a verified root domain as the primary domain for an environment.

You cannot move or remove a primary domain until you unset it as the primary domain.

## Limitations

Any number of Cloud environments can have a custom domain assigned to them. Each plan includes a number of custom domains across your entire organization:

* **Starter**: 10 custom domains per organization
* **Growth**: 50 custom domains per organization
* **Business**: 250 custom domains per organization
* **Enterprise**: Custom

Laravel Cloud bills additional custom domains beyond your plan's included amount at \$0.25 per domain per month. If you have a special use case that requires many domains (for example, multi-tenant applications), [contact us](https://laravel.com/cloud/docs/support) to discuss raising your limits.

## Troubleshooting

For guided troubleshooting and provider-specific DNS instructions, see the [Domain Verification](https://laravel.com/cloud/docs/knowledge-base/domain-verification) guide. If a connected domain shows as **Disconnected** or has a **Certificate issue**, see [domain health](#domain-health).

### Verify DNS from the terminal

To confirm that your records are publicly visible, run the following commands in your terminal. Replace `example.com` with your actual domain. The examples show both `dig` and `nslookup`, so use whichever is available on your system:

```bash theme={null}
# Which DNS provider is responsible for your domain?
dig NS example.com +short
nslookup -type=NS example.com

# Are your origin records resolving? (use the record type you configured, A or CNAME)
dig A example.com +short
dig CNAME example.com +short
nslookup -type=A example.com
nslookup -type=CNAME example.com

# Is the ownership verification record visible?
dig TXT _cf-custom-hostname.example.com +short
nslookup -type=TXT _cf-custom-hostname.example.com

# Are the SSL validation records visible? (may be TXT or CNAME depending on your setup)
dig TXT _acme-challenge.example.com +short
dig CNAME _acme-challenge.example.com +short
nslookup -type=TXT _acme-challenge.example.com
nslookup -type=CNAME _acme-challenge.example.com
```

If a command returns no output, the record is either missing or has not finished propagating.
