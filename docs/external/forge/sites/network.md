Source: https://laravel.com/forge/docs/sites/network.md

# Network

> Learn how Laravel Forge can manage your site’s redirect and security rules.

## Introduction

Laravel Forge can manage your site’s redirect and security rules.

## Security rules

Laravel Forge can configure password protection on your sites using [basic access authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). You can choose whether to protect your entire site or a specific path.

### Managing security rules

#### Creating security rules

To create a security rule, navigate to your site's dashboard and click the "Network" tab. Then, click the "Add security rule" button. After providing a security rule name, path and a list of credentials click "Add security rule".

#### Editing security rules

To edit a security rule, navigate to your site's dashboard and click the "Network" tab. Locate the security rule that you want to update, open the dropdown menu, click "Edit".

#### Deleting security rules

To delete a security rule, navigate to your site's dashboard and click the "Network" tab. Locate the security rule that you want to delete, open the dropdown menu, click "Delete".

### Credentials

Laravel Forge creates a unique `.htpasswd` file for each security rule, meaning each secured path may have its own set of credentials. This also means that you will need to re-enter the same credentials when securing multiple paths. If you need to modify the credentials, you can find the `.htpasswd` file at `/etc/nginx/forge-conf/.../server/.htpasswd-{ruleId}` on your servers.

> [!WARNING]
>
> Laravel Forge does not store your security rule passwords on our servers.

### Customization

Nginx allows you to add further access restrictions such as allowing and denying access to users by IP address. Laravel Forge does not provide the ability to configure this, but you are free to customize your own protected site configuration. Forge creates a `/etc/nginx/forge-conf/.../server/protected_site-{ruleId}.conf` configuration file for protected sites. You can read more about Nginx and basic access authentication [in the Nginx documentation](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/#).

## Redirect rules

Laravel Forge allows you to configure redirects that can be configured to automatically redirect visitors from one page to another. These redirect rules can be created via the "Redirects" tab of the site's management dashboard.

### Managing redirect rules

#### Creating redirect rules

To create a redirect rule, navigate to your site's dashboard and click the "Network" tab, and then into the "Redirects" sidebar. Then, click the "Add redirect rule" button. After providing a redirect rule name, path and a list of credentials click "Add redirect rule".

> [!TIP]
>
> Redirects are wrappers around Nginx's [`rewrite` rules](https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#rewrite) and can use the full redirect syntax supported by Nginx, including regular expressions. For example, you could use `^/$` to only match the root of the domain.

#### Editing redirect rules

To edit a redirect rule, navigate to your site's dashboard and click the "Network" tab, and then into the "Redirects" sidebar. Locate the redirect rule that you want to update, open the dropdown menu, click "Edit".

#### Deleting redirect rules

To delete a redirect rule, navigate to your site's dashboard and click the "Network" tab, and then into the "Redirects" sidebar. Locate the redirect rule that you want to delete, open the dropdown menu, click "Delete".

### Temporary vs. permanent redirects

Laravel Forge supports two types of redirects:

* Permanent (HTTP Status Code 301)
* Temporary (HTTP Status Code 302)

Although both of these redirect types are typically invisible to the user, the browser will treat them differently and it is important to know the difference.

#### Temporary redirects

When the browser encounters a temporary redirect, it will take you to the destination and forget that it was redirected from the original page. If you were to change the destination page and then visited the original page again, the browser would see the new redirect location and take you there.

#### Permanent redirects

With a permanent redirect, the browser will remember that it was redirected away from the original page. To save making another network request, the next time the browser visits the original page, it will see that it was redirected and immediately visit that page instead.

Although you can change the destination of a permanent redirect, you will need to clear the browser cache before you visit the original page again. It's considered bad practice to change a permanent redirect, so be careful when doing so.
