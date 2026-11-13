Source: https://laravel.com/cloud/docs/knowledge-base/domain-verification.md

# Domain Verification

Learn how to add, validate, and verify custom domains on Laravel Cloud.

When you add a custom domain to Laravel Cloud, Cloud needs to confirm that you own the domain and that your DNS records are set up correctly. This process is called verification. Occasionally, verification may appear stuck or time out entirely. The usual cause is a DNS record that is misconfigured or has not finished propagating. Propagation is the process by which DNS changes spread across the internet.

## Before you start

Add your records at the provider that serves DNS for your domain. That provider is not always where you purchased the domain. For example, if you registered at GoDaddy but pointed your nameservers to Cloudflare, you must add records in Cloudflare. Run the following command to check:

```bash theme={null}
dig NS example.com +short
```

The output lists nameserver hostnames (for example, `anna.ns.cloudflare.com`). Add your Laravel Cloud records at the provider that owns those nameservers.

## Add your DNS records

Add **all** records Laravel Cloud shows, including `www` and wildcard records if they are enabled. Pre-verification proves ownership and issues the SSL certificate before you switch traffic. If you chose pre-verification, Cloud also shows an ownership verification record and SSL validation records. Record names and values must match exactly. Even small differences, such as extra dots or missing prefixes, cause verification to fail.

### Enter only the subdomain

Most DNS providers have a host or name field that expects only the subdomain portion of a record name, not the full domain. Your provider appends the domain automatically:

* For `www.example.com`, enter `www`
* For `_cf-custom-hostname.example.com`, enter `_cf-custom-hostname`
* For `_acme-challenge.example.com`, enter `_acme-challenge`
* For `example.com` itself, most providers use `@` or leave the host blank

If you paste the full name into this field, your provider adds the domain twice and produces `_cf-custom-hostname.example.com.example.com` instead of `_cf-custom-hostname.example.com`.

After saving a record, re-open it in your provider's dashboard and confirm the assembled name matches exactly what Laravel Cloud shows. Re-opening the record is the most effective way to catch formatting mistakes early.

### Domain control validation records

Some domains need a domain control validation (DCV) delegation record. This record is a CNAME named `_acme-challenge` that points to Cloudflare. Laravel Cloud uses it to issue and renew your SSL certificates. Laravel Cloud shows this record when:

* The domain is a wildcard domain (such as `*.example.com`), or belongs to a domain with a wildcard enabled, including its `www` domain
* You chose **Cloudflare DNS and Proxy** for the domain, because your Cloudflare proxy would otherwise answer certificate validation requests before they reach Laravel Cloud

Add the record at your DNS provider like any other record, and keep it in place after verification. Removing it prevents your certificate from renewing.

### Provider-specific instructions

