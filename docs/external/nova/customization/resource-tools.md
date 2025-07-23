# Nova - Customization/Resource-Tools

*Source: https://nova.laravel.com/docs/v5/customization/resource-tools*

---

Resource Tools - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperResource ToolsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewDefining ToolsRegistering ToolsAuthorizationTool OptionsAccessing Tool OptionsDynamic OptionsBuilding ToolsRoutingAssetsRegistering AssetsCompiling AssetsDigging DeeperResource ToolsLearn how to build custom tools for your Nova resources.​Overview
Resource tools are very similar to custom tools; however, instead of being listed in the Nova sidebar, resource tools are displayed on a particular resource’s detail page. Like Nova tools, resource tools are incredibly customizable, and primarily consist of a single-file Vue component that is totally under your control.
​Defining Tools
Resource tools may be generated using the nova:resource-tool Artisan command. By default, all new tools will be placed in the nova-components directory of your application. When generating a tool using the nova:resource-tool command, the tool name you pass to the command should follow the Composer vendor/package format. So, if we were building a Stripe inspector tool, we might run the following command:
CopyAsk AIphp artisan nova:resource-tool acme/stripe-inspector

When generating a tool, Nova will prompt you to install the tool’s NPM dependencies, compile its assets, and update your application’s composer.json file. All custom tools are registered with your application as a Composer “path” repository.
Nova resource tools include all of the scaffolding necessary to build your tool. Each tool even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Tools
Nova resource tools may be registered in your resource’s fields method. This method returns an array of fields and tools available to the resource. To register your resource tool, add your tool to the array of fields returned by this method:
app/Nova/~Resource.phpCopyAsk AIuse Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field|\Laravel\Nova\ResourceTool&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()-&gt;sortable(),

        StripeInspector::make(),
    ];
}

​Authorization
If you would like to only expose a given tool to certain users, you may invoke the canSee method when registering your tool. The canSee method accepts a closure which should return true or false. The closure will receive the incoming HTTP request:
app/Nova/~Resource.phpCopyAsk AIuse Acme\StripeInspector\StripeInspector;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field|\Laravel\Nova\ResourceTool&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make(&#x27;ID&#x27;, &#x27;id&#x27;)-&gt;sortable(),

        StripeInspector::make()-&gt;canSee(function ($request) {
            return $request-&gt;user()-&gt;managesBilling();
        }),
    ];
}

​Tool Options
Often, you will need to allow the consumer’s of your tool to customize run-time configuration options on the tool. You may do this by exposing methods on your tool class. These methods may call the tool’s underlying withMeta method to add information to the tool’s metadata, which will be available within your Tool.vue component. The withMeta method accepts an array of key / value options:
nova-components/StripeInspector/src/StripeInspector.phpCopyAsk AInamespace Acme\StripeInspector;

use Laravel\Nova\ResourceTool;

class StripeInspector extends ResourceTool
{
    // ...

    /**
     * Indicates that the Stripe inspector should allow refunds.
     *
     * @re