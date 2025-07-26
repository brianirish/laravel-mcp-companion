# Nova - Customization/Assets

*Source: https://nova.laravel.com/docs/v5/customization/assets*

---

Assets - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
  --font-family-headings-custom: "Figtree";
  
  --font-family-body-custom: "Figtree";
  
}:root {
    --primary: 75 162 227;
    --primary-light: 75 162 227;
    --primary-dark: 75 162 227;
    --background-light: 255 255 255;
    --background-dark: 10 12 15;
    --gray-50: 245 247 249;
    --gray-100: 240 242 244;
    --gray-200: 224 227 229;
    --gray-300: 208 210 212;
    --gray-400: 160 163 165;
    --gray-500: 114 116 118;
    --gray-600: 82 84 86;
    --gray-700: 64 67 69;
    --gray-800: 39 42 44;
    --gray-900: 25 27 29;
    --gray-950: 12 15 17;
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperAssetsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewDefining AssetsRegistering AssetsCompiling AssetsDigging DeeperAssetsLearn how to extend or add additional functionality to Nova.​Overview
Assets allow you to extend or add additional functionality to Nova without the overhead of cards or resource tools. For example, you may wish to override a custom error component to match your branding or intercept Inertia interactions and provide additional data to routes.
​Defining Assets
Assets may be generated using the nova:asset Artisan command. By default, all new assets will be placed in the nova-components directory of your application. When generating an asset using the nova:asset command, the asset name you pass to the command should follow the Composer vendor/package format:
CopyAsk AIphp artisan nova:asset acme/analytics

When generating an asset, Nova will prompt you to install the assets NPM dependencies, compile its dependencies, and update your application’s composer.json file. All custom assets are registered with your application as a Composer “path” repository.
Nova assets include all of the scaffolding necessary to build your asset. Each asset even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Assets
Nova assets are automatically loaded through the use of Laravel’s auto-loader, so no additional registration is required.
​Compiling Assets
Your Nova asset contains a webpack.mix.js file, which is generated when Nova creates your custom asset. You may build your custom asset using the NPM dev and prod commands:
CopyAsk AI# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod

In addition, you may run the NPM watch command to auto-compile your assets when they are changed:
CopyAsk AInpm run watch
Was this page helpful?YesNoCSS / JavaScriptLocalizationAssistantResponses are generated using AI and may contain mistakes.Laravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy Policyxgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"9058\",\"static/chunks/9058-fc5eb8705bf7a22c.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"1725\",\"static/chunks/d30757c7-56ff534f625704fe.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"7261\",\"static/chunks/7261-2b892dc828f6e161.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"3892\",\"static/chunks/3892-251b69e2384ed286.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"7417\",\"static/chunks/7417-548f041b716e378a.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"1953\",\"static/chunks/1953-46fbce29c74b759e.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"9095\",\"static/chunks/9095-5e8c25cebc4b2bd6.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"9779\",\"static/chunks/9779-7bb45d52151006b8.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"3619\",\"static/chunks/3619-2c24842c619fda67.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"2398\",\"static/chunks/2398-3c77a562bc9286bb.js?dpl=dpl_AqSNbrLei4TBJhjH6LCuTrHpv4ND\",\"1862\",\"static/chunks/1862-d7c7b8aab3b4ffe6.js?dpl=dpl_AqSNbrLei4TBJ