# Forge - Servers/Cookbook

*Source: https://forge.laravel.com/docs/servers/cookbook*

---

Cookbook - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
  --font-family-headings-custom: "Figtree";
  
  --font-family-body-custom: "Figtree";
  
}:root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersCookbookDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageAWS Provisioned Servers Are DisappearingDigitalOcean Droplet Limit ExceededExpanding Server Disk SpaceChecking Current Disk UsageExpanding the FilesystemVerifying the ExpansionTroubleshootingOperating System Release UpgradesRecommended ApproachRestarting PHP FPMResetting The forge User Sudo PasswordDigital OceanServer Disconnected”Too Many Open Files” ErrorUpgrading ComposerUpgrading MeilisearchUpgrading NginxUpgrading Node.jsUpgrading npmServersCookbookCommon tasks and solutions for managing your Forge server.​AWS Provisioned Servers Are Disappearing
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
When connecting to your server via SSH, you may encounter messages like New release &#x27;24.04.1 LTS&#x27; available