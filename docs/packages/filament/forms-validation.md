# Filament - Forms/Validation

Source: https://filamentphp.com/docs/3.x/forms/validation

#Overview
---------

Validation rules may be added to any field.

In Laravel, validation rules are usually defined in arrays like `['required', 'max:255']` or a combined string like `required|max:255`. This is fine if you’re exclusively working in the backend with simple form requests. But Filament is also able to give your users frontend validation, so they can fix their mistakes before any backend requests are made.

Filament includes several dedicated validation methods, but you can also use any other Laravel validation rules, including custom validation rules.

> Beware that some validations rely on the field name and therefore won’t work when passed via `->rule()`/`->rules()`. Use the dedicated validation methods whenever you can.

#Available rules
----------------

### #Active URL

The field must have a valid A or AAAA record according to the `dns_get_record()` PHP function. See the Laravel documentation.

```php
Field::make('name')->activeUrl()

```
### #After (date)

The field value must be a value after a given date. See the Laravel documentation.

```php
Field::make('start_date')->after('tomorrow')

```
Alternatively, you may pass the name of another field to compare against:

```php
Field::make('start_date')
Field::make('end_date')->after('start_date')

```
### #After or equal to (date)

The field value must be a date after or equal to the given date. See the Laravel documentation.

```php
Field::make('start_date')->afterOrEqual('tomorrow')

```
Alternatively, you may pass the name of another field to compare against:

```php
Field::make('start_date')
Field::make('end_date')->afterOrEqual('start_date')

```
### #Alpha

The field must be entirely alphabetic characters. See the Laravel documentation.

```php
Field::make('name')->alpha()

```
### #Alpha Dash

The field may have alphanumeric characters, as well as dashes and underscores. See the Laravel documentation.

```php
Field::make('name')->alphaDash()

```
### #Alpha Numeric

The field must be entirely alphanumeric characters. See the Laravel documentation.

```php
Field::make('name')->alphaNum()

```
### #ASCII

The field must be entirely 7-bit ASCII characters. See the Laravel documentation.

```php
Field::make('name')->ascii()

```
### #Before (date)

The field value must be a date before a given date. See the Laravel documentation.

```php
Field::make('start_date')->before('first day of next month')

```
Alternatively, you may pass the name of another field to compare against:

```php
Field::make('start_date')->before('end_date')
Field::make('end_date')

```
### #Before or equal to (date)

The field value must be a date before or equal to the given date. See the Laravel documentation.

```php
Field::make('start_date')->beforeOrEqual('end of this month')

```
Alternatively, you may pass the name of another field to compare against:

```php
Field::make('start_date')->beforeOrEqual('end_date')
Field::make('end_date')

```
### #Confirmed

The field must have a matching field of `{field}_confirmation`. See the Laravel documentation.

```php
Field::make('password')->confirmed()
Field::make('password_confirmation')

```
### #Different

The field value must be different to another. See the Laravel documentation.

```php
Field::make('backup_email')->different('email')

```
### #Doesn’t Start With

The field must not start with one of the given values. See the Laravel documentation.

```php
Field::make('name')->doesntStartWith(['admin'])

```
### #Doesn’t End With

The field must not end with one of the given values. See the Laravel documentation.

```php
Field::make('name')->doesntEndWith(['admin'])

```
### #Ends With

The field must end with one of the given values. See the Laravel documentation.

```php
Field::make('name')->endsWith(['bot'])

```
### #Enum

The field must contain a valid enum value. See the Laravel documentation.

```php
Field::make('status')->enum(MyStatus::class)

```
### #Exists

The field value must exist in the database. See the Laravel documentation.

```php
Field::make('invitation')->exists()

```
By default, the form’s model will be searched, if it is registered. You may specify a custom table name or model to search:

```php
use App\Models\Invitation;

Field::make('invitation')->exists(table: Invitation::class)

```
By default, the field name will be used as the column to search. You may specify a custom column to search:

```php
Field::make('invitation')->exists(column: 'id')

```
You can further customize the rule by passing a closure to the `modifyRuleUsing` parameter:

```php
use Illuminate\Validation\Rules\Exists;

Field::make('invitation')
    ->exists(modifyRuleUsing: function (Exists $rule) {
        return $rule->where('is_active', 1);
    })

```
### #Filled

The field must not be empty when it is present. See the Laravel documentation.

```php
Field::make('name')->filled()

```
### #Greater than

The field value must be greater than another. See the Laravel documentation.

```php
Field::make('newNumber')->gt('oldNumber')

```
### #Greater than or equal to

The field value must be greater than or equal to another. See the Laravel documentation.

```php
Field::make('newNumber')->gte('oldNumber')

```
### #Hex color

The field value must be a valid color in hexadecimal format. See the Laravel documentation.

```php
Field::make('color')->hexColor()

```
### #In

The field must be included in the given list of values. See the Laravel documentation.

```php
Field::make('status')->in(['pending', 'completed'])

```
### #Ip Address

The field must be an IP address. See the Laravel documentation.

```php
Field::make('ip_address')->ip()
Field::make('ip_address')->ipv4()
Field::make('ip_address')->ipv6()

```
### #JSON

The field must be a valid JSON string. See the Laravel documentation.

```php
Field::make('ip_address')->json()

```
### #Less than

The field value must be less than another. See the Laravel documentation.

```php
Field::make('newNumber')->lt('oldNumber')

```
### #Less than or equal to

The field value must be less than or equal to another. See the Laravel documentation.

```php
Field::make('newNumber')->lte('oldNumber')

```
### #Mac Address

The field must be a MAC address. See the Laravel documentation.

```php
Field::make('mac_address')->macAddress()

```
### #Multiple Of

The field must be a multiple of value. See the Laravel documentation.

```php
Field::make('number')->multipleOf(2)

```
### #Not In

The field must not be included in the given list of values. See the Laravel documentation.

```php
Field::make('status')->notIn(['cancelled', 'rejected'])

```
### #Not Regex

The field must not match the given regular expression. See the Laravel documentation.

```php
Field::make('email')->notRegex('/^.+$/i')

```
### #Nullable

The field value can be empty. This rule is applied by default if the `required` rule is not present. See the Laravel documentation.

```php
Field::make('name')->nullable()

```
### #Prohibited

The field value must be empty. See the Laravel documentation.

```php
Field::make('name')->prohibited()

```
### #Prohibited If

The field must be empty *only if* the other specified field has any of the given values. See the Laravel documentation.

```php
Field::make('name')->prohibitedIf('field', 'value')

```
### #Prohibited Unless

The field must be empty *unless* the other specified field has any of the given values. See the Laravel documentation.

```php
Field::make('name')->prohibitedUnless('field', 'value')

```
### #Prohibits

If the field is not empty, all other specified fields must be empty. See the Laravel documentation.

```php
Field::make('name')->prohibits('field')

Field::make('name')->prohibits(['field', 'another_field'])

```
### #Required

The field value must not be empty. See the Laravel documentation.

```php
Field::make('name')->required()

```
### #Required If

The field value must not be empty *only if* the other specified field has any of the given values. See the Laravel documentation.

```php
Field::make('name')->requiredIf('field', 'value')

```
### #Required If Accepted

The field value must not be empty *only if* the other specified field is equal to “yes”, “on”, 1, “1”, true, or “true”. See the Laravel documentation.

```php
Field::make('name')->requiredIfAccepted('field')

```
### #Required Unless

The field value must not be empty *unless* the other specified field has any of the given values. See the Laravel documentation.

```php
Field::make('name')->requiredUnless('field', 'value')

```
### #Required With

The field value must not be empty *only if* any of the other specified fields are not empty. See the Laravel documentation.

```php
Field::make('name')->requiredWith('field,another_field')

```
### #Required With All

The field value must not be empty *only if* all the other specified fields are not empty. See the Laravel documentation.

```php
Field::make('name')->requiredWithAll('field,another_field')

```
### #Required Without

The field value must not be empty *only when* any of the other specified fields are empty. See the Laravel documentation.

```php
Field::make('name')->requiredWithout('field,another_field')

```
### #Required Without All

The field value must not be empty *only when* all the other specified fields are empty. See the Laravel documentation.

```php
Field::make('name')->requiredWithoutAll('field,another_field')

```
### #Regex

The field must match the given regular expression. See the Laravel documentation.

