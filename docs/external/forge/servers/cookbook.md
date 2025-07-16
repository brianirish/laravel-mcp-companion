# Forge - Servers/Cookbook

*Source: https://forge.laravel.com/docs/servers/cookbook*

---

- [Laravel Forge home page](https://forge.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#c4a2abb6a3a184a8a5b6a5b2a1a8eaa7aba9)
- [Dashboard](https://forge.laravel.com)
- [Dashboard](https://forge.laravel.com)

Search...NavigationServersCookbook[Documentation](/docs/introduction)[Changelog](/docs/changelog/changelog)- [Community](https://discord.com/invite/laravel)
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

Servers# Cookbook

Common tasks and solutions for managing your Forge server.

## [​](#restarting-php-fpm)Restarting PHP FPM

When configuring your server, Forge configures FPM so that it can be restarted without using your server’s “sudo” password. To do so, you should issue the following command. Of course, you should adjust the PHP version to match the version of PHP installed on your machine:

CopyAsk AI```
touch /tmp/fpmlock 2>/dev/null || true
( flock -w 10 9 || exit 1
    echo 'Restarting FPM...'; sudo -S service $FORGE_PHP_FPM reload ) 9</tmp/fpmlock

```

`flock` is used to prevent concurrent php-fpm reloads. Without a lock, simultaneous restart attempts could lead to race conditions, brief service interruptions, or inconsistent process states.

## [​](#resetting-the-forge-user-sudo-password)Resetting The `forge` User Sudo Password

Forge does not store your server’s `forge` user sudo password and is therefore unable to reset it for you. To reset the `forge` user sudo password, you’ll need to contact your server provider and regain SSH access to your server as the `root` user.

Once you are connected to your server as the `root` user, you should run the `passwd forge` command to redefine the `forge` user sudo password.

#### [​](#digital-ocean)Digital Ocean

If your servers are managed by DigitalOcean, the following steps should assist you in resetting the `forge` user’s sudo password using Digital Ocean’s dashboard.

- 
First, on DigitalOcean’s dashboard, click on the server name. Then, within the “Access” tab, click on “Reset Root Password”. Usually, this operation restarts the server and sends the new `root` user’s sudo password to your DigitalOcean account’s associated email address.

- 
Next, still on the “Access” tab, click on “Launch Droplet Console” to gain access to your server terminal as the `root` user. During this step, you will be asked to redefine the `root` user’s sudo password.

- 
Finally, execute the `passwd forge` terminal command as the `root` userto redefine the `forge` user’s sudo password.

## [​](#upgrading-composer)Upgrading Composer

The latest version of Composer is installed by Forge when a new server is provisioned. However, as your server ages, you may wish to upgrade the installed version of Composer. You may do so using the following command:

CopyAsk AI```
composer self-update --2

```

This will instruct Composer to update itself and specifically select version 2. If your application is not compatible with Composer 2, you can roll back to Composer 1 at any time:

CopyAsk AI```
composer self-update --1

```

Servers are provisioned with a Scheduled job that updates Composer. You should delete and recreate the existing job via the server’s “Scheduled Jobs” tab after upgrading Composer.

## [​](#upgrading-nginx)Upgrading Nginx

The latest version of Nginx is installed by Forge when a new server is provisioned. However, as your server ages, you may wish to upgrade the installed version of Nginx. You may do so using the following commands:

CopyAsk AI```
sudo apt-get install -y --only-upgrade nginx
sudo nginx -v
sudo service nginx restart

```

You should upgrade the Nginx version on your server at your own risk. Upgrading the version of Nginx installed on your server may cause downtime or conflict with other installed software.

## [​](#upgrading-node-js)Upgrading Node.js

The latest LTS version of Node.js is installed by Forge when it is provisioning a new server. However, as your server ages, you may wish to upgrade the version of Node.js:

CopyAsk AI```
sudo apt-get update --allow-releaseinfo-change && sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=22
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update --allow-releaseinfo-change && sudo apt-get install nodejs -y

```

[Node.js version information](https://nodejs.org/en/about/previous-releases/)

## [​](#upgrading-npm)Upgrading npm

The latest version of npm is installed by Forge when provisioning new servers. However, you may upgrade the installed version of npm using the following commands:

CopyAsk AI```
sudo npm install npm@latest -g

```

## [​](#upgrading-meilisearch)Upgrading Meilisearch

If you would like to install the latest Meilisearch binaries on your server, please follow [the official Meilisearch upgrade guide](https://www.meilisearch.com/docs/learn/update_and_migration/updating).

On most Forge servers, the Meilisearch binary is installed at `/usr/local/bin/meilisearch` and the database is stored at `/var/lib/meilisearch`.

## [​](#digitalocean-droplet-limit-exceeded)DigitalOcean Droplet Limit Exceeded

This error is returned by [DigitalOcean](https://digitalocean.com) when you have reached a limit on how many droplets you can create. You can ask DigitalOcean to increase your droplet limit by contacting their support. Once they have increased your limit, you may create servers in Forge.

## [​](#aws-provisioned-servers-are-disappearing)AWS Provisioned Servers Are Disappearing

To ensure Forge works correctly with AWS, please review [these requirements](/docs/servers/providers#amazon-aws-api-access).

## [​](#server-disconnected)Server Disconnected

There are several reasons why your server may have a “disconnected” status. We encourage you to check these common solutions before contacting support:

- Verify that the server is powered on via your server provider’s dashboard. If the server is powered off, you should restart it using your **provider’s dashboard**.

- Verify that the public IP address of the server is known to Forge (the public IP address may change between reboots of the actual VPS).

- Verify that the Forge generated public key for the server is included in the `/root/.ssh/authorized_keys` and `/home/forge/.ssh/authorized_keys` files. This key is available via the “Settings” tab of your server’s Forge management panel.

- If your server is behind a firewall, make sure you have [allowed Forge’s IP addresses to access the server](/docs/introduction#forge-ip-addresses).

- If you removed Port 22 from the server’s firewall rules, you will need to contact your server provider and ask them to restore the rule. Removing this rule prevents Forge from accessing your server via SSH.

- Remove any private keys or other lines that do not contain a valid public key from the `/root/.ssh/authorized_keys` and `/home/forge/.ssh/authorized_keys` files.

If you are still experiencing connectivity issues, you should also verify that the permissions and ownership of the following directories and files are correct:

CopyAsk AI```
# Fixes the "root" user (run as root)

chown root:root /root
chown -R root:root /root/.ssh
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys

# Fixes the "forge" user

chown forge:forge /home/forge
chown -R forge:forge /home/forge/.ssh
chmod 700 /home/forge/.ssh
chmod 600 /home/forge/.ssh/authorized_keys

```

If, after trying all of the above solutions, Forge is still unable to connect to your server but you can still SSH to the server, please run the following command as the `root` user and share the output with Forge support:

CopyAsk AI```
grep 'sshd' /var/log/auth.log | tail -n 10

```

If Forge is not able to connect to your server, you will not be able to manage it through the Forge dashboard until connectivity is restored.

## [​](#%E2%80%9Dtoo-many-open-files%E2%80%9D-error)”Too Many Open Files” Error

If you are receivin

*[Content truncated for length]*