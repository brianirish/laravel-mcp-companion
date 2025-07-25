# Forge - Servers/Provisioning-Process

*Source: https://forge.laravel.com/docs/servers/provisioning-process*

---

Root Access / Security - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersRoot Access / SecurityDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageProvisioningPost-ProvisioningSecurityAutomated Security UpdatesServersRoot Access / SecurityLearn about the security measures Forge takes to protect your server.​Provisioning
During the initial provisioning of your server, Forge will connect as the root user over SSH. This is so that Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.
The provisioning process can take upwards of 15 minutes, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.
​Post-Provisioning
After initially provisioning your server, Forge continues to use root access so that it can manage your server’s software, services, and configuration. For example, root access is needed to manage:

Firewalls
Daemons
Scheduled tasks
Isolated users
PHP configuration and management
Other operating system dependencies

​Security
We take security very seriously and ensure that we do everything we can to protect customer’s data. Below is a brief overview of some of the steps we take to ensure your server’s security:

Forge issues a unique SSH key for each server that it connects to.
Password based server SSH connections are disabled during provisioning.
Each server is issued a unique root password.
All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: 22 (SSH), 80 (HTTP) and 443 (HTTPS).
Automated security updates are installed using Ubuntu’s automated security release program.

​Automated Security Updates
Security updates are automatically applied to your server on a weekly basis. Forge accomplishes this by enabling and configuring Ubuntu’s automated security update service that is built in to the operating system.
Forge does not automatically update other software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application’s code is not compatible with the upgrade. However, it is possible to install new versions and patch existing versions of PHP manually via the Forge UI.Was this page helpful?YesNoManagementSSH Keys / Git AccessAssistantResponses are generated using AI and may contain mistakes.Laravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"9058\",\"static/chunks/9058-7f849e951ad85773.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"1725\",\"static/chunks/d30757c7-56ff534f625704fe.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"3892\",\"static/chunks/3892-251b69e2384ed286.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"7417\",\"static/chunks/7417-548f041b716e378a.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"1953\",\"static/chunks/1953-639d64e349958881.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"9095\",\"static/chunks/9095-5e8c25cebc4b2bd6.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"9779\",\"static/chunks/9779-7bb45d52151006b8.js?dpl=dpl_4cvasEmnnmTHoUNUH6upjSUH65df\",\"3619\",\"static/chunks/3619-2c24842c619fda67.js?dpl=dpl_4cvasEmnnmTHoUN