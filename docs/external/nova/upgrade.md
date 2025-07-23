# Nova - Upgrade

*Source: https://nova.laravel.com/docs/v5/upgrade*

---

Upgrade Guide - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedUpgrade GuideDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageDependency UpgradesServerClientUpdating Composer DependenciesUpdating Assets and TranslationsUpdating Third-Party Nova Packages ​Upgrading Authentication FeaturesUpdating Nova Components (Custom Tool, Cards, Fields, Filters)Inertia 2 CompatibilityReplacing form-backend-validationMedium Impact ChangesForm Abandonment (Using Browser Navigation)Algolia Place Field RemovedLow Impact ChangesUpdate Published StubsGet StartedUpgrade GuideLearn how to upgrade your Laravel Nova installation to the latest version.​Dependency Upgrades
Nova’s upstream dependencies have been upgraded. You will find a complete list of our dependency upgrades below:
​Server

PHP 8.1+
Laravel Framework 10.34+ and 11.0+
Inertia Laravel 1.3+ and 2.0+
Replaced laravel/ui with laravel/fortify v1.21+
Removed doctrine/dbal

​Client

Update to @inertiajs/vue3 v2
Update to Heroicons v2
Update to trix v2
Remove deprecated form-backend-validation
Remove deprecated places.js

​Updating Composer Dependencies
You should update your laravel/nova dependency to ^5.0 in your application’s composer.json file:
composer.jsonCopyAsk AI    &quot;require&quot;: {
-       &quot;laravel/nova&quot;: &quot;^4.0&quot;,
+       &quot;laravel/nova&quot;: &quot;^5.0&quot;,
    }

Next, install your updated Composer dependencies:
CopyAsk AIcomposer update mirrors

composer update

​Updating Assets and Translations
Next, you should update your application’s Nova assets and translation files. To get started, you may run the following commands to update your assets and translations.
You may wish to store a copy of your current translation file before running this command so you can easily port any custom translations back into the new file after running these commands.:
CopyAsk AIphp artisan vendor:publish --tag=nova-assets --force
php artisan vendor:publish --tag=nova-lang --force

​Updating Third-Party Nova Packages ​
If your application relies on Nova tools or packages developed by third-parties, it is possible that these packages are not yet compatible with Nova 5.0 and will require an update from their maintainers.
​Upgrading Authentication Features
Next, you will need to update your Nova configuration file. Ensure that the api_middleware configuration option within your application’s nova configuration file appears as follows:
config/nova.phpCopyAsk AIreturn [

    // ...

    &#x27;api_middleware&#x27; =&gt; [
        &#x27;nova&#x27;,
        \Laravel\Nova\Http\Middleware\Authenticate::class,
        // \Laravel\Nova\Http\Middleware\EnsureEmailIsVerified::class,
        \Laravel\Nova\Http\Middleware\Authorize::class,
    ],

];

Next, update the register method in your application’s App\Providers\NovaServiceProvider class to call the parent’s register method. The parent::register() method should be invoked before any other code in the method:
app/Nova/NovaServiceProvider.phpCopyAsk AI/**
 * Register any application services.
 */
public function register(): void 
{
    parent::register();

    //
}

​Updating Nova Components (Custom Tool, Cards, Fields, Filters)
​Inertia 2 Compatibility
In Nova 5, Nova’s frontend JavaScript now utilizes Inertia.js 2.x, which will affect any projects that directly import from @inertiajs/inertia or @inertiajs/inertia-vue3. You should inspect your custom components and packages to ensure all references have been updated as suggested in Inertia’s upgrade guide.
CopyAsk AI&lt;script&gt;
-import { usePage } from &#x27;@inertiajs/inertia-vue3&#x27;
-import { Inertia } from &#x27;@inertiajs/inertia&#x27;
+import { router as Inertia, usePage } from &#x27;@inertiajs/vue3&#x27;

// ...

&lt;/script&gt;

​Replacing form-backend-validation
The form-backend-validation repository h