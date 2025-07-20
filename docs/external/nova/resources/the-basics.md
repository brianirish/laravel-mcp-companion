# Nova - Resources/The-Basics

*Source: https://nova.laravel.com/docs/v5/resources/the-basics*

---

The Basics - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesThe BasicsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesThe BasicsLearn how to define, register, and customize Nova resources.​Introduction
Laravel Nova is a beautiful administration dashboard for Laravel applications. Of course, the primary feature of Nova is the ability to administer your underlying database records using Eloquent. Nova accomplishes this by allowing you to define a Nova “resource” that corresponds to each Eloquent model in your application.
​Defining Resources
By default, Nova resources are stored in the app/Nova directory of your application. You may generate a new resource using the nova:resource Artisan command:
CopyAsk AIphp artisan nova:resource Post

The most basic and fundamental property of a resource is its model property. This property tells Nova which Eloquent model the resource corresponds to:
app/Nova/Post.phpCopyAsk AInamespace App\Nova;

class Post extends Resource
{
    /**
     * The model the resource corresponds to.
     *
     * @var class-string
     */
    public static $model = \App\Models\Post::class;
}

Freshly created Nova resources only contain an ID field definition. Don’t worry, we’ll add more fields to our resource soon.
Nova contains a few reserved words which may not be used for resource names:
Card
Dashboard
Field
Impersonate
Metric
Resource
Search
Script
Style
Tool

​Registering Resources
By default, all resources within the app/Nova directory will automatically be registered with Nova. You are not required to manually register them.
Before resources are available within your Nova dashboard, they must first be registered with Nova. Resources are typically registered in your application’s app/Providers/NovaServiceProvider.php file. This file contains various configuration and bootstrapping code related to your Nova installation.
As mentioned above, you are not required to manually register your resources; however, if you choose to do so, you may do so by overriding the resources method of your NovaServiceProvider.
There are two approaches to manually registering resources. You may use the resourcesIn method to instruct Nova to register all Nova resources within a given directory. Alternatively, you may use the resources method to manually register individual resources:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse App\Nova\User;
use App\Nova\Post;

// ...

/**
 * Register the application&#x27;s Nova resources.
 */
protected function resources(): void
{
    Nova::resourcesIn(app_path(&#x27;Nova&#x27;));

    Nova::resources([
        User::class,
        Post::class,
    ]);
}

Once your resources are registered with Nova, they will be available in the Nova sidebar:
Dashboard
If you do not want a resource to appear in the sidebar, you may override the displayInNavigation property of your resource class:
app/Nova/Post.phpCopyAsk AI/**
 * Indicates if the resource should be displayed in the sidebar.
 *
 * @var bool
 */
public static $displayInNavigation = false;

​Customizing Resource Menus
You can customize the resource’s menu by defining a menu method on your resource class:
app/Nova/Post.phpCopyAsk AIuse Illuminate\Http\Request;

// ...

/**
 * Get the menu that should represent the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Laravel\Nova\Menu\MenuItem
 */
public function menu(Request $request)
{
    return parent::menu($request)-&gt;withBadge(function () {
        return static::$model::count();
    });
}

Please refer to the documentation on menu customization for more information.
​Grouping Resources
If you would like to separate resources into different sidebar groups, you may override the group property of your resource class:
app/Nova/Post.phpCopyAsk AI/**
 * The logical group associated with the resource.
 *
 * @var string
 */
public static $group = &#x27;Admin&#x27;;

​Resource Table Style Customization
Nova supports a few visual customization options for your resources.
​Table Styles
Sometimes it’s convenient to show more data on your resource index tables. To accomplish this, you can use the “tight” table style option designed to increase the visual density of your table rows. To accomplish this, override the static $tableStyle property or the static tableStyle method on your resource class:
app/Nova/Post.phpCopyAsk AI/**
 * The visual style used for the table. Available options are &#x27;tight&#x27; and &#x27;default&#x27;.
 *
 * @var string
 */
public static $tableStyle = &#x27;tight&#x27;;

This will display your table rows with less visual height, enabling more data to be shown:
Tight Table Style
​Column Borders
You can instruct Nova to display column borders by overriding the static $showColumnBorders property or the static showColumnBorders method on your resource class:
app/Nova/Post.phpCopyAsk AI/**
 * Whether to show borders for each column on the X-axis.
 *
 * @var bool
 */
public static $showColumnBorders = true;

Setting this property to true will instruct Nova to display the table with borders on every table item:
Table Column Borders
​Resource Table Click Action
By default, when clicking on a resource table row, Nova will navigate to the detail view for the resource. However, you may want Nova to navigate to the edit form instead. You can customize this behavior by changing the clickAction property or the static clickAction method on your resource class:
PropertyMethodCopyAsk AI/**
 * The click action to use when clicking on the resource in the table.
 *
 * Can be one of: &#x27;detail&#x27; (default), &#x27;edit&#x27;, &#x27;select&#x27;, &#x27;preview&#x27;, or &#x27;ignore&#x27;.
 *
 * @var string
 */
public static $clickAction = &#x27;edit&#x27;;

Choosing the select option will select the resource row’s checkbox. The ignore option instructs Nova to ignore click events altogether.
​Eager Loading
If you routinely need to access a resource’s relationships within your fields, resource title, or resource subtitle, it may be a good idea to add the relationship to the with property of your resource. This property instructs Nova to always eager load the listed relationships when retrieving the resource.
For example, if you access a Post resource’s user relationship within the Post resource’s subtitle method, you should add the user relationship to the Post resource’s with property:
app/Nova/Post.phpCopyAsk AI/**
 * The relationships that should be eager loaded on index queries.
 *
 * @var array
 */
public static $with = [&#x27;user&#x27;];

​Resource Default Attribute Values
By default, Laravel Nova will utilize the default attribute values defined by Eloquent over any default values set on each Field during resource creation. If you need to override the default values within a resource, you can do so by overriding the resource’s defaultAttributes method:
CopyAsk AI/**
 * Get the default atrtributes for the model represented by th