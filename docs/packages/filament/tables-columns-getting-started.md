# Filament - Tables/Columns/Getting Started

Source: https://filamentphp.com/docs/3.x/tables/columns/getting-started

#Overview
---------

![Filament](/docs/_astro/filament-laracasts-logo.CzN-P2OP.webp)  ![Laracasts](/docs/_astro/laracasts.xZHGp0JC.svg)

Table Columns

Watch the Rapid Laravel Development with Filament series on Laracasts - it will teach you the basics of adding columns to Filament resource tables.

Play Video

![Kevin McKee](https://avatars.githubusercontent.com/u/4503765?v=4)

Kevin McKee

Instructor

Column classes can be found in the `Filament\Tables\Columns` namespace. You can put them inside the `$table->columns()` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ]);
}

```
Columns may be created using the static `make()` method, passing its unique name. The name of the column should correspond to a column or accessor on your model. You may use “dot notation” to access columns within relationships.

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')

TextColumn::make('author.name')

```
#Available columns
------------------

Filament ships with two main types of columns - static and editable.

Static columns display data to the user:

* Text column
* Icon column
* Image column
* Color column

Editable columns allow the user to update data in the database without leaving the table:

* Select column
* Toggle column
* Text input column
* Checkbox column

You may also create your own custom columns to display data however you wish.

#Setting a label
----------------

By default, the label of the column, which is displayed in the header of the table, is generated from the name of the column. You may customize this using the `label()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->label('Post title')

```
Optionally, you can have the label automatically translated using Laravel’s localization features with the `translateLabel()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->translateLabel() // Equivalent to `label(__('Title'))`

```
#Sorting
--------

Columns may be sortable, by clicking on the column label. To make a column sortable, you must use the `sortable()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->sortable()

```
![Table with sortable column](/docs/3.x/images/light/tables/columns/sortable.jpg) ![Table with sortable column](/docs/3.x/images/dark/tables/columns/sortable.jpg)

If you’re using an accessor column, you may pass `sortable()` an array of database columns to sort by:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('full_name')
    ->sortable(['first_name', 'last_name'])

```
You may customize how the sorting is applied to the Eloquent query using a callback:

```php
use Filament\Tables\Columns\TextColumn;
use Illuminate\Database\Eloquent\Builder;

TextColumn::make('full_name')
    ->sortable(query: function (Builder $query, string $direction): Builder {
        return $query
            ->orderBy('last_name', $direction)
            ->orderBy('first_name', $direction);
    })

```
#Sorting by default
-------------------

You may choose to sort a table by default if no other sort is applied. You can use the `defaultSort()` method for this:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->defaultSort('stock', 'desc');
}

```
### #Persist sort in session

To persist the sorting in the user’s session, use the `persistSortInSession()` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->persistSortInSession();
}

```
### #Setting a default sort option label

To set a default sort option label, use the `defaultSortOptionLabel()` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->defaultSortOptionLabel('Date');
}

```
#Searching
----------

Columns may be searchable by using the text input field in the top right of the table. To make a column searchable, you must use the `searchable()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->searchable()

```
![Table with searchable column](/docs/3.x/images/light/tables/columns/searchable.jpg) ![Table with searchable column](/docs/3.x/images/dark/tables/columns/searchable.jpg)

If you’re using an accessor column, you may pass `searchable()` an array of database columns to search within:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('full_name')
    ->searchable(['first_name', 'last_name'])

```
You may customize how the search is applied to the Eloquent query using a callback:

```php
use Filament\Tables\Columns\TextColumn;
use Illuminate\Database\Eloquent\Builder;

TextColumn::make('full_name')
    ->searchable(query: function (Builder $query, string $search): Builder {
        return $query
            ->where('first_name', 'like', "%{$search}%")
            ->orWhere('last_name', 'like', "%{$search}%");
    })

```
#### #Customizing the table search field placeholder

You may customize the placeholder in the search field using the `searchPlaceholder()` method on the `$table`:

```php
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->searchPlaceholder('Search (ID, Name)');
}

```
### #Searching individually

You can choose to enable a per-column search input field using the `isIndividual` parameter:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->searchable(isIndividual: true)

```
![Table with individually searchable column](/docs/3.x/images/light/tables/columns/individually-searchable.jpg) ![Table with individually searchable column](/docs/3.x/images/dark/tables/columns/individually-searchable.jpg)

If you use the `isIndividual` parameter, you may still search that column using the main “global” search input field for the entire table.

To disable that functionality while still preserving the individual search functionality, you need the `isGlobal` parameter:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->searchable(isIndividual: true, isGlobal: false)

```
You may optionally persist the searches in the query string:

```php
use Livewire\Attributes\Url;

/**
 * @var array<string, string | array<string, string | null> | null>
 */
#[Url]
public array $tableColumnSearches = [];

```
### #Customizing the table search debounce

You may customize the debounce time in all table search fields using the `searchDebounce()` method on the `$table`. By default it is set to `500ms`:

```php
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->searchDebounce('750ms');
}

```
### #Searching when the input is blurred

Instead of automatically reloading the table contents while the user is typing their search, which is affected by the debounce of the search field, you may change the behavior so that the table is only searched when the user blurs the input (tabs or clicks out of it), using the `searchOnBlur()` method:

```php
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->searchOnBlur();
}

```
### #Persist search in session

To persist the table or individual column search in the user’s session, use the `persistSearchInSession()` or `persistColumnSearchInSession()` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->persistSearchInSession()
        ->persistColumnSearchesInSession();
}

```
#Column actions and URLs
------------------------

When a cell is clicked, you may run an “action”, or open a URL.

### #Running actions

To run an action, you may use the `action()` method, passing a callback or the name of a Livewire method to run. Each method accepts a `$record` parameter which you may use to customize the behavior of the action:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->action(function (Post $record): void {
        $this->dispatch('open-post-edit-modal', post: $record->getKey());
    })

```
#### #Action modals

You may open action modals by passing in an `Action` object to the `action()` method:

```php
use Filament\Tables\Actions\Action;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->action(
        Action::make('select')
            ->requiresConfirmation()
            ->action(function (Post $record): void {
                $this->dispatch('select-post', post: $record->getKey());
            }),
    )

```
Action objects passed into the `action()` method must have a unique name to distinguish it from other actions within the table.

### #Opening URLs

To open a URL, you may use the `url()` method, passing a callback or static URL to open. Callbacks accept a `$record` parameter which you may use to customize the URL:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->url(fn (Post $record): string => route('posts.edit', ['post' => $record]))

```
You may also choose to open the URL in a new tab:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->url(fn (Post $record): string => route('posts.edit', ['post' => $record]))
    ->openUrlInNewTab()

```
#Setting a default value
------------------------

To set a default value for columns with an empty state, you may use the `default()` method. This method will treat the default state as if it were real, so columns like image or color will display the default image or color.

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('description')
    ->default('No description.')

```
#Adding placeholder text if a column is empty
---------------------------------------------

Sometimes you may want to display placeholder text for columns with an empty state, which is styled as a lighter gray text. This differs from the default value, as the placeholder is always text and not treated as if it were real state.

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('description')
    ->placeholder('No description.')

```
![Column with a placeholder for empty state](/docs/3.x/images/light/tables/columns/placeholder.jpg) ![Column with a placeholder for empty state](/docs/3.x/images/dark/tables/columns/placeholder.jpg)

#Hiding columns
---------------

To hide a column conditionally, you may use the `hidden()` and `visible()` methods, whichever you prefer:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('role')
    ->hidden(! auth()->user()->isAdmin())
// or
TextColumn::make('role')
    ->visible(auth()->user()->isAdmin())

```
### #Toggling column visibility

Users may hide or show columns themselves in the table. To make a column toggleable, use the `toggleable()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('email')
    ->toggleable()

```
![Table with toggleable column](/docs/3.x/images/light/tables/columns/toggleable.jpg) ![Table with toggleable column](/docs/3.x/images/dark/tables/columns/toggleable.jpg)

#### #Making toggleable columns hidden by default

By default, toggleable columns are visible. To make them hidden instead:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('id')
    ->toggleable(isToggledHiddenByDefault: true)

```
#### #Customizing the toggle columns dropdown trigger action

To customize the toggle dropdown trigger button, you may use the `toggleColumnsTriggerAction()` method, passing a closure that returns an action. All methods that are available to customize action trigger buttons can be used:

```php
use Filament\Tables\Actions\Action;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->filters([
            // ...
        ])
        ->toggleColumnsTriggerAction(
            fn (Action $action) => $action
                ->button()
                ->label('Toggle columns'),
        );
}

```
#Calculated state
-----------------

Sometimes you need to calculate the state of a column, instead of directly reading it from a database column.

By passing a callback function to the `state()` method, you can customize the returned state for that column based on the `$record`:

```php
use App\Models\Order;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('amount_including_vat')
    ->state(function (Order $record): float {
        return $record->amount * (1 + $record->vat_rate);
    })

```
#Tooltips
---------

You may specify a tooltip to display when you hover over a cell:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->tooltip('Title')

```
![Table with column triggering a tooltip](/docs/3.x/images/light/tables/columns/tooltips.jpg) ![Table with column triggering a tooltip](/docs/3.x/images/dark/tables/columns/tooltips.jpg)

This method also accepts a closure that can access the current table record:

```php
use Filament\Tables\Columns\TextColumn;
use Illuminate\Database\Eloquent\Model;

TextColumn::make('title')
    ->tooltip(fn (Model $record): string => "By {$record->author->name}")

```
#Horizontally aligning column content
-------------------------------------

Table columns are aligned to the start (left in LTR interfaces or right in RTL interfaces) by default. You may change the alignment using the `alignment()` method, and passing it `Alignment::Start`, `Alignment::Center`, `Alignment::End` or `Alignment::Justify` options:

```php
use Filament\Support\Enums\Alignment;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('email')
    ->alignment(Alignment::End)

```
![Table with column aligned to the end](/docs/3.x/images/light/tables/columns/alignment.jpg) ![Table with column aligned to the end](/docs/3.x/images/dark/tables/columns/alignment.jpg)

Alternatively, you may use shorthand methods like `alignEnd()`:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->alignEnd()

```
#Vertically aligning column content
-----------------------------------

Table column content is vertically centered by default. You may change the vertical alignment using the `verticalAlignment()` method, and passing it `VerticalAlignment::Start`, `VerticalAlignment::Center` or `VerticalAlignment::End` options:

```php
use Filament\Support\Enums\VerticalAlignment;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->verticalAlignment(VerticalAlignment::Start)

```
![Table with column vertically aligned to the start](/docs/3.x/images/light/tables/columns/vertical-alignment.jpg) ![Table with column vertically aligned to the start](/docs/3.x/images/dark/tables/columns/vertical-alignment.jpg)

Alternatively, you may use shorthand methods like `verticallyAlignStart()`:

```php
use Filament\Support\Enums\VerticalAlignment;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->verticallyAlignStart()

```
#Allowing column headers to wrap
--------------------------------

By default, column headers will not wrap onto multiple lines, if they need more space. You may allow them to wrap using the `wrapHeader()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->wrapHeader()

```
#Controlling the width of columns
---------------------------------

By default, columns will take up as much space as they need. You may allow some columns to consume more space than others by using the `grow()` method:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->grow()

```
Alternatively, you can define a width for the column, which is passed to the header cell using the `style` attribute, so you can use any valid CSS value:

```php
use Filament\Tables\Columns\IconColumn;

IconColumn::make('is_paid')
    ->label('Paid')
    ->boolean()
    ->width('1%')

```
#Grouping columns
-----------------

You group multiple columns together underneath a single heading using a `ColumnGroup` object:

```php
use Filament\Tables\Columns\ColumnGroup;
use Filament\Tables\Columns\IconColumn;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('title'),
            TextColumn::make('slug'),
            ColumnGroup::make('Visibility', [
                TextColumn::make('status'),
                IconColumn::make('is_featured'),
            ]),
            TextColumn::make('author.name'),
        ]);
}

```
The first argument is the label of the group, and the second is an array of column objects that belong to that group.

![Table with grouped columns](/docs/3.x/images/light/tables/columns/grouping.jpg) ![Table with grouped columns](/docs/3.x/images/dark/tables/columns/grouping.jpg)

You can also control the group header alignment and wrapping on the `ColumnGroup` object. To improve the multi-line fluency of the API, you can chain the `columns()` onto the object instead of passing it as the second argument:

```php
use Filament\Support\Enums\Alignment;
use Filament\Tables\Columns\ColumnGroup;

ColumnGroup::make('Website visibility')
    ->columns([
        // ...
    ])
    ->alignment(Alignment::Center)
    ->wrapHeader()

```
#Custom attributes
------------------

The HTML of columns can be customized, by passing an array of `extraAttributes()`:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('slug')
    ->extraAttributes(['class' => 'bg-gray-200'])

```
These get merged onto the outer `<div>` element of each cell in that column.

#Global settings
----------------

If you wish to change the default behavior of all columns globally, then you can call the static `configureUsing()` method inside a service provider’s `boot()` method, to which you pass a Closure to modify the columns using. For example, if you wish to make all columns `searchable()` and `toggleable()`, you can do it like so:

```php
use Filament\Tables\Columns\Column;

Column::configureUsing(function (Column $column): void {
    $column
        ->toggleable()
        ->searchable();
});

```
Additionally, you can call this code on specific column types as well:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::configureUsing(function (TextColumn $column): void {
    $column
        ->toggleable()
        ->searchable();
});

```
Of course, you are still able to overwrite this on each column individually:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::make('name')
    ->toggleable(false)

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion