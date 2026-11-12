Source: https://laravel.com/forge/docs/knowledge-base/sites.md

# Sites

> Common tasks and solutions for managing your Laravel Forge sites.

## Nginx

### HTTP 403: Forbidden after installing a site

If you receive a HTTP 403: Forbidden response after installing a site, this typically indicates that there is no `index.php` or `index.html` file present in the web directory. Nginx is configured to not display directory listings by default for security reasons.

Forge no longer deploys sites with a default `index.html` file. To resolve this issue, you should:

1. Deploy your application code to the site.
2. Ensure your application has an `index.php` file in the web directory (typically `/public` for Laravel applications).
3. Verify that your site's web directory is correctly configured in the site settings.

If you have deployed your application and still see this error, verify that:

* Your deployment script completed successfully.
* The web directory path matches where your application's entry point is located.
* File permissions are correct (Forge sets these automatically during deployment).

## Site is stuck deploying

Rarely, your application may get stuck in a "deploying" state. When this occurs, you can reset the deployment state at the top right of the site management panel using the **Self Help** drop-down menu.

## Using user isolation with existing sites

It is not currently possible to use isolated users to manage existing sites that have already been created without user isolation. Instead, you will need to create a new site with the user isolation option enabled.

## Uncommitted commits during deployment

This error may occur when files under source control within the site directory have been changed by the application and will be overwritten by the fresh deployment.

You may discard these changes by accessing the **Self Help** drop-down menu at the top right of the site management panel and triggering the **Reset Git State** action. Please note that the changes made will be lost when this action is run.

You should also review your application and correct any parts of the applications that may be writing to a source controlled directory on your server. Otherwise, you may continue to encounter this error on further deployments.

### Adding Composer credentials during site creation

Composer credentials (for example, for private packages) can be added during site creation from **Advanced settings** under **Composer Authentication**. You can also add them after the site is created from your site's **Settings** tab under **Composer**.

> [!NOTE]
>
> If you do not add credentials during site creation and the site requires private packages, you must disable **Install Composer Dependencies** during site creation—otherwise the installation will fail. After the site is created, add your credentials in **Settings** → **Composer**, then run a deployment to install the dependencies.

See more at [Packages - Composer credentials](https://forge.laravel.com/docs/resources/packages.md#composer-credentials).
