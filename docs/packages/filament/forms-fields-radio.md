# Filament - Forms/Fields/Radio

Source: https://filamentphp.com/docs/3.x/forms/fields/radio

#Overview
---------

The radio input provides a radio button group for selecting a single value from a list of predefined options:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])

```
![Radio](/docs/3.x/images/light/forms/fields/radio/simple.jpg) ![Radio](/docs/3.x/images/dark/forms/fields/radio/simple.jpg)

#Setting option descriptions
----------------------------

You can optionally provide descriptions to each option using the `descriptions()` method:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published'
    ])
    ->descriptions([
        'draft' => 'Is not visible.',
        'scheduled' => 'Will be visible.',
        'published' => 'Is visible.'
    ])

```
![Radio with option descriptions](/docs/3.x/images/light/forms/fields/radio/option-descriptions.jpg) ![Radio with option descriptions](/docs/3.x/images/dark/forms/fields/radio/option-descriptions.jpg)

Be sure to use the same `key` in the descriptions array as the `key` in the option array so the right description matches the right option.

#Boolean options
----------------

If you want a simple boolean radio button group, with “Yes” and “No” options, you can use the `boolean()` method:

```php
Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()

```
![Boolean radio](/docs/3.x/images/light/forms/fields/radio/boolean.jpg) ![Boolean radio](/docs/3.x/images/dark/forms/fields/radio/boolean.jpg)

#Positioning the options inline with the label
----------------------------------------------

You may wish to display the options `inline()` with the label instead of below it:

```php
Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline()

```
![Inline radio](/docs/3.x/images/light/forms/fields/radio/inline.jpg) ![Inline radio](/docs/3.x/images/dark/forms/fields/radio/inline.jpg)

#Positioning the options inline with each other but below the label
-------------------------------------------------------------------

You may wish to display the options `inline()` with each other but below the label:

```php
Radio::make('feedback')
    ->label('Like this post?')
    ->boolean()
    ->inline()
    ->inlineLabel(false)

```
![Inline radio under label](/docs/3.x/images/light/forms/fields/radio/inline-under-label.jpg) ![Inline radio under label](/docs/3.x/images/dark/forms/fields/radio/inline-under-label.jpg)

#Disabling specific options
---------------------------

You can disable specific options using the `disableOptionWhen()` method. It accepts a closure, in which you can check if the option with a specific `$value` should be disabled:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')

```
![Radio with disabled option](/docs/3.x/images/light/forms/fields/radio/disabled-option.jpg) ![Radio with disabled option](/docs/3.x/images/dark/forms/fields/radio/disabled-option.jpg)

If you want to retrieve the options that have not been disabled, e.g. for validation purposes, you can do so using `getEnabledOptions()`:

```php
use Filament\Forms\Components\Radio;

Radio::make('status')
    ->options([
        'draft' => 'Draft',
        'scheduled' => 'Scheduled',
        'published' => 'Published',
    ])
    ->disableOptionWhen(fn (string $value): bool => $value === 'published')
    ->in(fn (Radio $component): array => array_keys($component->getEnabledOptions()))

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion