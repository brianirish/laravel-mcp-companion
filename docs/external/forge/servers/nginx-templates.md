# Forge - Servers/Nginx-Templates

*Source: https://forge.laravel.com/docs/servers/nginx-templates*

---

Nginx Templates - Laravel Forge(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"forge-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersNginx TemplatesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
On this pageOverviewManaging TemplatesCreate TemplateEdit TemplatesDelete TemplatesTemplate VariablesCircle PermissionsServersNginx TemplatesLearn how to use Nginx templates to customize your site configurations.​Overview
Nginx templates allow you to customize the Nginx site configuration that Forge uses when creating your new site.
Nginx templates that are not valid will prevent Nginx from properly working and your existing sites may stop responding. You should proceed with caution when creating and deploying custom Nginx templates.
​Managing Templates
​Create Template
You may create your own Nginx templates from within a server’s management dashboard. When creating a new template, you need to provide a template name and the template’s content. Forge will provide a default template that you may alter as required.
Although the default template does not show support for TLSv1.3, Forge will automatically update a site to support it if the server is able to do so.
​Edit Templates
You may edit the name and content of your Nginx template at any time. Changes to a template will not affect existing sites that use the template.
​Delete Templates
Deleting a template will not remove any sites which were configured to use it.
​Template Variables
Forge provides several variables that can be used within your templates to dynamically alter their content for new sites:
VariableDescription{{DIRECTORY}}The site’s configured web directory, e.g. /public{{DOMAINS}}The site’s configured domains to respond to, e.g. laravel.com alias.laravel.com{{PATH}}The site’s web accessible directory, e.g. /home/forge/laravel.com/public{{PORT}}The IPv4 port the site should listen to (:80). If the site name is default, this variable will also contain default_server{{PORT_V6}}The IPV6 port to listen to ([::]:80). If the site name is default, this variable will also contain default_server{{PROXY_PASS}}The PHP socket to listen on, e.g. unix:/var/run/php/php8.0-fpm.sock{{ROOT_PATH}}The root of the configured site, e.g. /home/forge/laravel.com{{SERVER_PUBLIC_IP}}The public IP address of the server{{SERVER_PRIVATE_IP}}The private IP address of the server, if available{{SITE}}The site’s name, e.g. laravel.com. This differs from {{DOMAINS}} in that it does not include site aliases.{{SITE_ID}}The site’s ID, e.g. 12345{{USER}}The site’s user, e.g. forge
When using these variables, you should ensure that they exactly match the syntax shown above.
​Circle Permissions
The ability to manage Nginx Templates is determined by the site:manage-nginx permission. This permission is also used to restrict the ability to edit an existing site’s Nginx configuration file.Was this page helpful?YesNoLoad BalancingDatabase BackupsAssistantResponses are generated using AI and may contain mistakes.Laravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"9058\",\"static/chunks/9058-fc5eb8705bf7a22c.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"1725\",\"static/chunks/d30757c7-56ff534f625704fe.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\