# Nova - Resources/Validation

*Source: https://nova.laravel.com/docs/v5/resources/validation*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/nova)

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

- [Rules](#rules)
- [Attaching Rules](#attaching-rules)
- [Creation Rules](#creation-rules)
- [Update Rules](#update-rules)
- [After Validation Hooks](#after-validation-hooks)
- [The afterValidation Method](#the-aftervalidation-method)
- [The afterCreationValidation Method](#the-aftercreationvalidation-method)
- [The afterUpdateValidation Method](#the-afterupdatevalidation-method)

Resources

# Validation

Nova provides a variety of ways to validate your resource fields.

Unless you like to live dangerously, any Nova fields that are displayed on the Nova creation / update pages will need some validation. Thankfully, it’s a cinch to attach all of the Laravel validation rules you’re familiar with to your Nova resource fields. Let’s get started.

## [​](#rules) Rules

### [​](#attaching-rules) Attaching Rules

When defining a field on a resource, you may use the `rules` method to attach [validation rules](https://laravel.com/docs/validation#available-validation-rules) to the field:

app/Nova/~Resource.php

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        Text::make('Name')
            ->sortable()
            ->rules('required', 'max:255'),
    ];
}

```

Of course, if you are leveraging Laravel’s support for [validation rule objects](https://laravel.com/docs/validation#using-rule-objects), you may attach those to resources as well:

Copy

Ask AI

```
use App\Rules\ValidState;
use Laravel\Nova\Fields\Text;

// ...

Text::make('State')
    ->sortable()
    ->rules('required', new ValidState),

```

You may also provide rules to the `rules` method via an array or Closure:

Copy

Ask AI

```
use App\Rules\ValidState;
use Laravel\Nova\Fields\Text;

// ...

// Using an array...
Text::make('State')->rules(['required', new ValidState]),

// Using a Closure...
Text::make('State')->rules(fn ($request) => [
    'required', 
    new ValidState(),
]);

```

Additionally, you may use [custom closure rules](https://laravel.com/docs/validation#using-closures) to validate your resource fields:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('State')
    ->sortable()
    ->rules('required', function($attribute, $value, $fail) {
        if (strtoupper($value) !== $value) {
            return $fail('The '.$attribute.' field must be uppercase.');
        }
    }),

```

### [​](#creation-rules) Creation Rules

If you would like to define rules that only apply when a resource is being created, you may use the `creationRules` method:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Email')
    ->sortable()
    ->rules('required', 'email', 'max:255')
    ->creationRules('unique:users,email'),

```

### [​](#update-rules) Update Rules

Likewise, if you would like to define rules that only apply when a resource is being updated, you may use the `updateRules` method. If necessary, you may use `resourceId` place-holder within your rule definition. This place-holder will automatically be replaced with the primary key of the resource being updated:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Email')
    ->sortable()
    ->rules('required', 'email', 'max:255')
    ->creationRules('unique:users,email')
    ->updateRules('unique:users,email,{{resourceId}}'),

```

## [​](#after-validation-hooks) After Validation Hooks

Nova also provides several methods that allow you to perform tasks after a resource has been validated, providing the opportunity to perform more custom validation before the resource is persisted to the database:

- [`afterValidation`](#after-validation-method)
- [`afterCreationValidation`](#after-creation-validation-method)
- [`afterUpdateValidation`](#after-update-validation-method)

#### [​](#the-aftervalidation-method) The `afterValidation` Method

The `afterValidation` method will always be called after a resource has been validated during its creation or during an update. This method will be called before calling `afterCreationValidation` or `afterUpdateValidation`:

app/Nova/~Resource.php

Copy

Ask AI

```
use Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-validation processing.
 *
 * @return void
 */
protected static function afterValidation( 
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator->errors()->add('field', 'Something is wrong with this field!');
    }
}

```

#### [​](#the-aftercreationvalidation-method) The `afterCreationValidation` Method

The `afterCreationValidation` method will be called after a resource that is being created has been validated:

app/Nova/~Resource.php

Copy

Ask AI

```
use Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-creation validation processing.
 * 
 * @return void
 */
protected static function afterCreationValidation(
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator->errors()->add('field', 'Something is wrong with this field!');
    }
}

```

#### [​](#the-afterupdatevalidation-method) The `afterUpdateValidation` Method

The `afterUpdateValidation` method will be called after a resource that is being updated has been validated:

app/Nova/~Resource.php

Copy

Ask AI

```
use Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-update validation processing.
 *
 * @return void
 */
protected static function afterUpdateValidation(
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator->errors()->add('field', 'Something is wrong with this field!');
    }
}

```

Was this page helpful?

YesNo

[Relationships](/docs/v5/resources/relationships)[Authorization](/docs/v5/resources/authorization)

Assistant

Responses are generated using AI and may contain mistakes.