# Nova - Customization/Dashboards

*Source: https://nova.laravel.com/docs/v5/customization/dashboards*

---

Dashboards - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperDashboardsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperDashboardsNova dashboards provide a convenient way to build information overview pages that contain a variety of metrics and cards.​Overview
Nova dashboards provide a convenient way to build information overview pages that contain a variety of metrics and cards.

​Default Dashboard
Nova ships with a default App\Nova\Dashboards\Main dashboard class containing a cards method. You can customize which cards are present on the default dashboard via this method:
app/Nova/Dashboards/Main.phpCopyAsk AInamespace App\Nova\Dashboards;

use Laravel\Nova\Cards\Help;
use Laravel\Nova\Dashboards\Main as Dashboard;

class Main extends Dashboard
{
    /**
     * Get the cards that should be displayed on the Nova dashboard.
     *
     * @return array&lt;int, \Laravel\Nova\Card&gt;
     */
    public function cards(): array
    {
        return [
            new Help,
        ];
    }
}

More information regarding dashboard metrics can be found within our documentation on metrics.
​Defining Dashboards
Custom dashboards may be generated using the nova:dashboard Artisan command. By default, all new dashboards will be placed in the app/Nova/Dashboards directory:
CopyAsk AIphp artisan nova:dashboard UserInsights

Once your dashboard class has been generated, you’re ready to customize it. Each dashboard class contains a cards method. This method should return an array of card or metric classes:
app/Nova/Dashboards/UserInsights.phpCopyAsk AInamespace App\Nova\Dashboards;

use Laravel\Nova\Dashboard;
use App\Nova\Metrics\TotalUsers;
use App\Nova\Metrics\UsersOverTime;

class UserInsights extends Dashboard
{
    /**
     * Get the cards for the dashboard.
     *
     * @return array&lt;int, \Laravel\Nova\Card&gt;
     */
    public function cards(): array
    {
        return [
            TotalUsers::make(),
            UsersOverTime::make(),
        ];
    }
}

​Dashboard Names
By default, Nova will use the dashboard’s class name to determine the displayable name of your dashboard that should be placed in the left-side navigation bar. You may customize the name of the dashboard displayed in the left-side navigation bar by overriding the name method within your dashboard class:
app/Nova/Dashboards/UserInsights.phpCopyAsk AI/**
 * Get the displayable name of the dashboard.
 *
 * @return \Stingable|string
 */
public function name()
{
    return &#x27;User Insights&#x27;;
}

​Dashboard URI Keys
If you need to change the URI of the dashboard, you may override the dashboard class’ uriKey method. Of course, the URI represents the browser location that Nova will navigate to in when you click on the dashboard link in the left-side navigation bar:
app/Nova/Dashboards/UserInsights.phpCopyAsk AI/**
 * Get the URI key of the dashboard.
 *
 * @return string
 */
public function uriKey()
{
    return &#x27;user-insights-improved&#x27;;
}

​Registering Dashboards
To register a dashboard, add the dashboard to the array returned by the dashboards method of your application’s App/Providers/NovaServiceProvider class. Once you have added the dashboard to this method, it will become available for navigation in Nova’s left-side navigation bar:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Nova\Dashboards\Main;
use App\Nova\Dashboards\UserInsights;

// ...

/**
 * Get the dashboards that should be listed in the Nova sidebar.
 *
 * @return array&lt;int, \Laravel\Nova\Dashboard&gt;
 */
protected function dashboards(): array
{
    return [
        Main::make(),
        UserInsights::make(),
    ];
}

​Customizing Dashboard Menus
You can customize the dashboard’s menu by defining a menu method on your dashboard class:
app/Nova/Dashboards/UserInsights.phpCopyAsk AIuse Illuminate\Http\Request;

// ...

/**
 * Get the menu that should represent the dashboard.
 *
 * @return \Laravel\Nova\Menu\MenuItem
 */
public function menu(Request $request)
{
    return parent::menu($request)-&gt;withBadge(function () {
        return &#x27;NEW!&#x27;;
    });
}

Please refer to the documentation on menu customization for more information.
​Refreshing Dashboard Metrics
Occasionally, you may wish to refresh all the metrics’ values inside your dashboard. You may do this by enabling the refresh button by using the showRefreshButton method on the dashboard instance:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Nova\Dashboards\Main;
use App\Nova\Dashboards\UserInsights;

// ...

/**
 * Get the dashboards that should be listed in the Nova sidebar.
 *
 * @return array&lt;int, \Laravel\Nova\Dashboard&gt;
 */
protected function dashboards(): array
{
    return [
        Main::make(),
        UserInsights::make()-&gt;showRefreshButton(),
    ];
}

​Authorization
If you would like to only expose a given dashboard to certain users, you may invoke the canSee method when registering your dashboard. The canSee method accepts a closure which should return true or false. The closure will receive the incoming HTTP request:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Models\User;
use App\Nova\Dashboards\Main;
use App\Nova\Dashboards\UserInsights;

// ...

/**
 * Get the dashboards that should be listed in the Nova sidebar.
 *
 * @return array&lt;int, \Laravel\Nova\Dashboard&gt;
 */
protected function dashboards(): array
{
    return [
        Main::make(),
        UserInsights::make()-&gt;canSee(function ($request) {
            return $request-&gt;user()-&gt;can(&#x27;viewUserInsights&#x27;, User::class);
        }),
    ];
}

In the example above, we are using Laravel’s Authorizable trait’s can method on our User model to determine if the authorized user is authorized for the viewUserInsights action. However, since proxying to authorization policy methods is a common use-case for canSee, you may use the canSeeWhen method to achieve the same behavior. The canSeeWhen method has the same method signature as the Illuminate\Foundation\Auth\Access\Authorizable trait’s can method:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Models\User;
use App\Nova\Dashboards\Main;
use App\Nova\Dashboards\UserInsights;

// ...

/**
 * Get the dashboards that should be listed in the Nova sidebar.
 *
 * @return array&lt;int, \Laravel\Nova\Dashboard&gt;
 */
protected function dashboards(): array
{
    return [
        Main::make(),
        UserInsights::make()-&gt;canSeeWhen(&#x27;viewUserInsights&#x27;, User::class),
    ];
}
Was this page helpful?YesNoRegistering MetricsMenusOn this pageOverviewDefault DashboardDefining DashboardsDashboard NamesDashboard URI KeysRegistering DashboardsCustomizing Dashboard MenusRefreshing Dashboard MetricsAuthorizationLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may co