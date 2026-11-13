Source: https://laravel.com/cloud/docs/sso.md

# Single sign-on

Configure single sign-on for your Laravel Cloud organization using SAML or OpenID Connect.

## Introduction

Laravel Cloud supports single sign-on (SSO) through Security Assertion Markup Language (SAML) 2.0 and OpenID Connect (OIDC). With SSO, members of your organization can authenticate through an identity provider such as Okta, Auth0, Microsoft Entra ID, or Google Workspace instead of managing separate Cloud credentials.

You configure SSO at the organization level. Once enabled, members of your organization can sign in to Cloud through your identity provider. Cloud continues to manage organization membership and roles.

## Configuring SSO

Setting up SSO begins by enabling it for your organization and verifying that you own the domain your members sign in with.

**1. Enable single sign-on**

Navigate to your organization's **Settings > General** page and toggle **Enable single sign-on**. The single sign-on configuration modal opens. In the modal, you first verify your domain and then configure your identity provider. Only Admins can configure SSO.

**2. Verify your domain**

Under **Domain verification**, enter your organization's domain and click **Add domain**. You can add multiple domains if members use email addresses from multiple domains.

**3. Add DNS records**

Add the DNS records Cloud provides to your domain. Cloud automatically verifies your domain after the records propagate. Propagation may take a few hours. You may close the modal and return later without losing progress.

**4. Configure your identity provider**

Once Cloud has verified your domain, complete the **Identity provider configuration** step to connect your identity provider. Each identity provider is different, so follow the steps presented in the SSO flow for your provider.

## Signing in with SSO

Once SSO is enabled, members of your organization can authenticate in two ways:

* Members can launch Cloud directly from their identity provider's application dashboard.
* Members can choose the SSO option on the Cloud login page and enter their work email address. Cloud then redirects them to your identity provider to authenticate.

After authenticating, members land in your organization's dashboard with the role assigned to them in Cloud. SSO handles authentication only. [Roles and permissions](https://laravel.com/cloud/docs/rbac) still control what each member can do.

## Member provisioning

When someone signs in through your identity provider for the first time and does not yet have a Cloud account, Cloud automatically creates an account for them and adds them to your organization. As a result, you can provision new members without sending individual invitations.

Cloud assigns newly provisioned members the [Developer](https://laravel.com/cloud/docs/rbac#developer) role by default. With SSO enabled, you can change the default role from your organization's **Settings > General** page. You can also adjust an individual member's role from the **Settings > Access** page after their first sign-in.

Removing a member from your identity provider's SSO application prevents them from signing in through SSO. To revoke their access entirely, also remove them from your organization in Cloud.

## Disabling SSO

To disable SSO, navigate to your organization's **Settings > General** page and remove the connection. Members can no longer authenticate through your identity provider and must sign in using their email address and password or another supported login method.

> [!WARNING]
>
> Before disabling SSO, make sure that members of your organization have another way to sign in. Members whose accounts Cloud provisioned through SSO may need to reset their password before they can sign in directly.
