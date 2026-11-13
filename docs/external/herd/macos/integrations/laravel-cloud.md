Source: https://herd.laravel.com/docs/macos/integrations/laravel-cloud.md

# Laravel Cloud

# Laravel Cloud

Herd integrates with [Laravel Cloud](https://cloud.laravel.com) and lets you ship your local application to production with a single click. Herd uses the Laravel Cloud CLI under the hood, so it creates the application on Laravel Cloud for you if it doesn't exist yet and deploys it right away.

## Connect Herd with your Laravel Cloud account

Open the settings, go to "General" and select "Integrations". Click "Connect Service" and select Laravel Cloud. Herd opens your browser to sign in to Laravel Cloud. Once you confirm the connection, you can close the browser tab and return to Herd.


Herd connects to every Laravel Cloud organization of your account and lists each organization separately in the integrations list.

You can also start the connection directly from the "Deploy to Laravel Cloud" button of a site. If you aren't connected yet, Herd asks you to sign in first and starts the deployment afterwards.

> [!NOTE]
>
> Herd also writes the tokens to the configuration of the Laravel Cloud CLI in `~/.config/cloud/config.json`. This way, you can use the `cloud` command in your terminal with the same account.

## Deploying a site

Select a site in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md) and click "Deploy to Laravel Cloud" in the inspector. You can also deploy from the Cloud tab in [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md).

If the site isn't on Laravel Cloud yet, click "Ship to Laravel Cloud". Herd creates a new Laravel Cloud application for the project and deploys it. When the Laravel Cloud CLI needs more information, like the region or the application name, Herd asks you in a native dialog. Cancelling a question stops the deployment.

If the site is already on Laravel Cloud, the popover shows its URL and a button to deploy again.

During the deployment, Herd shows the current step and the progress through the three stages Prepare, Build and Release. Click "Show output" to see the full output of the Laravel Cloud CLI. You can close the popover while Herd deploys your site in the background.

Once the deployment finishes, Herd shows the URL of your live application. The inspector of the site shows this URL from now on.

> [!NOTE]
>
> Herd detects that a site is on Laravel Cloud by its GitHub repository. Make sure that your project has a GitHub `origin` remote and that Laravel Cloud has access to the repository.

## Troubleshooting

If a deployment fails, Herd shows the reason that Laravel Cloud reported. The full output of the Laravel Cloud CLI has more details.

* **Laravel Cloud is rate limiting requests**: wait a few minutes and deploy again.
* **Laravel Cloud returned an error**: this often happens when the Laravel Cloud GitHub app can't access your repository. Check the repository permissions of the GitHub app.
* **The Laravel Cloud CLI could not be located**: the Laravel Cloud CLI requires PHP 8.2 or later. Install one of these PHP versions in the PHP settings.
