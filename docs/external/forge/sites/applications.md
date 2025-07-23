# Forge - Sites/Applications

*Source: https://forge.laravel.com/docs/sites/applications*

---

Applications - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesApplicationsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageOverviewRequirementsLaravel SchedulerMaintenance ModeMaintenance Mode “Secret”Laravel HorizonConverting Existing DaemonsLaravel OctaneConverting Existing DaemonsLaravel ReverbSSLConverting Existing DaemonsInertia Server Side RenderingConverting Existing DaemonsCircle PermissionsSitesApplicationsLearn how to create and manage your applications on Laravel Forge.​Overview
Forge provides first-class support for applications running Laravel, allowing you to quickly toggle and configure:

Laravel’s Task Scheduler
Laravel’s Maintenance Mode
Laravel Horizon Daemon
Laravel Octane Daemon
Laravel Reverb Daemon
Inertia.js Server Side Rendering (SSR) Daemon


To accomplish this, Forge parses the composer.json and composer.lock files from your application and inspects for the presence and version of the packages above.
​Requirements
Forge will only show the application panel for Laravel framework installations of version 5.0 or later. In addition, the panel’s supported packages must meet the following version requirements:
DependencyMinimum Versionlaravel/framework5.0laravel/horizon1.0laravel/octane1.0laravel/pulse1.0laravel/reverb*inertiajs/inertia-laravel0.6.6
​Laravel Scheduler
You may quickly enable or disable the Laravel scheduler via the “Laravel Scheduler” toggle. Forge will create the required Scheduler for you.
Forge will automatically configure the scheduler to run every minute using the site’s configured PHP version.
​Maintenance Mode
If you have deployed a Laravel application, Forge allows you to make use of Laravel’s maintenance mode feature. Clicking the Laravel Maintenance Mode toggle within the site’s Application tab will run the php artisan down Artisan command within your application, which will make your site unavailable. When the site is in maintenance mode, you can then toggle it off to make your site available again.
​Maintenance Mode “Secret”
Laravel 8.0+ applications can make use of the “secret” option to bypass maintenance mode. Using this option with older versions of Laravel is not supported.
​Laravel Horizon
You may quickly enable or disable the Laravel Horizon daemon via the “Laravel Horizon” toggle. Forge will create the required Horizon daemon for you.
If the site’s deploy script does not contain the horizon:terminate command, Forge will automatically append it for you.
​Converting Existing Daemons
If your server is already configured with a daemon that runs Laravel Horizon, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.
​Laravel Octane
You may quickly enable or disable the Laravel Octane daemon via the “Laravel Octane” toggle. Forge will create the required Octane daemon and install Octane dependencies for you.
When enabling the Octane daemon, Forge will ask you to provide the port number you would like to use for the Octane server as well as your Octane server of choice.

If the site’s deploy script does not contain the octane:reload command, Forge will automatically append it for you.
Before enabling Laravel Octane, you must set the OCTANE_SERVER environment variable to the Octane server you choose.
​Converting Existing Daemons
If your server is already configured with a daemon that runs Laravel Octane, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.
​Laravel Reverb
Determining the correct server type for hosting Laravel Reverb depends on your configuration requirements. You may use the table below to help inform your decision:
ConfigurationApp ServerWeb ServerReverb server alongside Laravel application⊙Dedicated Reverb server⊙Dedicated Reverb server with Pulse⊙Dedicated Reverb server with Pulse (seperate ingest and / or databa