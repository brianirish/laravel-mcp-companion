# Nova - Customization/Cards

*Source: https://nova.laravel.com/docs/v5/customization/cards*

---

Cards - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperCardsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperCardsLearn how to build custom cards for your Nova application.​Overview
Cards are similar to resource tools, but are small, miniature tools that are typically displayed at the top of your dashboard, resource index, or resource detail pages. In fact, if you have used Nova metrics, you have already seen Nova cards. Custom Nova cards allow you to build your own, metric-sized tools.
​Defining Cards
Cards may be generated using the nova:card Artisan command. By default, all new cards will be placed in the nova-components directory of your application. When generating a card using the nova:card command, the card name you pass to the command should follow the Composer vendor/package format. So, if we were building a traffic analytics card, we might run the following command:
CopyAsk AIphp artisan nova:card acme/analytics

When generating a card, Nova will prompt you to install the card’s NPM dependencies, compile its assets, and update your application’s composer.json file. All custom cards are registered with your application as a Composer “path” repository.
Nova cards include all of the scaffolding necessary to build your card. Each card even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Cards
Nova cards may be registered in your resource’s cards method. This method returns an array of cards available to the resource. To register your card, add your card to the array of cards returned by this method:
app/Nova/Post.phpCopyAsk AInamespace App\Nova;

use Acme\Analytics\Analytics;
use Laravel\Nova\Http\Requests\NovaRequest;

class Post extends Resource
{
    /**
     * Get the cards available for the resource.
     *
     * @return array&lt;int, \Laravel\Nova\Card&gt;
     */
    public function cards(NovaRequest $request)
    {
        return [
            new Analytics,
        ];
    }
}

​Authorization
If you would like to only expose a given card to certain users, you may invoke the canSee method when registering your card. The canSee method accepts a closure which should return true or false. The closure will receive the incoming HTTP request:
app/Nova/Post.phpCopyAsk AIuse Acme\Analytics\Analytics;

// ...

/**
 * Get the cards available for the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Card&gt;
 */
public function cards(NovaRequest $request)
{
    return [
        (new Analytics)-&gt;canSee(function ($request) {
            return false;
        }),
    ];
}

​Card Options
Often, you will need to allow the consumer’s of your card to customize run-time configuration options on the card. You may do this by exposing methods on your card class. These methods may call the card’s underlying withMeta method to add information to the card’s metadata, which will be available within your Card.vue component. The withMeta method accepts an array of key / value options:
nova-components/Analytics/src/Analytics.phpCopyAsk AInamespace Acme\Analytics;

use Laravel\Nova\Card;

class Analytics extends Card
{
    // ...

    /**
     * Indicates that the analytics should show current visitors.
     *
     * @return $this
     */
    public function currentVisitors()
    {
        return $this-&gt;withMeta([&#x27;currentVisitors&#x27; =&gt; true]);
    }
}

After registering your custom card, don’t forget to actually call any custom option methods you defined:
CopyAsk AI(new Acme\Analytics\Analytics)-&gt;currentVisitors(),

​Accessing Card Options
Your card’s Card.vue component receives a card Vue prop. This property provides access to any card options that may be available on the card:
CopyAsk AIconst currentVisitors = this.card.currentVisitors;

​Building Cards
Each card generated by Nova includes its own service provider and “card” class. Using the analytics card as an example, the card class will be located at src/Analytics.php.
The card’s service provider is also located within the src directory of the card, and is registered in the extra section of your card’s composer.json file so that it will be auto-loaded by Laravel.
​Routing
Often, you will need to define Laravel routes that are called by your card via Nova.request. When Nova generates your card, it creates a routes/api.php routes file. If needed, you may use this file to define any routes your card requires.
All routes within this file are automatically defined inside a route group by your card’s CardServiceProvider. The route group specifies that all routes within the group should receive a /nova-vendor/card-name prefix, where card-name is the “kebab-case” name of your card. So, for example, /nova-vendor/analytics. You are free to modify this route group definition, but take care to make sure your Nova card will co-exist with other Nova packages.
When building routes for your card, you should always add authorization to these routes using Laravel gates or policies.
​Assets
When Nova generates your card, resources/js and resources/css directories are generated for you. These directories contain your card’s JavaScript and CSS stylesheets. The primary files of interest in these directories are: resources/js/components/Card.vue and resources/css/card.css.
The Card.vue file is a single-file Vue component that contains your card’s front-end. From this file, you are free to build your card however you want. Your card can make HTTP requests using Axios via Nova.request.
​Registering Assets
Your Nova card’s service provider registers your card’s compiled assets so that they will be available to the Nova front-end:
nova-components/Analytics/src/CardServiceProvider.phpCopyAsk AI/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    $this-&gt;app-&gt;booted(function () {
        $this-&gt;routes();
    });

    Nova::serving(function (ServingNova $event) {
        Nova::mix(&#x27;acme-analytic&#x27;, __DIR__.&#x27;/../dist/mix-manifest.json&#x27;);

        Nova::translations(__DIR__.&#x27;/../resources/lang/en/card.json&#x27;);
    });
}

Alternatively you can also explicitly register script and style using the following code:
CopyAsk AINova::serving(function (ServingNova $event) {
-   Nova::mix(&#x27;acme-analytic&#x27;, __DIR__.&#x27;/../dist/mix-manifest.json&#x27;);
+   Nova::script(&#x27;acme-analytic&#x27;, __DIR__.&#x27;/../dist/js/card.js&#x27;);
+   Nova::style(&#x27;acme-analytic&#x27;, __DIR__.&#x27;/../dist/css/card.css&#x27;);
    Nova::translations(__DIR__.&#x27;/../resources/lang/en/card.json&#x27;);
});

Your component is bootstrapped and registered in the resources/js/card.js file. You are free to modify this file or register additional components here as needed.
​Compiling Assets
Your Nova resource card contains a webpack.mix.js file, which is generated when Nova creates y