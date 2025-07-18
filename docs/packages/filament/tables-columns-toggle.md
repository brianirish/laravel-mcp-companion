# Filament - Tables/Columns/Toggle

Source: https://filamentphp.com/docs/3.x/tables/columns/toggle

#Overview
---------

The toggle column allows you to render a toggle button inside the table, which can be used to update that database record without needing to open a new page or a modal:

```php
use Filament\Tables\Columns\ToggleColumn;

ToggleColumn::make('is_admin')

```
![Toggle column](/docs/3.x/images/light/tables/columns/toggle/simple.jpg) ![Toggle column](/docs/3.x/images/dark/tables/columns/toggle/simple.jpg)

#Lifecycle hooks
----------------

Hooks may be used to execute code at various points within the toggle’s lifecycle:

```php
ToggleColumn::make()
    ->beforeStateUpdated(function ($record, $state) {
        // Runs before the state is saved to the database.
    })
    ->afterStateUpdated(function ($record, $state) {
        // Runs after the state is saved to the database.
    })

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion