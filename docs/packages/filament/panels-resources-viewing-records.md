# Filament - Panels/Resources/Viewing Records

Source: https://filamentphp.com/docs/3.x/panels/resources/viewing-records

#Creating a resource with a View page
-------------------------------------

To create a new resource with a View page, you can use the `--view` flag:

```php
php artisan make:filament-resource User --view

```
#Using an infolist instead of a disabled form
---------------------------------------------

![Filament](/docs/_astro/filament-laracasts-logo.CzN-P2OP.webp)  ![Laracasts](/docs/_astro/laracasts.xZHGp0JC.svg)

Infolists

Watch the Rapid Laravel Development with Filament series on Laracasts - it will teach you the basics of adding infolists to Filament resources.

Play Video

![Kevin McKee](https://avatars.githubusercontent.com/u/4503765?v=4)

Kevin McKee

Instructor

By default, the View page will display a disabled form with the record’s data. If you preferred to display the record’s data in an “infolist”, you can define an `infolist()` method on the resource class:

```php
use Filament\Infolists;
use Filament\Infolists\Infolist;

public static function infolist(Infolist $infolist): Infolist
{
    return $infolist
        ->schema([
            Infolists\Components\TextEntry::make('name'),
            Infolists\Components\TextEntry::make('email'),
            Infolists\Components\TextEntry::make('notes')
                ->columnSpanFull(),
        ]);
}

```
The `schema()` method is used to define the structure of your infolist. It is an array of entries and layout components, in the order they should appear in your infolist.

Check out the Infolists docs for a guide on how to build infolists with Filament.

#Adding a View page to an existing resource
-------------------------------------------

If you want to add a View page to an existing resource, create a new page in your resource’s `Pages` directory:

```php
php artisan make:filament-page ViewUser --resource=UserResource --type=ViewRecord

```
You must register this new page in your resource’s `getPages()` method:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListUsers::route('/'),
        'create' => Pages\CreateUser::route('/create'),
        'view' => Pages\ViewUser::route('/{record}'),
        'edit' => Pages\EditUser::route('/{record}/edit'),
    ];
}

```
#Viewing records in modals
--------------------------

If your resource is simple, you may wish to view records in modals rather than on the View page. If this is the case, you can just delete the view page.

If your resource doesn’t contain a `ViewAction`, you can add one to the `$table->actions()` array:

```php
use Filament\Tables;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->actions([
            Tables\Actions\ViewAction::make(),
            // ...
        ]);
}

```
#Customizing data before filling the form
-----------------------------------------

You may wish to modify the data from a record before it is filled into the form. To do this, you may define a `mutateFormDataBeforeFill()` method on the View page class to modify the `$data` array, and return the modified version before it is filled into the form:

```php
protected function mutateFormDataBeforeFill(array $data): array
{
    $data['user_id'] = auth()->id();

    return $data;
}

```
Alternatively, if you’re viewing records in a modal action, check out the Actions documentation.

#Lifecycle hooks
----------------

Hooks may be used to execute code at various points within a page’s lifecycle, like before a form is filled. To set up a hook, create a protected method on the View page class with the name of the hook:

```php
use Filament\Resources\Pages\ViewRecord;

class ViewUser extends ViewRecord
{
    // ...

    protected function beforeFill(): void
    {
        // Runs before the disabled form fields are populated from the database. Not run on pages using an infolist.
    }

    protected function afterFill(): void
    {
        // Runs after the disabled form fields are populated from the database. Not run on pages using an infolist.
    }
}

```
#Authorization
--------------

For authorization, Filament will observe any model policies that are registered in your app.

Users may access the View page if the `view()` method of the model policy returns `true`.

#Creating another View page
---------------------------

One View page may not be enough space to allow users to navigate a lot of information. You can create as many View pages for a resource as you want. This is especially useful if you are using resource sub-navigation, as you are then easily able to switch between the different View pages.

To create a View page, you should use the `make:filament-page` command:

```php
php artisan make:filament-page ViewCustomerContact --resource=CustomerResource --type=ViewRecord

```
You must register this new page in your resource’s `getPages()` method:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListCustomers::route('/'),
        'create' => Pages\CreateCustomer::route('/create'),
        'view' => Pages\ViewCustomer::route('/{record}'),
        'view-contact' => Pages\ViewCustomerContact::route('/{record}/contact'),
        'edit' => Pages\EditCustomer::route('/{record}/edit'),
    ];
}

```
Now, you can define the `infolist()` or `form()` for this page, which can contain other components that are not present on the main View page:

```php
use Filament\Infolists\Infolist;

public function infolist(Infolist $infolist): Infolist
{
    return $infolist
        ->schema([
            // ...
        ]);
}

```
#Customizing relation managers for a specific view page
-------------------------------------------------------

You can specify which relation managers should appear on a view page by defining a `getAllRelationManagers()` method:

```php
protected function getAllRelationManagers(): array
{
    return [
        CustomerAddressesRelationManager::class,
        CustomerContactsRelationManager::class,
    ];
}

```
This is useful when you have multiple view pages and need different relation managers on
each page:

```php
// ViewCustomer.php
protected function getAllRelationManagers(): array
{
    return [
        RelationManagers\OrdersRelationManager::class,
        RelationManagers\SubscriptionsRelationManager::class,
    ];
}

// ViewCustomerContact.php
protected function getAllRelationManagers(): array
{
    return [
        RelationManagers\ContactsRelationManager::class,
        RelationManagers\AddressesRelationManager::class,
    ];
}

```
If `getAllRelationManagers()` isn’t defined, any relation managers defined in the resource will be used.

#Adding view pages to resource sub-navigation
---------------------------------------------

If you’re using resource sub-navigation, you can register this page as normal in `getRecordSubNavigation()` of the resource:

```php
use App\Filament\Resources\CustomerResource\Pages;
use Filament\Resources\Pages\Page;

public static function getRecordSubNavigation(Page $page): array
{
    return $page->generateNavigationItems([
        // ...
        Pages\ViewCustomerContact::class,
    ]);
}

```
#Custom view
------------

For further customization opportunities, you can override the static `$view` property on the page class to a custom view in your app:

```php
protected static string $view = 'filament.resources.users.pages.view-user';

```
This assumes that you have created a view at `resources/views/filament/resources/users/pages/view-user.blade.php`.

Here’s a basic example of what that view might contain:

```php
<x-filament-panels::page>
    @if ($this->hasInfolist())
        {{ $this->infolist }}
    @else
        {{ $this->form }}
    @endif

    @if (count($relationManagers = $this->getRelationManagers()))
        <x-filament-panels::resources.relation-managers
            :active-manager="$this->activeRelationManager"
            :managers="$relationManagers"
            :owner-record="$record"
            :page-class="static::class"
        />
    @endif
</x-filament-panels::page>

```
To see everything that the default view contains, you can check the `vendor/filament/filament/resources/views/resources/pages/view-record.blade.php` file in your project.

Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion