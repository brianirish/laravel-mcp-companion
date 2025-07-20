# Nova - Customization/Resource-Tools

*Source: https://nova.laravel.com/docs/v5/customization/resource-tools*

---

Resource Tools - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperResource ToolsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperResource ToolsLearn how to build custom tools for your Nova resources.​Overview
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
     * @return $this
     */
    public function issuesRefunds()
    {
        return $this-&gt;withMeta([&#x27;issuesRefunds&#x27; =&gt; true]);
    }
}

​Accessing Tool Options
Your resource tool’s Tool.vue component receives several Vue props: resourceName, resourceId, and panel. The resourceId property contains the primary key of the resource the tool is currently attached to. You may use the resourceId when making requests to your controllers. The panel prop provides access to any tool options that may be available via the fields:
CopyAsk AIconst issuesRefunds = this.panel.fields[0].issuesRefunds;

​Dynamic Options
Resource tools also offer the ability to dynamically set options on the tool without a setter method by simple calling the desired option as a method when registering the tool. If called with an argument, it will be set as the option’s value:
CopyAsk AIuse Acme\StripeInspector\StripeInspector;
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

        StripeInspector::make()-&gt;issuesRefunds(),
    ];
}

​Building Tools
Each tool generated by Nova includes its own service provider and “tool” class. Using the stripe-inspector tool as an example, the tool class will be located at src/StripeInspector.php.
The tool’s service provider is also located within the src directory of the tool, and is registered within the extra section of your tool’s composer.json file so that it will be auto-loaded by Laravel.
​Routing
Often, you will need to define Laravel routes that are called by your tool. When Nova generates your tool, it creates a routes/api.php routes file. If needed, you may use this file to define any routes your tool requires.
All routes within this file are automatically defined inside a route group by your tool’s ToolServiceProvider. The route group specifies that all routes within the group should receive a /nova-vendor/tool-name prefix, where tool-name is the “kebab-case” name of your tool. So, for example, /nova-vendor/stripe-inspector. You are free to modify this route group definition, but take care to make sure your Nova tool will co-exist with other Nova packages.
When building routes for your tool, you should always add authorization to these routes using Laravel gates or policies.
​Assets
When Nova generates your tool, resources/js and resources/css directories are generated for you. These directories contain your tool’s JavaScript and CSS. The primary files of interest in these directories are: resources/js/components/Tool.vue and resources/css/tool.css.
The Tool.vue file is a single-file Vue component that contains your tool’s front-end. From this file, you are free to build your tool however you want. Your tool can make HTTP requests using Axios via Nova.request.
​Registering Assets
Your Nova tool’s service provider registers your tool’s compiled assets so that they will be available to the Nova front-end:
nova-components/StripeInspector/src/ToolServiceProvider.phpCopyAsk AIuse Laravel\Nova\Nova;
use Laravel\Nova