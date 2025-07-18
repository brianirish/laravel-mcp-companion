# Filament - Forms/Fields/Hidden

Source: https://filamentphp.com/docs/3.x/forms/fields/hidden

#Overview
---------

The hidden component allows you to create a hidden field in your form that holds a value.

```php
use Filament\Forms\Components\Hidden;

Hidden::make('token')

```
Please be aware that the value of this field is still editable by the user if they decide to use the browser’s developer tools. You should not use this component to store sensitive or read-only information.

Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion