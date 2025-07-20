# Nova - Resources/Fields

*Source: https://nova.laravel.com/docs/v5/resources/fields*

---

Fields - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesFieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesFieldsNova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.​Defining Fields
Each Nova resource contains a fields method. This method returns an array of fields, which generally extend the Laravel\Nova\Fields\Field class. Nova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.
To add a field to a resource, you may simply add it to the resource’s fields method. Typically, fields may be created using their static make method. This method accepts several arguments; however, you usually only need to pass the “human readable” name of the field. Nova will automatically “snake case” this string to determine the underlying database column:
app/Nova/User.phpCopyAsk AIuse Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()-&gt;sortable(),
        Text::make(&#x27;Name&#x27;)-&gt;sortable(),
    ];
}

​Field Column Conventions
As noted above, Nova will “snake case” the displayable name of the field to determine the underlying database column. However, if necessary, you may pass the column name as the second argument to the field’s make method:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;, &#x27;name_column&#x27;),

If the field has a JSON, ArrayObject, or array cast assigned to it, you may use the -&gt; operator to specify nested properties within the field:
CopyAsk AIuse Laravel\Nova\Fields\Timezone;

// ...

Timezone::make(&#x27;User Timezone&#x27;, &#x27;settings-&gt;timezone&#x27;),

​Showing / Hiding Fields
Often, you will only want to display a field in certain situations. For example, there is typically no need to show a Password field on a resource index listing. Likewise, you may wish to only display a Created At field on the creation / update forms. Nova makes it a breeze to hide / show fields on certain pages.
The following methods may be used to show / hide fields based on the display context:

showOnIndex
showOnDetail
showOnCreating
showOnUpdating
showOnPreview
showWhenPeeking
hideFromIndex
hideFromDetail
hideWhenCreating
hideWhenUpdating
onlyOnIndex
onlyOnDetail
onlyOnForms
exceptOnForms

You may chain any of these methods onto your field’s definition in order to instruct Nova where the field should be displayed:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;)-&gt;hideFromIndex(),

Alternatively, you may pass a callback to the following methods.

showOnIndex
showOnDetail
showOnCreating
showOnUpdating
showWhenPeeking
hideFromIndex
hideFromDetail
hideWhenCreating
hideWhenUpdating
showOnPreview
onlyOnPreview

For show* methods, the field will be displayed if the given callback returns true:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;)-&gt;showOnIndex(function (NovaRequest $request, $resource) {
    return $this-&gt;name === &#x27;Taylor Otwell&#x27;;
}),

For hide* methods, the field will be hidden if the given callback returns true:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;)-&gt;hideFromIndex(function (NovaRequest $request, $resource) {
    return $this-&gt;name === &#x27;Taylor Otwell&#x27;;
}),

​Showing Fields When Peeking
You may allow a field to be visible when peeking at the resource by invoking the showWhenPeeking method when defining the field:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;)-&gt;showWhenPeeking(),

​Resource Preview Modal
You may also define which fields should be included in the resource’s “preview” modal. This modal can be displayed for a given resource by the user when viewing the resource’s index:
CopyAsk AIuse Laravel\Nova\Fields\Markdown;
use Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Title&#x27;)-&gt;showOnPreview(),

Markdown::make(&#x27;Content&#x27;)-&gt;showOnPreview(),

Alternatively, you may pass a callback to the showOnPreview method:
CopyAsk AIuse Laravel\Nova\Fields\Markdown;

// ...

Markdown::make(&#x27;Content&#x27;)-&gt;showOnPreview(function (NovaRequest $request, $resource) {
    return $request-&gt;user()-&gt;can(&#x27;previewContent&#x27;);
}),


​Dynamic Field Methods
If your application requires it, you may specify a separate list of fields for specific display contexts. For example, imagine you have a resource with the following list of fields:
app/Nova/~Resource.phpCopyAsk AIuse Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        Text::make(&#x27;First Name&#x27;),
        Text::make(&#x27;Last Name&#x27;),
        Text::make(&#x27;Job Title&#x27;),
    ];
}

On your detail page, you may wish to show a combined name via a computed field, followed by the job title. In order to do this, you could add a fieldsForDetail method to the resource class which returns a separate list of fields that should only be displayed on the resource’s detail page:
app/Nova/~Resource.phpCopyAsk AIuse Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Get the fields displayed by the resource on detail page.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fieldsForDetail(NovaRequest $request): array
{
    return [
        Text::make(&#x27;Name&#x27;, function () {
            return sprintf(&#x27;%s %s&#x27;, $this-&gt;first_name, $this-&gt;last_name);
        }),

        Text::make(&#x27;Job Title&#x27;),
    ];
}

The available methods that may be defined for individual display contexts are:

fieldsForIndex
fieldsForDetail
fieldsForInlineCreate
fieldsForCreate
fieldsForUpdate
fieldsForPreview

The fieldsForIndex, fieldsForDetail, fieldsForInlineCreate, fieldsForCreate,fieldsForUpdate, and fieldsForPreview methods always take precedence over the fields method.
​Default Values
There are times you may wish to provide a default value to your fields. Nova offers this functionality via the default method, which accepts a value or callback. This value will be used as the field’s default input value on the resource’s creation view:
CopyAsk AIuse Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\Text;

// ...

BelongsTo::make(&#x27;Name&#x27;)-&gt;default($request-&gt;user()-&gt;getKey()),

Text::make(&#x27;Uuid&#x27;)-&gt;default(function ($request) {
    return Str::orderedUuid();
}),

​Field Placeholder