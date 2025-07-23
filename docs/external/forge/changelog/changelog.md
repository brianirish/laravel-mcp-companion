# Forge - Changelog/Changelog

*Source: https://forge.laravel.com/docs/changelog/changelog*

---

Changelog - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationChangelogDocumentationChangelogCommunityBlogChangelog(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageWeek of May 13, 2025Week of May 2, 2025Week of Apr 25, 2025Week of Apr 18, 2025Week of Mar 28, 2025Week of Mar 17, 2025Week of Mar 3, 2025Week of Feb 17, 2025Week of Feb 10, 2025Week of Feb 3, 2025Week of Jan 27, 2025Week of Jan 20, 2025Week of Jan 13, 2025Week of Jan 6, 2025Changelog​Week of May 13, 2025Changed
Removed support for Ubuntu 20.04 as it has reached end-of-life (EOL)

​Week of May 2, 2025Improvements
Increased performance around the sites API
SSH key fingerprinting algorithm
Performance of server events page
Fixes
Server packages page now loads correctly when the server has no sites
API now allows custom frequencies when creating a scheduled job

​Week of Apr 25, 2025Improvements
Provisioning process now checks for Ubuntu version
New deployment scripts now use a read-only file descriptor to prevent concurrent PHP-FPM reloads

​Week of Apr 18, 2025Improvements
Added subjects to emails sent from Forge
Better handling when archiving disconnected servers
Fixes
Trim excessive recipe output
Fix running of recipes
Daemons no longer get stuck with an incorrect status
Recipe notifications are now working again

​Week of Mar 28, 2025Improvements
Prevent deployments of sites not ready to be deployed
Slack authorization handling
Fixes
Circle invitation validation
Aikido integration correctly matches repositories
Log files can now be cleared again
Daemons can now be created with startsecs=0

​Week of Mar 17, 2025Improvements
Updated font on invoice
Fixes
No notification when server failed to delete at provider
Supplying empty username when creating a site via the API
Aikido setup when using custom GitLab
Required email field when editing backup configuration
Server disappearing from dashboard when deleting a load balanced site
pool.d file missing when changing PHP version on an isolated site
stopwaitsecs missing in deamons API (was part of docs)
Removing Laravel specific daemons sometimes removed wrong deamon
Servers not marked as connecting while refreshing status

​Week of Mar 3, 2025Fixes
Creating an isolated site via the API with invalid usernames

​Week of Feb 17, 2025Improvements
Role ARNs are required when editing AWS credentials
Fixes
Reverb and Octane daemons are created with custom ports
“Run Job Now” correctly reports the status of the job

​Week of Feb 10, 2025Improvements
Improved performance of server and site name searching
Improved server password generation
Fixes
Notification channels are now correctly removed when transferring servers
Reverb site name is now updated when a site is renamed
Blackfire is now correctly removed for PHP 8.4 when the integration is disabled
Clean up failed Reverb installations

​Week of Feb 3, 2025Improvements
Clarify Deployment Script’s reloading of PHP FPM
Increased security requirements for new passwords
Fixes
Correctly handle transferring of AWS servers when using Role ARN based credentials
Fixed deleting of Circles with pending invitations
Fixed error when transferring servers that are part of a circle

​Week of Jan 27, 2025Improvements
SSH banners are now muted when Forge connects to a server
Newly provisioned servers now write a .hushlogin file to prevent errors caused by MOTD
Improved handling of disconnected servers when running scripts
Enabled X-Frame-Options=SAMEORIGIN header for improved security
Fixes
When deleting AWS servers, the EBS block volumes are also deleted
Reload PHP-FPM when restarting Nginx
Fixed create server modal not hiding in some cases
Improved authorization retry logic when connected to Bitbucket

​Week of Jan 20, 2025Improvements
Add support for Swoole with PHP 8.4
Add Thailand (ap-southeast-1) to AWS regions list
Add Mexico (mx-central-1) to AWS regions list
New AWS credentials will use short-lived tokens via AWS Roles
Fixes
Sites can now be safely renamed back to default
Add -s flag when syncing MySQL databases to prevent errors
Fixed recipe reports

​Week of Jan 13, 2025Improvements
Server names now include a wider variety of names
SSH keys generated by Forge will now be use ed25519
Node 22.x is now installed by default (previously 18.x)
Forge now detects the process status of all daemons
Server Ubuntu versions are now shown in the information bar
Fixes
Disabled Microsoft Teams notifications
Firewall IPs may be comma separated including spaces
Worker information will now