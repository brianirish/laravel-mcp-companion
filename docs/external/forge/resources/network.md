# Forge - Resources/Network

*Source: https://forge.laravel.com/docs/resources/network*

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
- [Managing server networks and firewalls](#managing-server-networks-and-firewalls)
- [Server networks](#server-networks)
- [Firewall management](#firewall-management)
- [Creating firewall rules](#creating-firewall-rules)
- [Deleting firewall rules](#deleting-firewall-rules)
- [Enhanced security options](#enhanced-security-options)
- [Allow and deny rules](#allow-and-deny-rules)
- [Default firewall configuration](#default-firewall-configuration)
- [Health check service IP addresses](#health-check-service-ip-addresses)
- [Recovering from deleted SSH rules](#recovering-from-deleted-ssh-rules)

Resources

# Network

Copy page

Learn how to manage your server network and firewall.

Copy page

## [​](#introduction) Introduction

Laravel Forge provides comprehensive network management capabilities. This includes firewall configuration and server-to-server connectivity management, allowing you to control traffic flow and establish secure connections between your infrastructure components.

Manually created `ufw` rules on your server won’t appear in the Laravel Forge dashboard. Forge only displays and manages rules created through its interface.

## [​](#managing-server-networks-and-firewalls) Managing server networks and firewalls

### [​](#server-networks) Server networks

Server networks simplify the process of connecting servers for dedicated database, cache, or queue functionality. To establish internal network connections, servers must meet these requirements:

- Created by the same server provider
- Using identical server provider credentials
- Owned by the same user account
- Located within the same geographical region and VPC

Once network access is granted between servers, you can connect using private IP addresses for secure, high-performance internal communication.

## [​](#firewall-management) Firewall management

Laravel Forge provides complete firewall control, allowing you to open specific ports to internet traffic. Common use cases include opening port `21` for FTP services or custom application ports.

### [​](#creating-firewall-rules) Creating firewall rules

To create a firewall rule, navigate to your server’s settings page and click the “Network” tab. Then, click the “Add rule” button. Configure the rule by specifying the port or port range, type, and optionally restrict access to specific IP addresses. Click the “Create rule” button to apply the new firewall configuration.
When creating rules, you can specify port ranges using the format `8000:8010` to open multiple consecutive ports, or provide multiple IP addresses as a comma-separated list for enhanced security.

### [​](#deleting-firewall-rules) Deleting firewall rules

To delete a firewall rule, navigate to your server’s “Network” tab. Then, click on the dropdown next to the rule you want to remove. Click the “Delete” dropdown item and confirm the deletion.
**Warning:** Never delete the SSH rule (typically port 22) as this will prevent Laravel Forge from connecting to and managing your server.

### [​](#enhanced-security-options) Enhanced security options

You can restrict port access to specific IP addresses for additional security. The “From IP Address” field accepts multiple addresses as a comma-separated list: `192.168.1.1,192.168.1.2,192.168.1.3`.

### [​](#allow-and-deny-rules) Allow and deny rules

Configure traffic permissions by selecting allow or deny actions for each rule. Deny rules prevent matching traffic from reaching services and are automatically prioritized above allow rules for proper security enforcement.

New IPv4 deny rules are positioned above existing deny rules for optimal priority handling. IPv6 rules currently don’t support first-priority positioning in UFW.

## [​](#default-firewall-configuration) Default firewall configuration

Laravel Forge automatically configures essential firewall rules during server provisioning:

- **SSH:** Port 22 access from any IP address
- **HTTP:** Port 80 access from any IP address
- **HTTPS:** Port 443 access from any IP address

While port 22 remains open for SSH connections, only SSH key-based authentication is accepted, preventing brute force attacks. **Never delete the SSH rule—doing so will break Forge’s ability to connect to and manage your server.**
Mail ports (25, 465, 587) are blocked by default on Laravel VPS servers to prevent abuse. If you need to send email from your server, use an HTTP / API based service like [Resend](https://resend.com), or contact [Laravel Forge support](/docs/support) to request these ports be unblocked.

### [​](#health-check-service-ip-addresses) Health check service IP addresses

If you have enabled [deployment health checks](/docs/sites/deployments#deployment-health-checks) for your sites, you should ensure that the following IP addresses are allowed through your HTTP and HTTPS firewall rules. Health check requests are made from these addresses to verify your application is accessible after deployments. These IPs will **not make** SSH connections to the server.

- 209.38.170.132
- 206.189.255.228
- 139.59.222.70

Alternatively, you can allow the health check service by its `User-Agent` header value: `Laravel-Healthcheck/1.0`.

### [​](#recovering-from-deleted-ssh-rules) Recovering from deleted SSH rules

If you accidentally delete the SSH firewall rule (typically port 22), Forge loses server connectivity and cannot restore the rule automatically. To resolve this issue:

1. Access your server directly through your cloud provider’s console (such as DigitalOcean’s remote access feature)
2. Connect as the `root` user
3. Restore SSH access by running: `ufw allow 22`

This will re-establish Forge’s connection capability to your server.

Was this page helpful?

YesNo

[Scheduler](/docs/resources/scheduler)[Packages](/docs/resources/packages)

⌘I

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)