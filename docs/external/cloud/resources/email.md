Source: https://laravel.com/cloud/docs/resources/email.md

# Email

Send transactional email from your environments with Resend

## Introduction

Laravel Cloud integrates directly with [Resend](https://resend.com), so you can send transactional email from your applications without copying API keys between two dashboards.

You connect a Resend account to your organization once, then attach email to any environment, choosing or creating a sending domain along the way. Laravel Cloud creates a sending key for that environment and injects the mail environment variables your application needs.

Resend is the only email provider Laravel Cloud manages for you. You may still configure any other provider manually through your environment variables.

## Connecting a Resend account

You connect a Resend account at the organization level, and each organization may connect one account. Before you connect, you need an existing [Resend account](https://resend.com/signup).

You may connect your account from your organization's settings, as described below, or the first time you [attach email to an environment](#attaching-email-to-an-environment). Either way, Laravel Cloud sends you to Resend to approve access.

**1. Open your integration settings**

From your organization, go to **Settings**, then open the **Integrations** tab and find the **Resend** panel.

**2. Connect your account**

Click **Connect**. Laravel Cloud redirects you to Resend, where you approve access for Laravel Cloud. You do not need to create or paste an API key.

When Resend asks which permission to grant, choose **Full access**. Without it, Laravel Cloud cannot import your existing domains or set up the webhooks it needs.

**3. Review your imported domains**

After you approve access, Laravel Cloud imports the sending domains that already exist in your Resend account and begins tracking their verification status.

Connecting and disconnecting a Resend account requires the **Edit organization integrations** permission, which the Admin and Manager roles include. See the [roles and permissions documentation](https://laravel.com/cloud/docs/rbac) to learn more.

## Sending domains

A sending domain is a domain you have proven you own, which allows Resend to send email on its behalf. You may create a sending domain while [attaching email to an environment](#attaching-email-to-an-environment), or manage all of your sending domains from the **Resend** panel in your organization's integration settings.

Sending domains have their own permissions: **View sending domains**, **Create sending domains**, **Verify sending domains**, and **Delete sending domains**. The Admin and Manager roles include all four, while the Developer and Viewer roles include none. With [custom roles](https://laravel.com/cloud/docs/rbac#custom-roles), you may grant them separately, such as allowing a member to add and verify domains without being able to delete them.

### Adding a domain

Enter the domain you want to send from and choose the region Resend should send from. In your organization's integration settings, click **Add domain**. When attaching email to an environment, click **Create new sending domain**, then **Create**.

Resend supports the following regions:

| Region | Location |
| - | - |
| `us-east-1` | US East (N. Virginia) |
| `eu-west-1` | EU West (Ireland) |
| `sa-east-1` | South America (São Paulo) |
| `ap-northeast-1` | Asia Pacific (Tokyo) |

We recommend sending from a subdomain such as `notifications.example.com` rather than your root domain. A subdomain keeps the sending reputation of your application's email separate from any other email sent from your domain.

### Verifying a domain

After you add a domain, Laravel Cloud shows the DNS records you need to create at your DNS provider. Add each record exactly as shown, then click **Verify records** to have Resend check them.

Verification is not instant. DNS changes can take up to 72 hours to propagate, and Laravel Cloud updates the domain's status as Resend reports progress. A domain moves through the following states:

| Status | Meaning |
| - | - |
| Not verified | The records have not been checked yet |
| Verifying | Resend is checking your records |
| Verified | Your records are correct and you can send from this domain |
| Failed | One or more records could not be verified |

If verification fails, Laravel Cloud lists the records that did not pass so you can correct them, then retry. Open a domain from the list at any time to review its configuration, its DNS records, and the status of each individual record.

### Deleting a domain

Deleting a domain from Laravel Cloud also deletes it from Resend, and your application can no longer send email from that domain. Environments that were sending from the domain keep their sending key, but Resend rejects their messages until you point them at a verified domain.

## Attaching email to an environment

Sending domains belong to your organization, but sending keys belong to an environment. Attach email to each environment that needs to send. Attaching email requires the **Edit environments** permission, which the Developer role also includes.

**1. Add the resource**

Open the environment's canvas, click **Add resource**, then choose **Emails**. If your organization has not connected a Resend account yet, click **Connect Resend** and approve **Full access** in Resend. Laravel Cloud then returns you to the same environment.

**2. Choose a sending domain**

Select a verified domain from the list. To use a domain that is not verified yet, select it to view its DNS records. To send from a new domain, click **Create new sending domain**, enter the domain and region, then click **Create**.

For a new or unverified domain, add the DNS records at your DNS provider and click **Verify records**. Once Resend [verifies the domain](#verifying-a-domain), click **Continue**.

**3. Configure the sender and sending key**

Enter the sender address and sender name your application should send from. Then choose a sending key:

* **Create a new key** creates a full access key used only by this environment, so you may rotate or revoke it without affecting anything else. Because the key has full access, your application may also use it for other Resend features, such as managing contacts or audiences.
* **Reuse existing key** shares a key already used by another environment in your organization. Rotating or revoking it later affects every environment that uses it.

Resend cannot limit full access keys to a single domain, so a key created for one environment can manage your entire Resend account. Treat it with the same care as any other production credential.

**4. Review and confirm**

Review the variables Laravel Cloud will inject, then click **Confirm and attach email**.

**5. Deploy the environment**

Deploy the environment for your application to receive the mail variables.

After you attach email, the canvas displays an **Email** card with the sender address and the name of the sending key. To open the key in Resend, or to detach email from the environment, use the card's options menu.

### Injected environment variables

Attaching email injects the following variables into the environment:

```ini theme={null}
RESEND_API_KEY=re_xxxxxxxxxxxx
RESEND_KEY=re_xxxxxxxxxxxx
MAIL_MAILER=resend
MAIL_FROM_ADDRESS=hello@notifications.example.com
MAIL_FROM_NAME="Your application name"
```

`MAIL_FROM_ADDRESS` and `MAIL_FROM_NAME` use the sender address and sender name you entered when attaching email. `RESEND_KEY` holds the same sending key as `RESEND_API_KEY`, for applications that read the older variable name. Laravel Cloud encrypts both and masks them in your environment's variables, the same way it handles your database password.

Custom environment variables take priority over injected ones, so you may override any of these values by defining a custom variable with the same name, then deploying. See the [environment variables documentation](https://laravel.com/cloud/docs/environments#environment-variables) to learn more.

This also means that if you defined any of these variables yourself before attaching email, your application keeps using your values. For example, a `RESEND_API_KEY` you added manually continues to override the sending key Laravel Cloud created for the environment. To replace the sending key entirely, define both `RESEND_API_KEY` and `RESEND_KEY`. To use the injected values instead, delete the custom variables, then deploy the environment.

### Configuring your application

> [tab] Laravel
>
> Install Resend's Laravel package, which provides the `resend` mail transport and reads the injected `RESEND_API_KEY` variable:
>
> ```sh theme={null}
> composer require resend/resend-laravel
> ```
>
> Laravel's own Resend transport, which only requires the `resend/resend-php` SDK, reads its key from the `services.resend.key` configuration value instead. Applications created from Laravel 11 or Laravel 12 skeletons before v12.10.0 set this value from a `RESEND_KEY` variable. Laravel Cloud injects `RESEND_KEY` as well as `RESEND_API_KEY`, so these applications work without changing `config/services.php`.
>
> Once your application can read the key, send mail as you normally would:
>
> ```php theme={null}
> use Illuminate\Support\Facades\Mail;
>
> Mail::to($user)->send(new OrderShipped($order));
> ```

> [tab] Other frameworks
>
> Laravel Cloud injects the same variables for every runtime, since `RESEND_API_KEY` is what your application needs regardless of the language it is written in. Read the key from your environment and pass it to [Resend's API](https://resend.com/docs/api-reference/introduction) or one of Resend's SDKs.

> [!TIP]
>
> If you queue your mail, a delivery problem may appear as a failed job rather than a failed request. [Laravel Nightwatch](https://nightwatch.laravel.com) traces your queued mail jobs and alerts you when they start failing.

## Detaching and disconnecting

Detaching email from an environment deletes that environment's sending key from Resend, and Laravel Cloud stops injecting the mail variables. Deploy the environment afterward so your application stops receiving them. Your sending domains stay as they are, and other environments continue sending.

Disconnecting your Resend account from the organization is broader. Laravel Cloud deletes the sending key belonging to every attached environment, detaches email from those environments, and discards the access you granted it during the connection flow.

Your Resend account itself is unaffected. Your sending domains stay in Resend and keep their verification, so reconnecting later imports them again without repeating DNS setup.

> [!WARNING]
>
> Disconnecting stops every environment in the organization from sending email. Deploy each affected environment afterward so it stops receiving the mail variables.

## Pricing

Laravel Cloud does not charge for the Resend integration, and it does not bill you for the email you send. You pay Resend directly under your own Resend plan.
