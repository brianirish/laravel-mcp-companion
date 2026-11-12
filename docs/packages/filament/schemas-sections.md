Source: https://filamentphp.com/docs/5.x/schemas/sections.md

# Sections

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/schemas/sections.md

## Introduction

You may want to separate your fields into sections, each with a heading and description. To do this, you can use a section component:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
```

As well as allowing static values, the ` make() ` and ` description() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |




You can also use a section without a header, which just wraps the components in a simple card:

```php
use Filament\Schemas\Components\Section;

Section::make()
    ->schema([
        // ...
    ])
```



## Adding an icon to the section's header

You may add an [icon](https://filamentphp.com/docs/5.x/styling/icons.md) to the section's header using the ` icon() ` method:

```php
use Filament\Schemas\Components\Section;
use Filament\Support\Icons\Heroicon;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->icon(Heroicon::ShoppingBag)
    ->schema([
        // ...
    ])
```

As well as allowing a static value, the ` icon() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |




## Positioning the heading and description aside

You may use the ` aside() ` to align heading & description on the left, and the components inside a card on the right:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside()
    ->schema([
        // ...
    ])
```



Optionally, you may pass a boolean value to control if the section should be aside or not:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->aside(FeatureFlag::active())
    ->schema([
        // ...
    ])
```

As well as allowing a static value, the ` aside() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


### Positioning the content before the heading

Use ` contentBefore() ` with ` aside() ` to position the content before the heading and description on medium and larger screens:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->aside()
    ->contentBefore()
    ->schema([
        // ...
    ])
```

You may pass a boolean or a closure to ` contentBefore() ` to control this condition.

## Collapsing sections

Sections may be ` collapsible() ` to optionally hide long content:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
```

Your sections may be ` collapsed() ` by default:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsed()
```



Optionally, the ` collapsible() ` and ` collapsed() ` methods accept a boolean value to control if the section should be collapsible and collapsed or not:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible(FeatureFlag::active())
    ->collapsed(FeatureFlag::active())
```

As well as allowing static values, the ` collapsible() ` and ` collapsed() ` methods also accept functions to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


If a collapsed section contains components that are expensive to render, you can [lazy load its content](https://filamentphp.com/docs/5.x/schemas/sections.md#lazy-loading-section-content) when the section is expanded.

### Persisting collapsed sections in the user's session

You can persist whether a section is collapsed in local storage using the ` persistCollapsed() ` method, so it will remain collapsed when the user refreshes the page:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed()
```

To persist the collapse state, the local storage needs a unique ID to store the state. This ID is generated based on the heading of the section. If your section does not have a heading, or if you have multiple sections with the same heading that you do not want to collapse together, you can manually specify the ` id() ` of that section to prevent an ID conflict:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed()
    ->id('order-cart')
```

Optionally, the ` persistCollapsed() ` method accepts a boolean value to control if the section should persist its collapsed state or not:

```php
use Filament\Schemas\Components\Section;

Section::make('Cart')
    ->description('The items you have selected for purchase')
    ->schema([
        // ...
    ])
    ->collapsible()
    ->persistCollapsed(FeatureFlag::active())
```

As well as allowing static values, the ` persistCollapsed() ` and ` id() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


## Compact section styling

When nesting sections, you can use a more compact styling:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->compact()
```



Optionally, the ` compact() ` method accepts a boolean value to control if the section should be compact or not:

```php
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->compact(FeatureFlag::active())
```

As well as allowing a static value, the ` compact() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


## Secondary section styling

By default, sections have a contrasting background color, which makes them stand out against a gray background. Secondary styling gives the section a less contrasting background, so it is usually slightly darker. This is a better styling when the background color behind the section is the same color as the default section background color, for example when a section is nested inside another section. Secondary sections can be created using the ` secondary() ` method:

```php
use Filament\Schemas\Components\Section;

Section::make('Notes')
    ->schema([
        // ...
    ])
    ->secondary()
    ->compact()
```



Optionally, the ` secondary() ` method accepts a boolean value to control if the section should be secondary or not:

```php
use Filament\Schemas\Components\Section;

Section::make('Notes')
    ->schema([
        // ...
    ])
    ->secondary(FeatureFlag::active())
```

## Inserting actions and other components in the header of a section

You may insert [actions](https://filamentphp.com/docs/5.x/actions) and any other schema component (usually [prime components](https://filamentphp.com/docs/5.x/schemas/primes.md)) into the header of a section by passing an array of components to the ` afterHeader() ` method:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->afterHeader([
        Action::make('test'),
    ])
    ->schema([
        // ...
    ])
```

As well as allowing a static value, the ` afterHeader() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |




## Inserting actions and other components in the footer of a section

You may insert [actions](https://filamentphp.com/docs/5.x/actions) and any other schema component (usually [prime components](https://filamentphp.com/docs/5.x/schemas/primes.md)) into the footer of a section by passing an array of components to the ` footer() ` method:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Section;

Section::make('Rate limiting')
    ->description('Prevent abuse by limiting the number of requests per period')
    ->schema([
        // ...
    ])
    ->footer([
        Action::make('test'),
    ])
```

As well as allowing a static value, the ` footer() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |




## Using grid columns within a section

You may use the ` columns() ` method to easily create a [grid](https://filamentphp.com/docs/5.x/schemas/layouts.md#grid-system) within the section:

```php
use Filament\Schemas\Components\Section;

Section::make('Heading')
    ->schema([
        // ...
    ])
    ->columns(2)
```



As well as allowing a static value, the ` columns() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


## Lazy loading section content

If the content of a section is expensive to render, you can pass a ` Schema ` object to ` schema() ` and use ` lazyLoaded() `. This is particularly useful for a section that is [collapsed](https://filamentphp.com/docs/5.x/schemas/sections.md#collapsing-sections) by default. The section and its header will render immediately, while its content will not be loaded until the section is expanded and the content enters the viewport:

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Section;
use Filament\Schemas\Schema;

Section::make('Customer details')
    ->key('customerDetails')
    ->schema(
        Schema::make()
            ->components([
                TextInput::make('name'),
                TextInput::make('email')
                    ->email(),
            ])
            ->lazyLoaded(),
    )
    ->collapsed()
```

Every lazy schema must have a unique key. In this example, the child schema inherits its key from the section. You can learn more in the [schema overview](https://filamentphp.com/docs/5.x/schemas/overview.md#lazy-loading-a-child-schema).
