# Forge - Changelog

*Source: https://forge.laravel.com/docs/changelog*

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

New updates and improvements to Laravel Forge.

[​](#december-5%2C-2025)

December 5, 2025

## [​](#package-manager-support) Package manager support

You may now select your preferred package manager when creating new sites. Select from npm, pnpm, Bun, or Yarn.

![](https://mintcdn.com/forge-laravel/EsEkZvY_b4TWYHCT/images/changelogs/12-5-25/package_manager.png?fit=max&auto=format&n=EsEkZvY_b4TWYHCT&q=85&s=69ce6d1bd25e1d2f32a417cb3012791a)

## [​](#improved-monorepo-support) Improved monorepo support

It’s now possible to configure your application’s “root” directory, making it more convenient to serve applications housed within monorepos.

![](https://mintcdn.com/forge-laravel/EsEkZvY_b4TWYHCT/images/changelogs/12-5-25/root_path.png?fit=max&auto=format&n=EsEkZvY_b4TWYHCT&q=85&s=e8b5b3845c58e577bb35a7ece905f9f8)

Show Improvements (8)

- **Manually update database version**: Added a refresh button on the database page allowing you to manually sync the database version.
- **Increased FastCGI buffers**: Increased FastCGI buffers and FastCGI buffer size to decrease the chances exceeding buffer thresholds, triggering a 502 error.
- **Branch details**: Branch details are now visible on the deployments tab and the deployment details page.
- **Deployment logs**: Deployment logs automatically open on the deployment details page after initiating a new deployment.
- **Scheduled job frequency**: The cron expression now displays when hovering over Custom frequency on the scheduled job card.
- **Copy certificate output**: There is now a button to copy the full certificate output in the output modal.
- **Site install automation**: Site installation will trigger the install and build commands automatically.
- **Accessibility**: Dropdowns are now navigable using the arrow keys when opened using the the `Tab` key. Additionally, pressing `Esc` closes the dropdown.

Show Fixes (9)

- Add users modal is now properly sized to avoid overlapping.
- Commenting out deployment script macros now works as expected.
- Organizations no longer overlap while switching organizations when using the Safari browser.
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

![](https://mintcdn.com/forge-laravel/hcLEf7Sqd4f72HGx/images/changelogs/11-21-2025/amazon_ebs_gp3.png?fit=max&auto=format&n=hcLEf7Sqd4f72HGx&q=85&s=45fc5b7da5ef5cdc4c6a924e18c641dd)

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
- Scheduled jobs now accurately display next expected run time instead of always showing as UTC.
- A Z-index issue on the domain dropdown of the Let’s Encrypt modal has been fixed.
- Fixed a bug causing Forge to re-add server’s SSH key to source control provider when creating a site with a deploy key.
- Site logs are available in the Observe tab when Custom and Other are selected in the Framework setting.
- Confirmed users assigned a Viewer role at an organization level are not shown organization level settings they do not have permissions to edit.
- Hetzner server sizes and prices now display accurate pricing when provisioning a new server.
- The new schedule job modal now has a placeholder reflecting the current directory.
- Confirmed users are being shown the billing button in the admin dashboard after they’ve completed onboarding, instead of being prompted to subscribe.
- Sync database button is now showing for server types other than Database.
- Log file dropdown has been expanded to accommodate longer options.
- Backup configuration has been updated to ensure deleted databases are shown for removal.
- Resolved a bug causing database backups with server database driver set to MariaDB to fail.
- Laravel VPS servers are now displayed in the drop down when configuring a load balancer.

[​](#november-14%2C-2025)

November 14, 2025

## [​](#introducing-support-for-postgresql-18) Introducing support for PostgreSQL 18

Forge now offers support for PostgreSQL 18 when provisioning new servers, including Laravel VPS servers.

![](https://mintcdn.com/forge-laravel/u1I1iXJo6d23a1Ko/images/changelogs/11-14-25/postgres-18.png?fit=max&auto=format&n=u1I1iXJo6d23a1Ko&q=85&s=f4d1790efb2263a7564cebad788b9c3d)

Show Improvements (4)

- **Sync network rules**: Automatically sync UFW rules with Forge. Missing server rules will be added to Forge and orphaned rules will be removed.
- **Toggle certificates via API**: Enableing and disabling existing certificates is now possible via the API.
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

![](https://mintcdn.com/forge-laravel/wSpywaUjjpMc8duW/images/changelogs/11-7-2025/ssl-certificate-ui.png?fit=max&auto=format&n=wSpywaUjjpMc8duW&q=85&s=4c4bb065caa1bf2ff476b130d43a1d39)

Show Improvements (5)

- **Deployment error handling**: Continued work to ensure deployment error output is helpful to customers.
- **F

*[Content truncated for length]*