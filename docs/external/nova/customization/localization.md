# Nova - Customization/Localization

*Source: https://nova.laravel.com/docs/v5/customization/localization*

---

Localization - Laravel Nova
              document.documentElement.style.setProperty('--font-family-headings-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-headings-custom', '');
              document.documentElement.style.setProperty('--font-family-body-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-body-custom', '');
            
    (function() {
      try {
        var bannerKey = "nova-laravel-bannerDismissed";
        var bannerContent = undefined;
        
        if (!bannerContent) {
          document.documentElement.setAttribute('data-banner-state', 'hidden');
          return;
        }
        
        var dismissedValue = localStorage.getItem(bannerKey);
        var shouldShowBanner = !dismissedValue || dismissedValue !== bannerContent;
        
        document.documentElement.setAttribute('data-banner-state', shouldShowBanner ? 'visible' : 'hidden');
      } catch (e) {
        document.documentElement.setAttribute('data-banner-state', 'hidden');
      }
    })();
  :root{--font-inter:'Inter', 'Inter Fallback';--font-jetbrains-mono:'JetBrains Mono', 'JetBrains Mono Fallback'}((e,i,s,u,m,a,l,h)=>{let d=document.documentElement,w=["light","dark"];function p(n){(Array.isArray(e)?e:[e]).forEach(y=>{let k=y==="class",S=k&&a?m.map(f=>a[f]||f):m;k?(d.classList.remove(...S),d.classList.add(a&&a[n]?a[n]:n)):d.setAttribute(y,n)}),R(n)}function R(n){h&&w.includes(n)&&(d.style.colorScheme=n)}function c(){return window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}if(u)p(u);else try{let n=localStorage.getItem(i)||s,y=l&&n==="system"?c():n;p(y)}catch(n){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true):root {
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
  }h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperLocalizationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperLocalizationLearn how to localize your Nova application.​Overview
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

In addition, you should also override the label and singularLabel methods on the related resource:
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

​Filters
Filter names may be localized by overriding the name method on the filter class:
app/Nova/Filters/~Filter.phpCopyAsk AI/**
 * Get the displayable name of the filter.
 *
 * @return string
 */
public function name()
{
    return __(&#x27;Admin Users&#x27;);
}

​Lenses
Lens names may be localized by overriding the name method on the lens class:
app/Nova/Lenses/~Lens.phpCopyAsk AI/**
 * Get the displayable name of the lens.
 *
 * @return string
 */
public function name()
{
    return __(&#x27;Most Valuable Users&#x27;);
}

​Actions
Action names may be localized by overriding the name method on the action class:
app/Nova/Actions/~Action.phpCopyAsk AI/**
 * Get the displayable name of the action.
 *
 * @return string
 */
public function name()
{
    return __(&#x27;Email Account Profile&#x27;);
}

​Metrics
Metric names may be localized by overriding the name method on the metric class:
app/Nova/Metrics/~Metric.phpCopyAsk AI/**
 * Get the displayable name of the metric.
 *
 * @return string
 */
public function name()
{
    return __(&#x27;Total Users&#x27;);
}

​Frontend
To propagate your localizations to the frontend, you should call the Nova::translations method within your NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::translations($pathToFile);
    });
}

You may also pass an array of key / value pairs representing each localization:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::translations([
            &#x27;Total Users&#x27; =&gt; &#x27;Total Users&#x27;
        ]);
    });
}

As in Laravel, you may use the __ helper within your custom Vue components to access these translations. To accomplish this, add the following mixins to your Inertia page component or Vue component:
Option APIComposition APICopyAsk AI&lt;template&gt;
  &lt;h2&gt;{{ __(&#x27;Total Users&#x27;) }}&lt;/h2&gt;
&lt;/template&gt;

&lt;script&gt;
import { Localization } from &#x27;laravel-nova&#x27;

export default {
  mixins: [Localization]

  // ...
}
&lt;/script&gt;
Was this page helpful?YesNoAssetsStubsOn this pageOverviewCreating New Localization FilesUser Locale OverridesResourcesFieldsRelationshipsFiltersLensesActionsMetricsFrontendLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0