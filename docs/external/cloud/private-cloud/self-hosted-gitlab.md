Source: https://laravel.com/cloud/docs/private-cloud/self-hosted-gitlab.md

# Self-hosted GitLab

Deploy applications from a GitLab instance your organization runs itself.

## Introduction

Laravel Cloud deploys from GitHub, GitLab, and Bitbucket. If your organization runs its own GitLab instance, Private Cloud can deploy from that instance as well.

You connect the two by registering Laravel Cloud as an OAuth application inside your GitLab instance, then giving Cloud the resulting credentials. Cloud uses them to read your repositories and receive push events, then deploys your applications as it does for GitLab.com.

The connection belongs to your Cloud organization, so you configure it once and everyone in the organization can import repositories from your instance.

> [!NOTE]
>
> Self-hosted GitLab is available only with [Private Cloud](https://laravel.com/cloud/docs/private-cloud). If you do not see **Self-hosted GitLab** under your organization's integrations, [contact us](https://laravel.com/enterprise).

## Requirements

Before you begin, make sure the following are in place:

* You have administrator access to your GitLab instance. You need it to register an instance-wide application.
* Cloud can reach your GitLab instance over HTTPS to read repositories and complete the OAuth flow.
* Your GitLab instance can reach Cloud to deliver push events. If your instance sits behind a firewall, allow outbound traffic to Cloud.
* Your GitLab instance is running v16.4 or later.

## Connecting your instance

You will switch between Cloud and GitLab during setup, so keep the Cloud dialog open while you create the application in GitLab.

**1. Open the integration in Cloud**

Navigate to **Settings > Integrations > Self-hosted GitLab** and click **Connect GitLab instance**. A dialog appears with a callback URL. Copy it.

**2. Create an application in GitLab**

In your GitLab instance, open **Admin** from the menu in the top right, then select **Applications** in the sidebar and click **Add new application**.

**3. Configure the application**

Give the application any name you like, such as "Laravel Cloud", and paste the callback URL you copied into the **Redirect URI** field. Then configure the following settings:

* **Confidential**: checked
* **Device authorization grant**: checked
* **Scopes**: `api`

Save the application. GitLab then shows an application ID and a secret. The secret appears only once, so copy it before leaving the page.

**4. Finish the connection in Cloud**

Return to the dialog in Cloud and enter the URL of your GitLab instance, the application ID, and the secret. Click **Connect**.

## Deploying from your instance

After you connect the instance, everyone in your Cloud organization sees a new **Connect** option for it when they create an application. Choosing it redirects them to your GitLab instance to authorize with their own GitLab account.

Cloud follows your instance's permissions, so each user sees only the repositories their GitLab account can access. From there, importing a repository and deploying it works the same as it does for any other [source control provider](https://laravel.com/cloud/docs/source-control).

## Troubleshooting

| Symptom | Resolution |
| - | - |
| GitLab reports a redirect URI mismatch | The **Redirect URI** in your GitLab application does not match the callback URL exactly. Copy it from the Cloud dialog again and apply it verbatim. |
| Authorization fails with an insufficient scope error | The application is missing the `api` scope. Edit it in GitLab, enable `api`, and connect again. |
| Cloud cannot connect to the instance | The instance URL is incorrect or Cloud cannot reach it. Check that the URL includes `https://`, that the instance is reachable from outside your network, and that it presents a valid TLS certificate. |
| A user sees no repositories after authorizing | Their GitLab account does not have access to those projects. Grant access in GitLab and reauthorize. |