```php
Field::make('email')->regex('/^.+@.+$/i')

```
### #Same

The field value must be the same as another. See the Laravel documentation.

```php
Field::make('password')->same('passwordConfirmation')

```
### #Starts With

The field must start with one of the given values. See the Laravel documentation.

```php
Field::make('name')->startsWith(['a'])

```
### #String

The field must be a string. See the Laravel documentation.

```php
Field::make('name')->string()

```
### #Unique

The field value must not exist in the database. See the Laravel documentation.

```php
Field::make('email')->unique()

```
By default, the form’s model will be searched, if it is registered. You may specify a custom table name or model to search:

```php
use App\Models\User;

Field::make('email')->unique(table: User::class)

```
By default, the field name will be used as the column to search. You may specify a custom column to search:

```php
Field::make('email')->unique(column: 'email_address')

```
Sometimes, you may wish to ignore a given model during unique validation. For example, consider an “update profile” form that includes the user’s name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question.

```php
Field::make('email')->unique(ignorable: $ignoredUser)

```
If you’re using the Panel Builder, you can easily ignore the current record by using `ignoreRecord` instead:

```php
Field::make('email')->unique(ignoreRecord: true)

```
You can further customize the rule by passing a closure to the `modifyRuleUsing` parameter:

```php
use Illuminate\Validation\Rules\Unique;

Field::make('email')
    ->unique(modifyRuleUsing: function (Unique $rule) {
        return $rule->where('is_active', 1);
    })

```
### #ULID

The field under validation must be a valid Universally Unique Lexicographically Sortable Identifier (ULID). See the Laravel documentation.

```php
Field::make('identifier')->ulid()

```
### #UUID

The field must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID). See the Laravel documentation.

```php
Field::make('identifier')->uuid()

```
#Other rules
------------

You may add other validation rules to any field using the `rules()` method:

```php
TextInput::make('slug')->rules(['alpha_dash'])

```
A full list of validation rules may be found in the Laravel documentation.

#Custom rules
-------------

You may use any custom validation rules as you would do in Laravel:

```php
TextInput::make('slug')->rules([new Uppercase()])

```
You may also use closure rules:

```php
use Closure;

TextInput::make('slug')->rules([
    fn (): Closure => function (string $attribute, $value, Closure $fail) {
        if ($value === 'foo') {
            $fail('The :attribute is invalid.');
        }
    },
])

```
You may inject utilities like `$get` into your custom rules, for example if you need to reference other field values in your form:

```php
use Closure;
use Filament\Forms\Get;

TextInput::make('slug')->rules([
    fn (Get $get): Closure => function (string $attribute, $value, Closure $fail) use ($get) {
        if ($get('other_field') === 'foo' && $value !== 'bar') {
            $fail("The {$attribute} is invalid.");
        }
    },
])

```
#Customizing validation attributes
----------------------------------

When fields fail validation, their label is used in the error message. To customize the label used in field error messages, use the `validationAttribute()` method:

```php
use Filament\Forms\Components\TextInput;

TextInput::make('name')->validationAttribute('full name')

```
#Validation messages
--------------------

By default Laravel’s validation error message is used. To customize the error messages, use the `validationMessages()` method:

```php
use Filament\Forms\Components\TextInput;

TextInput::make('email')
    ->unique(// ...)
    ->validationMessages([
        'unique' => 'The :attribute has already been registered.',
    ])

```
#Sending validation notifications
---------------------------------

If you want to send a notification when validation error occurs, you may do so by using the `onValidationError()` method on your Livewire component:

```php
use Filament\Notifications\Notification;
use Illuminate\Validation\ValidationException;

protected function onValidationError(ValidationException $exception): void
{
    Notification::make()
        ->title($exception->getMessage())
        ->danger()
        ->send();
}

```
Alternatively, if you are using the Panel Builder and want this behavior on all the pages, add this inside the `boot()` method of your `AppServiceProvider`:

```php
use Filament\Notifications\Notification;
use Filament\Pages\Page;
use Illuminate\Validation\ValidationException;

Page::$reportValidationErrorUsing = function (ValidationException $exception) {
    Notification::make()
        ->title($exception->getMessage())
        ->danger()
        ->send();
};

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion