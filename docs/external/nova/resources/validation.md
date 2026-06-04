# Nova - Resources/Validation

*Source: https://nova.laravel.com/docs/v5/resources/validation*

---

## On this page
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
```
use App\Rules\ValidState;
use Laravel\Nova\Fields\Text;

// ...

Text::make('State')
    ->sortable()
    ->rules('required', new ValidState),
```
You may also provide rules to the `rules` method via an array or Closure:
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
⌘I