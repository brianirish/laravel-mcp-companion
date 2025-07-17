# Forge - Changelog/Changelog

*Source: https://forge.laravel.com/docs/changelog/changelog*

---

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

Search...

⌘KAsk AI

- Support
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...

Navigation

Changelog

[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)

#####

- [Changelog](/docs/changelog/changelog)

# Changelog

[​](#week-of-may-13%2C-2025)

Week of May 13, 2025

**Changed**

- Removed support for Ubuntu 20.04 as it has reached end-of-life (EOL)

[​](#week-of-may-2%2C-2025)

Week of May 2, 2025

**Improvements**

- Increased performance around the sites API
- SSH key fingerprinting algorithm
- Performance of server events page

**Fixes**

- Server packages page now loads correctly when the server has no sites
- API now allows custom frequencies when creating a scheduled job

[​](#week-of-apr-25%2C-2025)

Week of Apr 25, 2025

**Improvements**

- Provisioning process now checks for Ubuntu version
- New deployment scripts now use a read-only file descriptor to prevent concurrent PHP-FPM reloads

[​](#week-of-apr-18%2C-2025)

Week of Apr 18, 2025

**Improvements**

- Added subjects to emails sent from Forge
- Better handling when archiving disconnected servers

**Fixes**

- Trim excessive recipe output
- Fix running of recipes
- Daemons no longer get stuck with an incorrect status
- Recipe notifications are now working again

[​](#week-of-mar-28%2C-2025)

Week of Mar 28, 2025

**Improvements**

- Prevent deployments of sites not ready to be deployed
- Slack authorization handling

**Fixes**

- Circle invitation validation
- Aikido integration correctly matches repositories
- Log files can now be cleared again
- Daemons can now be created with `startsecs=0`

[​](#week-of-mar-17%2C-2025)

Week of Mar 17, 2025

**Improvements**

- Updated font on invoice

**Fixes**

- No notification when server failed to delete at provider
- Supplying empty username when creating a site via the API
- Aikido setup when using custom GitLab
- Required email field when editing backup configuration
- Server disappearing from dashboard when deleting a load balanced site
- `pool.d` file missing when changing PHP version on an isolated site
- `stopwaitsecs` missing in deamons API (was part of docs)
- Removing Laravel specific daemons sometimes removed wrong deamon
- Servers not marked as connecting while refreshing status

[​](#week-of-mar-3%2C-2025)

Week of Mar 3, 2025

**Fixes**

- Creating an isolated site via the API with invalid usernames

[​](#week-of-feb-17%2C-2025)

Week of Feb 17, 2025

**Improvements**

- Role ARNs are required when editing AWS credentials

**Fixes**

- Reverb and Octane daemons are created with custom ports
- “Run Job Now” correctly reports the status of the job

[​](#week-of-feb-10%2C-2025)

Week of Feb 10, 2025

**Improvements**

- Improved performance of server and site name searching
- Improved server password generation

**Fixes**

- Notification channels are now correctly removed when transferring servers
- Reverb site name is now updated when a site is renamed
- Blackfire is now correctly removed for PHP 8.4 when the integration is disabled
- Clean up failed Reverb installations

[​](#week-of-feb-3%2C-2025)

Week of Feb 3, 2025

**Improvements**

- Clarify Deployment Script’s reloading of PHP FPM
- Increased security requirements for new passwords

**Fixes**

- Correctly handle transferring of AWS servers when using Role ARN based credentials
- Fixed deleting of Circles with pending invitations
- Fixed error when transferring servers that are part of a circle

[​](#week-of-jan-27%2C-2025)

Week of Jan 27, 2025

**Improvements**

- SSH banners are now muted when Forge connects to a server
- Newly provisioned servers now write a `.hushlogin` file to prevent errors caused by MOTD
- Improved handling of disconnected servers when running scripts
- Enabled `X-Frame-Options=SAMEORIGIN` header for improved security

**Fixes**

- When deleting AWS servers, the EBS block volumes are also deleted
- Reload PHP-FPM when restarting Nginx
- Fixed create server modal not hiding in some cases
- Improved authorization retry logic when connected to Bitbucket

[​](#week-of-jan-20%2C-2025)

Week of Jan 20, 2025

**Improvements**

- Add support for Swoole with PHP 8.4
- Add Thailand (`ap-southeast-1`) to AWS regions list
- Add Mexico (`mx-central-1`) to AWS regions list
- New AWS credentials will use short-lived tokens via [AWS Roles](/docs/servers/providers#amazon-aws-api-access)

**Fixes**

- Sites can now be safely renamed back to `default`
- Add `-s` flag when syncing MySQL databases to prevent errors
- Fixed recipe reports

[​](#week-of-jan-13%2C-2025)

Week of Jan 13, 2025

**Improvements**

- Server names now include a wider variety of names
- SSH keys generated by Forge will now be use `ed25519`
- Node 22.x is now installed by default (previously 18.x)
- Forge now detects the process status of all daemons
- Server Ubuntu versions are now shown in the information bar

**Fixes**

- Disabled Microsoft Teams notifications
- Firewall IPs may be comma separated including spaces
- Worker information will now show all known information
- Daemon status syncing is now more resilient
- Pinned `awscli` to v2.22.35 to resolve issues when using DigitalOcean and Vultr S3 providers with database backups

[​](#week-of-jan-6%2C-2025)

Week of Jan 6, 2025

**Improvements**

- Add validation message when archiving balancers from API
- Switched field order when installing existing certificates
- Report rate limiting errors to the frontend

**Fixes**

- Allow installing repositories with special characters in branch names
- AWS VPC is no longer always required when creating new AWS servers
- “Skip this step” button now redirects correctly when onboarding
- Disabled “Blogo” starter kit within Statamic integration
- Let’s Encrypt certificates should timeout less frequently
- Forge now reloads PHP-FPM when reloading Nginx configurations (previously calling restart could cause moments of downtime)

Was this page helpful?

YesNo

On this page

- [Week of May 13, 2025](#week-of-may-13%2C-2025)
- [Week of May 2, 2025](#week-of-may-2%2C-2025)
- [Week of Apr 25, 2025](#week-of-apr-25%2C-2025)
- [Week of Apr 18, 2025](#week-of-apr-18%2C-2025)
- [Week of Mar 28, 2025](#week-of-mar-28%2C-2025)
- [Week of Mar 17, 2025](#week-of-mar-17%2C-2025)
- [Week of Mar 3, 2025](#week-of-mar-3%2C-2025)
- [Week of Feb 17, 2025](#week-of-feb-17%2C-2025)
- [Week of Feb 10, 2025](#week-of-feb-10%2C-2025)
- [Week of Feb 3, 2025](#week-of-feb-3%2C-2025)
- [Week of Jan 27, 2025](#week-of-jan-27%2C-2025)
- [Week of Jan 20, 2025](#week-of-jan-20%2C-2025)
- [Week of Jan 13, 2025](#week-of-jan-13%2C-2025)
- [Week of Jan 6, 2025](#week-of-jan-6%2C-2025)

[Laravel Forge home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg)](https://forge.laravel.com)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)

[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)

Assistant

Responses are generated using AI and may contain mistakes.