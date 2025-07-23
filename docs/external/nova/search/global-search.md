# Nova - Search/Global-Search

*Source: https://nova.laravel.com/docs/v5/search/global-search*

---

Global Search - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchGlobal SearchDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageTitle / Subtitle AttributesSubtitlesCustomizationLimiting Global Search ResultsGlobal Search DebounceCustom Avatars / CoversDisabling Global Search for a ResourceDisabling Global Search GloballySearchGlobal SearchLearn how to use Nova’s global search feature to search across all your resources.Nova not only allows you to search within specific resources and relationships, you may also globally search across all your resources using the global search input located within the top-navigation bar of the Nova administration panel:

You can focus the global search input by pressing / (forward slash) on your keyboard. Pressing ESC (the escape key) will also close the global search input.
​Title / Subtitle Attributes
When a resource is shown within the search results, the results will display the “title” of the resource. For example, a User resource may specify the name attribute as its title. Then, when the resource is shown within the global search results, that attribute will be displayed.
To customize the “title” attribute of a resource, you may define a title property or title method on the resource class:
PropertyMethodCopyAsk AInamespace App\Nova;

class Team extends Resource 
{
    /**
     * The single value that should be used to represent the resource when being displayed.
     *
     * @var string
     */
    public static $title = &#x27;name&#x27;;
}

You may also display resource’s “avatar” next to the title in the search result by adding an Avatar field to the resource.
​Subtitles
You may also display a smaller “subtitle” attribute within the global search results. The subtitle will be placed directly under the title attribute. In this screenshot, you can see that the Post resource’s author is displayed as a subtitle, allowing quick identification of who wrote a given post:

To define a resource’s subtitle, you should override the subtitle method of the resource:
app/Nova/Post.phpCopyAsk AI/**
 * Get the search result subtitle for the resource.
 *
 * @return string
 */
public function subtitle()
{
    return &quot;Author: {$this-&gt;user-&gt;name}&quot;;
}

If your subtitle accesses information on a related resource, you should consider adding the related resource to your resource’s eager load array.
​Customization
​Limiting Global Search Results
You can limit the number of results that are returned via global search for a given resource by overriding the globalSearchResults property on the resource:
app/Nova/Post.phpCopyAsk AI/**
 * The maximum number of results to include when searching globally.
 *
 * @var int
 */
public static $globalSearchResults = 5;

​Global Search Debounce
You can configure the debounce timing of the global search field using the Nova::globalSearchDebounce method. Normally, this method should be called from within your application’s NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void 
{
    parent::boot();
    
    Nova::globalSearchDebounce(1); // 1 second
}

​Custom Avatars / Covers
If you are building a custom field that you would like to serve as the “avatar image” / cover art for global search results, your field should implement the Laravel\Nova\Contracts\Cover interface. This interface requires you to define a resolveThumbnailUrl method, which should return the URL of your desired “cover art”:
app/Nova/Team.phpCopyAsk AInamespace App\Nova;

class Team extends Resource 
{
    /**
     * Resolve the thumbnail URL for the field.
     *
     * @return string|null
     */
    public function resolveThumbnailUrl()
    {
        return &#x27;https://www.example.com/avatar/&#x27;.md5(strtolower($this-&gt;value)).&#x27;?s=300&#x27