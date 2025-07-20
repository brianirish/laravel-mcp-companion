# Nova - Resources/Repeater-Fields

*Source: https://nova.laravel.com/docs/v5/resources/repeater-fields*

---

Repeater Fields - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesRepeater FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesRepeater FieldsRepeater fields allow you to create and edit repeatable, structured data.​Overview
The Repeater field allows you to create and edit repeatable, structured data and store that data in a JSON column or HasMany relationship:
app/Nova/Invoice.phpCopyAsk AInamespace App\Nova;

use App\Nova\Repeaters;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Repeater;
use Laravel\Nova\Http\Requests\NovaRequest;
 
class Invoice extends Resource
{
	/**  
	 * Get the fields displayed by the resource. 
	 * 
	 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
	 */
	public function fields(NovaRequest $request): array
	{
		return [
			ID::make(),
			Repeater::make(&#x27;Line Items&#x27;)
				-&gt;repeatables([
					Repeaters\LineItem::make(),
				]),
		];
	}
}

After defining a Repeater field, your resource will have an elegant interface for adding and editing repeatable items in the field:

​Repeatables
A Repeatable object represents the repeatable data for a Repeater field. It defines the set of fields used for the repeatable item. It also optionally defines an Eloquent Model class when the Repeater is using the HasMany preset.
The Repeater field is not limited to a single type of repeatable. It also supports multiple “repeatable” types, which may contain their own unique field sets and models. These repeatables could be used to create interfaces for editing flexible content areas, similar to those offered by content management systems.
​Generating Repeatables
To generate a new Repeatable, invoke the nova:repeatable Artisan command:
CopyAsk AIphp artisan nova:repeatable LineItem

After invoking the command above, Nova generates a new file at app/Nova/Repeater/LineItem.php. This file contains a fields method in which you may list any supported Nova field. For example, below we will define a Repeatable representing a line item for an invoice:
app/Nova/Repeaters/LineItem.phpCopyAsk AInamespace App\Nova\Repeaters;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Fields\Currency;
use Laravel\Nova\Fields\Number;
use Laravel\Nova\Fields\Repeater\Repeatable;
use Laravel\Nova\Fields\Textarea;

class LineItem extends Repeatable
{
	/**
	 * Get the fields displayed by the repeatable.
	 *
	 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
	 */
	public function fields(NovaRequest $request): array
	{
		return [
			Number::make(&#x27;Quantity&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;numeric&#x27;),
			Textarea::make(&#x27;Description&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;max:255&#x27;),
			Currency::make(&#x27;Price&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;numeric&#x27;),
		];
	}
}

​Confirming Repeatable Removal
You may instruct Nova to present a confirmation modal before removing a repeatable by invoking the confirmRemoval method when defining the repeatable:
CopyAsk AIuse App\Nova\Repeaters;
use Laravel\Nova\Fields\Repeater;
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
		Repeater::make(&#x27;Attachments&#x27;)-&gt;repeatables([
			Repeaters\File::make()-&gt;confirmRemoval(),
			Repeaters\Note::make(),
			Repeaters\Video::make()-&gt;confirmRemoval(),
		]),
	];
}

​Repeater Presets
The Repeater field includes two storage “presets” out-of-the-box: Json and HasMany. Each preset defines how the repeatable data is stored and retrieved from your database.
For example, an Invoice resource could use a Repeater field to edit the line items for an invoice. Using the Laravel\Nova\Fields\Repeater\JSON preset, those line items would be stored in a line_items JSON column. However, when using the HasMany preset, the line items would be stored in a separate ‘line_items’ database table, with fields corresponding to each database column.
​JSON Preset
The JSON preset stores repeatables in a JSON column in your database. For example, the line items for an invoice could be store in a line_items column. When a resource with a Repeater field using the JSON preset is saved, the repeatables are serialized and saved to the column.
To use the JSON preset, simply invoke the asJson method on your Repeater field definition:
CopyAsk AIuse App\Nova\Repeaters;

// ...

/**
 * Get the fields displayed by the resource. 
 * 
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
	return [
		Repeater::make(&#x27;Line Items&#x27;, &#x27;line_items&#x27;)
			-&gt;repeatables([
				Repeaters\LineItem::make(),
			])
			-&gt;asJson(),
	];
}

Before using this preset, you should ensure that the underlying Eloquent attribute for the resource’s repeater column is configured to cast to an array (or equivalent) within your Eloquent model class:
app/Models/Invoce.phpCopyAsk AI/**
 * The attributes that should be cast.
 *
 * @var array&lt;string, mixed&gt;
 */
protected $casts = [
	&#x27;line_items&#x27; =&gt; &#x27;array&#x27;,
];

​HasMany Preset
The HasMany preset stores repeatables via Eloquent using a HasMany relationship. For example, instead of storing the line items for an invoice in JSON format, the data would be saved in a separate line_items database table, complete with dedicated columns mapping to each field in the repeatable. The Repeater field will automatically manage these relations when editing your resources.
To use the HasMany preset, simply invoke the asHasMany method on your Repeater field definition:
CopyAsk AIuse App\Nova\Repeaters;

// ...

/**
 * Get the fields displayed by the resource. 
 * 
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
	return [
		Repeater::make(&#x27;Line Items&#x27;, &#x27;lineItems&#x27;)
			-&gt;repeatables([
				Repeaters\LineItem::make(),
			])
			-&gt;asHasMany(),
	];
}

The HasMany preset requires each repeatable to specify the underlying model it represents by setting the model property on the Repeatable. For example, a LineItem repeatable would need to specify the underlying \App\Models\LineItem model it represents:
app/Nova/Repeaters/LineItem.phpCopyAsk AI/**  
 * The underlying model the repeatable represents. 
 * 
 * @var class-string
 */
public static $model = \App\Models\LineItem::class;

​Upserting Repeatables Using Unique Fields
By default, when editing your repeatables configured with the HasMany preset, Nova will delete all of the related items and recreate them every time you save your resource. To instruct Nova to “upsert” the repeatable data instead, you should ensure you have a unique identifier column on your related models. Typically, this will be an auto-incrementing column or a UUID. You may then use the uniqueFie