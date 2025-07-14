# Vapor - Projects/Domains

*Source: https://docs.vapor.build/projects/domains*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#7f091e0f100d3f131e0d1e091a13511c1012)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationProjectsDomains[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/vapor)
##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

Projects# Domains

Learn how to manage domains in Laravel Vapor.

## [​](#introduction)Introduction

When using Vapor, each environment is provided a unique vanity domain that you can use to access the environment after it is deployed. However, it’s important to keep in mind that vanity domains are intended for development purposes only and Vapor automatically adds “no-index” headers to responses from these URLs to prevent them from being indexed by search engines.

In addition, these vanity domains will continue to function even when an application is in maintenance mode, allowing you to test your environment before disabling maintenance mode and restoring general access.

While vanity domains are useful during the development process, it’s not recommended to use them for a production environment or share them with the public. Instead, it’s a best practice to use your own custom domain.

## [​](#adding-domains)Adding Domains

You may add a domain that you own to Vapor through Vapor’s domain screen or by using the `domain` CLI command. When adding a domain to Vapor, always add the root domain, even if you plan to serve your application from a subdomain:

CopyAsk AI```
vapor domain example.com

```

Of course, you can review the details of your Vapor domains from the Vapor UI or using the `domain:list` CLI command:

CopyAsk AI```
vapor domain:list

```

## [​](#managing-dns-records)Managing DNS Records

When you add a domain to Vapor, you will be provided with nameservers that you should provide to your domain registrar’s nameserver configuration screen. This will designate Vapor as the entity managing the DNS records for the domain. This also allows Vapor to automatically add and remove DNS records to the domain as needed.

**If you prefer to manage your DNS records on your own**, requesting a certificate or attaching the domain to an environment will require you to **manually create DNS records** via your domain registrar.

### [​](#custom-dns-records)Custom DNS Records

If you have chosen to allow Vapor to manage your DNS records, you can add, update, or DNS records at any time as needed. Vapor provides two ways for you to manage your DNS records: through the Vapor UI’s domain detail screen or via the Vapor CLI. To create a DNS record using the Vapor CLI, you can use the `record` command:

CopyAsk AI```
vapor record example.com A www 192.168.1.1

vapor record example.com A @ 192.168.1.1

vapor record example.com CNAME foo another-example.com

vapor record example.com MX foo "10 example.com,20 example2.com"

```

The `record` command functions as an “UPSERT” operation. If an existing record exists with the given type and name, its value will be updated to the given value. If no record exists with the given type or name, the record will be created.

To delete a record using the Vapor CLI, you can use the `record:delete` command:

CopyAsk AI```
vapor record:delete example.com A www

```

## [​](#requesting-ssl-certificates)Requesting SSL Certificates

Before attaching a domain to an existing Vapor environment, you must have a valid SSL certificate. Vapor offers free, automatically renewing SSL certificates for your Vapor environment through AWS Certificate Manager.

Typically, users choose the “us-east-1” region for their certificate, which is the required certificate region for all environments using API Gateway 1.0. However, environments using API Gateway 2.0 or Application Load Balancers require a certificate in the same region as the project.

You can create a certificate through the Vapor UI’s domain screen or by using the `cert` CLI command:

CopyAsk AI```
vapor cert example.com

```

At this point, no further action is required and your certificate will be validated and issued within minutes.

If you self-manage your domain’s DNS records, Vapor will not be able to automatically update them. In this case, you can obtain the domain’s certificate CNAME record from the Vapor UI’s domain detail screen or by running the vapor `record:list example.com` command. Then, you can update your DNS records at the external domain registrar accordingly.

Please note that some DNS providers will automatically append the domain name to the CNAME name. In these instances, you can remove the domain name from the CNAME name.

You can view the validation status of your certificates on the Vapor UI or by using the `cert:list` CLI command:

CopyAsk AI```
vapor cert:list example.com

```

If you want to delete an old certificate that is not attached to an environment, you can do so through the Vapor UI’s domain detail screen or by using the `cert:delete` CLI command. After running the command, Vapor will prompt you to select the specific certificate you want to delete for the given domain:

CopyAsk AI```
vapor cert:delete example.com

```

## [​](#attaching-domains-to-environments)Attaching Domains To Environments

Once your domain has a valid SSL certificate, you can attach your domain to your environment using the `domain` configuration option in your application’s `vapor.yml` file. When attaching a domain to an environment, you don’t need to include the “www” subdomain:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        domain: example.com
        build:
            - 'composer install --no-dev'

```

During deployment, Vapor will automatically configure the environment to handle requests on this domain. However, due to the nature of AWS CloudFront, custom domains often take 30-45 minutes to become fully active. So, do not worry if your custom domain is not immediately accessible after deployment.

If you self-manage your domain’s DNS records, Vapor will not be able to automatically update them. In this case, you can obtain the domain’s environment CNAME records from the Vapor UI’s domain detail screen or by running the vapor `record:list example.com` command. Then, you can update your DNS records at the external domain registrar accordingly.

### [​](#multiple-domains)Multiple Domains

Vapor allows you to attach multiple domains to a single project. Before doing so, ensure you have a valid certificate for each of the domains. Then, update your application’s `vapor.yml` file to include each domain:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        domain:
            - example1.com
            - example2.com
        build:
            - 'composer install --no-dev'

```

### [​](#wildcard-subdomains)Wildcard Subdomains

You may indicate that a domain should support wildcard subdomains as long as you have a valid certificate for the primary domain. To attach a wildcard domain to an environment, specify `*` as the subdomain:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        domain: '*.example.com'
        build:
            - 'composer install --no-dev'

```

### [​](#multi-level-subdomains)Multi-level Subdomains

Vapor provides support for multi-level subdomains - for example `v1.api.example.com`. To make use of this functionality, a certificate must be requested which explicitly includes the full multi-level subdomain.

The certificate can be requested from the Vapor CLI:

CopyAsk AI```
vapor cert v1.api.example.com

```

It’s also possible to obtain a certificate for a multi-level subdomain from the [Vapor domains dashboard](https://vapor.laravel.com/app/domains) by setting the multi-level subdomain as either the “Domain Name” or any of the “Alternative Names” in the “Advanced Settings” when requesting a certificate.

When the certificate has been issued, you may access your application from your multi-level subdomain by including it in the `domain` section of your `vapor.yml` configuration file and carrying out a full deployment from the Vapor CLI:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        domain: 'v1.api.example.com'
        build:
            - 'composer install --no-dev'

```

Wildcard certificates provided by AWS Certificate Manager can only protect single-level subdomains. As such, it is not possible to access your application via a multi-level subdomain when using only wildcard subdomains. The multi-level subdomain must be explicitly added to your `vapor.yml` file.

## [​](#removing-vanity-domains)Removing Vanity Domains

If you no longer want a vanity domain to be attached to your environment, you may remove it using the `vanity-domain:delete <environment>` commmand:

CopyAsk AI```
vapor vanity-domain:delete production

```
Was this page helpful?

YesNo[Development](/projects/development)[Queues](/resources/queues)On this page
- [Introduction](#introduction)
- [Adding Domains](#adding-domains)
- [Managing DNS Records](#managing-dns-records)
- [Custom DNS Records](#custom-dns-records)
- [Requesting SSL Certificates](#requesting-ssl-certificates)
- [Attaching Domains To Environments](#attaching-domains-to-environments)
- [Multiple Domains](#multipl

*[Content truncated for length]*