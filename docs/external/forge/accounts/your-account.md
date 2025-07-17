# Forge - Accounts/Your-Account

*Source: https://forge.laravel.com/docs/accounts/your-account*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI

- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationAccountsYour Account[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/forge)
##### Get Started

- [Introduction](/docs/introduction)
- [Forge CLI](/docs/cli)
- [Forge SDK](/docs/sdk)

##### Accounts

- [Your Account](/docs/accounts/your-account)
- [Circles](/docs/accounts/circles)
- [Source Control](/docs/accounts/source-control)
- [SSH Keys](/docs/accounts/ssh)
- [API](/docs/accounts/api)
- [Tags](/docs/accounts/tags)
- [Troubleshooting](/docs/accounts/cookbook)

##### Servers

- [Server Providers](/docs/servers/providers)
- [Server Types](/docs/servers/types)
- [Management](/docs/servers/management)
- [Root Access / Security](/docs/servers/provisioning-process)
- [SSH Keys / Git Access](/docs/servers/ssh)
- [PHP](/docs/servers/php)
- [Packages](/docs/servers/packages)
- [Recipes](/docs/servers/recipes)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Database Backups](/docs/servers/backups)
- [Monitoring](/docs/servers/monitoring)
- [Cookbook](/docs/servers/cookbook)

##### Sites

- [The Basics](/docs/sites/the-basics)
- [Applications](/docs/sites/applications)
- [Deployments](/docs/sites/deployments)
- [Commands](/docs/sites/commands)
- [Packages](/docs/sites/packages)
- [Queues](/docs/sites/queues)
- [Security Rules](/docs/sites/security-rules)
- [Redirects](/docs/sites/redirects)
- [SSL](/docs/sites/ssl)
- [User Isolation](/docs/sites/user-isolation)
- [Cookbook](/docs/sites/cookbook)

##### Resources

- [Daemons](/docs/resources/daemons)
- [Databases](/docs/resources/databases)
- [Caches](/docs/resources/caches)
- [Network](/docs/resources/network)
- [Scheduler](/docs/resources/scheduler)
- [Integrations](/docs/resources/integrations)
- [Cookbook](/docs/resources/cookbook)

##### Integrations

- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)

##### Other

- [Abuse](/docs/abuse)

Accounts# Your Account

Learn how to manage your Forge account, including updating your profile information, securing your account with Two Factor Authentication, managing authenticated sessions, deleting your account, sharing your account’s servers with other users, receiving invoices via email, accessing previous invoices, and adding business receipts.

## [​](#user-account)User Account

### [​](#updating-your-profile-information)Updating Your Profile Information

You may update your name, email, and password from Forge’s [Authentication dashboard](https://forge.laravel.com/user-profile/authentication) within your user profile.

### [​](#securing-your-account-with-two-factor-authentication)Securing Your Account With Two Factor Authentication

You may add additional security to your user account by setting up Two Factor Authentication (2FA) via Forge’s [Authentication dashboard](https://forge.laravel.com/user-profile/authentication). Once you enable 2FA, please remember to scan the 2FA barcode into your authentication app, such as [Google Authenticator](https://support.google.com/accounts/answer/1066447).

When enabling 2FA, Forge will display:

- A QR code to can with your authentication app

- A security code (if you can’t scan the QR code)

- Several recovery codes

The recovery codes should be stored securely and can be used if you no longer have access to your 2FA device, thus it is recommended to not store your recovery codes exclusively on the device that you use for 2FA. Each recovery code can only be used once. You may re-generate the recovery codes at any time from your account’s dashboard.

If you have configured 2FA on your account and lose access to your it and your recovery codes, you will need to email [[email protected]](/cdn-cgi/l/email-protection#04626b76636144686576657261682a676b69) to reset it by confirming your identity.

We recommend using the [Google Authenticator](https://support.google.com/accounts/answer/1066447) application on your smartphone to manage your Forge 2FA configuration.

### [​](#managing-authenticated-sessions)Managing Authenticated Sessions

To improve your account security, we allow you to view and logout any active sessions for your user account via the [Authentication dashboard](https://forge.laravel.com/user-profile/authentication). This is particularly useful if you forgot to logout on a device you no longer have access to.

### [​](#deleting-your-account)Deleting Your Account

You can delete your account at any time from the [Authentication dashboard](https://forge.laravel.com/user-profile/authentication).

Deleting your account will cancel your subscription and delete all of your account’s data. **Your data, including billing information, will not be recoverable**; however, your servers will not be deleted from your connected server providers.

### [​](#sharing-your-account%E2%80%99s-servers-with-other-users)Sharing Your Account’s Servers With Other Users

If you need to allow other users to help manage the servers in your Forge account, you can create a [Circle](/docs/accounts/circles).

## [​](#billing)Billing

### [​](#receiving-invoices-via-email)Receiving Invoices via Email

Specifying the email addresses you would like to receive new invoices can be done in Forge’s [Billing Management](https://forge.laravel.com/billing) page. You may specify several email addresses by providing a comma separated list.

### [​](#accessing-previous-invoices)Accessing Previous Invoices

The [Billing Management](https://forge.laravel.com/billing) page list all previous invoices for you account.

### [​](#business-receipts)Business Receipts

If you need to add specific contact or tax information to your receipts such as your full business name, VAT / tax identification number, or address of record, you can add this extra billing information on the [Billing Management](https://forge.laravel.com/billing) page in your account. We’ll make sure this information is displayed on every receipt.

Was this page helpful?

YesNo[Forge SDK](/docs/sdk)[Circles](/docs/accounts/circles)On this page
- [User Account](#user-account)
- [Updating Your Profile Information](#updating-your-profile-information)
- [Securing Your Account With Two Factor Authentication](#securing-your-account-with-two-factor-authentication)
- [Managing Authenticated Sessions](#managing-authenticated-sessions)
- [Deleting Your Account](#deleting-your-account)
- [Sharing Your Account’s Servers With Other Users](#sharing-your-account%E2%80%99s-servers-with-other-users)
- [Billing](#billing)
- [Receiving Invoices via Email](#receiving-invoices-via-email)
- [Accessing Previous Invoices](#accessing-previous-invoices)
- [Business Receipts](#business-receipts)

[Laravel Forge home page](https://forge.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)[Term of Service](https://forge.laravel.com/terms-of-service)[Privacy Policy](https://forge.laravel.com/privacy-policy)[Data Processing Agreement (DPA)](https://forge.laravel.com/data-processing-agreement)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.