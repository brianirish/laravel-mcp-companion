# Forge - Servers/Laravel-Vps

*Source: https://forge.laravel.com/docs/servers/laravel-vps*

---

## On this page
- [Introduction](#introduction)
- [Benefits of Laravel VPS](#benefits-of-laravel-vps)
- [Forge Terminal](#forge-terminal)
- [Migrating to Laravel VPS](#migrating-to-laravel-vps)
- [Private networking](#private-networking)
- [Mail ports](#mail-ports)
- [Sudo password reset](#sudo-password-reset)
- [Pricing](#pricing)
Servers
# Laravel VPS
Copy pageCopy page
Learn about Laravel VPS and instant provisioning.
Copy pageCopy page
## [​](#introduction) Introduction
Laravel VPS cuts server provisioning from minutes to seconds. One click gets you a fully configured server optimized for modern applications. All Laravel VPS servers are Ubuntu powered servers that you receive full access to, and are offered through our infrastructure partnership with DigitalOcean.
But Laravel VPS offers more than just speed. It’s one of the most affordable cloud provider options in Forge, making it easier to experiment with new projects or scale existing ones. You’ll also get simplified billing through Forge instead of managing separate charges from multiple providers.
## [​](#benefits-of-laravel-vps) Benefits of Laravel VPS
Using Laravel VPS servers offers several benefits:
- No need to link Forge to external server providers like AWS.
- Provision servers in seconds. External server providers can take over 10 minutes.
- Utilize Laravel VPS integrated terminal, and instantly gain SSH access to your Laravel VPS servers directly from Forge.
- Consolidate billing on Laravel Forge, instead of managing billing via an external server provider and Forge.
- You are only billed for the number of hours your Laravel VPS is provisioned.
## [​](#forge-terminal) Forge Terminal
When using Laravel VPS, you can gain SSH access to the server with a fully-functional terminal directly from Forge. To get started, navigate to any of your servers or sites and click the context menu for the server or site, usually on the right side of the page and represented by three dots. Then, click “Launch terminal”.
Alternatively, you may launch the terminal from any server or site page using the `` Control+` `` keyboard shortcut.
## [​](#migrating-to-laravel-vps) Migrating to Laravel VPS
You can migrate your DigitalOcean servers to Laravel VPS by opening the dropdown menu next to the “Create Site” button in the server’s “Overview” page. Then, click the “Migrate to Laravel VPS” item.
During the migration, Forge will take a snapshot of your DigitalOcean droplet, transfer it to Laravel VPS, and use it to create the new server. Your server’s status will change to “Migrating”.
After the migration is complete, the server’s IP address will be changed and the server network will be reset. Before updating your DNS records to point to the new IP address, make sure you update the server’s network settings by adding other Laravel VPS servers to the server network and updating your firewall rules.
After updating the DNS records and verifying that everything works as expected, you may delete your DigitalOcean droplet from DigitalOcean’s control panel.
Only servers running Ubuntu 24.04 are eligible for migration to Laravel VPS; earlier Ubuntu versions are not supported.
## [​](#private-networking) Private networking
When configuring networking between Laravel VPS servers, you should use the server’s public IP address.
You can find your server’s public IP address on the server’s “Overview” page in the sidebar, under the “Networking” section. Use this IP address when configuring connections between Laravel VPS servers, such as connecting to a dedicated database server or cache server.
## [​](#mail-ports) Mail ports
Mail ports (25, 465, 587) are blocked by default on Laravel VPS servers to prevent abuse. If you need to send email from your server, use an HTTP / API based service like [Resend](https://resend.com), or contact [Laravel Forge support](/docs/support) to request these ports be unblocked.
## [​](#sudo-password-reset) Sudo password reset
To reset the `forge` sudo password for your Laravel VPS server, navigate to your server’s dashboard and click “Settings”. Within the “Danger Zone” section, click the “Reset password” button in the “Reset sudo password” section.
## [​](#pricing) Pricing
Usage is charged in increments of 1 hour blocks. For example, running a server for 5 minutes will be billed as 1 hour of usage.
Free bandwidth is included when using Laravel VPS servers. This is subject to fair usage, and abuse will be blocked. For more information, see our [trust center](https://trust.laravel.com/?product=forge).
Was this page helpful?
YesNo
[Server Types](/docs/servers/types)[PHP](/docs/servers/php)
⌘I