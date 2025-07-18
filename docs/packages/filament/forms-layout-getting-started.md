# Filament - Forms/Layout/Getting Started

Source: https://filamentphp.com/docs/3.x/forms/layout/getting-started

#Overview
---------

![Filament](/docs/_astro/filament-laracasts-logo.CzN-P2OP.webp)  ![Laracasts](/docs/_astro/laracasts.xZHGp0JC.svg)

Layouts

Watch the Rapid Laravel Development with Filament series on Laracasts - it will teach you the basics of customizing the layout of a Filament form.

Play Video

![Kevin McKee](https://avatars.githubusercontent.com/u/4503765?v=4)

Kevin McKee

Instructor

Filament forms are not limited to just displaying fields. You can also use “layout components” to organize them into an infinitely nestable structure.

Layout component classes can be found in the `Filament\Forms\Components` namespace. They reside within the schema of your form, alongside any fields.

Components may be created using the static `make()` method. Usually, you will then define the child component `schema()` to display inside:

```php
use Filament\Forms\Components\Grid;

Grid::make(2)
    ->schema([
        // ...
    ])

```
#Available layout components
----------------------------

Filament ships with some layout components, suitable for arranging your form fields depending on your needs:

* Grid
* Fieldset
* Tabs
* Wizard
* Section
* Split
* Placeholder

You may also create your own custom layout components to organize fields however you wish.

#Setting an ID
--------------

You may define an ID for the component using the `id()` method:

```php
use Filament\Forms\Components\Section;

Section::make()
    ->id('main-section')

```
#Adding extra HTML attributes
-----------------------------

You can pass extra HTML attributes to the component, which will be merged onto the outer DOM element. Pass an array of attributes to the `extraAttributes()` method, where the key is the attribute name and the value is the attribute value:

```php
use Filament\Forms\Components\Section;

Section::make()
    ->extraAttributes(['class' => 'custom-section-style'])

```
Classes will be merged with the default classes, and any other attributes will override the default attributes.

#Global settings
----------------

If you wish to change the default behavior of a component globally, then you can call the static `configureUsing()` method inside a service provider’s `boot()` method, to which you pass a Closure to modify the component using. For example, if you wish to make all section components have 2 columns by default, you can do it like so:

```php
use Filament\Forms\Components\Section;

Section::configureUsing(function (Section $section): void {
    $section
        ->columns(2);
});

```
Of course, you are still able to overwrite this on each field individually:

```php
use Filament\Forms\Components\Section;

Section::make()
    ->columns(1)

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion