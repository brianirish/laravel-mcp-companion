# Filament - Panels/Resources/Widgets

Source: https://filamentphp.com/docs/3.x/panels/resources/widgets

#Overview
---------

![Filament](/docs/_astro/filament-laracasts-logo.CzN-P2OP.webp)  ![Laracasts](/docs/_astro/laracasts.xZHGp0JC.svg)

Widgets

Watch the Rapid Laravel Development with Filament series on Laracasts - it will teach you the basics of adding widgets to Filament resources.

Play Video

![Kevin McKee](https://avatars.githubusercontent.com/u/4503765?v=4)

Kevin McKee

Instructor

Filament allows you to display widgets inside pages, below the header and above the footer.

You can use an existing dashboard widget, or create one specifically for the resource.

#Creating a resource widget
---------------------------

To get started building a resource widget:

```php
php artisan make:filament-widget CustomerOverview --resource=CustomerResource

```
This command will create two files - a widget class in the `app/Filament/Resources/CustomerResource/Widgets` directory, and a view in the `resources/views/filament/resources/customer-resource/widgets` directory.

You must register the new widget in your resource’s `getWidgets()` method:

```php
public static function getWidgets(): array
{
    return [
        CustomerResource\Widgets\CustomerOverview::class,
    ];
}

```
If you’d like to learn how to build and customize widgets, check out the Dashboard documentation section.

#Displaying a widget on a resource page
---------------------------------------

To display a widget on a resource page, use the `getHeaderWidgets()` or `getFooterWidgets()` methods for that page:

```php
<?php

namespace App\Filament\Resources\CustomerResource\Pages;

use App\Filament\Resources\CustomerResource;

class ListCustomers extends ListRecords
{
    public static string $resource = CustomerResource::class;

    protected function getHeaderWidgets(): array
    {
        return [
            CustomerResource\Widgets\CustomerOverview::class,
        ];
    }
}

```
`getHeaderWidgets()` returns an array of widgets to display above the page content, whereas `getFooterWidgets()` are displayed below.

If you’d like to customize the number of grid columns used to arrange widgets, check out the Pages documentation.

#Accessing the current record in the widget
-------------------------------------------

If you’re using a widget on an Edit or View page, you may access the current record by defining a `$record` property on the widget class:

```php
use Illuminate\Database\Eloquent\Model;

public ?Model $record = null;

```
#Accessing page table data in the widget
----------------------------------------

If you’re using a widget on a List page, you may access the table data by first adding the `ExposesTableToWidgets` trait to the page class:

```php
use Filament\Pages\Concerns\ExposesTableToWidgets;
use Filament\Resources\Pages\ListRecords;

class ListProducts extends ListRecords
{
    use ExposesTableToWidgets;

    // ...
}

```
Now, on the widget class, you must add the `InteractsWithPageTable` trait, and return the name of the page class from the `getTablePage()` method:

```php
use App\Filament\Resources\ProductResource\Pages\ListProducts;
use Filament\Widgets\Concerns\InteractsWithPageTable;
use Filament\Widgets\Widget;

class ProductStats extends Widget
{
    use InteractsWithPageTable;

    protected function getTablePage(): string
    {
        return ListProducts::class;
    }

    // ...
}

```
In the widget class, you can now access the Eloquent query builder instance for the table data using the `$this->getPageTableQuery()` method:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

Stat::make('Total Products', $this->getPageTableQuery()->count()),

```
Alternatively, you can access a collection of the records on the current page using the `$this->getPageTableRecords()` method:

```php
use Filament\Widgets\StatsOverviewWidget\Stat;

Stat::make('Total Products', $this->getPageTableRecords()->count()),

```
#Passing properties to widgets on resource pages
------------------------------------------------

When registering a widget on a resource page, you can use the `make()` method to pass an array of Livewire properties to it:

```php
protected function getHeaderWidgets(): array
{
    return [
        CustomerResource\Widgets\CustomerOverview::make([
            'status' => 'active',
        ]),
    ];
}

```
This array of properties gets mapped to public Livewire properties on the widget class:

```php
use Filament\Widgets\Widget;

class CustomerOverview extends Widget
{
    public string $status;

    // ...
}

```
Now, you can access the `status` in the widget class using `$this->status`.

Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion