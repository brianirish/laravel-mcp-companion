# Envoyer - Projects/Servers

*Source: https://docs.envoyer.io/projects/servers*

---

Servers - Envoyer(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"envoyer-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
  --font-family-headings-custom: "Figtree";
  
  --font-family-body-custom: "Figtree";
  
}:root {
    --primary: 249 51 43;
    --primary-light: 249 51 43;
    --primary-dark: 249 51 43;
    --background-light: 255 255 255;
    --background-dark: 14 10 12;
    --gray-50: 250 244 244;
    --gray-100: 245 239 239;
    --gray-200: 230 224 223;
    --gray-300: 213 207 207;
    --gray-400: 166 160 159;
    --gray-500: 119 113 113;
    --gray-600: 87 81 81;
    --gray-700: 70 64 63;
    --gray-800: 44 38 38;
    --gray-900: 30 24 24;
    --gray-950: 17 11 11;
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  false,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Envoyer home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationProjectsServersDocumentationCommunityGet StartedIntroductionQuick StartAccountsSource ControlYour AccountProjectsManagementServersDeployment HooksHeartbeatsNotificationsCollaborators(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewServer ConfigurationConfiguring Multiple PHP VersionsNon-Standard PHP ServicesImporting Laravel Forge ServersManaging Uploaded FilesProjectsServersLearn how Envoyer deploys your projects to servers.​Overview
After creating a project, you may add as many servers as you like to the project. After adding a server, you will be given an SSH key to add to your server. You should add the SSH key to the ~/.ssh/authorized_keys file for the users Envoyer should connect to the server as.
After you have added the SSH key to the server, click the “refresh” icon next to the server’s “Connection Status” indicator. Envoyer will attempt to connect to your server and run a few health checks on the server, such as attempting to restart PHP FPM (if it is installed on the server).
If Envoyer was unable to restart PHP FPM, you will receive an alert on your project overview. The information modal for the alert will provide the command needed to allow Envoyer to restart FPM without a password.
​Server Configuration
There are several options you may configure when managing a server:
FieldDescriptionNameGive your server a name that you can identify easily.Hostname / IP AddressThe IPv4 address of your server.PortThe port Envoyer should use to connect to your server.Connect AsThe user that Envoyer should use to connect to your server.Receives Code DeploymentsDetermines whether the server should receive code deployments.Project PathThe absolute path to the project’s root directory on your server.Reload FPM After DeploymentsDetermines whether the PHP-FPM service will be reloaded after each deployment.FreeBSDIndicates whether the server is running the FreeBSD operating system.PHP VersionThe version of PHP being used (also determines the version of the PHP-FPM service that will be reloaded).PHP PathThe absolute path to the PHP binary on your system.Composer PathThe absolute path to the Composer binary on your system.
​Configuring Multiple PHP Versions
If your server is configured to run multiple versions of PHP, you may find that the Install Composer Dependencies step uses the wrong version. To resolve this, you should define a custom Composer path configuration setting, such as php8.0 /usr/local/bin/composer. This setting will instruct Composer to run using PHP 8.0 instead of the system default.
​Non-Standard PHP Services
Some VPS providers run custom versions of Ubuntu that manage PHP services in a variety of ways that are not typical. If Envoyer is not able to correctly identify and reload the correct PHP service, you will need to disable the Reload FPM After Deployments setting and create a custom Deployment Hook that reloads the correct service.
​Importing Laravel Forge Servers
If you have provisioned your server with Laravel Forge, you may import it into your Envoyer project. You’ll need to create an API token on your Forge account and then connect it to your Envoyer account from the Integrations dashboard.
When adding a server to your project, click the Import Forge Server button. Envoyer will display a modal asking you to select the server from your account and the site from the server.
Once selected, Envoyer will add the required SSH key to the connected site’s user (typically forge, unless using a Forge configured isolated user). Envoyer will use this SSH key to connect to your server and deploy your site.
​Managing Uploaded Files
When storing user uploaded files in an Envoyer deployed Laravel application, you should store them in the application’s storage directory. Then, you may use the “Manage Linked Folders” feature of Envoyer to create a symbolic link from your public directory to the storage directory. The “Manage Linked Folders” button can be found on the “Deployment Hooks” tab of your project.
If you are not using Laravel, you will essentially follow the same process. However, you will need to manually create a storage directory in the deployment path of your application (the same directory level as the current symbolic link).Was this page helpful?YesNoManagementDeployment HooksAssistantResponses are generated using AI and may contain mistakes.Envoyer home pagexgithubdiscor