# Forge - Sites/The-Basics

*Source: https://forge.laravel.com/docs/sites/the-basics*

---

The Basics - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesThe BasicsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageCreating SitesAutomatic RedirectsCircle PermissionsApps / ProjectsGit RepositoryDeploy KeysWordPressphpMyAdminDefault SitesNginx ConfigurationProtecting Against Unconfigured DomainsPHP VersionChanging A Site’s Installed PHP VersionSite LogsLogrotateSitesThe BasicsCreating sites, installing applications, and managing your server.​Creating Sites
When creating a new site on your Forge server, a variety of configuration options are available to you:

Root Domain: The domain name that the server should respond to.
Aliases: Additional domains that the site should respond to.
Project Type: This configuration setting indicates if the project installed for your site will be a General PHP / Laravel / Symfony project or a static HTML site. This setting is used to determine the structure of the Nginx configuration file that is created for your site.
Web Directory: The directory that should be publicly accessible via the Internet. For Laravel applications, this is typically the /public directory.
PHP Version: If you have multiple versions of PHP installed on your server, you can select which one should be used to serve the site.
Nginx Template: If you have configured any Nginx Templates for you server, you will have the option to select one as the site’s Nginx configuration, otherwise Forge will utilise its default Nginx configuration for you new site.
Wildcard Sub-Domains: This configuration setting will enable the site to respond to any subdomain under its configured root domain.
Website Isolation: This configuration setting indicates whether the PHP-FPM process should run under its own user account. You may learn more about website isolation by consulting the full documentation regarding this feature.
Create Database: This setting indicates if you would like a new database to be created for your site.

​Automatic Redirects
When creating your site, Forge will automatically create a redirect from the www subdomain to the root domain. For example, if you create a site with the root domain example.com, Forge will automatically create a redirect from www.example.com to example.com. Likewise, if your site’s domain is www.example.com, Forge will automatically create a redirect from example.com to www.example.com.
​Circle Permissions
You may grant a circle member authority to create and delete sites by granting the site:create and site:delete permissions.
​Apps / Projects
Once the site has been created in Forge, you can then install an application or project. Projects contain the actual source code of your application. Forge can install three types of applications: an application that exists within a Git repository, WordPress, or phpMyAdmin.
​Git Repository
Before you can install a Git repository, you must first ensure that you have connected your source control provider to your Forge account.
Once you have connected your source control provider accounts, you may choose the provider from one of the available options. If you’re self-hosting your own code or using a provider that Forge doesn’t include first-party support for, you may select the Custom option. When using either the Bitbucket or Custom provider option, you will need to manually add the Forge SSH key to the provider.
You will also need to provide the repository name. For GitHub, GitLab, and Bitbucket providers, you should provide the name in user/repository format, e.g. laravel/laravel. Self-hosted projects should use the full SSH URL, e.g. [email&#160;protected]:laravel/laravel.git.
Before you install the repository, you can also decide whether or not to install Composer dependencies. If your project does not contain a composer.json file, you should uncheck this option.
​Deploy Keys
Sometimes you may wish to only grant the Forge user access to a specific repository. This is typically accomplished by adding an SSH key t