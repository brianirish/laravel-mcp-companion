# Forge - Changelog

*Source: https://forge.laravel.com/docs/changelog*

---

[Laravel Forge home page![light logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)![dark logo](https://mintcdn.com/forge-laravel/DhXK7kFkCTo-2V2J/logo/logo.svg?fit=max&auto=format&n=DhXK7kFkCTo-2V2J&q=85&s=a66298a7f876f35c44132183267a2cd6)](https://forge.laravel.com)

Search...

⌘KAsk AI

- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)

Search...

Navigation

Other

Changelog

[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)

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
- [Storage Providers](/docs/storage-providers)
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

- [January 30, 2026](#january-30%2C-2026)
- [January 23, 2026](#january-23%2C-2026)
- [January 16, 2026](#january-16%2C-2026)
- [January 9, 2026](#january-9%2C-2026)
- [December 12, 2025](#december-12%2C-2025)
- [December 5, 2025](#december-5%2C-2025)
- [November 21, 2025](#november-21%2C-2025)
- [November 14, 2025](#november-14%2C-2025)
- [November 7, 2025](#november-7%2C-2025)
- [October 31, 2025](#october-31%2C-2025)
- [October 24, 2025](#october-24%2C-2025)
- [October 17, 2025](#october-17%2C-2025)
- [October 7, 2025](#october-7%2C-2025)

Other

# Changelog

Copy page

New updates and improvements to Laravel Forge.

Copy page

[​](#january-30%2C-2026)

January 30, 2026

Show Improvements (2)

- **MySQL 8.4**: MySQL 8.0 has been replaced with MySQL 8.4, making it the new default MySQL version for newly provisioned servers.
- **Power cycle for Laravel VPS**: You can now power cycle Laravel VPS servers.

Show Fixes (1)

- Resolved an issue with duplicate backup configurations resulting in failed backups.

[​](#january-23%2C-2026)

January 23, 2026

Show Improvements (1)

- **Server configuration UI**: Advanced settings on the server configuration modal now detail which options are included in the advanced settings modal.

Show Fixes (4)

- Log viewer now refreshes after selecting “Delete contents” in the drop down.
- When a site stops using a PHP version, the corresponding PHP-FPM pool configuration and service are removed for that version.
- Isolated users are now given updated SSH keys.
- Fixed a bug causing the PM2 process to fail after changing primary domain on NextJS sites.

[​](#january-16%2C-2026)

January 16, 2026

Show Improvements (1)

- **Hetzner S3**: Hetzner S3 object storage in now available as an option for database backups.

Show Fixes (7)

- Addressed a bug preventing users from scrolling modals across Forge.
- Modals in the create a certificate flow now display properly when using Safari.
- Shared paths are now saving properly after being updated on the settings deployments page.
- Removed access key and secret key required fields from the database backup configuration modal when using EC2 assumed role.
- The tooltip under the deployment script form now displays a tooltip instead of submitting the form.
- Resolved a bug preventing users from setting up Meilisearch servers.
- The directory fields supports using slashes again, allowing users to point to subdirectories.

[​](#january-9%2C-2026)

January 9, 2026

Show Improvements (4)

- **Default branch**: Forge will now automatically select the default branch in a repository in the new site modal.
- **Zero downtime tooltip**: Added a tooltip under deployments clarifying that zero downtime deployment is only supported for new Forge sites.
- **Handling text overflow**: Expanded the Migrate to Forge modal, and enabled multiple lines to prevent text overflow.
- **Rate limit errors**: Forge now differentiates between user and service-driven rate limit errors for LetsEncrypt.

Show Fixes (6)

- The second modal in the “create backup” flow now opens at the top of the page, instead of opening halfway down.
- Resolved Let’s Encrypt modal display issues when using Safari.
- The delete option in the drop-down has been removed from the final domain on sites.
- Resolved a bug leaving SSL certificate renewals stuck in a renewing state.
- Resolved a caching issue preventing the new site modal from appearing after backing out of this flow using the browser back button.
- Users can now delete domains on sites even when there is no primary domain.

[​](#december-12%2C-2025)

December 12, 2025

Show Improvements (2)

- **New heartbeat notification settings**: You can now choose to be notified about failed heartbeats after 30 or 60 minutes.
- **Nginx API endpoints**: Implemented API endpoints to retrieve and update domain Nginx configurations.

Show Fixes (12)

- Let’s Encrypt certificates are no longer renewing prematurely.
- Users without active subscriptions can now access past invoices on the billing page.
- DNS verification now works when the root domain is not authoritative.
- Fixed resized servers not updating to show new specs on the settings page.
- Fixed ARIA attributes for dropdowns to resolve accessibility issues.
- Ensured backup configuration API updates the DB backup script after database removal.
- Fixed the queue worker —force flag UI so the toggle state displays correctly.
- Isolated Users are added to the supervisor sudoers so they can restart background tasks after deployment.
- Aligned git clone authentication behavior between Zero Downtime Deployment and non‑Zero Downtime Deployment site creation.
- Fixed server metrics failures on Hetzner caused by a console error.
- Corrected Let’s Encrypt domain builder so wildcard certificates no longer add an unnecessary www host.
- Restored visibility of Hetzner Intel/AMD (x86) servers in Forge.

[​](#december-5%2C-2025)

December 5, 2025

## [​](#package-manager-support) Package manager support

You may now select your preferred package manager when creating new sites. Select from npm, pnpm, Bun, or Yarn.

![](https://mintcdn.com/forge-laravel/EsEkZvY_b4TWYHCT/images/changelogs/12-5-25/package_manager.png?fit=max&auto=format&n=EsEkZvY_b4TWYHCT&q=85&s=69ce6d1bd25e1d2f32a417cb3012791a)

## [​](#improved-monorepo-support) Improved monorepo support

It’s now possible to configure your application’s “root” directory, making it more convenient to serve applications housed within monorepos.

![](https://mintcdn.com/forge-laravel/EsEkZvY_b4TWYHCT/images/changelogs/12-5-25/root_path.png?fit=max&auto=format&n=EsEkZvY_b4TWYHCT&q=85&s=e8b5b3845c58e577bb35a7ece905f9f8)

Show Improvements (8)

- **Manually update database version**: Added a refresh button on the database page, allowing you to manually sync the database version.
- **Increased FastCGI buffers**: Increased FastCGI buffers and FastCGI buffer size to decrease the chances of exceeding buffer thresholds, triggering a 502 error.
- **Branch details**: Branch details are now visible on the deployments tab and the deployment details page.
- **Deployment logs**: Deployment logs automatically open on the deployment details page after initiating a new deployment.
- **Scheduled job frequency**: The cron expression now displays when hovering over Custom frequency on the scheduled job card.
- **Copy certificate output**: There is now a button to copy the full certificate output in the output modal.
- **Site install automation**: Site installation will trigger the install and build commands automatically.
- **Accessibility**: Dropdowns are now navigable using the arrow keys when opened using the `Tab` key. Additionally, pressing `Esc` closes the dropdown.

Show Fixes (9)

- The add users modal is now properly sized to avoid overlapping.
- Commenting out deployment script macros now works as expected.
- Organizations no longer overlap when switching organizations when using the Safari browser.
- The Let’s Encrypt modal now expands correctly for sites with many domains.
- Users can now view archived servers even when there are no active servers.
- DNS certificates will automatically reuse verification names for the same domain.
- Resolved an error appearing in the console when using (command + K) to open the search feature.
- Resolved a bug preventing some organization owners from removing users.
- Recipe logs now display properly, without collapsing when extensive.

[​](#

*[Content truncated for length]*