> [accordion] Cloudflare
>
> **1. Open your domain in Cloudflare**
>
> In Cloudflare, select your website and open **DNS**. Confirm you are editing DNS records in the correct Cloudflare account and zone.
>
> **2. Add the origin record(s) from Laravel Cloud**
>
> In Laravel Cloud, open your domain's configuration and copy the **origin** records. These records tell Cloudflare where to send traffic for your domain.
>
> For the record name in Cloudflare:
>
> * Use `@` for the root domain (for example, `example.com`)
> * Use `www` for `www.example.com`
> * Use `*` for `*.example.com` (wildcards), if shown
>
> For proxy status (the orange or gray cloud icon in Cloudflare):
>
> * Origin records are typically safe to proxy (orange cloud) if you selected a Cloudflare proxy option in Laravel Cloud.
> * If you are unsure, start with the proxy status Laravel Cloud recommends in the UI.
>
> **3. Add the pre-verification TXT record (if shown)**
>
> If Laravel Cloud shows an ownership verification record like `_cf-custom-hostname.example.com`, add it as a **TXT** record named `_cf-custom-hostname`.
>
> **4. Add SSL validation records (if shown)**
>
> Laravel Cloud may show `_acme-challenge` records used to issue your domain's SSL certificate. Copy them exactly as shown.
>
> If an `_acme-challenge` record is a **CNAME**, such as a [DCV delegation record](#domain-control-validation-records), keep it set to **DNS only** (gray cloud) at all times. If you proxy it, Laravel Cloud cannot issue or renew the SSL certificate.
>
> If you are pre-verifying your domain and see Cloudflare-related verification errors, you may need to set the hostname's record to **DNS only** until verification completes. You can re-enable the proxy afterward.

> [accordion] Amazon Route 53
>
> Unlike most providers, Route 53 accepts fully qualified record names, so you can paste the complete name from Laravel Cloud (for example, `_cf-custom-hostname.example.com`) directly into the name field. Route 53 may add a trailing dot (for example, `_cf-custom-hostname.example.com.`). The trailing dot is standard DNS formatting and is expected.
>
> If you are not sure you are editing the correct hosted zone, confirm that the nameservers from the [`dig NS` check](#before-you-start) match the nameservers listed in your Route 53 hosted zone.

> [accordion] GoDaddy
>
> GoDaddy's DNS editor calls the subdomain field **Host**. After saving, GoDaddy displays the full record name, so you can confirm there that it matches Laravel Cloud exactly, with no repeated or missing parts.

> [accordion] Namecheap
>
> Namecheap's DNS editor calls the subdomain field **Host**. For root-domain records, which are records for `example.com` itself, use `@` as the host value.

> [accordion] Squarespace and Google Domains
>
> Squarespace (which acquired Google Domains) has its own naming conventions, but the subdomain rule applies to any name or host field. For a wildcard `*.example.com`, enter `*`.

## Verification timeline

Most domains verify within 15 minutes once the correct DNS records are publicly visible. Propagation can take longer depending on your DNS provider and the record's TTL (time-to-live). The TTL controls how long resolvers cache DNS results before refreshing them.

Laravel Cloud automatically retries verification checks for approximately 12 hours. If verification still cannot complete after that period, the domain times out. You may then need to correct your DNS records and retry.

## Check your records in the terminal

You can verify that your DNS records are publicly visible by running `dig` commands in your terminal. Replace `example.com` with your actual domain:

```bash theme={null}
# Which DNS provider is responsible for your domain?
dig NS example.com +short

# Are your origin records (the records that point traffic to Laravel Cloud) resolving?
dig A example.com +short
dig CNAME example.com +short

# Is the ownership verification record visible?
dig TXT _cf-custom-hostname.example.com +short

# Are the SSL validation records visible? (may be TXT or CNAME depending on your setup)
dig TXT _acme-challenge.example.com +short
dig CNAME _acme-challenge.example.com +short
```

If any command returns no output, that record is either missing or has not finished propagating.

## Common verification issues

### Missing `www` records when redirects are enabled

Laravel Cloud's **Redirect from [www](http://www).** setting is enabled by default and is the recommended configuration. When the setting is enabled, Laravel Cloud validates both `example.com` and `www.example.com`, so both hostnames need DNS records.

If you added records only for `example.com` and skipped `www`, verification can fail. Make sure you added records for both hostnames exactly as shown in the domain configuration screen.

### Records have propagated but the domain is still verifying

If your records look correct when checked with `dig` or an external DNS tool, but the domain is still showing as **Verifying** or **Timed out** in Laravel Cloud, our network provider (Cloudflare) may have flagged the domain for manual review. Cloudflare can flag your domain even if it is not hosted on Cloudflare, because Laravel Cloud uses Cloudflare's infrastructure to manage SSL certificates and routing.

Cloudflare's automated systems occasionally flag domains over potential abuse concerns. Some of these flags are false positives, and resolving them requires intervention on the Cloudflare side. If you believe a flag is affecting your domain, [contact support](#when-to-contact-support) so the team can help.

## When to contact support

If your domain is still stuck after working through this guide, contact support through the **Help** portal in your Laravel Cloud dashboard. To help the team diagnose the issue quickly, include:

* Your domain name
* Screenshots of the DNS records as they appear in your DNS provider's dashboard
* The output from the commands in [Check your records in the terminal](#check-your-records-in-the-terminal)
