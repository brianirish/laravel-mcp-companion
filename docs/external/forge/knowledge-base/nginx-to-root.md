Source: https://laravel.com/forge/docs/knowledge-base/nginx-to-root.md

# Nginx to Root security advisory (NGINX2Root)

> Security advisory for the "Nginx to Root" vulnerabilities fixed in Nginx 1.30.7 and 1.31.9, and how to patch Nginx on Laravel Forge servers.

## Overview

On November 18, 2026, the Nginx team released fixes for five vulnerabilities that are collectively known as ["Nginx to Root"](https://nginx2root.com/) (NGINX2Root): CVE-2026-123007, CVE-2026-123634, CVE-2026-123633, CVE-2026-121810, and CVE-2026-113425. The most severe of these allows an unauthenticated remote attacker to execute commands on your server over HTTP/2, which is commonly enabled on sites served over HTTPS.

The researchers who discovered the vulnerabilities also demonstrated that this remote code execution can be chained with a separate Linux kernel vulnerability to gain root access to the server.

> [!WARNING]
>
> Laravel Forge's automatic security updates **do not** patch Nginx. Forge installs Nginx from a dedicated package repository, and Ubuntu's unattended upgrades only apply updates from Ubuntu's own security repository. You must update Nginx on each of your servers yourself, using the steps below. The Forge service itself has already been patched.

## Affected Nginx versions

| Nginx Branch | Fixed Version |
| - | - |
| Stable | 1.30.7 and later |
| Mainline | 1.31.9 and later |

The HTTP/2 vulnerability has existed since Nginx introduced HTTP/2 support in version 1.9.5, released in 2015, so you should assume that every Forge server is vulnerable until it is patched.

The Linux kernel vulnerability used to escalate to root is tracked separately and requires its own kernel update. Patching Nginx closes the way in, but we recommend keeping automatic security updates enabled and rebooting your servers once the kernel patch is released.

## Where Forge installs Nginx from

The package source depends on when your server was provisioned:

| Server Provisioned | Package Source |
| - | - |
| After approximately April 27, 2026 | `nginx.org` (official Nginx packages) |
| Before approximately April 27, 2026 | Ondřej Surý's `ondrej/nginx` PPA |

The `ondrej/nginx` PPA has since been removed from Launchpad, so servers that still use it will not receive the fixed version. These servers must be switched to the official `nginx.org` repository before they can be patched, as described in [Step 3](#step-3-switch-to-the-nginx-org-repository).

### Ubuntu 20.04 LTS and earlier

Servers running Ubuntu 20.04, 18.04, 16.04, or 14.04 **cannot be patched**. These Ubuntu versions have reached end of life, and `nginx.org` no longer builds packages for them. On Ubuntu 20.04, the newest available version is 1.27.5, which is still vulnerable.

We strongly recommend migrating your applications to a new server running Ubuntu 22.04 or later, ideally Ubuntu 26.04, or upgrading the operating system.

## What you need to do

The following steps apply to servers running Ubuntu 22.04 LTS and later. Work through them in order.

### Step 1: Check your current Nginx version

SSH into your server, check the installed Nginx version, and check whether the `nginx.org` repository is already configured:

```bash theme={null}
nginx -v
grep -rs "nginx.org/packages" /etc/apt/sources.list /etc/apt/sources.list.d/
```

If the version shown is 1.30.7 or later (stable), or 1.31.9 or later (mainline), the server is already patched and you may stop here.

### Step 2: Check where Nginx was installed from

Check the installed package version and its maintainer:

```bash theme={null}
dpkg-query -W -f='${Version}  ${Maintainer}\n' nginx
```

If the output contains `NGINX Packaging <nginx-packaging@f5.com>`, the package already comes from `nginx.org`, so you may skip to [Step 4](#step-4-install-the-update). If the output contains `Ubuntu` or `sury.org` (Ondřej Surý), continue with Step 3.

### Step 3: Switch to the nginx.org repository

Run the following commands in order. Do not use `add-apt-repository --remove` to remove the old PPA, as it fails now that Launchpad has removed the PPA.

```bash theme={null}
# Remove the old Ondřej PPA
sudo rm -f /etc/apt/sources.list.d/ondrej-ubuntu-nginx-*
sudo apt-get update

# Install the nginx.org signing key
curl -fsSL https://nginx.org/keys/nginx_signing.key | gpg --dearmor | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg > /dev/null

# Add the nginx.org mainline repository
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] https://nginx.org/packages/mainline/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list

# Prefer nginx.org packages
printf "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | sudo tee /etc/apt/preferences.d/99nginx
```

### Step 4: Install the update

Refresh the package lists and upgrade Nginx. The `--only-upgrade` flag ensures that no new packages are installed, and the `--force-confold` option keeps your existing Nginx configuration files:

```bash theme={null}
sudo apt-get update
sudo apt-get install --only-upgrade -o Dpkg::Options::=--force-confold nginx
```

Follow any prompts regarding services and daemons that need to be restarted.

### Step 5: Verify the fix is active

Confirm that the new version is installed:

```bash theme={null}
nginx -v
```

If the version shown is 1.30.7 or later (stable), or 1.31.9 or later (mainline), the server is running a fixed version. Next, verify that Nginx is able to load your configuration:

```bash theme={null}
sudo nginx -t
```

You should see the following output. Any `listen ... http2 is deprecated` warnings are harmless:

```text theme={null}
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

If the test fails, check the service status and remove any affected modules, as described in [Notes and edge cases](#notes-and-edge-cases):

```bash theme={null}
systemctl status nginx
```

Reloading Nginx does not load the new binary. If the service was not restarted during the upgrade, restart it so that the patched version is running:

```bash theme={null}
sudo systemctl restart nginx
```

## Notes and edge cases

* **Removed modules:** The Ondřej module packages (`brotli`, `geoip`, `image-filter`, `xslt`, and `ssl-ct`) are removed when switching to `nginx.org`. The `stream` and `mail` modules are compiled into the `nginx.org` builds. If Nginx does not start, remove the `load_module` lines for any missing modules from `/etc/nginx/nginx.conf` and `/etc/nginx/modules-enabled`.
* **Default server:** The `nginx.org` package adds `/etc/nginx/conf.d/default.conf`. Check that your own default server still takes precedence.
* **`apt` is locked:** Another package operation is running. Wait a few minutes and try again.
* **`needrestart` prompts:** Accept the defaults. A reboot may be recommended if a new kernel was installed.

If you cannot update right away, you may temporarily mitigate the HTTP/2 vulnerabilities by disabling HTTP/2 in your sites' Nginx configuration. Note that this does not address the remaining vulnerabilities, so you should still update Nginx as soon as possible.

Given the variety of server setups that are affected, there may be edge cases that this guide does not cover. If you run into one, please [contact Forge support](https://forge.laravel.com/docs/support.md).

## More information

For the full details of each vulnerability, see [nginx2root.com](https://nginx2root.com/) and the [Xint research write-up](https://xint.io/blog/nginx2root-remote-code-execution). The fix is documented in the [Nginx 1.31.9 release notes](https://github.com/nginx/nginx/releases/tag/release-1.31.9).
