# Envoyer - Projects/Deployment-Hooks

*Source: https://docs.envoyer.io/projects/deployment-hooks*

---

Deployment Hooks - Envoyer(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"envoyer-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  false,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Envoyer home pageSearch...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationProjectsDeployment HooksDocumentationCommunityGet StartedIntroductionQuick StartAccountsSource ControlYour AccountProjectsManagementServersDeployment HooksHeartbeatsNotificationsCollaborators(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(false, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewPush To Deploy URLDeployment URL OptionsDeployment LifecycleHook VariablesProjectsDeployment HooksLearn how to deploy your projects with Deployment Hooks.​Overview
Deployment hooks allow you to customize your entire deployment plan by writing small Bash scripts to automate parts of your deployment. You may also specify the servers on which each hook is executed and the user that runs the hook.
Envoyer creates several first-party deployment hooks that cannot be modified or re-ordered:

Clone New Release
Install Composer Dependencies (if you have configured your project to do so)
Activate New Release
Purge Old Releases

Your custom hooks can be re-ordered before / after each of these fixed actions.
Like any other step during your deployment, if a deployment hook exits with a non-zero status code, the entire deployment will be cancelled. This prevents your application from experiencing downtime due to a broken deployment.
​Push To Deploy URL
If you need to trigger deployments as part of your CI or other automated process instead of when code is pushed to your repository, you can choose to use the “Push To Deploy” URL that is generated by Envoyer for your project. To trigger a deployment using this URL, simply make an HTTP GET or POST request to the URL.
You may regenerate the “Push To Deploy” URL at any time by clicking the refresh icon next to the URL within the Deployment Hooks tab of your project.
​Deployment URL Options
You may pass either a sha or branch parameter to the deployment URL to choose which branch or Git commit to deploy. These parameters may be passed as query string variables or POST fields.
​Deployment Lifecycle
When a deployment is triggered for your project, Envoyer will execute your deployment plan. By default, this consists of downloading a tarball of your project, installing the Composer dependencies (if configured), pointing the current symbolic link at the latest release, and finally purging any old deployments from your server.
Of course, any deployment hooks you have configured will also be run during the deployment in their configured sequence.
​Hook Variables
Within your deployment hook scripts, you may use the release variable to access the most current release directory. For example:
CopyAsk AIcd {{ release }}

php artisan command

Other available variables are:
NameDescriptionauthorThe author of the commit that is being deployedbranchThe branch that Envoyer is configured to deploymessageThe message of the commit that is being deployedprojectThe project’s root directory (the directory which contains current, releases and storage)releaseThe current release path, within releasesshaThe commit hash that is being deployedtimeThe current deployment formatted as YmdHisphpThe server’s configured PHP pathcomposerThe server’s configured Composer pathnameThe project’s name
Variables can be written with or without a space inside of the curly braces. For example, {{ variable }} is the same as {{variable}}Was this page helpful?YesNoServersHeartbeatsAssistantResponses are generated using AI and may contain mistakes.Envoyer home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy Policyxgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-2b892dc828f6e161.js\",\"9058\",\"static/chunks/9058-7f849e951ad85773.js\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js\",\"1725\",\"static/chunks/d30757c7-56ff534f625704fe.js\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js\",\"7261\",\"static/chunks/7261-2b892dc828f6e161.js\",\"3892\",\"static/chunks/3892-251b69e2384ed286.js\",\"7417\",\"static/chunks/7417-548f041b716e378a.js\",\"1953\",\"static/chunks/1953-639d64e349958881.js\",\"9095\",\"static/chunks/9095-5e8c25cebc4b2bd6.js\",\"9779\",\"static/chunks/9779-7bb45d52151006b8.js\",\"3619\",\"