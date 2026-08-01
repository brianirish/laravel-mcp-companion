# Forge - Integrations/Aikido

*Source: https://forge.laravel.com/docs/integrations/aikido*

---

## On this page
- [Introduction](#introduction)
- [Connecting with Aikido](#connecting-with-aikido)
- [Enabling Aikido for sites](#enabling-aikido-for-sites)
- [Viewing security findings](#viewing-security-findings)
Integrations
# Aikido
Copy pageCopy page
Aikido provides security scanning with Laravel Forge integration.
Copy pageCopy page
## [​](#introduction) Introduction
[Aikido](https://aikido.dev?utm_source=laravel&utm_medium=referral) provides security scanning for repositories. Laravel Forge has partnered with Aikido to allow for a seamless integration with your Forge sites, enabling you to identify and resolve security vulnerabilities directly from the Forge dashboard.
## [​](#connecting-with-aikido) Connecting with Aikido
To begin using Aikido with Laravel Forge, you’ll need to enable the integration at the organization level. Navigate to your organization’s settings, select the “Integrations” tab, and toggle the Aikido integration on.
Follow the prompts to connect your Forge organization to an Aikido workspace. After creating your Aikido workspace, you may easily check the security findings for any of your Forge-powered sites.
You can connect multiple Aikido workspaces to a single Forge organization, each representing a different organization or group in your source control provider.
## [​](#enabling-aikido-for-sites) Enabling Aikido for sites
Once your organization is connected to Aikido, you can enable Aikido security scanning for individual sites. Navigate to your site’s “Settings / Integrations” panel and toggle the Aikido integration on.
Click “Enable Aikido” to activate security scanning for the site. Laravel Forge will automatically match the site’s repository and source control provider to enable Aikido scanning.
## [​](#viewing-security-findings) Viewing security findings
Once Aikido is enabled for a site, security findings will be displayed directly in the site’s “Integrations” panel. If Aikido has not found any security issues for your repository, you will see a confirmation message. You can click “View on Aikido” to see more detailed information on the Aikido platform.
You may disable Aikido for a site at any time by toggling the integration off. This will deactivate Aikido from the repository, and scanning will be stopped.
The Aikido integration is only supported for GitHub, GitLab, GitLab Self-Hosted, and Bitbucket.
Was this page helpful?
YesNo
[Sentry](/docs/integrations/sentry)[OpenClaw](/docs/integrations/openclaw)
⌘I