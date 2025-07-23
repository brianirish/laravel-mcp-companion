# Envoyer - Projects/Management

*Source: https://docs.envoyer.io/projects/management*

---

Management - Envoyer(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"envoyer-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  false,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Envoyer home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationProjectsManagementDocumentationCommunityGet StartedIntroductionQuick StartAccountsSource ControlYour AccountProjectsManagementServersDeployment HooksHeartbeatsNotificationsCollaborators(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewCreating a ProjectProject SettingsHealth ChecksHealth Check IP AddressesSource ControlTransfer ProjectDelete ProjectProjectsManagementHow to manage your Envoyer projects.​Overview
Within Envoyer, your application is represented by a “project”. Projects can be deployed to one or more servers at the same time.
​Creating a Project
To create a project, click the Add Project button at the top of the Envoyer dashboard. You will be presented with a modal that asks you to provide a few details about the project.
If you don’t see the Source Control provider that you need, make sure that you’ve linked it in your account settings.
Once you’ve provided the details regarding your project, click Save Project.
To create new projects, you must be subscribed to one of Envoyer’s paid subscriptions.
​Project Settings
To make changes to your project settings, click the Settings button at the top of the project’s dashboard.
From here, you can change the project settings, source control settings, and delete the project. In addition, you can edit the project’s name, type, health check URL, and how many deployments to retain for the project
​Health Checks
When your site has finished deploying, Envoyer can ping it to ensure that it is still available. Health checks are performed from three locations:

New York
London
Singapore

If you have configured notifications on your project, Envoyer will notify these channels of the result of the health check.
The configured URL must return a 2xx status code. All other status codes will be considered a failure.
​Health Check IP Addresses
If your application firewall requires you to allow access from the health check monitors by IP address, you should allow the following IP addresses so that Envoyer can ping your URL:

New York: 198.199.84.22
London: 167.71.140.19
Singapore: 167.71.208.72

​Source Control
You can manage how the project is deployed via the project’s source control settings. Specifically, you may configure from which source control provider the project is deployed, the branch that is deployed, and you may also choose whether to install the project’s Composer dependencies.
You may also enable the project’s Deploy When Code Is Pushed setting. Enabling this setting will add a webhook to your source control provider. When code is pushed to the selected branch, Envoyer will automatically trigger a new deployment.
​Transfer Project
Projects may be transferred to other Envoyer accounts from the project’s Settings panel. To transfer the project, you must provide the email address of the Envoyer account you wish to transfer the project to. The Envoyer account that is receiving the project will receive an email asking them to confirm the transfer request.
You may only transfer projects to Envoyer accounts with an active subscription.
​Delete Project
If you no longer need the project, you may delete it via the project settings dashboard. After confirming the name of the project, click the Delete Project button.
Deleting your project is an irreversible action, and we will be unable to recover the project’s settings for you.Was this page helpful?YesNoYour AccountServersAssistantResponses are generated using AI and may contain mistakes.Envoyer home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy Policyxgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-74071ac740b599a5.js\",\"9058\",\"static/chunks/9058-7f849e951ad85773.js\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js\",\"1725\",\"static/chunks/d30757c7-de545030e34cf23b.js\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js\",\"7261\",\"static/chunks/7261-74071ac740b599a5.js\",\"3892\",\"static/chunks/3892-7f882638e4a83cba.js\",\"7417\",\"static/chunks/7417-548f041b716e378a.js\",\"1953\",\"static/chunks/1953-c04af94f764c403d.js\",\"9