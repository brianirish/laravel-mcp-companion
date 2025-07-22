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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersCookbookDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersCookbookCommon tasks and solutions for managing your Forge server.​AWS Provisioned Servers Are Disappearing
To ensure Forge works correctly with AWS, please review these requirements.
​DigitalOcean Droplet Limit Exceeded
This error is returned by DigitalOcean when you have reached a limit on how many droplets you can create. You can ask DigitalOcean to increase your droplet limit by contacting their support. Once they have increased your limit, you may create servers in Forge.
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

Once you created free space on the disk, you can proceed with the disk expansion steps above.
Consider setting up disk usage monitoring to receive alerts before your disk space runs critically low, giving you time to expand the disk proactively.
​Operating System Release Upgrades
When connecting to your server via SSH, you may encounter messages like New release &#x27;24.04.1 LTS&#x27; available or be instructed to run do-release-upgrade. However, we strongly advise against performing operating system release upgrades on Forge-managed servers.
Upgrading your server’s operating system version can break Forge’s ability to manage your server and may cause application downtime.
During initial provisioning, Forge configures your Ubuntu server with specific settings, services, and applications that are tailored to work seamlessly together. A release upgrade can:

Overwrite critical configuration files
Change system service behaviors
Break compatibility with installed PHP versions, databases, and other services
Prevent Forge from properly managing your server
Cause unexpected application errors or downtime

​Recommended Approach
Instead of upgrading, we recommend provisioning a new server with your desired Ubuntu version through Forge, then migrating your sites to the new server. This approach ensures full Forge compatibility and reduces the risk of unexpected issues that can arise from in-place upgrades.
For teams that prefer a fully managed solution, Laravel Cloud eliminates operating system concerns entirely. While Forge provides maximum control and flexibility over your infrastructure, Laravel Cloud’s fully-managed approach means you never need to think about server maintenance or OS versions.
​Restarting PHP FPM
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


​Server Disconnected
There are several reasons why your server may have a “disconnected” status. We encourage you to check these common solutions before contacting support:

Verify that the server is powered on via your server provider’s dashboard. If the server is powered off, you should restart it using your provider’s dashboard.
Verify that the public IP address of