# Envoyer - Quick-Start

*Source: https://docs.envoyer.io/quick-start*

---

Quick Start - Envoyer(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"envoyer-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  false,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Envoyer home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedQuick StartDocumentationCommunityGet StartedIntroductionQuick StartAccountsSource ControlYour AccountProjectsManagementServersDeployment HooksHeartbeatsNotificationsCollaborators(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewSource Control ProvidersProjectsServersImport From ForgeManual ImportConnect From ForgeDeploymentsGet StartedQuick StartThere are just a few simple and intuitive steps to get started.​Overview
The following documentation provides a step-by-step guide to configure your application and infrastructure for zero downtime deployments with Envoyer.
​Source Control Providers
Once you have subscribed to a plan, you will need to connect Envoyer with your preferred source control provider. Envoyer supports GitHub, Bitbucket, GitLab, and self-hosted GitLab.
From the onboarding screen, select your provider and follow the authentication flow for that provider. This grants Envoyer permission to interact with your repositories on your behalf.

Once you’ve connected to your source control provider, this step of the onboarding flow will be complete. Should you wish to connect additional providers, you may do so from the integrations panel of your account.
​Projects
With your source control provider connected, you can now configure your first project.
Click the “Add project” button to open the project creation modal.

Give your project a descriptive name and select the source control provider associated with your application.
Finally, enter the repository information in the format organization/repository along with the branch name you want to deploy. Envoyer will automatically deploy the provided branch unless this is overridden at the start of a deployment.
​Servers
With your project created, you now need to tell Envoyer which server or servers to deploy to. There are three ways to do this.
​Import From Forge
Envoyer has a first-party integration with Laravel Forge - Laravel’s preferred server provisioning and management platform - and you may import servers directly from Forge into your project.
Click the “Provide API Token” option from the onboarding screen and provide a Forge API token. From the project overview, you may now select the “Import” option to open the import modal. From here, select the server and site you wish to import. Envoyer will retrieve the connection details of the server and automatically add an SSH key which allows it to connect.

​Manual Import
Don’t worry if you’re not using Forge; you may configure your server manually. Select the “Configure” option from the onboarding screen in the “Manual Configuration” section. After adding the connection details for your server, add the provided SSH key to the ~/.ssh/authorized_keys file for the users Envoyer should connect to the server as.

​Connect From Forge
It’s also possible to attach a server to your Envoyer project directly from Forge. When creating a new site on Laravel Forge, you may choose “Configure with Envoyer,” allowing you to select the Envoyer project you wish the site to be attached to. Doing so will automatically configure the connection between Envoyer and Forge, install an SSH key, and set the path from which the project should be served.

​Deployments
The final part of your journey to zero downtime deployments is configuring what should happen during the deployment itself.
Envoyer provides a lot of flexibility and control over your deployments - you can read more about that in the hooks section, but for your first deployment, there are only two things to consider:

Which directory on your server(s) should Envoyer deploy your application?
Which directory should your application be served from?

You may configure the deployment directory by opening the “Update server” modal from your project’s “Servers” tab.

Envoyer creates a releases directory in which your latest code is copied when you initiate a deployment. A current symlink is also created that links to the latest release.
If your deployment path is /home/forge/app.com, you should set your web server’s document root directory to /home/forge/app.com/current/public.
When adding a server to Envoyer from Forge, the application path and the web root are set automatically.
Finally, Envoyer can manage your application’s environment variables across all servers associated with a project. You should likely configure this before your fi