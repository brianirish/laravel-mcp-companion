# Nova - Releases

*Source: https://nova.laravel.com/docs/v5/releases*

---

## On this page
- [Modernizing Dependencies](#modernizing-dependencies)
- [Tab Panels](#tab-panels)
- [Fields & Filters Improvements](#fields-%26-filters-improvements)
  - [New Dependent Computed Field via Field::computed() method](#new-dependent-computed-field-via-fieldcomputed-method)
  - [New Field::immutable() method](#new-fieldimmutable-method)
  - [Other Field Improvements](#other-field-improvements)
- [Separate Policy Classes for Nova Resources](#separate-policy-classes-for-nova-resources)
Get Started
# Release Notes
Laravel Nova Release Notes
Nova 5 continues the improvements made in Nova 4.x by introducing support for tab panels, searchable select filters, dependent field improvements, third party component improvements, and dependency modernization with support for Inertia.js 2.x.
## [​](#modernizing-dependencies) Modernizing Dependencies
Nova 5 removes support for Laravel 8.x and 9.x, while also requiring PHP 8.1+. This dependency upgrade allows for deeper integration with the Laravel ecosystem, including Fortify, Prompts, and Pennant.
Furthermore, Nova’s frontend code has been updated to utilize Vue 3.5, Heroicons 2.x, and Inertia.js 2.x. Please refer to the Nova [upgrade guide](./upgrade#dependency-upgrades) for a detailed description of these changes and how they affect your application.
## [​](#tab-panels) Tab Panels
Nova 5 further improves the resource UI with the introduction of **Tabs Panels** on the resource detail and form pages:
app/Nova/Event.php
```
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\HasManyThrough;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Tabs\Tab;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field|\Laravel\Nova\Panel>
 */
public function fields(NovaRequest $request): array
{
    return [
        // ...

        Tab::group('Details', [
            Tab::make('Purchases', [ /* List of fields */ ]),
            Tab::make('Registrations', [ /* List of fields */ ]),
            Tab::make('Event & Venue', [ /* List of fields */ ]),
        ]),

        Tab::group(attribute: 'Relations', fields: [
            HasMany::make('Orders', 'orders', Order::class),
            HasManyThrough::make('Tickets', 'tickets', Ticket::class),
        ]),
    ];
}
```
For example, the code snippet above will generate the following tabs:
To learn more about adding tab panels to your Nova resources, check out the [tab documentation](./resources/panels#tabs).
## [​](#fields-&-filters-improvements) Fields & Filters Improvements
### [​](#new-dependent-computed-field-via-fieldcomputed-method) New Dependent Computed Field via `Field::computed()` method
Nova 5 introduces an enhanced `computed` method that builds upon the previous computed fields feature. While computed fields have always been valuable for displaying additional resource information, they previously lacked a unique `$attribute` identifier, which limited their use as dependent fields. This limitation has been resolved in Nova 5:
```
use Laravel\Nova\Fields\Boolean;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

Boolean::make('Would you like to leave a comment?', 'comment_boolean')
    ->computed(),

Text::make('Comment')
    ->hidden()
    ->dependsOn('comment_boolean', function (Text $field, NovaRequest $request, FormData $formData) {
        if ($formData->boolean('comment_boolean') === true) {
            $field->show();
        }
    }),
```
More information on computed fields can be found within the [computed field documentation](./resources/dependent-fields#dependable-computed-fields).
### [​](#new-fieldimmutable-method) New `Field::immutable()` method
While [readonly fields](./resources/fields#readonly-fields) disable a field’s input and prevent form submission of its value, immutable fields offer more flexibility. By invoking the `immutable` method on a field, you can prevent users from modifying the field’s value while still allowing it to be submitted with the form.
You may also pass a boolean argument to the `immutable` method to dynamically control whether a field should be immutable:
```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')->immutable(),
```
Further reading is available on the [documentation](./resources/fields#immutable-fields).
### [​](#other-field-improvements) Other Field Improvements
- [Enums may now be used as `Select::options()`](./resources/fields#using-enum-as-options)
- [Searchable select filters are now supported](./filters/registering-filters#searchable-select-filter)
- JSON `Repeater` fields are now displayed on the resource detail page
## [​](#separate-policy-classes-for-nova-resources) Separate Policy Classes for Nova Resources
In previous Nova releases, Nova resources shared authorization policies with your user-facing application. This approach to authorization can present problems if your application’s authorization logic differs from how resource authorization should be handled for Nova operations.
In Nova 5, you may now create a separate policy class that is only used for operations that are triggered via Nova:
```
php artisan nova:policy
```
To enable the new policy you need to add the following code:
app/Nova/User.php
```
namespace App\Nova;

class User extends Resource
{
    /**
     * The policy the resource corresponds to.
     *
     * @var class-string
     */
    public static $policy = Policies\UserPolicy::class;
}
```
Further reading is available on the [Authorization](./resources/authorization#using-separate-policy-class-for-nova-resource) documentation.
Was this page helpful?
YesNo
[Installation](/docs/v5/installation)[Upgrade Guide](/docs/v5/upgrade)
⌘I