# Nova - Customization/Menus

*Source: https://nova.laravel.com/docs/v5/customization/menus*

---

Menus - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperMenusDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperMenusNova menus provide a convenient way to customize the main and user menus.​Overview
By default, Nova’s main left-side navigation menu displays all of your application’s dashboards, resources, and any custom tools you have registered.

When rendering the main menu, Nova will order your dashboards according to the order in which they are returned by the dashboards method within your application’s App\Providers\NovaServiceProvider class.
Nova will also automatically group your resources under the default “Resources” menu section according to the group property defined in the Resource class. In addition, any custom tools you have registered will be listed in the order they are defined within your application’s NovaServiceProvider.
​Customizing the Main Menu
While Nova’s default main menu is sufficient for most applications, there are times you may wish to completely customize the menu based on your own preferences. For that reason, Nova allows you to define your own main menu via the Nova::mainMenu method. Typically, this method should be invoked within the boot method of your application’s App\Providers\NovaServiceProvider class:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Illuminate\Http\Request;
use Laravel\Nova\Menu\Menu;
use Laravel\Nova\Menu\MenuItem;
use Laravel\Nova\Menu\MenuSection;
use Laravel\Nova\Nova;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::mainMenu(function (Request $request) {
        return [
            MenuSection::dashboard(Main::class)-&gt;icon(&#x27;chart-bar&#x27;),

            MenuSection::make(&#x27;Customers&#x27;, [
                MenuItem::resource(User::class),
                MenuItem::resource(License::class),
            ])-&gt;icon(&#x27;user&#x27;)-&gt;collapsable(),

            MenuSection::make(&#x27;Content&#x27;, [
                MenuItem::resource(Series::class),
                MenuItem::resource(Release::class),
            ])-&gt;icon(&#x27;document-text&#x27;)-&gt;collapsable(),
        ];
    });
}


​Customizing the User Menu
Nova also allows you to customize the “user” menu found in the top-right navigation area. You can customize Nova’s user menu by calling the Nova::userMenu method. This method is typically invoked within the boot method of your application’s App\Providers\NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Illuminate\Http\Request;
use Laravel\Nova\Menu\Menu;
use Laravel\Nova\Menu\MenuItem;
use Laravel\Nova\Nova;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::userMenu(function (Request $request, Menu $menu) {
        if ($request-&gt;user()-&gt;subscribed()) {
            $menu-&gt;append(
                MenuItem::make(&#x27;Subscriber Dashboard&#x27;)
                    -&gt;path(&#x27;/subscribers/dashboard&#x27;)
            );
        }

        $menu-&gt;prepend(
            MenuItem::make(
                &#x27;My Profile&#x27;,
                &quot;/resources/users/{$request-&gt;user()-&gt;getKey()}&quot;
            )
        );

        return $menu;
    });
}

By default, Nova is configured to display a “logout” link in the user menu. This link may not be removed.
Nova’s user menu only supports MenuItem objects. Using MenuSection or MenuGroup inside the user menu will throw an Exception.
​Appending / Prepending to the Menu
You may call the append and prepend methods on a Menu instance to prepend or append new items to the. These methods are typically most helpful when customizing the user menu, since you often do not want to completely replace the existing menu:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Illuminate\Http\Request;
use Laravel\Nova\Menu\Menu;
use Laravel\Nova\Menu\MenuItem;
use Laravel\Nova\Nova;

// ...

Nova::userMenu(function (Request $request, Menu $menu) {
    return $menu
        -&gt;append(MenuItem::externalLink(&#x27;API Docs&#x27;, &#x27;http://example.com&#x27;))
        -&gt;prepend(MenuItem::link(&#x27;My Profile&#x27;, &#x27;/resources/users/&#x27;.$request-&gt;user()-&gt;getKey()));
});

​Menu Sections
Menu sections represent a top-level navigation item and are typically displayed with an corresponding icon representing the types of items in the menu. You can create a new menu section by calling the MenuSection::make method. This method accepts the name of the menu section and array of menu groups / items that should be placed within the section:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Nova\Dashboards\Sales;
use App\Nova\Lenses\MostValuableUsers;
use App\Nova\License;
use App\Nova\Refund;
use App\Nova\User;

// ...

Nova::mainMenu(function (Request $request, Menu $menu) {
    return [
        MenuSection::make(&#x27;Business&#x27;, [
            MenuGroup::make(&#x27;Licensing&#x27;, [
                MenuItem::dashboard(Sales::class),
                MenuItem::resource(License::class),
                MenuItem::resource(Refund::class),
                MenuItem::externalLink(&#x27;Stripe Payments&#x27;, &#x27;https://dashboard.stripe.com/payments?status%5B%5D=successful&#x27;),
            ]),

            MenuGroup::make(&#x27;Customers&#x27;, [
                MenuItem::lens(User::class, MostValuableUsers::class),
            ]),
        ]),
    ];
});

Instead of displaying a list of links, you may indicate that a menu section should just be a large, emphasized link to another location. To accomplish this, you may invoke the path method when defining the menu section:
CopyAsk AIuse Laravel\Nova\Menu\MenuSection;

// ...

MenuSection::make(&#x27;Dashboard&#x27;)-&gt;path(&#x27;/dashboards/main&#x27;);

For convenience, if you are only creating a menu section to serve as a large, emphasized link to a Nova dashboard, you may invoke the MenuSection::dashboard method:
CopyAsk AIuse App\Nova\Dashboards\Sales;
use Laravel\Nova\Menu\MenuSection;

// ...

MenuSection::dashboard(Sales::class);

Since you will often be creating links to Nova resources, you may use the resource method to quickly create a link to the appropriate path for a given resource:
CopyAsk AIuse App\Nova\User;
use Laravel\Nova\Menu\MenuSection;

// ...

MenuSection::resource(User::class);

Similarly, you may create links to Nova lenses via the lens method:
CopyAsk AIuse App\Nova\Lenses\MostValuableUsers;
use App\Nova\User;
use Laravel\Nova\Menu\MenuSection;

// ...

MenuSection::lens(User::class, MostValuableUsers::class);

Menu sections that are defined as collapsable do not support also being a link. Calling path on a menu section when it’s collapseable will result in no link being shown.
​Menu Section Icons
You can customize the icon displayed for your menu section by invoking the icon method when defining t