Source: https://filamentphp.com/docs/5.x/schemas/overview.md

# Overview

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/schemas/overview.md

## Introduction

Schemas let you build user interfaces in PHP by combining components for input, display, and layout. A schema is represented by a ` Filament\Schemas\Schema ` object, and you pass its components to the ` components() ` method. Components can contain child schemas to create nested layouts.

Filament packages provide you with various components. You can find a full list in the [available components section](https://filamentphp.com/docs/5.x/schemas/overview.md#available-components):

- [Form fields](https://filamentphp.com/docs/5.x/forms) accept input from the user, for example, a text input, a select, or a checkbox. They come with integrated validation.
- [Infolist entries](https://filamentphp.com/docs/5.x/infolists) are components for rendering "description lists." Entries are key-value UI elements that can present read-only information like text, icons, and images. The data for an infolist can be sourced from anywhere but commonly comes from an individual Eloquent record.
- [Layout components](https://filamentphp.com/docs/5.x/schemas/layouts.md) are used to structure the components. For example, a grid, tabs, or a multi-step form wizard.
- [Prime components](https://filamentphp.com/docs/5.x/schemas/primes.md) are simple components that are used to render basic stand-alone static content, such as text, images, and buttons (actions).

## Available components

For building [forms](https://filamentphp.com/docs/5.x/forms), Filament includes a set of fields for different data types:

- [Text input](https://filamentphp.com/docs/5.x/forms/text-input.md)
- [Select](https://filamentphp.com/docs/5.x/forms/select.md)
- [Checkbox](https://filamentphp.com/docs/5.x/forms/checkbox.md)
- [Toggle](https://filamentphp.com/docs/5.x/forms/toggle.md)
- [Checkbox list](https://filamentphp.com/docs/5.x/forms/checkbox-list.md)
- [Radio](https://filamentphp.com/docs/5.x/forms/radio.md)
- [Date-time picker](https://filamentphp.com/docs/5.x/forms/date-time-picker.md)
- [File upload](https://filamentphp.com/docs/5.x/forms/file-upload.md)
- [Rich editor](https://filamentphp.com/docs/5.x/forms/rich-editor.md)
- [Markdown editor](https://filamentphp.com/docs/5.x/forms/markdown-editor.md)
- [Repeater](https://filamentphp.com/docs/5.x/forms/repeater.md)
- [Builder](https://filamentphp.com/docs/5.x/forms/builder.md)
- [Tags input](https://filamentphp.com/docs/5.x/forms/tags-input.md)
- [Textarea](https://filamentphp.com/docs/5.x/forms/textarea.md)
- [Key-value](https://filamentphp.com/docs/5.x/forms/key-value.md)
- [Color picker](https://filamentphp.com/docs/5.x/forms/color-picker.md)
- [Toggle buttons](https://filamentphp.com/docs/5.x/forms/toggle-buttons.md)
- [Slider](https://filamentphp.com/docs/5.x/forms/slider.md)
- [Code editor](https://filamentphp.com/docs/5.x/forms/code-editor.md)
- [Hidden](https://filamentphp.com/docs/5.x/forms/hidden.md)
- Or, build your own [custom form field](https://filamentphp.com/docs/5.x/forms/custom-fields.md)

For displaying data in a label-value "description list" format, Filament includes [infolist](https://filamentphp.com/docs/5.x/infolists) entry components:

- [Text entry](https://filamentphp.com/docs/5.x/infolists/text-entry.md)
- [Icon entry](https://filamentphp.com/docs/5.x/infolists/icon-entry.md)
- [Image entry](https://filamentphp.com/docs/5.x/infolists/image-entry.md)
- [Color entry](https://filamentphp.com/docs/5.x/infolists/color-entry.md)
- [Code entry](https://filamentphp.com/docs/5.x/infolists/code-entry.md)
- [Key-value entry](https://filamentphp.com/docs/5.x/infolists/key-value-entry.md)
- [Repeatable entry](https://filamentphp.com/docs/5.x/infolists/repeatable-entry.md)
- Or, build your own [custom infolist entry](https://filamentphp.com/docs/5.x/infolists/custom-entries.md)

To arrange components into a [layout](https://filamentphp.com/docs/5.x/schemas/layouts.md), Filament includes layout components:

- [Grid](https://filamentphp.com/docs/5.x/schemas/layouts.md#grid-component)
- [Flex](https://filamentphp.com/docs/5.x/schemas/layouts.md#flex-component)
- [Fieldset](https://filamentphp.com/docs/5.x/schemas/layouts.md#fieldset-component)
- [Section](https://filamentphp.com/docs/5.x/schemas/sections.md)
- [Tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md)
- [Wizard](https://filamentphp.com/docs/5.x/schemas/wizards.md)
- [Callout](https://filamentphp.com/docs/5.x/schemas/callouts.md)
- [Empty states](https://filamentphp.com/docs/5.x/schemas/empty-states.md)
- Or, build your own [custom layout component](https://filamentphp.com/docs/5.x/schemas/custom-components.md#custom-component-classes)

For displaying arbitrary content, Filament includes [prime](https://filamentphp.com/docs/5.x/schemas/primes.md) components:

- [Text](https://filamentphp.com/docs/5.x/schemas/primes.md#text-component)
- [Icon](https://filamentphp.com/docs/5.x/schemas/primes.md#icon-component)
- [Image](https://filamentphp.com/docs/5.x/schemas/primes.md#image-component)
- [Unordered list](https://filamentphp.com/docs/5.x/schemas/primes.md#unordered-list-component)

You can also insert "action" buttons into schemas. These can run PHP functions, and even open modals. For more information, see the [actions documentation](https://filamentphp.com/docs/5.x/actions).

You can learn more about building custom components to render your own Blade views in the [custom components documentation](https://filamentphp.com/docs/5.x/schemas/custom-components.md).

## An example schema

For example, you may want to build a form with a schema. The name of the schema is usually dictated by the name of the method that it is defined in (` form ` in this example). Filament creates the ` Schema ` object and passes it to the method, which then returns the schema with the components added:

```php
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

$schema
    ->components([
        Grid::make(2)
            ->schema([
                Section::make('Details')
                    ->schema([
                        TextInput::make('name'),
                        Select::make('position')
                            ->options([
                                'developer' => 'Developer',
                                'designer' => 'Designer',
                            ]),
                        Checkbox::make('is_admin'),
                    ]),
                Section::make('Auditing')
                    ->schema([
                        TextEntry::make('created_at')
                            ->dateTime(),
                        TextEntry::make('updated_at')
                            ->dateTime(),
                    ]),
            ]),
    ])
```



[Grid](https://filamentphp.com/docs/5.x/schemas/layouts.md#grid-component) is a layout component that renders multiple components together in a responsive grid. The number of columns in the grid is specified in the ` make() ` method. The ` schema() ` method is used to nest components within the grid.

[Section](https://filamentphp.com/docs/5.x/schemas/sections.md) is another layout component that renders multiple components together in a card, with a heading at the top.

[TextInput](https://filamentphp.com/docs/5.x/forms/text-input.md), [Select](https://filamentphp.com/docs/5.x/forms/select.md), and [Checkbox](https://filamentphp.com/docs/5.x/forms/checkbox.md) are form components that accept input from the user.

[TextEntry](https://filamentphp.com/docs/5.x/infolists/text-entry.md) is an infolist component that displays read-only information. In this example, it is used to display the created and updated timestamps of the record. The ` dateTime() ` method is used to format the timestamps as dates and times.

The schema object is the container for the components and can now be rendered. Rendering the schema will render all the components within it in the correct layout.

## Component utility injection

The vast majority of methods used to configure entries accept functions as parameters instead of hardcoded values:

```php
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

Grid::make()->columns(fn (): array => [
    'lg' => auth()->user()->isAdmin() ? 4 : 6,
])->schema([
    // ...
])

Section::make()
    ->heading(fn (): string => auth()->user()->isAdmin() ? 'Admin Dashboard' : 'User Dashboard')
    ->schema([
        // ...
    ])
```

This alone unlocks many customization possibilities.

The package is also able to inject many utilities to use inside these functions, as parameters. All customization methods that accept functions as arguments can inject utilities.

These injected utilities require specific parameter names to be used. Otherwise, Filament doesn't know what to inject.

### Injecting the state of another component

You may also retrieve the state (value) of a form field or infolist entry from within a callback, using a ` $get ` parameter:

```php
use Filament\Schemas\Components\Utilities\Get;

function (Get $get) {
    $email = $get('email'); // Store the value of the `email` entry in the `$email` variable.
    //...
}
```

> [!TIP]
> Unless a form field is [reactive](https://filamentphp.com/docs/5.x/forms/overview.md#the-basics-of-reactivity), the schema will not refresh when the value of the field changes, only when the next user interaction occurs that makes a request to the server. If you need to react to changes in a field's value, it should be ` live() `.

By default, ` Get ` and ` Set ` avoid resolving fresh child schemas of the component being evaluated while searching for state, but can still search its cached descendants. This prevents recursive schema evaluation. If you need to include fresh child schemas, you can call ` skipComponentsChildSchemasWhileSearching(false) ` on the utility before using it. Do not disable this protection inside a child schema callback that would resolve itself again.

### Injecting the current Eloquent record

You may retrieve the Eloquent record for the current schema using a ` $record ` parameter:

```php
use Illuminate\Database\Eloquent\Model;

function (?Model $record) {
    // ...
}
```

### Injecting the current operation

If you're writing a schema for a panel resource or relation manager, and you wish to check if a schema is ` create `, ` edit ` or ` view `, use the ` $operation ` parameter:

```php
function (string $operation) {
    // ...
}
```

> [!NOTE]
> You can manually set a schema's operation using the ` $schema->operation() ` method.

### Injecting the current Livewire component instance

If you wish to access the current Livewire component instance, define a ` $livewire ` parameter:

```php
use Livewire\Component;

function (Component $livewire) {
    // ...
}
```

### Injecting the current component instance

If you wish to access the current component instance, define a ` $component ` parameter:

```php
use Filament\Schemas\Components\Component;

function (Component $component) {
    // ...
}
```

### Injecting multiple utilities

The parameters are injected dynamically using reflection, so you are able to combine multiple parameters in any order:

```php
use Filament\Schemas\Components\Utilities\Get;
use Filament\Schemas\Components\Utilities\Set;
use Livewire\Component as Livewire;

function (Livewire $livewire, Get $get, Set $set) {
    // ...
}
```

### Injecting dependencies from Laravel's container

You may inject anything from Laravel's container like normal, alongside utilities:

```php
use Filament\Schemas\Components\Utilities\Set;
use Illuminate\Http\Request;

function (Request $request, Set $set) {
    // ...
}
```

## Lazy loading a child schema

By default, a schema's components are rendered when the page loads. If a child schema is expensive to render, you can lazy load it when it enters the viewport using the ` lazyLoaded() ` method:

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
```

The lazy schema initially renders a loading indicator. When the loading indicator enters the viewport, only that schema is rendered in a new request. If the schema contains a validation error before it has loaded, it is loaded automatically so the validation error can be revealed.

If a lazy schema is inside a concealed component, such as a collapsed section or an inactive tab, it will not load until its parent is revealed and it enters the viewport. Once a schema has loaded, it remains loaded for the lifetime of the Livewire component.

Every lazy schema needs a unique key. In this example, the child schema inherits the ` customerDetails ` key from the section. You can instead call ` key() ` on the child schema itself. If multiple child schemas of the same component are lazy, such as a section's content and footer schemas, you must call ` key() ` on each additional schema so that they do not inherit the same key. If you lazy load the schema for a repeater item or builder block, each item schema automatically receives a unique key from its state path:

```php
use Filament\Forms\Components\Repeater;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

Repeater::make('members')
    ->schema(
        Schema::make()
            ->components([
                TextInput::make('name'),
                TextInput::make('email')
                    ->email(),
            ])
            ->lazyLoaded(),
    )
```

You may also pass a boolean or function to ` lazyLoaded() ` to control it conditionally.

## Setting the root heading level

By default, headings in a schema start at level two, since schemas are usually rendered below a page's level-one heading. If you render a schema elsewhere in the document hierarchy, you can change its root heading level using the ` rootHeadingLevel() ` method:

```php
use Filament\Schemas\Schema;

public function productSchema(Schema $schema): Schema
{
    return $schema
        ->rootHeadingLevel(3)
        ->components([
            // ...
        ]);
}
```

In this example, the schema is rendered below a level-two heading, so its headings start at level three. Nested section headings automatically use the next level. Labelled repeater and builder items also advance the heading level used by components inside them.

## Global settings

If you wish to change the default behavior of a component globally, then you can call the static ` configureUsing() ` method inside a service provider's ` boot() ` method, to which you pass a Closure to modify the component using. For example, if you wish to make all section components have [2 columns](https://filamentphp.com/docs/5.x/schemas/sections.md#using-grid-columns-within-a-section) by default, you can do it like so:

```php
use Filament\Schemas\Components\Section;

Section::configureUsing(function (Section $section): void {
    $section
        ->columns(2);
});
```

Of course, you are still able to overwrite this on each component individually:

```php
use Filament\Schemas\Components\Section;

Section::make()
    ->columns(1)
```

## Restricting Livewire file uploads to schema components

If you build a custom Livewire component on top of ` InteractsWithSchemas `, Livewire's file upload RPC methods accept uploads to any property path by default. See [Restricting Livewire file uploads to schema components](https://filamentphp.com/docs/5.x/advanced/security.md#restricting-livewire-file-uploads-to-schema-components) in the security documentation for the ` RestrictsFileUploadsToSchemaComponents ` trait that locks them down.
