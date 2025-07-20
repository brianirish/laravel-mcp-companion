# Nova - Customization/Fields

*Source: https://nova.laravel.com/docs/v5/customization/fields*

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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperFieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperFieldsLearn how to build custom fields for your Nova resources.​Overview
Nova ships with a variety of field types; however, sometimes you may need a field type that isn’t provided out of the box. For this reason, Nova allows you to build custom fields. Custom fields consist of three Vue components that determine how the field is displayed in various contexts.
​Defining Fields
Custom fields may be generated using the nova:field Artisan command. By default, all new fields will be placed in the nova-components directory of your application. When generating a field using the nova:field command, the field name you pass to the command should follow the Composer vendor/package format. So, if we were building a color-picker field, we might run the following command:
CopyAsk AIphp artisan nova:field acme/color-picker

When generating a field, Nova will prompt you to install the field’s NPM dependencies, compile its assets, and update your application’s composer.json file. All custom fields are registered with your application as a Composer “path” repository.
Nova fields include all of the scaffolding necessary to build your field. Each field even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Fields
Nova fields may be registered in your resource’s fields method. This method returns an array of fields available to the resource. To register your field, add your field to the array of fields returned by this method:
app/Nova/~Resource.phpCopyAsk AIuse Acme\ColorPicker\ColorPicker;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make(&#x27;ID&#x27;, &#x27;id&#x27;)-&gt;sortable(),

        ColorPicker::make(&#x27;Color&#x27;),
    ];
}

​Field Options
Often, you will need to allow the consumers of your field to customize run-time configuration options on the field. You may do this by exposing methods on your field class. These methods may call the field’s underlying withMeta method to add information to the field’s metadata, which will be available within your field’s Vue components. The withMeta method accepts an array of key / value options:
nova-components/ColorPicker/src/ColorPicker.phpCopyAsk AInamespace Acme\ColorPicker;

use Laravel\Nova\Fields\Field;

class ColorPicker extends Field
{
    /**
     * The field&#x27;s component.
     *
     * @var string
     */
    public $component = &#x27;color-picker&#x27;;

    /**
     * Set the hues that may be selected by the color picker.
     *
     * @param  array  $hues
     * @return $this
     */
    public function hues(array $hues)
    {
        return $this-&gt;withMeta([&#x27;hues&#x27; =&gt; $hues]);
    }
}

​Accessing Field Options
Your field’s Vue components receive a field Vue prop. The field property provides access to any field options that may be available:
CopyAsk AIconst hues = this.field.hues;

​Building Fields
Each field generated by Nova includes its own service provider and “field” class. Using the color-picker field as an example, the field class will be located at src/ColorPicker.php.
The field’s service provider is also located within the src directory of the field, and is registered within the extra section of your field’s composer.json file so that it will be auto-loaded by Laravel.
​Index Fields
When Nova generates your field, it creates a resources/js/components/IndexField.vue Vue component. This component contains the template and logic for your field when it is displayed on a resource index page. By default, this component simply displays the field’s value in a simple &lt;span&gt; element; however, you are free to modify this field component as needed.
​Detail Fields
When creating fields, Nova also creates a resources/js/components/DetailField.vue Vue component. This component contains the template and logic for your field when it is displayed on a resource detail page. By default, this template contains the necessary mark-up needed to display your field’s value. However, you are free to adjust this template as required by your application.
​Form Fields
Finally, Nova creates a resources/js/components/FormField.vue Vue component. This component contains the template and logic for your field when it is displayed on a creation or update form. By default, this template contains a simple input control to modify your field’s underlying value; however, you are free to customize this template. For example, we may update the template to display a color-picker control:
nova-components/ColorPicker/resources/js/components/FormField.jsCopyAsk AI&lt;template&gt;
    &lt;DefaultField :field=&quot;field&quot;&gt;
        &lt;template #field&gt;
            &lt;input :id=&quot;field.name&quot; type=&quot;color&quot;
                class=&quot;w-full form-control form-input form-input-bordered&quot;
                :class=&quot;errorClasses&quot;
                :placeholder=&quot;field.name&quot;
                v-model=&quot;value&quot;
            /&gt;

            &lt;p v-if=&quot;hasError&quot; class=&quot;my-2 text-red-500&quot;&gt;
                {{ firstError }}
            &lt;/p&gt;
        &lt;/template&gt;
    &lt;/DefaultField&gt;
&lt;/template&gt;

&lt;script&gt;
import { FormField, HandlesValidationErrors } from &#x27;laravel-nova&#x27;

export default {
  mixins: [FormField, HandlesValidationErrors],

  //
}
&lt;/script&gt;

​Preview Fields
When creating fields, Nova also creates a resources/js/components/PreviewField.vue Vue component. This component contains the template and logic for your field when it is displayed on a resource detail page. By default, this template extends Detail Field Vue component but you are free to adjust this template as required by your application.
To enable using PreviewField Vue component instead of DetailField, you need to enable it via resources/js/field.js:
nova-components/ColorPicker/resources/js/field.jsCopyAsk AIimport IndexField from &#x27;./components/IndexField&#x27;
import DetailField from &#x27;./components/DetailField&#x27;
import FormField from &#x27;./components/FormField&#x27;
import PreviewField from &#x27;./components/PreviewField&#x27;

Nova.booting((app, store) =&gt; {
  app.component(&#x27;index-color-picker&#x27;, IndexField)
  app.component(&#x27;detail-color-picker&#x27;, DetailField)
  app.component(&#x27;form-color-picker&#x27;, FormField)
  app.component(&#x27;preview-color-picker&#x27;, PreviewField)
})

​Setting the Form Value
Before creating or updating a resource, Nova asks each field on the form to “fill” the outgoing FormData object with key / value pairs. Each field may add as many elements to the F