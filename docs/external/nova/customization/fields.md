# Nova - Customization/Fields

*Source: https://nova.laravel.com/docs/v5/customization/fields*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Digging Deeper
Fields
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
- [Blog](https://blog.laravel.com)
##### Get Started
- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)
##### Resources
- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)
##### Search
- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)
##### Filters
- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)
##### Lenses
- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)
##### Actions
- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)
##### Metrics
- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)
##### Digging Deeper
- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)
On this page
- [Overview](#overview)
- [Defining Fields](#defining-fields)
- [Registering Fields](#registering-fields)
- [Field Options](#field-options)
- [Accessing Field Options](#accessing-field-options)
- [Building Fields](#building-fields)
- [Index Fields](#index-fields)
- [Detail Fields](#detail-fields)
- [Form Fields](#form-fields)
- [Preview Fields](#preview-fields)
- [Setting the Form Value](#setting-the-form-value)
- [Dependent Form Field](#dependent-form-field)
- [Hydrating the Model](#hydrating-the-model)
- [Assets](#assets)
- [Registering Assets](#registering-assets)
- [Compiling Assets](#compiling-assets)
Digging Deeper
# Fields
Learn how to build custom fields for your Nova resources.
## [​](#overview) Overview
Nova ships with a variety of field types; however, sometimes you may need a field type that isn’t provided out of the box. For this reason, Nova allows you to build custom fields. Custom fields consist of three Vue components that determine how the field is displayed in various contexts.
## [​](#defining-fields) Defining Fields
Custom fields may be generated using the `nova:field` Artisan command. By default, all new fields will be placed in the `nova-components` directory of your application. When generating a field using the `nova:field` command, the field name you pass to the command should follow the Composer `vendor/package` format. So, if we were building a color-picker field, we might run the following command:
Copy
Ask AI
```
php artisan nova:field acme/color-picker
```
When generating a field, Nova will prompt you to install the field’s NPM dependencies, compile its assets, and update your application’s `composer.json` file. All custom fields are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova fields include all of the scaffolding necessary to build your field. Each field even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.
## [​](#registering-fields) Registering Fields
Nova fields may be registered in your resource’s `fields` method. This method returns an array of fields available to the resource. To register your field, add your field to the array of fields returned by this method:
app/Nova/~Resource.php
Copy
Ask AI
```
use Acme\ColorPicker\ColorPicker;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make('ID', 'id')->sortable(),

        ColorPicker::make('Color'),
    ];
}
```
### [​](#field-options) Field Options
Often, you will need to allow the consumers of your field to customize run-time configuration options on the field. You may do this by exposing methods on your field class. These methods may call the field’s underlying `withMeta` method to add information to the field’s metadata, which will be available within your field’s Vue components. The `withMeta` method accepts an array of key / value options:
nova-components/ColorPicker/src/ColorPicker.php
Copy
Ask AI
```
namespace Acme\ColorPicker;

use Laravel\Nova\Fields\Field;

class ColorPicker extends Field
{
    /**
     * The field's component.
     *
     * @var string
     */
    public $component = 'color-picker';

    /**
     * Set the hues that may be selected by the color picker.
     *
     * @param  array  $hues
     * @return $this
     */
    public function hues(array $hues)
    {
        return $this->withMeta(['hues' => $hues]);
    }
}
```
#### [​](#accessing-field-options) Accessing Field Options
Your field’s Vue components receive a `field` Vue `prop`. The `field` property provides access to any field options that may be available:
Copy
Ask AI
```
const hues = this.field.hues;
```
## [​](#building-fields) Building Fields
Each field generated by Nova includes its own service provider and “field” class. Using the `color-picker` field as an example, the field class will be located at `src/ColorPicker.php`.
The field’s service provider is also located within the `src` directory of the field, and is registered within the `extra` section of your field’s `composer.json` file so that it will be auto-loaded by Laravel.
### [​](#index-fields) Index Fields
When Nova generates your field, it creates a `resources/js/components/IndexField.vue` Vue component. This component contains the template and logic for your field when it is displayed on a resource index page. By default, this component simply displays the field’s value in a simple `<span>` element; however, you are free to modify this field component as needed.
### [​](#detail-fields) Detail Fields
When creating fields, Nova also creates a `resources/js/components/DetailField.vue` Vue component. This component contains the template and logic for your field when it is displayed on a resource detail page. By default, this template contains the necessary mark-up needed to display your field’s value. However, you are free to adjust this template as required by your application.
### [​](#form-fields) Form Fields
Finally, Nova creates a `resources/js/components/FormField.vue` Vue component. This component contains the template and logic for your field when it is displayed on a creation or update form. By default, this template contains a simple `input` control to modify your field’s underlying value; however, you are free to customize this template. For example, we may update the template to display a color-picker control:
nova-components/ColorPicker/resources/js/components/FormField.js
Copy
Ask AI
```
<template>
    <DefaultField :field="field">
        <template }
            </p>
        </template>
    </DefaultField>
</template>

<script>
import { FormField, HandlesValidationErrors } from 'laravel-nova'

export default {
  mixins: [FormField, HandlesValidationErrors],

  //
}
</script>
```
### [​](#preview-fields) Preview Fields
When creating fields, Nova also creates a `resources/js/components/PreviewField.vue` Vue component. This component contains the template and logic for your field when it is displayed on a resource detail page. By default, this template extends [Detail Field](#detail-fields) Vue component but you are free to adjust this template as required by your application.
To enable using `PreviewField` Vue component instead of `DetailField`, you need to enable it via `resources/js/field.js`:
nova-components/ColorPicker/resources/js/field.js
Copy
Ask AI
```
import IndexField from './components/IndexField'
import DetailField from './components/DetailField'
import FormField from './components/FormField'
import PreviewField from './components/PreviewField'

Nova.booting((app, store) => {
  app.component('index-color-picker', IndexField)
  app.component('detail-color-picker', DetailField)
  app.component('form-color-picker', FormField)
  app.component('preview-color-picker', PreviewField)
})
```
#### [​](#setting-the-form-value) Setting the Form Value
Before creating or updating a resource, Nova asks each field on the form to “fill” the outgoing [FormData](https://developer.mozilla.org/en-US/docs/Web/API/FormData) object with key / value pairs. Each field may add as many elements to the `FormData` as needed. This may be done in your `FormField.vue` file’s `fill` method:
nova-components/ColorPicker/resources/js/components/FormField.js
Copy
Ask AI
```
/**
 * Fill the given FormData object with the field's internal value.
 */
fill(formData) {
  this.fillIfVisible(formData, this.fieldAttribute, this.value || '')
}
```
#### [​](#dependent-form-field) Dependent Form Field
By default, all custom fields will be created such that they use the `FormField` mixin. However, if you are building a [dependent field](./../resources/fields#dependent-fields), you should replace `FormField` with `DependentFormField`:
nova-components/ColorPicker/resources/js/components/FormField.js
Copy
Ask AI
```
-import { FormField, HandlesValidationErrors } from 'laravel-nova'
+import { DependentFormField, HandlesValidationErrors } from 'laravel-nova'

export default {
- mixins: [FormField, HandlesValidationErrors],
+ mixins: [DependentFormField, HandlesValidationErrors],

  //
}
```
Next, within your Vue template, you should typically refer to your field using `this.currentField` instead of `this.field`:
nova-components/ColorPicker/resources/js/components/FormField.js
Copy
Ask AI
```
<template>
- <DefaultField :field="field" :errors="errors">
+ <DefaultField :field="currentField" :errors="errors">
    <template }
      </p>
    </template>
  </DefaultField>
</template>
```
Next, don’t forget to use the `Laravel\Nova\Fields\SupportsDependentFields` trait on your `Field` class:
nova-components/ColorPicker/src/ColorPicker.php
Copy
Ask AI
```
use Laravel\Nova\Fields\Field;
+use Laravel\Nova\Fields\SupportsDependentFields;

class ColorPicker extends Field
{
+   use SupportsDependentFields;

    // ...
}
```
#### [​](#hydrating-the-model) Hydrating the Model
By default, when saving a model, your field class will simply copy the incoming form field value into the field’s associated model attribute. However, you may customize how your field hydrates the resource model. To accomplish this, override the `fillModelWithData` method on your field class:
nova-components/ColorPicker/src/ColorPicker.php
Copy
Ask AI
```
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Str;
use Laravel\Nova\Support\Fluent;

// ... 

/**
 * Fill the model's attribute with data.
 * 
 * @return void
 */
public function fillModelWithData(Model|Fluent $model, mixed $value, string $attribute)
{
    $model->forceFill([
      Str::replace('.', '->', $attribute) => $value
    ]);
}
```
This method receives several arguments. Of course, it receives the incoming HTTP request and the model that is being updated. The method also receives the `$requestAttribute`, which is the name of the incoming form field on the HTTP request. Additionally, it receives the `$attribute`, which is the name of the model attribute the field’s value should be placed in.
## [​](#assets) Assets
When Nova generates your field, `resources/js` and `resources/css` directories are generated for you. These directories contain your field’s JavaScript and CSS.
### [​](#registering-assets) Registering Assets
Your Nova field’s service provider registers your field’s compiled assets so that they will be available to the Nova front-end:
nova-components/ColorPicker/src/FieldServiceProvider.php
Copy
Ask AI
```
use Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function (ServingNova $event) {
        Nova::mix('stripe-inspector', __DIR__.'/../dist/mix-manifest.json');
    });
}
```
Your components are bootstrapped and registered in the `resources/js/field.js` file. You are free to modify this file or register additional components here as needed.
### [​](#compiling-assets) Compiling Assets
Your Nova field contains a `webpack.mix.js` file, which is generated when Nova creates your field. You may build your field using the NPM `dev` and `prod` commands:
Copy
Ask AI
```
# Prepare Laravel Nova's dependencies...
npm run nova:install

# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod
```
In addition, you may run the NPM `watch` command to auto-compile your assets when they are changed:
Copy
Ask AI
```
npm run watch
```
The `nova:install` NPM command installs the mixins used by Nova’s built-in fields for use in your field. Please refer to the [Nova mixins](./frontend#using-nova-mixins) documentation for more information.
Was this page helpful?
YesNo
[Cards](/docs/v5/customization/cards)[Filters](/docs/v5/customization/filters)
⌘I
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.