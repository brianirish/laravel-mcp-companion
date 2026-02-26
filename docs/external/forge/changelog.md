# Forge - Changelog

*Source: https://forge.laravel.com/docs/changelog*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Other
Changelog
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
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
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [February 20, 2026](#february-20-2026)
- [February 13, 2026](#february-13-2026)
- [February 6, 2026](#february-6-2026)
- [January 30, 2026](#january-30-2026)
- [January 23, 2026](#january-23-2026)
- [January 16, 2026](#january-16-2026)
- [January 9, 2026](#january-9-2026)
- [December 12, 2025](#december-12-2025)
- [December 5, 2025](#december-5-2025)
- [November 21, 2025](#november-21-2025)
- [November 14, 2025](#november-14-2025)
- [November 7, 2025](#november-7-2025)
- [October 31, 2025](#october-31-2025)
- [October 24, 2025](#october-24-2025)
- [October 17, 2025](#october-17-2025)
- [October 7, 2025](#october-7-2025)
Other
# Changelog
Copy page
New updates and improvements to Laravel Forge.
Copy page
[​](#february-20-2026)
February 20, 2026
## [​](#npm-private-packages) npm private packages
You can now configure npm credentials at the server and site levels to install private packages during deployments. Forge manages the
`.npmrc` configuration automatically, supporting scoped registries like GitHub Packages and custom registries.
Show Improvements (2)
- **Vultr VX1 servers**: Added support for Vultr VX1 server types when provisioning servers.
- **Server unlinking**: Added the ability to unlink a server directly from the delete server modal.
Show Fixes (6)
- Fixed SSL certificates displaying incorrect expiry dates.
- Resolved an issue preventing recipes from being unselected after selection.
- Fixed wildcard domains being treated as literal values on legacy sites, causing site path and Nginx configuration conflicts.
- Resolved storage provider credential fields being autofilled by the browser.
- Fixed duplicated heartbeat notifications.
- Fixed the add server to network modal layout issues.
[​](#february-13-2026)
February 13, 2026
## [​](#mysql-9-x-support) MySQL 9.x support
MySQL 9 is now available as a database option when provisioning new servers.
Show Fixes (4)
- Resolved an issue with Laravel VPS servers that do not have a private hostname.
- Fixed an issue preventing the creation of scheduled jobs.
- Fixed Aikido not finding the correct workspace.
- Resolved an issue with database syncing creating duplicate entries.
[​](#february-6-2026)
February 6, 2026
## [​](#openclaw-server-type) OpenClaw server type
You can now create OpenClaw servers on Laravel VPS.
Show Improvements (2)
- **Command palette filtering**: Improved the accuracy of command filtering.
- **Server list**: Displayed the OS version in the server list.
Show Fixes (1)
- Resolved an issue preventing the delivery of email notifications when a scheduled job’s heartbeat is in a failing state.
[​](#january-30-2026)
January 30, 2026
Show Improvements (2)
- **MySQL 8.4**: Updated the default MySQL version for newly provisioned servers from MySQL 8.0 to MySQL 8.4.
- **Power cycle for Laravel VPS**: Added the ability to power cycle Laravel VPS servers.
Show Fixes (1)
- Resolved an issue with duplicate backup configurations resulting in failed backups.
[​](#january-23-2026)
January 23, 2026
Show Improvements (1)
- **Server configuration UI**: Improved the server configuration modal to clarify which options are included in advanced settings.
Show Fixes (4)
- Fixed the log viewer to refresh after selecting “Delete contents” in the dropdown.
- Removed the corresponding PHP-FPM pool configuration and service when a site stops using a PHP version.
- Updated SSH keys for isolated users.
- Fixed a bug causing the PM2 process to fail after changing primary domain on NextJS sites.
[​](#january-16-2026)
January 16, 2026
Show Improvements (1)
- **Hetzner S3**: Hetzner S3 object storage is now available as an option for database backups.
Show Fixes (7)
- Fixed a bug preventing users from scrolling modals across Forge.
- Fixed display issues in the create certificate flow when using Safari.
- Fixed shared paths so updates save properly on the deployment settings page.
- Removed access key and secret key required fields from the database backup configuration modal when using EC2 assumed role.
- Fixed the tooltip under the deployment script form so it opens the tooltip instead of submitting the form.
- Resolved a bug preventing users from setting up Meilisearch servers.
- Fixed the directory fields to support slashes again, allowing users to point to subdirectories.
[​](#january-9-2026)
January 9, 2026
Show Improvements (4)
- **Default branch**: Added automatic default branch selection in the new site modal.
- **Zero downtime tooltip**: Added a tooltip under deployments clarifying that zero downtime deployment is only supported for new Forge sites.
- **Handling text overflow**: Expanded the Migrate to Forge modal, and enabled multiple lines to prevent text overflow.
- **Rate limit errors**: Improved LetsEncrypt rate limit errors by differentiating user-driven and service-driven failures.
Show Fixes (6)
- Fixed the second modal in the “create backup” flow to open at the top of the page instead of halfway down.
- Resolved Let’s Encrypt modal display issues when using Safari.
- Removed the delete option from a site’s final domain in the dropdown.
- Resolved a bug leaving SSL certificate renewals stuck in a renewing state.
- Resolved a caching issue preventing the new site modal from appearing after backing out of this flow using the browser back button.
- Fixed domain deletion so users can delete domains even when no primary domain is set.
[​](#december-12-2025)
December 12, 2025
Show Improvements (2)
- **New heartbeat notification settings**: Added 30-minute and 60-minute options for failed heartbeat notifications.
- **Nginx API endpoints**: Implemented API endpoints to retrieve and update domain Nginx configurations.
Show Fixes (12)
- Fixed premature Let’s Encrypt certificate renewals.
- Restored access to past invoices on the billing page for users without active subscriptions.
- Fixed DNS verification when the root domain is not authoritative.
- Fixed resized servers not updating to show new specs on the settings page.
- Fixed ARIA attributes for dropdowns to resolve accessibility issues.
- Fixed the backup configuration API to update the DB backup script after database removal.
- Fixed the queue worker —force flag UI so the toggle state displays correctly.
- Added isolated users to supervisor sudoers so they can restart background tasks after deployment.
- Aligned git clone authentication behavior between Zero Downtime Deployment and non‑Zero Downtime Deployment site creation.
- Fixed server metrics failures on Hetzner caused by a console error.
- Corrected Let’s Encrypt domain builder so wildcard certificates no longer add an unnecessary www host.
- Restored visibility of Hetzner Intel/AMD (x86) servers in Forge.
[​](#december-5-2025)
December 5, 2025
## [​](#package-manager-support) Package manager support
You may now select your preferred package manager when creating new sites. Select from npm, pnpm, Bun, or Yarn.
## [​](#improved-monorepo-support) Improved monorepo support
It’s now possible to configure your application’s “root” directory, making it more convenient to serve applications housed within monorepos.
Show Improvements (8)
- **Manually update database version**: Added a refresh button on the database page, allowing you to manually sync the database version.
- **Increased FastCGI buffers**: Increased FastCGI buffers and FastCGI buffer size to decrease the chances of exceeding buffer thresholds, triggering a 502 error.
- **Branch details**: Branch details are now visible on the deployments tab and the deployment details page.
- **Deployment logs**: Deployment logs automatically open on the deployment details page after initiating a new deployment.
- **Scheduled job frequency**: The cron expression now displays when hovering over Custom frequency on the scheduled job card.
- **Copy certificate output**: Added a button to copy the full certificate output in the output modal.
- **Site install automation**: Site installation will trigger the install and build commands automatically.
- **Accessibility**: Dropdowns are now navigable using the arrow keys when opened using the `Tab` key. Additionally, pressing `Esc` closes the dropdown.
Show Fixes (9)
- Fixed sizing for the Add Users modal to prevent overlapping.
- Fixed deployment script macros so commented lines work as expected.
- Fixed overlapping organizations when switching organizations in Safari.
- Fixed the Let’s Encrypt modal to expand correctly for sites with many domains.
- Restored archived server visibility when no active servers exist.
- Updated DNS certificates to automatically reuse verification names for the same domain.
- Resolved an error appearing in the console when using (command + K) to open the search feature.
- Resolved a bug preventing some organization owners from removing users.
- Fixed recipe logs so long output no longer collapses unexpectedly.
[​](#november-21-2025)
November 21, 2025
## [​](#provision-aws-servers-with-ebs-gp3) Provision AWS servers with EBS gp3
You can now provision an AWS server with EBS GP3. GP2 will remain the default for already provisioned AWS servers. All new servers will be provisioned with EBS gp3.To move your existing servers from gp2 to gp3, visit your AWS dashboard.
Show Improvements (8)
- **Recipes search results**: Updated the recipe search UI to accurately show that a search returned zero matching results, instead of displaying “no recipes”.
- **Manual certificate renewal**: Added manual certificate renewal for Let’s Encrypt certificates after a failed attempt on the Domains tab.
- **Site notes**: Added site notes in the Settings tab, similar to notes on servers.
- **Accessibility improvements**: Improved color contrast and form labeling across the platform.
- **Scheduled jobs paths**: Added copy support for scheduled job paths in the scheduler.
- **Clone certificate endpoint**: Added an API endpoint to clone certificates. This mirrors functionality already available in the Forge UI.
- **Copy debug info**: Added the site path to the information included in the copy debug info action.
- **Destructive commands**: Added a confirmation step when attempting to run destructive commands.
Show Fixes (14)
- Resolved a bug causing the Used Memory monitor to display “unknown” after being installed.
- Fixed scheduled jobs to display the next expected run time instead of always showing UTC.
- Fixed a z-index issue on the domain dropdown in the Let’s Encrypt modal.
- Fixed a bug causing Forge to re-add server’s SSH key to the source control provider when creating a site with a deploy key.
- Restored site logs in the Observe tab when Custom and Other are selected in the Framework setting.
- Fixed organization-level permissions so users with the Viewer role are not shown settings they cannot edit.
- Fixed Hetzner server sizes and prices to display accurate values during provisioning.
- Added a current-directory placeholder to the new scheduled job modal.
- Fixed onboarding state so users see the billing button in the admin dashboard instead of a subscribe prompt.
- Added the Sync Database button for server types other than Database.
- Expanded the log file dropdown to accommodate longer options.
- Updated backup configuration to ensure deleted databases are shown for removal.
- Resolved a bug causing database backups with the server database driver set to MariaDB to fail.
- Laravel VPS servers are now displayed in the drop-down when configuring a load balancer.
[​](#november-14-2025)
November 14, 2025
## [​](#introducing-support-for-postgresql-18) Introducing support for PostgreSQL 18
Forge now offers support for PostgreSQL 18 when provisioning new servers, including Laravel VPS servers.
Show Improvements (4)
- **Sync network rules**: Added automatic UFW rule syncing with Forge, including adding missing rules and removing orphaned rules.
- **Toggle certificates via API**: Added API support for enabling and disabling existing certificates.
- **Improved validation errors**: Validation errors for required fields are now easier to identify.
- **Improved Composer credential validation**: Added context to clarify how fields should be formatted when adding Composer credentials.
Show Fixes (4)
- Fixed a bug causing the Update Site API endpoint to reset other keys.
- Fixed a z-index issue on site deployment pages.
- Fixed an issue in Forge’s API `project_type` match statement causing HTTP 500 errors.
- Resolved reliability issues when adding and removing domains on sites with many domains.
[​](#november-7-2025)
November 7, 2025
## [​](#ssl-certificate-information) SSL Certificate Information
We have made several improvements to the SSL certificate UI.You can now see relevant domains, status, issue date, and expiration date on the certificate card under Certificates, on the Domains tab.Details about why the most recent attempt to renew or issue a certificate failed are now easily accessible in the View Output option.Multiple domains sharing a certificate can be copied all at once by clicking on the domains listed in the card details. [Learn more](https://forge.laravel.com/docs/sites/domains)
Show Improvements (5)
- **Deployment error handling**: Improved deployment error output to make troubleshooting easier.
- **Firewall rule order**: Updated the order that firewall rules display to mirror UFW order on the server.
- **Command palette**: Added support for command/control + click in the command palette to open multiple selections at once.
- **API command output**: Added Forge API support for fetching command outputs.
- **Update Ubuntu records**: Added a manual update option for Forge’s Ubuntu records in server overview details.
Show Fixes (4)
- Fixed health check URLs to update automatically when the primary domain changes.
- Resolved a bug causing the deploy button to be unresponsive on the Deployments tab.
- Added validation for certificate field uploads in the existing certificate upload modal.
- Fixed a bug causing site and server details to display over the navigation bar.
[​](#october-31-2025)
October 31, 2025
## [​](#deployment-pipeline-improvements) Deployment Pipeline Improvements
We have made several improvements to the deployment pipeline to better recover from failed deployments and timeouts.Deployments will now always use the version of PHP configured on the site, even when calling `php` inside `composer.json` and `package.json` files. Notably, this fixes issues using Laravel Wayfinder during deployments.
## [​](#site-command-improvements) Site Command Improvements
Commands now correctly use the version of PHP configured for the site.
## [​](#reset-forge-sudo-password) Reset Forge Sudo Password
It is now possible to reset the `forge` sudo password for Laravel VPS servers.
Show Improvements (7)
- **Tag API servers and sites**: Added support for tagging servers and sites during API creation.
- **Disk usage metric updates**: Added the disk usage metric to the server Overview.
- **Increased command palette results**: Increased command palette results to 10 for servers, sites, and recipes.
- **VAT ID improvements**: Improved VAT ID entry for EU countries.
- **Searchable team members**: Added member search on the team members page.
- **Improved Octane and Reverb port selection**: Forge now suggests the next available port.
- **Select all text**: Added support for selecting all text within the UI.
Show Fixes (7)
- Fixed sudo mode so it enables correctly when restoring database backups.
- Fixed background process validation for sites and servers.
- Fixed the command palette hotkey display so ⌘ is not shown for Windows and Linux users.
- Fixed monitoring notifications to link to the correct location.
- Resolved a 404 when unsharing resources from teams.
- Restored MariaDB 11.4 installation support.
- Fixed invitation acceptance flow so invitations can be accepted at all times.
[​](#october-24-2025)
October 24, 2025
## [​](#improved-mobile-experience) Improved Mobile Experience
We’ve improved the mobile experience for the following features: dropdowns, modals, notification center, tables, and breadcrumbs.
## [​](#reintegrated-aikido-for-sites) Reintegrated Aikido for Sites
When Aikido is enabled at the organization level (via the Integrations page), it activates Aikido features for all sites owned by that organization.
Sites under that organization can then individually opt in to Aikido, enabling security scans and syncing results from Aikido’s API. This ensures a consistent setup while maintaining per-site control. [Learn more about our Aikido integration](https://forge.laravel.com/docs/integrations/aikido#aikido)
Show Improvements (10)
- **Improved search results**: Archived servers have been removed from the command palette.
- **Improved navigation**: Linked overview page section titles to their corresponding pages.
- **Subdomain aliases**: Added support for retroactively enabling and disabling wildcards on domains.
- **Pagination and search**: Improved command palette searchability across pages.
- **Let’s Encrypt controller validation**: Added domain-wide validation in the controller to avoid errors.
- **Restored databases**: Added a sudo mode requirement (password confirmation) when restoring databases.
- **Site repository updates**: Added support for changing site Git repositories and branches.
- **New metric**: Added disk usage visibility for Laravel VPS.
- **Site queue workers**: Added site queue workers to Background Processes at the server level.
- **EOL Ubuntu versions**: Improved handling of servers running EOL Ubuntu versions.
Show Fixes (8)
- Fixed visibility of Add Server and Add Recipe buttons for all users.
- Fixed the ellipsis button so closing it no longer opens a selection on site and server pages.
- Fixed long branch names in the “Deploy Branch” dropdown.
- Fixed the server provider list to show recently authorized providers.
- Fixed command palette partial searches to return complete results.
- Fixed outbound bandwidth metric display scaling.
- Fixed shared site visibility for team members with View access on the Site dashboard.
- Fixed API site creation with custom domains so the `on-Forge` suffix is not appended.
[​](#october-17-2025)
October 17, 2025
## [​](#optional-repositories) Optional Repositories
It’s now possible to create new sites with any project type without specifying a repository. This is ideal if you’re starting a new project from scratch or want to deploy code manually.When creating a new site, leave the repository field blank. Forge will set up the server and web root for you, allowing you to upload your code later via SFTP, SCP, or any other method you prefer.
## [​](#database-sizes) Database Sizes
Laravel Forge will now show you the estimated size of databases on your server. This is useful to identify large databases that may require optimization or archiving. [Learn more about managing databases in Forge](https://forge.laravel.com/docs/resources/databases)
Show Improvements (9)
- **Improved dark mode**: Improved contrast and readability for dark mode users.
- **Pagination and searching:** Improved the pagination and searching of larger tables.
- **Rename background processes:** Added customizable names for background processes.
- **Clone SSL certificates:** We’ve reintroduced the ability to clone SSL certificates.
- **Copyable IDs:** Added quick copy support for resource IDs from dropdown menus.
- **Deploy keys now work with zero-downtime deployments:** Added support for using deploy keys with zero-downtime deployments.
- **Maintenance mode redirect path:** Added support for redirect paths when enabling maintenance mode on Laravel sites.
- **Display more information about sites and servers:** Added PHP version and isolated username details to site and server list items when applicable.
- **Better Statamic support:** Additional Laravel integrations have been enabled for sites using the Statamic project type.
Show Fixes (8)
- Fixed the environment encryption key resetting.
- Disabled deployments when a site does not have a deploy script.
- Reinstated deploy keys for sites. You can find this in the site’s Deployments tab.
- Disabled the PHP 8.5 option while support is unavailable.
- Fixed issues in the Envoyer deployment hooks migration flow.
- Fixed account deletion for users with organizations that do not have servers.
- Fixed duplicate Nginx upstream errors in load balancers.
- Fixed zero-downtime deployments to symlink `auth.json` only when the file exists.
[​](#october-7-2025)
October 7, 2025
## [​](#the-next-generation-of-forge-is-here) The Next Generation of Forge is Here
Launched on October 1, [the next generation of Laravel Forge](https://laravel.com/blog/everything-you-need-to-know-about-the-new-forge-laravel-vps) delivers speed, control, and ease of use, supporting any modern web stack. This was Forge’s biggest update since its original release in 2014.
### [​](#instant-provisioning-with-laravel-vps) Instant Provisioning with Laravel VPS
You can now deploy a server in under 10 seconds (for most use cases) using Laravel VPS. Fully configure servers with a single click, reducing server setup time from minutes to seconds.Billing for Laravel VPS appears on your Forge invoice, so you avoid juggling multiple provider bills. An integrated terminal supports SSH collaboration, allowing multiple developers to debug the same session in real-time. [See how to provision a server with Laravel VPS](https://youtu.be/WElvWyBMsx4)
### [​](#zero-downtime-deployments) Zero-Downtime Deployments
Deployments now run without taking your site offline, giving you added confidence every time you ship. When creating a new website in Forge, zero-downtime deployments are enabled by default; however, you can choose to disable this feature.You cannot enable zero-downtime deployments for existing sites. [Learn more](/docs/sites/deployments#zero-downtime-deployments)
### [​](#envoyer-migration-tool) Envoyer Migration Tool
You can now migrate sites from Envoyer to Forge’s zero-downtime deployment system.From your site’s dashboard, click “Migrate to Forge” to start. Forge will check if your site uses multiple servers and guide you through the right steps.Zero-downtime deployments currently support one server per site. If you deploy to multiple servers, we recommend continuing to use Envoyer for now. Existing subscriptions remain fully supported. [Read the docs](/docs/integrations/envoyer#migrating-an-existing-site-to-envoyer)
### [​](#nuxt-and-next-js-support) Nuxt and Next.js Support
Forge now includes first-class support for Nuxt and Next.js applications. This update makes it easier than ever to manage full-stack applications on Forge. You can deploy modern JavaScript frameworks alongside your PHP or Laravel projects without extra configuration.When creating a new site, choose Nuxt or Next.js as the project type. Forge will automatically handle the build process, set up the correct runtime environment, and configure your site for production. [Start a Nuxt or Next.js project](https://forge.laravel.com/sign-in)
### [​](#improved-domain-and-ssl-management) Improved Domain and SSL Management
Domains and TLS are now simpler, faster, and more reliable, especially for sites with multiple aliases. SSL certificates are now issued per domain, eliminating multi-domain delays and reducing configuration errors. Managing your Nginx configs is also much easier.Each new site also gets an optional default `on-forge.com` domain for quick testing and sharing, which can be disabled if you don’t need it. [Learn more](https://forge.laravel.com/docs/sites/domains#certificates)
### [​](#streamlined-ui-and-command-palette) Streamlined UI and Command Palette
Forge’s interface has been redesigned for faster, more intuitive navigation. Features are now grouped into logical tabs at the top of each page, reducing clutter and making tools easier to find.The new command palette (`⌘K`) lets you jump to any page or action without reaching for the mouse, speeding up everyday tasks. [Explore the new interface](https://forge.laravel.com/sign-in)
### [​](#organizations-and-teams) Organizations and Teams
Circles have been replaced with a more standard Organizations and Teams structure.
- Organizations are now the primary billing entity across all Forge plans, making it easier to separate billing for different clients or projects.
- Teams live inside organizations and can share servers, recipes, and resources. Teams are available on the [Business plan](https://forge.laravel.com/pricing).
No action is required on your end: all existing Circles and shared resources are migrated automatically. Learn more about [Organizations](/docs/organizations) and [Teams](/docs/teams)
### [​](#heartbeats-and-health-checks) Heartbeats and Health Checks
You can now catch connectivity and routing issues before your users notice them with Forge’s Health checks. This feature pings your application from three regions (London, New York, and Singapore), so you’ll know right away if it’s reachable worldwide.Heartbeats monitor your scheduled jobs by expecting a ping when they finish. If a backup or data processing task fails silently, Forge alerts you immediately, turning job monitoring from a reactive chore into a proactive safeguard. [Enable Health checks and Heartbeats](https://forge.laravel.com/sign-in)
Show Improvements (6)
- **Stacked and queued deployments**: Added complete visibility into what is deploying and when.
- **Health checks and Heartbeats**: Added proactive monitoring to catch connectivity issues and routing problems before they impact users.
- **Real-time metrics charts**: Added live CPU, memory, and bandwidth usage charts.
- **Role-based access control**: Added role-based access control for managing permissions.
- **Organizations as billable entities**: Made multi-client billing management more straightforward.
- **New modern API**: Added a performant, scalable API with comprehensive documentation.
Show Fixes (18)
- Improved DNS verification performance and reliability.
- Fixed load-balanced servers appearing as “Unknown.”
- Added support for configurable deployment retention.
- Fixed organization-level SSH key creation and deletion.
- Added permanent redirects from legacy URLs to new Forge URLs.
- Expanded allowed character sets for database passwords.
- Fixed `/storage` shared paths not being configured during Envoyer migration.
- Fixed Laravel Octane configuration files being written to the incorrect folder.
- Fixed discounted Laravel VPS prices not appearing in the “Resize” dropdown.
- Improved support for self-hosted GitLab and custom Git repositories with zero-downtime deployments.
- Added links to breadcrumb dropdown items so Cmd/Ctrl+Click works as expected.
- Added missing pagination to potentially long lists (databases, SSH keys, etc.).
- Fixed `.env` file reads and writes using the incorrect location for Nuxt.js sites.
- Improved tax ID verification reliability when editing billing information.
- Fixed team-scoped servers being inaccessible.
- Fixed the repository picker not loading more than 100 repositories when using Bitbucket.
- Fixed repeated tab navigation failures on smaller viewports.
- Fixed an issue in the support widget that prevented customers from contacting support.
Was this page helpful?
YesNo
[Support](/docs/support)[Abuse](/docs/abuse)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.