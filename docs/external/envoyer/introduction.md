# Envoyer - Introduction

*Source: https://docs.envoyer.io/introduction*

---

Introduction - Envoyer(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"envoyer-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  false,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Envoyer home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedIntroductionDocumentationCommunityGet StartedIntroductionQuick StartAccountsSource ControlYour AccountProjectsManagementServersDeployment HooksHeartbeatsNotificationsCollaborators(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageWhat Is Envoyer?Forge IntegrationEnvoyer IP AddressesEnvoyer APILimitationsLegal and ComplianceGet StartedIntroductionWelcome to Envoyer, a zero downtime deployment service for PHP.Create An AccountCreate your Envoyer account todayWatch MoreWatch the free Envoyer series on Laracasts
​What Is Envoyer?
Envoyer is a zero downtime deployment service for PHP. Some highlights of Envoyer’s features include:


GitHub, GitLab &amp; Bitbucket Integration


GitLab Self-Hosted Integration


Seamless Deployment Rollbacks


Application Health Checks


Integrated Chat Notifications


Tuned for Laravel Apps


Deploy Any PHP Project


Unlimited Deployments


Deploy To Multiple Servers


Cron Job Monitoring


Unlimited Team Members


Customize Your Deployments


Import Your Laravel Forge Servers


​Forge Integration
Laravel Forge now offers a first-party integration with Envoyer. Learn more.

​Envoyer IP Addresses
If you are restricting SSH access to your server using IP whitelisting, you must whitelist the following IP addresses:


159.65.47.205


157.245.120.132


134.122.14.47


144.126.248.121


You may also need to whitelist the Health Check IP addresses.
​Envoyer API
Envoyer provides a powerful API that allows you to manage your servers programmatically, providing access to the vast majority of Envoyer features. You can find the Envoyer API documentation here.
​Limitations
Envoyer is not necessary for applications running Laravel Octane, as Octane already includes zero-downtime deployments out of the box.
​Legal and Compliance
Our Terms of Service and Privacy Policy provide details on the terms, conditions, and privacy practices for using Envoyer.Was this page helpful?YesNoQuick StartAssistantResponses are generated using AI and may contain mistakes.Envoyer home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy Policyxgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-1f4bcac893329b6b.js\",\"9058\",\"static/chunks/9058-fc5eb8705bf7a22c.js\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js\",\"1725\",\"static/chunks/d30757c7-d1a658b63aa94b97.js\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js\",\"7261\",\"static/chunks/7261-1f4bcac893329b6b.js\",\"3892\",\"static/chunks/3892-251b69e2384ed286.js\",\"7417\",\"static/chunks/7417-548f041b716e378a.js\",\"1953\",\"static/chunks/1953-46fbce29c74b759e.js\",\"9095\",\"static/chunks/9095-5e8c25cebc4b2bd6.js\",\"9779\",\"static/chunks/9779-7bb45d52151006b8.js\",\"3619\",\"static/chunks/3619-3e497b0446e2fdfc.js\",\"2398\",\"static/chunks/2398-3c77a562bc9286bb.js\",\"1862\",\"static/chunks/1862-d7c7b8aab3b4ffe6.js\",\"2755\",\"static/chunks/2755-e2a765a591a8496d.js\",\"1350\",\"static/chunks/1350-26b6b0bf9ffa1c90.js\",\"5456\",\"static/chunks/app/%255Fsites/%5Bsubdomain%5D/(multitenant)/layout-b596e085fd7c2d45.js\"],\"ThemeProvider\"]\n"])self.__next_f.push([1,"6:I[81925,[\"7261\",\"static/chunks/7261-1f4bcac893329b6b.js\",\"9058\",\"static/chunks/9058-fc5eb8705bf7a22c.js\",\"9249\",\"static/chunks/app/%255Fsites/%5Bsubdomain%5D/error-d4ab46b84560464d.js\"],\"default\"]\n12:I[71256,[],\"\"]\n:HL[\"/mintlify-assets/_next/static/media/bb3ef058b751a6ad-s.p.woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n:HL[\"/mintlify-assets/_next/static/media/e4af272ccee01ff0-s.p.woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n:HL[\"/mintlify-assets/_next/static/css/ca797da4e9f8f21c.css\",\"style\"]\n:HL[\"/mintlify-assets/_next/static/css/f61b4e54ca51c353.css\",\"style\"]\n:HL[\"/mintlify-assets/_next/static/css/19e66b131dc509b0.css\",\"style\"]\n"])self.__next_f.push([1,"0:{\"P\":null,\"b\":\"Oi0K6WmEWh_sjAi1Dj1bk\",\"p\":\"/mintlify-assets\",\"c\":[\"\",\"_sites\",\"docs.envoyer.io\",\"introduction\"],\"i\":false,\"f\":[[[\"\",{\"children\":[\"%5Fsites\",{\"