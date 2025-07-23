# Nova - Customization/Localization

*Source: https://nova.laravel.com/docs/v5/customization/localization*

---

Localization - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperLocalizationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewCreating New Localization FilesUser Locale OverridesResourcesFieldsRelationshipsFiltersLensesActionsMetricsFrontendDigging DeeperLocalizationLearn how to localize your Nova application.​Overview
Nova may be fully localized using Laravel’s localization services. After running the nova:install command during installation. Your application will contain a lang/vendor/nova translation directory.
Within this directory, you may customize the en.json file or create a new JSON translation file for your language. In addition, the en directory contains a few additional validation translation lines that are utilized by Nova.
​Creating New Localization Files
To quickly create a new translation file for your language, you may execute the nova:translate Artisan command. This command will simply copy the default en.json translation file, allowing you to begin translating the strings into your own language:
CopyAsk AIphp artisan nova:translate es

​User Locale Overrides
Laravel Nova frontend libraries, including the browser, Numbro.js, Luxon, and other libraries will utilize the locale value available via app()-&gt;getLocale() by default. However, if your application is only using ISO 639-1 language codes (en), you may wish to consider migrating your languages to IETF language tags (en-US, en-GB) for wider support across the various frontend libraries used by Nova.
To map your existing locales to IETF language tags, you may use the Nova::userLocale method. Typically, you should invoke this method in the boot method of your application’s NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::userLocale(function () {
        return match (app()-&gt;getLocale()) {
            &#x27;en&#x27; =&gt; &#x27;en-US&#x27;,
            &#x27;de&#x27; =&gt; &#x27;de-DE&#x27;,
            default =&gt; null,
        };
    });
}

​Resources
Resource names may be localized by overriding the label and singularLabel methods on the resource class:
app/Nova/~Resource.phpCopyAsk AI/**
 * Get the displayable label of the resource.
 *
 * @return string
 */
public static function label()
{
    return __(&#x27;Posts&#x27;);
}

/**
 * Get the displayable singular label of the resource.
 *
 * @return string
 */
public static function singularLabel()
{
    return __(&#x27;Post&#x27;);
}

To customize labels for the resource’s create and update buttons, you may override the createButtonLabel and updateButtonLabel methods on the resource:
app/Nova/~Resource.phpCopyAsk AI/**
 * Get the text for the create resource button.
 *
 * @return string|null
 */
public static function createButtonLabel()
{
    return __(&#x27;Publish Post&#x27;);
}

/**
 * Get the text for the update resource button.
 *
 * @return string|null
 */
public static function updateButtonLabel()
{
    return __(&#x27;Save Changes&#x27;);
}

​Fields
Field names may be localized when you attach the field to your resource. The first argument to all fields is its display name, which you may customize. For example, you might localize the title of an email address field like so:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(__(&#x27;Email Address&#x27;), &#x27;email_address&#x27;),

​Relationships
Relationship field names may be customized by localizing the first argument passed to their field definition. The second and third arguments to Nova relationship fields are the relationship method name and the related Nova resource, respectively:
CopyAsk AIuse App\Nova\Post;
use Laravel\Nova\Fields\HasMany;

// ...

HasMany::make(__(&#x27;Posts&#x27;), &#x27;posts&#x27;, Post::class),

In additio