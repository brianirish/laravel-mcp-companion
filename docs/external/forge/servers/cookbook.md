# Forge - Servers/Cookbook

*Source: https://forge.laravel.com/docs/servers/cookbook*

---

Cookbook - Laravel Forge
              document.documentElement.style.setProperty('--font-family-headings-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-headings-custom', '');
              document.documentElement.style.setProperty('--font-family-body-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-body-custom', '');
            
    (function() {
      try {
        var bannerKey = "forge-laravel-bannerDismissed";
        var bannerContent = undefined;
        
        if (!bannerContent) {
          document.documentElement.setAttribute('data-banner-state', 'hidden');
          return;
        }
        
        var dismissedValue = localStorage.getItem(bannerKey);
        var shouldShowBanner = !dismissedValue || dismissedValue !== bannerContent;
        
        document.documentElement.setAttribute('data-banner-state', shouldShowBanner ? 'visible' : 'hidden');
      } catch (e) {
        document.documentElement.setAttribute('data-banner-state', 'hidden');
      }
    })();
  :root{--font-inter:'Inter', 'Inter Fallback';--font-jetbrains-mono:'JetBrains Mono', 'JetBrains Mono Fallback'}((e,i,s,u,m,a,l,h)=>{let d=document.documentElement,w=["light","dark"];function p(n){(Array.isArray(e)?e:[e]).forEach(y=>{let k=y==="class",S=k&&a?m.map(f=>a[f]||f):m;k?(d.classList.remove(...S),d.classList.add(a&&a[n]?a[n]:n)):d.setAttribute(y,n)}),R(n)}function R(n){h&&w.includes(n)&&(d.style.colorScheme=n)}function c(){return window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}if(u)p(u);else try{let n=localStorage.getItem(i)||s,y=l&&n==="system"?c():n;p(y)}catch(n){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true):root {
    --primary: 24 182 155;
    --primary-light: 24 182 155;
    --primary-dark: 24 182 155;
    --background-light: 255 255 255;
    --background-dark: 9 12 14;
    --gray-50: 243 248 247;
    --gray-100: 238 243 242;
    --gray-200: 223 228 227;
    --gray-300: 206 211 210;
    --gray-400: 159 164 163;
    --gray-500: 112 117 116;
    --gray-600: 80 85 84;
    --gray-700: 63 68 67;
    --gray-800: 38 42 42;
    --gray-900: 23 28 27;
    --gray-950: 10 15 14;
  }h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersCookbookDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersCookbookCommon tasks and solutions for managing your Forge server.​Restarting PHP FPM
When configuring your server, Forge configures FPM so that it can be restarted without using your server’s “sudo” password. To do so, you should issue the following command. Of course, you should adjust the PHP version to match the version of PHP installed on your machine:
CopyAsk AItouch /tmp/fpmlock 2&gt;/dev/null || true
( flock -w 10 9 || exit 1
    echo &#x27;Restarting FPM...&#x27;; sudo -S service $FORGE_PHP_FPM reload ) 9&lt;/tmp/fpmlock

flock is used to prevent concurrent php-fpm reloads. Without a lock, simultaneous restart attempts could lead to race conditions, brief service interruptions, or inconsistent process states.
​Resetting The forge User Sudo Password
Forge does not store your server’s forge user sudo password and is therefore unable to reset it for you. To reset the forge user sudo password, you’ll need to contact your server provider and regain SSH access to your server as the root user.
Once you are connected to your server as the root user, you should run the passwd forge command to redefine the forge user sudo password.
​Digital Ocean
If your servers are managed by DigitalOcean, the following steps should assist you in resetting the forge user’s sudo password using Digital Ocean’s dashboard.


First, on DigitalOcean’s dashboard, click on the server name. Then, within the “Access” tab, click on “Reset Root Password”. Usually, this operation restarts the server and sends the new root user’s sudo password to your DigitalOcean account’s associated email address.


Next, still on the “Access” tab, click on “Launch Droplet Console” to gain access to your server terminal as the root user. During this step, you will be asked to redefine the root user’s sudo password.


Finally, execute the passwd forge terminal command as the root userto redefine the forge user’s sudo password.


​Upgrading Composer
The latest version of Composer is installed by Forge when a new server is provisioned. However, as your server ages, you may wish to upgrade the installed version of Composer. You may do so using the following command:
CopyAsk AIcomposer self-update --2

This will instruct Composer to update itself and specifically select version 2. If your application is not compatible with Composer 2, you can roll back to Composer 1 at any time:
CopyAsk AIcomposer self-update --1

Servers are provisioned with a Scheduled job that updates Composer. You should delete and recreate the existing job via the server’s “Scheduled Jobs” tab after upgrading Composer.
​Upgrading Nginx
The latest version of Nginx is installed by Forge when a new server is provisioned. However, as your server ages, you may wish to upgrade the installed version of Nginx. You may do so using the following commands:
CopyAsk AIsudo apt-get install -y --only-upgrade nginx
sudo nginx -v
sudo service nginx restart

You should upgrade the Nginx version on your server at your own risk. Upgrading the version of Nginx installed on your server may cause downtime or conflict with other installed software.
​Upgrading Node.js
The latest LTS version of Node.js is installed by Forge when it is provisioning a new server. However, as your server ages, you may wish to upgrade the version of Node.js:
CopyAsk AIsudo apt-get update --allow-releaseinfo-change &amp;&amp; sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=22
echo &quot;deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main&quot; | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update --allow-releaseinfo-change &amp;&amp; sudo apt-get install nodejs -y

Node.js version information
​Upgrading npm
The latest version of npm is installed by Forge when provisioning new servers. However, you may upgrade the installed version of npm using the following commands:
CopyAsk AIsudo npm install npm@latest -g

​Upgrading Meilisearch
If you would like to install the latest Meilisearch binaries on your server, please follow the official Meilisearch upgrade guide.
On most Forge servers, the Meilisearch binary is installed at /usr/local/bin/meilisearch and the database is stored at /var/lib/meilisearch.
​Expanding Server Disk Space
When you increase your server’s disk size through your VPS provider, the additional space is not automatically available to your Ubuntu filesystem. You will need to expand the operating system’s filesystem to use the newly allocated space.
We strongly recommend creating a backup or snapshot of your server through your VPS provider before proceeding with disk expansion operations. While these commands are generally safe, disk operations carry inherent risks.
​Checking Current Disk Usage
First, check your current disk usage to identify which partition needs expansion:
CopyAsk AIdf -h

This command will show you all mounted filesystems and their usage. Look for the partition that’s running low on space (typically /).
​Expanding the Filesystem
Most Forge servers use standard partitions without LVM (Logical Volume Manager). If your system uses LVM, the disk expansion process is different and requires additional steps using the pvresize and lvextend commands.
For standard, non-LVM systems, follow these steps:


First, check your partition table:
CopyAsk AIsudo fdisk -l



If the partition needs to be expanded, use the growpart command:
CopyAsk AI# Install growpart if it is not available...
sudo apt-get update &amp;&amp; sudo apt-get install -y cloud-guest-utils

# Grow the partition...
sudo growpart /dev/vda1  # Replace with your actual device and partition number (e.g., /dev/sda1, /dev/xvda1)



Resize the filesystem:
CopyAsk AI# For ext4 filesystems...
sudo resize2fs /dev/vda1  # Replace with your actual device (e.g., /dev/sda1, /dev/xvda1)

# For XFS filesystems...
sudo xfs_growfs /



​Verifying the Expansion
After completing the expansion, verify that the additional space is available:
CopyAsk AIdf -h

The filesystem should now show the increased capacity.
​Troubleshooting
“No space left on device” Error
If you encounter an error like mkdir: cannot create directory &#x27;/tmp/growpart.xxxx&#x27;: No space left on device, your root filesystem is completely full, preventing even basic commands from running. You will need to free up some temporary space first:
CopyAsk AI# Clear apt cache...
sudo apt-get clean

# Clear journal logs (keep only last 50M)...
sudo journalctl --vacuum-size=50M

# Remove old snap versions...
sudo sh -c &#x27;snap list --all | grep disabled | awk &quot;{print \$1, \$3}&quot; | while read name rev; do snap remove &quot;$name&quot; --revision=&quot;$rev&quot;; done&#x27;

# Check if you now have space...
df -h /

Once you created free space