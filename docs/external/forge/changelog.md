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
[​](#february-13%2C-2026)
February 13, 2026
## [​](#mysql-9-x-support) MySQL 9.x support
MySQL 9 is now available as a database option when provisioning new servers.
Show Fixes (4)
- Resolved an issue with Laravel VPS servers that do not have a private hostname.
- Fixed an issue preventing the creation of scheduled jobs.
- Fixed Aikido not finding the correct workspace.
- Resolved an issue with database syncing creating duplicate entries.
[​](#february-6%2C-2026)
February 6, 2026
## [​](#openclaw-server-type) OpenClaw server type
You can now create an OpenClaw servers on Laravel VPS.
Show Improvements (2)
- **Command palette filtering**: Improve accuracy of command filtering.
- **Server list**: Display the OS version in the server list.
Show Fixes (1)
- Resolved an issue preventing the delivery of email notifications when a scheduled job’s heartbeat is in a failing state.
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
## [​](#improved-monorepo-support) Improved monorepo support
It’s now possible to configure your application’s “root” directory, making it more convenient to serve applications housed within monorepos.
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
[​](#november-21%2C-2025)
November 21, 2025
## [​](#provision-aws-servers-with-ebs-gp3) Provision AWS servers with EBS gp3
You can now provision an AWS server with EBS GP3. GP2 will remain the default for already provisioned AWS servers. All new servers will be provisioned with EBS gp3.To move your existing servers from gp2 to gp3, visit your AWS dashboard.
Show Improvements (8)
- **Recipes search results**: Updated the recipe search UI to accurately show that a search returned zero matching results, instead of displaying “no recipes”.
- **Manual certificate renewal**: You can now manually trigger a certificate renewal for Let’s Encrypt certificates after a failed attempt on the Domains tab.
- **Site notes**: Sites now allow you to leave notes in the Settings tab, similar to the notes feature for servers. Use them to keep track of important information.
- **Accessibility improvements**: Continued to improve color contrast and form labeling across the platform.
- **Scheduled jobs paths**: Scheduled job paths are now copyable from the scheduler.
- **Clone certificate endpoint**: Added an API endpoint to clone certificates. Mirroring functionality available in the Forge UI now.
- **Copy debug info**: Added the site path to the information included in the copy debug info action.
- **Destructive commands**: Added a confirmation step when attempting to run destructive commands.
Show Fixes (14)
- Resolved a bug causing the Used Memory monitor to display “unknown” after being installed.
- Scheduled jobs now accurately display the next expected run time instead of always showing as UTC.
- A Z-index issue on the domain dropdown of the Let’s Encrypt modal has been fixed.
- Fixed a bug causing Forge to re-add server’s SSH key to the source control provider when creating a site with a deploy key.
- Site logs are available in the Observe tab when Custom and Other are selected in the Framework setting.
- Confirmed users assigned a Viewer role at an organization level are not shown organization-level settings they do not have permissions to edit.
- Hetzner server sizes and prices now display accurate pricing when provisioning a new server.
- The new schedule job modal now has a placeholder reflecting the current directory.
- Confirmed users are being shown the billing button in the admin dashboard after they’ve completed onboarding, instead of being prompted to subscribe.
- Sync database button is now showing for server types other than Database.
- Log file dropdown has been expanded to accommodate longer options.
- Backup configuration has been updated to ensure deleted databases are shown for removal.
- Resolved a bug causing database backups with the server database driver set to MariaDB to fail.
- Laravel VPS servers are now displayed in the drop-down when configuring a load balancer.
[​](#november-14%2C-2025)
November 14, 2025
## [​](#introducing-support-for-postgresql-18) Introducing support for PostgreSQL 18
Forge now offers support for PostgreSQL 18 when provisioning new servers, including Laravel VPS servers.
Show Improvements (4)
- **Sync network rules**: Automatically sync UFW rules with Forge. Missing server rules will be added to Forge and orphaned rules will be removed.
- **Toggle certificates via API**: Enabling and disabling existing certificates is now possible via the API.
- **Improved validation errors**: Validation errors for required fields are now easier to identify.
- **Improved Composer credential validation**: Added context to clarify how fields should be formatted when adding Composer credentials.
Show Fixes (4)
- Fixed bug causing the Update Site API endpoint to reset other keys.
- Fixed z-index issue on site deployment pages.
- Fixed issue in Forge’s API `project_type` match statement causing HTTP 500 errors.
- Improved reliability when adding and removing domains from sites with many domains has been improved.
[​](#november-7%2C-2025)
November 7, 2025
## [​](#ssl-certificate-information) SSL Certificate Information
We have made several improvements to the SSL certificate UI.You can now see relevant domains, status, issue date, and expiration date on the certificate card under Certificates, on the Domains tab.Details on why the most recent attempt to renew or issue a certificate are now easily accessible in the View Output option.Multiple domains sharing a certificate can be copied all at once by clicking on the domains listed in the card details. [Learn more](https://forge.laravel.com/docs/sites/domains)
Show Improvements (5)
- **Deployment error handling**: Continued work to ensure deployment error output is helpful to customers.
- **Firewall rule order**: Updated the order that firewall rules display to mirror UFW order on the server.
- **Command palette**: Use command/control + click in the command palette to open multiple selections at once.
- **API command output**: The Forge API can now fetch command outputs.
- **Update Ubuntu records**: You can manually update Forge’s Ubuntu records in the details section of the server overview.
Show Fixes (4)
- The health check URL will automatically update to reflect primary domain changes.
- Resolved a bug causing the deploy button to be unresponsive on the Deployments tab.
- We now validate certificate field uploads in the existing certificate upload modal.
- Addressed a bug causing site and server details to display over the navigation bar.
[​](#october-31%2C-2025)
October 31, 2025
## [​](#deployment-pipeline-improvements) Deployment Pipeline Improvements
We have made several improvements to the deployment pipeline to better recover from failed deployments and timeouts.Deployments will now always use the version of PHP configured on the site, even when calling `php` inside `composer.json` and `package.json` files. Notably, this fixes issues using Laravel Wayfinder during deployments.
## [​](#site-command-improvements) Site Command Improvements
Commands now correctly use the version of PHP configured for the site.
## [​](#reset-forge-sudo-password) Reset Forge Sudo Password
It is now possible to reset the `forge` sudo password for Laravel VPS servers.
Show Improvements (9)
- **Tag API servers and sites**: Add tags to servers and sites when creating them via the API.
- **Disk usage metric updates**: The disk usage metric now shows in the server’s Overview.
- **Increased command palette results**: The command palette now shows 10 results for servers, sites and recipes.
- **VAT ID improvements**: It’s now easier to fill in the VAT ID in EU countries.
- **Searchable team members**: The team members page now allows you to search for members.
- **Improved Octane and Reverb port selection**: The suggested next available port.
- **Searchable team members**: Team members are now searchable.
- **Improved EU VAT collection**: EU tax IDs are now easier to provide.
- **Select everything:** It’s now possible to select all text within the UI.
Show Fixes (7)
- Sudo mode now enables correctly when restoring database backups.
- Background process validation now correctly validates for sites and servers.
- The command palette hotkey no longer shows ⌘ for Windows and Linux users.
- The monitoring notification now links to the correct place.
- Resolved a 404 when unsharing resources from teams.
- Installing MariaDB 11.4 now works again.
- Invitations can now be accepted at all times.
[​](#october-24%2C-2025)
October 24, 2025
## [​](#improved-mobile-experience) Improved Mobile Experience
We’ve improved the mobile experience for the following features: dropdowns, modals, notification center, tables, and breadcrumbs.
## [​](#reintegrated-aikido-for-sites) Reintegrated Aikido for Sites
When Aikido is enabled at the organization level (via the Integrations page), it activates Aikido features for all sites owned by that organization.
Sites under that organization can then individually opt in to Aikido, enabling security scans and syncing results from Aikido’s API. This ensures a consistent setup while maintaining per-site control. [Learn more about our Aikido integration](https://forge.laravel.com/docs/integrations/aikido#aikido)
Show Improvements (10)
- **Improved search results**: Archived servers have been removed from the command palette.
- **Improved navigation**: Overview page section titles now link to the corresponding page.
- **Subdomain aliases**: Can now retroactively enable/disable wildcards on domains.
- **Pagination and search**: Continued work to ensure pages are searchable from the command palette.
- **Let’s Encrypt controller validation**: Controller will now validate all domains to avoid errors.
- **Restored databases**: Restoring databases now requires sudo mode (password confirmation).
- **Site repository updates**: Sites can now change Git repository and branch.
- **New metric**: Disk usage is now visible for Laravel VPS.
- **Site queue workers**: Now display in Background Processes on a server level.
- **EOL Ubuntu versions**: Improved handling of servers running EOL Ubuntu versions
Show Fixes (8)
- Add server and recipe buttons now appear for all users.
- Closing the ellipsis button on the site page and server page will no longer open the selection.
- Long branch names now display properly in the “Deploy Branch” dropdown.
- Recently authorized server providers will appear in the server provider list.
- Partial searches in the command palette will return complete results.
- Outbound bandwidth metric display updated to scale appropriately.
- Team members with View access can now see shared sites on the Site dashboard.
- Creating Sites via API using a custom domain will no longer include the suffix on-Forge.
[​](#october-17%2C-2025)
October 17, 2025
## [​](#optional-repositories) Optional Repositories
It’s now possible to create new sites with any project type without specifying a repository. This is ideal if you’re starting a new project from scratch or want to deploy code manually.When creating a new site, leave the repository field blank. Forge will set up the server and web root for you, allowing you to upload your code later via SFTP, SCP, or any other method you prefer.
## [​](#database-sizes) Database Sizes
Laravel Forge will now show you the estimated size of databases on your server. This is useful to identify large databases that may require optimization or archiving. [Learn more about managing databases in Forge](https://forge.laravel.com/docs/resources/databases)
Show Improvements (9)
- **Improved dark mode**: Improved contrast and readability for dark mode users.
- **Pagination and searching:** Improved the pagination and searching of larger tables.
- **Rename background processes:** Easily identify your background processes by giving them customizable names.
- **Clone SSL certificates:** We’ve reintroduced the ability to clone SSL certificates.
- **Copyable IDs:** Quickly copy the ID of various resources from their dropdown menu.
- **Deploy keys now work with zero-downtime deployments:** It’s now possible to use zero-downtime deployments in combination with deploy keys.
- **Maintenance mode redirect path:** It’s now possible to provide a redirect path when enabling maintenance mode on your Laravel sites.
- **Display more information about sites and servers:** Sites and server list items now display the version of PHP they’re running and the isolated username, if applicable.
- **Better Statamic support:** Additional Laravel integrations have been enabled for sites using the Statamic project type.
Show Fixes (8)
- Fixed the environment encryption key resetting.
- Deployments are now unavailable when a site does not have a deploy script.
- Reinstate deploy keys for sites. You can find this in the site’s Deployments tab.
- PHP 8.5 is not currently working, so the option has been disabled for now.
- Improved the Envoyer deployment hooks migration flow.
- Accounts now can be deleted by users with organizations without servers.
- Fixed duplicate Nginx upstream errors in load balancers.
- Only attempt to symlink `auth.json` during zero-downtime deployments if the file exists.
[​](#october-7%2C-2025)
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
### [​](#streamlined-ui-and-command-palette) **Streamlined UI and Command Palette**
Forge’s interface has been redesigned for faster, more intuitive navigation. Features are now grouped into logical tabs at the top of each page, reducing clutter and making tools easier to find.The new command palette (`⌘K`) lets you jump to any page or action without reaching for the mouse, speeding up everyday tasks. [Explore the new interface](https://forge.laravel.com/sign-in)
### [​](#organizations-and-teams) Organizations and Teams
Circles have been replaced with a more standard Organizations and Teams structure.
- Organizations are now the primary billing entity across all Forge plans, making it easier to separate billing for different clients or projects.
- Teams live inside organizations and can share servers, recipes, and resources. Teams are available on the [Business plan](https://forge.laravel.com/pricing).
No action is required on your end: all existing Circles and shared resources are migrated automatically. Learn more about [Organizations](/docs/organizations) and [Teams](/docs/teams)
### [​](#heartbeats-and-health-checks) Heartbeats and Health Checks
You can now catch connectivity and routing issues before your users notice them with Forge’s Health checks. This feature pings your application from three regions (London, New York, and Singapore), so you’ll know right away if it’s reachable worldwide.Heartbeats monitor your scheduled jobs by expecting a ping when they finish. If a backup or data processing task fails silently, Forge alerts you immediately, turning job monitoring from a reactive chore into a proactive safeguard. [Enable Health checks and Heartbeats](https://forge.laravel.com/sign-in)
Show Improvements (6)
- **Stacked and queued deployments**: Gain complete visibility into what’s deploying and when.
- **Health checks and Heartbeats**: Catch connectivity issues and routing problems before your users with proactive monitoring for your apps and scheduled jobs.
- **Real-time metrics charts**: See live CPU, memory, and bandwidth usage data.
- **Role-based access control**: Manage who accesses what with ease.
- **Organizations as billable entities**: Working with multiple clients is now more straightforward.
- **New modern API**: Access an API that is performant, scalable, and has comprehensive documentation.
Show Fixes (18)
- Improve performance and reliability of DNS verification.
- Fix load-balanced servers appearing as “Unknown.”
- Add support for configurable deployment retentions.
- Fix organization-level SSH key creation and deletion.
- Add permanent redirects from legacy URLs to new Forge URLs.
- Widen allowed character sets for database passwords.
- Fix `/storage` shared paths not being configured during Envoyer migration.
- Fix Laravel Octane configuration file being written to incorrect folder.
- Fix discounted Laravel VPS prices not showing inside of “Resize” dropdown.
- Improve support for self-hosted GitLab and custom Git repositories with zero-downtime deployments.
- Create breadcrumb dropdown item links so that Cmd/Ctrl+Click works as expected.
- Add missing pagination to potentially long lists (databases, SSH keys, etc.).
- Fix `.env` file reading from and writing to incorrect place for Nuxt.js sites.
- Improve reliability of tax ID verification when editing billing information.
- Fix team-scoped servers not being accessible.
- Fix repository picker not loading more than 100 repositories when using Bitbucket.
- Fix repeated tab navigation not working on smaller viewports.
- Fix issue in support widget preventing customers from contacting support.
Was this page helpful?
YesNo
[Support](/docs/support)[Abuse](/docs/abuse)
⌘I