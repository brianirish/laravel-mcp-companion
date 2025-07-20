# Nova - Resources/Relationships

*Source: https://nova.laravel.com/docs/v5/resources/relationships*

---

Relationships - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesRelationshipsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesRelationshipsNova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.In addition to the variety of fields we’ve already discussed, Nova has full support for all of Laravel’s relationships. Once you add relationship fields to your Nova resources, you’ll start to experience the full power of the Nova dashboard, as the resource detail page will allow you to quickly view and search a resource’s related models:

​HasOne
The HasOne field corresponds to a hasOne Eloquent relationship. For example, let’s assume a User model hasOne Address model. We may add the relationship to our User Nova resource like so:
CopyAsk AIuse Laravel\Nova\Fields\HasOne;

// ...

HasOne::make(&#x27;Address&#x27;),

Like other types of fields, relationship fields will automatically “camel case” the displayable name of the field to determine the underlying relationship method / attribute. However, you may explicitly specify the name of the relationship method by passing it as the second argument to the field’s make method:
CopyAsk AIuse Laravel\Nova\Fields\HasOne;

// ...

HasOne::make(&#x27;Dirección&#x27;, &#x27;address&#x27;),

​HasOneOfMany
The HasOne relationship field can be transformed into an “has one of many” Eloquent relationship using the ofMany method. For example, let’s assume a User model hasMany Post models. We may add the “has one of many” relationship to our User Nova resource like so:
CopyAsk AIuse App\Nova\Post;
use Laravel\Nova\Fields\HasOne;

// ...

HasOne::ofMany(&#x27;Latest Post&#x27;, &#x27;latestPost&#x27;, Post::class),

​HasMany
The HasMany field corresponds to a hasMany Eloquent relationship. For example, let’s assume a User model hasMany Post models. We may add the relationship to our User Nova resource like so:
CopyAsk AIuse Laravel\Nova\Fields\HasMany;

// ...

HasMany::make(&#x27;Posts&#x27;),

Once the field has been added to your resource, it will be displayed on the resource’s detail page.
When defining HasMany relationships, make sure to use the plural form of the relationship so Nova can infer the correct singular resource name:CopyAsk AIuse Laravel\Nova\Fields\HasMany;

// ...

HasMany::make(&#x27;Posts&#x27;),

​HasOneThrough
The HasOneThrough field corresponds to a hasOneThrough Eloquent relationship. For example, let’s assume a Mechanic model has one Car, and each Car may have one Owner. While the Mechanic and the Owner have no direct connection, the Mechanic can access the Owner through the Car itself. You can display this relationship by adding it to your Nova resource:
CopyAsk AIuse Laravel\Nova\Fields\HasOneThrough;

// ...

HasOneThrough::make(&#x27;Owner&#x27;),

​HasManyThrough
The HasManyThrough field corresponds to a hasManyThrough Eloquent relationship. For example, a Country model might have many Post models through an intermediate User model. In this example, you could easily gather all blog posts for a given country. To display this relationship within Nova, you may add it to your Nova resource:
CopyAsk AIuse Laravel\Nova\Fields\HasManyThrough;

// ...

HasManyThrough::make(&#x27;Posts&#x27;),

​BelongsTo
The BelongsTo field corresponds to a belongsTo Eloquent relationship. For example, let’s assume a Post model belongsTo a User model. We may add the relationship to our Post Nova resource like so:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;User&#x27;),

You may customize the resource class used by the relation field by providing the second and third arguments of the make method, which define the name of the relationship and the underlying Nova resource class:CopyAsk AIuse App\Nova\User;
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;Author&#x27;, &#x27;author&#x27;, User::class),

​Peeking at BelongsTo Relationships
When hovering over a BelongsTo link when viewing the index or detail views, Nova will show a small card allowing you to “take a peek” at the linked relation:

​Preventing Peeking at BelongsTo Relationships
Relationship peeking is enabled by default; however, you can prevent the user from peeking at the relation using the noPeeking helper on your BelongsTo field:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;Author&#x27;)
    -&gt;noPeeking(),

You may also use the peekable method to determine whether the user should be allowed to peek at the relation:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

BelongsTo::make(&#x27;Author&#x27;)
    -&gt;peekable(function (NovaRequest $request) {
        return $request-&gt;isResourceDetailRequest();
    }),

​Nullable Relationships
If you would like your BelongsTo relationship to be nullable, you may simply chain the nullable method onto the field’s definition:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;User&#x27;)
    -&gt;nullable(),

​Title Attributes
When a BelongsTo field is shown on a resource creation / update page, a drop-down selection menu or search menu will display the “title” of the resource. For example, a User resource may use the name attribute as its title. Then, when the resource is shown in a BelongsTo selection menu, that attribute will be displayed:

To customize the “title” attribute of a resource, you may define a title property or title method on the resource class:
PropertyMethodCopyAsk AI/**
 * The single value that should be used to represent the resource when being displayed.
 *
 * @var string
 */
public static $title = &#x27;name&#x27;;

​Disable Ordering by Title
By default, associatable resources will be sorted by their title when listed in a select dropdown. Using the dontReorderAssociatables method, you can disable this behavior so that the resources as sorted based on the ordering specified by the relatable query:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;User&#x27;)
    -&gt;dontReorderAssociatables(),

​Filter Trashed Items
By default, the BelongsTo field will allow users to select soft-deleted models; however, this can be disabled using the withoutTrashed method:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make(&#x27;User&#x27;)
    -&gt;withoutTrashed(),

​BelongsToMany
The BelongsToMany field corresponds to a belongsToMany Eloquent relationship. For example, let’s assume a User model belongsToMany Role models:
app/Models/User.phpCopyAsk AIuse App\Models\Role;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

// ...

public function roles(): BelongsToMany
{
    return $this-&gt;belongsToMany(Role::class);
}

We may add the relationship to our User Nova resource like so:
app/Nova/User.phpCopyAsk AIuse Laravel\Nova\Fields\BelongsToMany;

// ...

/**
 * Get the