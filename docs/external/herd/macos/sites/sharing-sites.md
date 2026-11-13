Source: https://herd.laravel.com/docs/macos/sites/sharing-sites.md

# Sharing Sites

# How to share a site

Herd makes it easy to share your local sites with the world. This is great for testing your sites on different devices, receiving webhooks, or sharing them with clients and colleagues.
Herd uses [Expose](https://expose.dev) to share your sites.

## Sharing sites via Expose

> [!NOTE]
>
> Expose may not be available in all geographical regions due to regulatory reasons. If Expose isn't available in your country, try [ngrok](#sharing-sites-via-ngrok).

To share your site using Expose, you need an Expose account. Open the settings, go to the "Sharing" tab and click "Connect with Expose". Herd opens your browser where you can sign in to Expose or [create a free account](https://expose.dev/register). Once you confirm the connection, Herd stores your Expose token for you.


The Sharing tab shows your Expose plan and lets you select the default server for your shares. Expose Pro users can also select a default custom domain. Click "Manage Account" to see your Expose connection in the integrations settings, where you can also disconnect it. Disconnecting stops all active shares.

If you prefer the CLI, you can also set your token manually:

```shell theme={null}
expose token YOUR_TOKEN_HERE
```

## Sharing from the Applications window

Select a site in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md) and click the share icon next to its URL. Herd starts sharing the site right away and shows the public URL, which you can copy or open. "Open Dashboard" opens the local Expose dashboard where you can inspect all requests to your share. Click "Stop Sharing" once you're done.

Shares from the Applications window use the default server and domain from the Sharing settings. The share icon turns green while a site is shared, and [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md) shows the same share for the site. Herd stops all shares when you quit Herd.

## Sharing via the CLI

Once you connected your Expose account, you can share your sites by running `herd share` or `expose share` in the site directory that you want to share.

```shell theme={null}
cd ~/Herd/example-site

herd share

# Share a linked site:
herd share http://your-local-site.test

# You can share a secured site with:
herd share https://your-secured-local-site.test
```

You can specify a subdomain or server region for best performance and by adding parameters for them to the `share` command.

```shell theme={null}
herd share https://example-site.test --subdomain=my-project-name --server=us-1
```

## Sharing with basic authentication

You may protect your share links with basic authentication by using the `--basicAuth` argument when sharing your site.

```shell theme={null}
herd share https://example-site.test --basicAuth="user:password"
```

## Sharing sites via ngrok

If you want to use ngrok, install it according to their instructions. After that, you can share Herd sites via the terminal:

```shell theme={null}
ngrok http --host-header=rewrite unsecured-site.test
ngrok http --host-header=rewrite secured-site.test:443
```
