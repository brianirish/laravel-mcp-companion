# Filament - Forms/Fields/Checkbox

Source: https://filamentphp.com/docs/3.x/forms/fields/checkbox

#Overview
---------

The checkbox component, similar to a toggle, allows you to interact a boolean value.

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')

```
![Checkbox](/docs/3.x/images/light/forms/fields/checkbox/simple.jpg) ![Checkbox](/docs/3.x/images/dark/forms/fields/checkbox/simple.jpg)

If you’re saving the boolean value using Eloquent, you should be sure to add a `boolean` cast to the model property:

```php
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected $casts = [
        'is_admin' => 'boolean',
    ];

    // ...
}

```
#Positioning the label above
----------------------------

Checkbox fields have two layout modes, inline and stacked. By default, they are inline.

When the checkbox is inline, its label is adjacent to it:

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')->inline()

```
![Checkbox with its label inline](/docs/3.x/images/light/forms/fields/checkbox/inline.jpg) ![Checkbox with its label inline](/docs/3.x/images/dark/forms/fields/checkbox/inline.jpg)

When the checkbox is stacked, its label is above it:

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_admin')->inline(false)

```
![Checkbox with its label above](/docs/3.x/images/light/forms/fields/checkbox/not-inline.jpg) ![Checkbox with its label above](/docs/3.x/images/dark/forms/fields/checkbox/not-inline.jpg)

#Checkbox validation
--------------------

As well as all rules listed on the validation page, there are additional rules that are specific to checkboxes.

### #Accepted validation

You may ensure that the checkbox is checked using the `accepted()` method:

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('terms_of_service')
    ->accepted()

```
### #Declined validation

You may ensure that the checkbox is not checked using the `declined()` method:

```php
use Filament\Forms\Components\Checkbox;

Checkbox::make('is_under_18')
    ->declined()

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion