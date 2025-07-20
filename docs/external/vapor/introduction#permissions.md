# Vapor - Introduction#Permissions

*Source: https://docs.vapor.build/introduction#permissions*

---

Introduction - Laravel Vapor(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"vapor-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
  --font-family-headings-custom: "Figtree";
  
  --font-family-body-custom: "Figtree";
  
}:root {
    --primary: 0 177 228;
    --primary-light: 0 177 228;
    --primary-dark: 0 177 228;
    --background-light: 255 255 255;
    --background-dark: 9 12 15;
    --gray-50: 242 248 249;
    --gray-100: 238 243 244;
    --gray-200: 222 227 229;
    --gray-300: 206 211 212;
    --gray-400: 158 163 165;
    --gray-500: 111 117 118;
    --gray-600: 79 85 86;
    --gray-700: 62 67 69;
    --gray-800: 37 42 44;
    --gray-900: 22 28 29;
    --gray-950: 10 15 17;
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Vapor home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedIntroductionDocumentationKnowledge BaseCommunityBlogGet StartedIntroductionProjectsThe BasicsEnvironmentsDeploymentsDevelopmentDomainsResourcesQueuesStorageNetworksDatabasesCachesLogsIntegrationsSentryOtherAbuse(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageWhat Is Vapor?RequirementsAccount CreationInstalling The Vapor CLILogging InInstalling The Vapor CoreSandbox AccountsTeamsCurrent Team &amp; Switching TeamsCollaboratorsLinking With AWSCreating An IAM RolePermissionsDefining Your AWS BudgetAWS Service LimitsNotification MethodsSlackLegal and ComplianceGet StartedIntroductionManage your Laravel infrastructure on Vapor and fall in love with the scalability and simplicity of serverless.Create An AccountCreate your Vapor account todayWatch MoreWatch the free Vapor series on Laracasts
​What Is Vapor?
Laravel Vapor is an auto-scaling, serverless deployment platform for Laravel, powered by AWS Lambda. Manage your Laravel infrastructure on Vapor and fall in love with the scalability and simplicity of serverless.
Vapor abstracts the complexity of managing Laravel applications on AWS Lambda, as well as interfacing those applications with SQS queues, databases, Redis clusters, networks, CloudFront CDN, and more. Some highlights of Vapor’s features include:


Auto-scaling web / queue infrastructure fine tuned for Laravel


Zero-downtime deployments and rollbacks


Environment variable / secret management


Database management, including point-in-time restores and scaling


Redis Cache management, including cluster scaling


Database and cache tunnels, allowing for easy local inspection


Automatic uploading of assets to Cloudfront CDN during deployment


Unique, Vapor assigned vanity URLs for each environment, allowing immediate inspection


Custom application domains


DNS management


Certificate management and renewal


Application, database, and cache metrics


CI friendly


In short, you can think of Vapor as Laravel Forge for serverless technology.
​Requirements
Vapor requires that your application be compatible with PHP 7.3+ and Laravel 6.0+.
​Account Creation
Before integrating Vapor into your application, you should create a Vapor account. If you are just collaborating with others on their projects, you are not required to have a Vapor subscription. To create and manage your own projects, you will need a Vapor subscription.
​Installing The Vapor CLI
You will deploy your Laravel Vapor applications using the Vapor CLI. This CLI may be installed globally or on a per-project basis using Composer:
CopyAsk AIcomposer require laravel/vapor-cli --update-with-dependencies

composer global require laravel/vapor-cli --update-with-dependencies

When the CLI is installed per project, you will likely need to execute it via the vendor/bin directory of your project, which is where Composer installs executables. For example, to view all of the available Vapor CLI commands, you may use the list command:
CopyAsk AIphp vendor/bin/vapor list

To save keystrokes when interacting with per-project installations of the Vapor CLI, you may add a shell alias to your operating system that aliases the vapor command to php vendor/bin/vapor.
To learn more about a command and its arguments, execute the help command with the name of the command you wish to explore:
CopyAsk AIphp vendor/bin/vapor help deploy

​Logging In
After you have installed the Vapor CLI, you should authenticate with your Vapor account using the login command:
CopyAsk AIvapor login

​Installing The Vapor Core
The laravel/vapor-core package must be installed as a dependency of every Laravel application that is deployed using Vapor. This package contains various Vapor runtime files and a service provider to allow your application to run on Vapor. You may install the Vapor Core into your project using Composer:
CopyAsk AIcomposer require laravel/vapor-core --update-with-dependencies

​Sandbox Accounts
After creating a Vapor account, your account will be on our free “sandbox” plan, which allows you to experience the power of Vapor without the upfront commitment of subscribing to a paid plan. A sandbox account allows you to provision services such as networks, databases, and caches. You may add a single project which, once deployed, will be accessible via an AWS Lambda function URL.
Sandbox projects may not utilize API Gateway versions, l