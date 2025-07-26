# Forge - Servers/Cookbook

*Source: https://forge.laravel.com/docs/servers/cookbook*

---

- [Community](https://discord.com/invite/laravel)
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

On this page

- [AWS Provisioned Servers Are Disappearing](#aws-provisioned-servers-are-disappearing)
- [DigitalOcean Droplet Limit Exceeded](#digitalocean-droplet-limit-exceeded)
- [Expanding Server Disk Space](#expanding-server-disk-space)
- [Checking Current Disk Usage](#checking-current-disk-usage)
- [Expanding the Filesystem](#expanding-the-filesystem)
- [Verifying the Expansion](#verifying-the-expansion)
- [Troubleshooting](#troubleshooting)
- [Operating System Release Upgrades](#operating-system-release-upgrades)
- [Recommended Approach](#recommended-approach)
- [Restarting PHP FPM](#restarting-php-fpm)
- [Resetting The forge User Sudo Password](#resetting-the-forge-user-sudo-password)
- [Digital Ocean](#digital-ocean)
- [Server Disconnected](#server-disconnected)
- [”Too Many Open Files” Error](#%E2%80%9Dtoo-many-open-files%E2%80%9D-error)
- [Upgrading Composer](#upgrading-composer)
- [Upgrading Meilisearch](#upgrading-meilisearch)
- [Upgrading Nginx](#upgrading-nginx)
- [Upgrading Node.js](#upgrading-node-js)
- [Upgrading npm](#upgrading-npm)

Servers

# Cookbook

Common tasks and solutions for managing your Forge server.

## [​](#aws-provisioned-servers-are-disappearing) AWS Provisioned Servers Are Disappearing

To ensure Forge works correctly with AWS, please review [these requirements](/docs/servers/providers#amazon-aws-api-access).

## [​](#digitalocean-droplet-limit-exceeded) DigitalOcean Droplet Limit Exceeded

This error is returned by [DigitalOcean](https://digitalocean.com) when you have reached a limit on how many droplets you can create. You can ask DigitalOcean to increase your droplet limit by contacting their support. Once they have increased your limit, you may create servers in Forge.

## [​](#expanding-server-disk-space) Expanding Server Disk Space

When you increase your server’s disk size through your VPS provider, the additional space is not automatically available to your Ubuntu filesystem. You will need to expand the operating system’s filesystem to use the newly allocated space.

We strongly recommend creating a backup or snapshot of your server through your VPS provider before proceeding with disk expansion operations. While these commands are generally safe, disk operations carry inherent risks.

#### [​](#checking-current-disk-usage) Checking Current Disk Usage

First, check your current disk usage to identify which partition needs expansion:

Copy

Ask AI

```
df -h

```

This command will show you all mounted filesystems and their usage. Look for the partition that’s running low on space (typically `/`).

#### [​](#expanding-the-filesystem) Expanding the Filesystem

Most Forge servers use standard partitions without LVM (Logical Volume Manager). If your system uses LVM, the disk expansion process is different and requires additional steps using the `pvresize` and `lvextend` commands.
For standard, non-LVM systems, follow these steps:

1. First, check your partition table:

   Copy

   Ask AI

   ```
   sudo fdisk -l

   ```
2. If the partition needs to be expanded, use the `growpart` command:

   Copy

   Ask AI

   ```
   # Install growpart if it is not available...
   sudo apt-get update && sudo apt-get install -y cloud-guest-utils

   # Grow the partition...
   sudo growpart /dev/vda1  # Replace with your actual device and partition number (e.g., /dev/sda1, /dev/xvda1)

   ```
3. Resize the filesystem:

   Copy

   Ask AI

   ```
   # For ext4 filesystems...
   sudo resize2fs /dev/vda1  # Replace with your actual device (e.g., /dev/sda1, /dev/xvda1)

   # For XFS filesystems...
   sudo xfs_growfs /

   ```

#### [​](#verifying-the-expansion) Verifying the Expansion

After completing the expansion, verify that the additional space is available:

Copy

Ask AI

```
df -h

```

The filesystem should now show the increased capacity.

#### [​](#troubleshooting) Troubleshooting

**“No space left on device” Error**
If you encounter an error like `mkdir: cannot create directory '/tmp/growpart.xxxx': No space left on device`, your root filesystem is completely full, preventing even basic commands from running. You will need to free up some temporary space first:

Copy

Ask AI

```
# Clear apt cache...
sudo apt-get clean

# Clear journal logs (keep only last 50M)...
sudo journalctl --vacuum-size=50M

# Remove old snap versions...
sudo sh -c 'snap list --all | grep disabled | awk "{print \$1, \$3}" | while read name rev; do snap remove "$name" --revision="$rev"; done'

# Check if you now have space...
df -h /

```

Once you created free space on the disk, you can proceed with the disk expansion steps above.

Consider setting up [disk usage monitoring](/docs/servers/monitoring) to receive alerts before your disk space runs critically low, giving you time to expand the disk proactively.

## [​](#operating-system-release-upgrades) Operating System Release Upgrades

When connecting to your server via SSH, you may encounter messages like `New release '24.04.1 LTS' available` or be instructed to run `do-release-upgrade`. However, we strongly advise against performing operating system release upgrades on Forge-managed servers.

Upgrading your server’s operating system version can break Forge’s ability to manage your server and may cause application downtime.

During initial provisioning, Forge configures your Ubuntu server with specific settings, services, and applications that are tailored to work seamlessly together. A release upgrade can:

- Overwrite critical configuration files
- Change system service behaviors
- Break compatibility with installed PHP versions, databases, and other services
- Prevent Forge from properly managing your server
- Cause unexpected application errors or downtime

#### [​](#recommended-approach) Recommended Approach

Instead of upgrading, we recommend provisioning a new server with your desired Ubuntu version through Forge, then migrating your sites to the new server. This approach ensures full Forge compatibility and reduces the risk of unexpected issues that can arise from in-place upgrades.

For teams that prefer a fully managed solution, [Laravel Cloud](https://cloud.laravel.com) eliminates operating system concerns entirely. While Forge provides maximum control and flexibility over your infrastructure, Laravel Cloud’s fully-managed approach means you never need to think about server maintenance or OS versions.

## [​](#restarting-php-fpm) Restarting PHP FPM

When configuring your server, Forge configures FPM so that it can be restarted without using your server’s “sudo” password. To do so, you should issue the following command. Of course, you should adjust the PHP version to match the version of PHP installed on your machine:

Copy

Ask AI

```
touch /tmp/fpmlock 2>/dev/null || true
( flock -w 10 9 || exit 1
    echo 'Restarting FPM...'; sudo -S service $FORGE_PHP_FPM reload ) 9</tmp/fpmlock

```

`flock` is used to prevent concurrent php-fpm reloads. Without a lock, simultaneous restart attempts could lead to race conditions, brief service interruptions, or inconsistent process states.

## [​](#resetting-the-forge-user-sudo-password) Resetting The `forge` User Sudo Password

Forge does not store your server’s `forge` user sudo password and is therefore unable to reset it for you. To reset the `forge` user sudo password, you’ll need to contact your server provider and regain SSH access to your server as the `root` user.
Once you are connected to your server as the `root` user, you should run the `passwd forge` command to redefine the `forge` user sudo password.

#### [​](#digital-ocean) Digital Ocean

If your servers are managed by DigitalOcean, the following steps should assist you in resetting the `forge` user’s sudo password using Digital Ocean’s dashboard.

1. First, on DigitalOcean’s dashboard, click on the server name. Then, within the “Access” tab, click on “Reset Root Password”. Usually, this operation restarts the server and sends the new `root` user’s sudo password to your DigitalOcean account’s associated email address.
2. Nex

*[Content truncated for length]*