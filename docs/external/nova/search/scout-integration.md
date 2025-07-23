# Nova - Search/Scout-Integration

*Source: https://nova.laravel.com/docs/v5/search/scout-integration*

---

Scout Integration - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchScout IntegrationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageCustomizing Scout SearchesLimiting Scout Search ResultsDisabling Scout SearchSearchScout IntegrationIntegrate Laravel Scout with your Nova resources.By default, Nova searches your resources using the resource’s database columns.
However, this can become inefficient and lacks support for robust fuzzy matching capabilities provided by dedicated search engines.
For this reason, Nova integrates seamlessly with Laravel Scout. When the Laravel\Scout\Searchable trait is attached to a model associated with a Nova resource, Nova will automatically begin using Scout when performing searches against that resource. There is no other configuration required.
​Customizing Scout Searches
If you would like to call methods on the Laravel\Scout\Builder instance before it executes your search query against your search engine, you may override the scoutQuery method on your resource:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Scout\Builder as ScoutBuilder;

class User extends Resource 
{
    // ... 

    /**
     * Build a Scout search query for the given resource.
     */
    public static function scoutQuery(NovaRequest $request, ScoutBuilder $query): ScoutBuilder
    {
        return $query;
    }
}

​Limiting Scout Search Results
You can customize the amount of search results returned from your Scout search engine by defining the scoutSearchResults property on the resource class that is associated with the Scout searchable model:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource 
{
    // ...

    /**
     * The number of results to display when searching the resource using Scout.
     *
     * @var int
     */
    public static $scoutSearchResults = 200;
}

​Disabling Scout Search
You may disable Scout search support for a specific resource by defining a usesScout method on the resource class. When Scout search support is disabled, simple database queries will be used to search against the given resource, even if the associated resource model includes the Scout Searchable trait:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource 
{
    /**
     * Determine if this resource uses Laravel Scout.
     *
     * @return bool
     */
    public static function usesScout()
    {
        return false;
    }
}
Was this page helpful?YesNoGlobal SearchDefining FiltersAssistantResponses are generated using AI and may contain mistakes.Laravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy Policyxgithubdiscordlinkedin(self.__next_f=self.__next_f||[]).push([0])self.__next_f.push([1,"1:\"$Sreact.fragment\"\n2:I[47132,[],\"\"]\n3:I[55983,[\"7261\",\"static/chunks/7261-1f4bcac893329b6b.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"9058\",\"static/chunks/9058-7f849e951ad85773.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"8039\",\"static/chunks/app/error-dad69ef19d740480.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\"],\"default\"]\n4:I[75082,[],\"\"]\n"])self.__next_f.push([1,"5:I[85506,[\"3473\",\"static/chunks/891cff7f-2ca7d0df884db9d0.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"4129\",\"static/chunks/7bf36345-5ba13855b95a82b2.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"1725\",\"static/chunks/d30757c7-d1a658b63aa94b97.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"803\",\"static/chunks/cd24890f-549fb4ba2f588ca6.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"7261\",\"static/chunks/7261-1f4bcac893329b6b.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"3892\",\"static/chunks/3892-7f882638e4a83cba.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"7417\",\"static/chunks/7417-548f041b716e378a.js?dpl=dpl_27CFEPFpTWdX7wUS4cAbtp2GmPdZ\",\"1953