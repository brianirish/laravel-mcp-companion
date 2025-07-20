# Nova - Customization/Tools

*Source: https://nova.laravel.com/docs/v5/customization/tools*

---

Tools - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperToolsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperToolsLearn how to build custom tools for your Nova application.​Overview
Sometimes, your business may need additional functionality that isn’t provided by Nova. For this reason, Nova allows you to build custom tools and add them to the Nova sidebar. Nova tools are incredibly customizable, as they primarily consist of a single-file Vue component that is totally under your control. Within your Vue component, you are free to make HTTP requests to any controller within your application.
​Defining Tools
Custom tools may be generated using the nova:tool Artisan command. By default, all new tools will be placed in the nova-components directory of your application. When generating a tool using the nova:tool command, the tool name you pass to the command should follow the Composer vendor/package format. So, if we were building a price tracker tool, we might run the following command to generate our tool:
CopyAsk AIphp artisan nova:tool acme/price-tracker

When generating a tool, Nova will prompt you to install the tool’s NPM dependencies, compile its assets, and update your application’s composer.json file. All custom tools are registered with your application as a Composer “path” repository.
Nova tools include all of the scaffolding necessary to build your tool. Each tool even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Tools
Nova tools may be registered in your application’s App/Providers/NovaServiceProvider class. Your service provider contains a tools method, which returns an array of tools. To register your tool, simply add it to the list of tools returned by this method. For example, if you created a Nova tool named acme/price-tracker, you may register the tool like so:
app/Nova/NovaServiceProvider.phpCopyAsk AIuse Acme\PriceTracker\PriceTracker;

// ..

/**
 * Get the tools that should be listed in the Nova sidebar.
 */
public function tools(): array
{
    return [
        new PriceTracker,
    ];
}

​Authorization
If you would like to only expose a given tool to certain users, you may chain the canSee method onto your tool’s registration. The canSee method accepts a Closure which should return true or false. The Closure will receive the incoming HTTP request:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Acme\PriceTracker\PriceTracker;

// ...

/**
 * Get the tools that should be listed in the Nova sidebar.
 */
public function tools(): array
{
    return [
        (new PriceTracker)-&gt;canSee(function ($request) {
            return false;
        }),
    ];
}

​Building Tools
Each tool generated by Nova includes its own service provider and “tool” class. Using the price-tracker tool as an example, the tool class will be located at src/PriceTracker.php. The tool class must be registered with your application’s NovaServiceProvider as previously noted.
The tool’s service provider is also located within the src directory of the tool, and is registered within the extra section of your tool’s composer.json file so that it will be auto-loaded by Laravel.
​Routing
Often, you will need to define Laravel routes that are called by your tool. When Nova generates your tool, it creates routes/inertia.php and routes/api.php route files.
The routes/inertia.php file is tasked with rendering your tool via Inertia, while the routes/api.php file may be used to define any routes that your Inertia based tool will be making requests to in order to gather additional data or perform additional tasks.
All routes within the routes/api.php file are automatically defined inside a route group by your tool’s ToolServiceProvider. The route group specifies that all “API routes”, which will typically be invoked from the client via Nova.request, should receive a /nova-vendor/tool-name URL prefix, where tool-name is the “kebab-case” name of your tool.
Similarly, routes within the routes/inertia.php file are also placed within a route group that prefixes all of the routes within the file with the name of your tool.
You are free to modify this route group definition, but you should ensure your Nova tool will easily co-exist with other Nova packages.
​Routing Authorization
Your Nova tool is generated with an Authorize middleware. You should not typically need to modify this middleware, as it automatically determines whether the authenticated user can “see” the tool before it processes any requests to routes within your tool’s route group; however, you are free to modify this middleware if needed.
​Navigation
Your Nova tool class contains a menu method. This method should return a custom menu that renders your tool’s left-side navigation links. You are free to customize this method as needed:
nova-components/PriceTracker/src/PriceTracker.phpCopyAsk AIuse Illuminate\Http\Request;
use Laravel\Nova\Menu\MenuSection;

// ...

/**
 * Build the menu that renders the navigation links for the tool.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return mixed
 */
public function menu(Request $request)
{
    return MenuSection::make(&#x27;Price Tracker&#x27;)
        -&gt;path(&#x27;/price-tracker&#x27;)
        -&gt;icon(&#x27;server&#x27;);
}

If you have customized Nova’s main sidebar menu, a link to your tool will not automatically display in Nova’s sidebar. You will need to manually define your tool’s menu inside your custom Nova::mainMenu callback.
​Sidebar Icons
Nova utilizes the free Heroicons icon set by Steve Schoger. Therefore, you may simply specify the name of one of these icons when providing the icon name to the icon method.
​Assets
When Nova generates your tool, resources/js and resources/css directories are generated for you. These directories contain your tool’s JavaScript and CSS. The primary files of interest in these directories are: resources/js/components/Tool.vue and resources/css/tool.css.
The Tool.vue file is a single-file Vue component that contains your tool’s front-end. From this file, you are free to build your tool however you want. Your tool can make HTTP requests using Axios via Nova.request.
​Registering Assets
Your Nova tool class contains a boot method. This method is executed when the tool is registered and available. By default, this method registers your tool’s compiled assets so that they will be available to the Nova front-end:
nova-components/PriceTracker/src/ToolServiceProvider.phpCopyAsk AIuse Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Perform any tasks that need to happen on tool registration.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::mix(&#x27;price-tracker&#x27;, __DIR__.&#x27;/../dist/mix-manifest.json&#x27;);
    });
}

​JavaScript Bootstrap &amp; Components
Your component is boo