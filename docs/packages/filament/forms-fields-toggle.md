# Filament - Forms/Fields/Toggle

Source: https://filamentphp.com/docs/3.x/forms/fields/toggle

#Overview
---------

The toggle component, similar to a checkbox, allows you to interact a boolean value.

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')

```
![Toggle](/docs/3.x/images/light/forms/fields/toggle/simple.jpg) ![Toggle](/docs/3.x/images/dark/forms/fields/toggle/simple.jpg)

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
#Adding icons to the toggle button
----------------------------------

Toggles may also use an icon to represent the “on” and “off” state of the button. To add an icon to the “on” state, use the `onIcon()` method. To add an icon to the “off” state, use the `offIcon()` method:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->onIcon('heroicon-m-bolt')
    ->offIcon('heroicon-m-user')

```
![Toggle icons](/docs/3.x/images/light/forms/fields/toggle/icons.jpg) ![Toggle icons](/docs/3.x/images/dark/forms/fields/toggle/icons.jpg)

#Customizing the color of the toggle button
-------------------------------------------

You may also customize the color representing the “on” or “off” state of the toggle. These may be either `danger`, `gray`, `info`, `primary`, `success` or `warning`. To add a color to the “on” state, use the `onColor()` method. To add a color to the “off” state, use the `offColor()` method:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->onColor('success')
    ->offColor('danger')

```
![Toggle off color](/docs/3.x/images/light/forms/fields/toggle/off-color.jpg) ![Toggle off color](/docs/3.x/images/dark/forms/fields/toggle/off-color.jpg)

![Toggle on color](/docs/3.x/images/light/forms/fields/toggle/on-color.jpg) ![Toggle on color](/docs/3.x/images/dark/forms/fields/toggle/on-color.jpg)

#Positioning the label above
----------------------------

Toggle fields have two layout modes, inline and stacked. By default, they are inline.

When the toggle is inline, its label is adjacent to it:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->inline()

```
![Toggle with its label inline](/docs/3.x/images/light/forms/fields/toggle/inline.jpg) ![Toggle with its label inline](/docs/3.x/images/dark/forms/fields/toggle/inline.jpg)

When the toggle is stacked, its label is above it:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_admin')
    ->inline(false)

```
![Toggle with its label above](/docs/3.x/images/light/forms/fields/toggle/not-inline.jpg) ![Toggle with its label above](/docs/3.x/images/dark/forms/fields/toggle/not-inline.jpg)

#Toggle validation
------------------

As well as all rules listed on the validation page, there are additional rules that are specific to toggles.

### #Accepted validation

You may ensure that the toggle is “on” using the `accepted()` method:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('terms_of_service')
    ->accepted()

```
### #Declined validation

You may ensure that the toggle is “off” using the `declined()` method:

```php
use Filament\Forms\Components\Toggle;

Toggle::make('is_under_18')
    ->declined()

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion