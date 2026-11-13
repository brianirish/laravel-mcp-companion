Source: https://filamentphp.com/docs/5.x/forms/builder.md

# Builder

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/forms/builder.md

## Introduction

Similar to a [repeater](https://filamentphp.com/docs/5.x/forms/repeater.md), the builder component allows you to output a JSON array of repeated form components. Unlike the repeater, which only defines one form schema to repeat, the builder allows you to define different schema "blocks", which you can repeat in any order. This makes it useful for building more advanced array structures.

The primary use of the builder component is to build web page content using predefined blocks. This could be content for a marketing website, or maybe even fields in an online form. The example below defines multiple blocks for different elements in the page content. On the frontend of your website, you could loop through each block in the JSON and format it how you wish.

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;

Builder::make('content')
    ->blocks([
        Block::make('heading')
            ->schema([
                TextInput::make('content')
                    ->label('Heading')
                    ->required(),
                Select::make('level')
                    ->options([
                        'h1' => 'Heading 1',
                        'h2' => 'Heading 2',
                        'h3' => 'Heading 3',
                        'h4' => 'Heading 4',
                        'h5' => 'Heading 5',
                        'h6' => 'Heading 6',
                    ])
                    ->required(),
            ])
            ->columns(2),
        Block::make('paragraph')
            ->schema([
                Textarea::make('content')
                    ->label('Paragraph')
                    ->required(),
            ]),
        Block::make('image')
            ->schema([
                FileUpload::make('url')
                    ->label('Image')
                    ->image()
                    ->required(),
                TextInput::make('alt')
                    ->label('Alt text')
                    ->required(),
            ]),
    ])
```



We recommend that you store builder data with a ` JSON ` column in your database. Additionally, if you're using Eloquent, make sure that column has an ` array ` cast.

As evident in the above example, blocks can be defined within the ` blocks() ` method of the component. Blocks are ` Builder\Block ` objects, and require a unique name, and a component schema:

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;

Builder::make('content')
    ->blocks([
        Block::make('heading')
            ->schema([
                TextInput::make('content')->required(),
                // ...
            ]),
        // ...
    ])
```

## Setting a block's label

By default, the label of the block will be automatically determined based on its name. To override the block's label, you may use the ` label() ` method. Customizing the label in this way is useful if you wish to use a [translation string for localization](https://laravel.com/docs/localization#retrieving-translation-strings):

```php
use Filament\Forms\Components\Builder\Block;

Block::make('heading')
    ->label(__('blocks.heading'))
```

### Labelling builder items based on their content

You may add a label for a builder item using the same ` label() ` method. This method accepts a closure that receives the item's data in a ` $state ` variable. If ` $state ` is null, you should return the block label that should be displayed in the block picker. Otherwise, you should return a string to be used as the item label:

```php
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;

Block::make('heading')
    ->schema([
        TextInput::make('content')
            ->live(onBlur: true)
            ->required(),
        // ...
    ])
    ->label(function (?array $state): string {
        if ($state === null) {
            return 'Heading';
        }

        return $state['content'] ?? 'Untitled heading';
    })
```

Any fields that you use from ` $state ` should be ` live() ` if you wish to see the item label update live as you use the form.

You can inject various utilities into the function passed to ` label() ` as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Index | ` int ` | ` $index ` | The zero-based index of the current block. |
| Key | ` string ` | ` $key ` | The key for the current block. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` array<string, mixed> ` | ` $state ` | The raw unvalidated data for the current block. |




### Numbering builder items

By default, items in the builder have a number next to their label. You may disable this using the ` blockNumbers(false) ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->blockNumbers(false)
```

As well as allowing a static value, the ` blockNumbers() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Setting a block's icon

Blocks may also have an [icon](https://filamentphp.com/docs/5.x/styling/icons.md), which is displayed next to the label. You can add an icon by passing its name to the ` icon() ` method:

```php
use Filament\Forms\Components\Builder\Block;
use Filament\Support\Icons\Heroicon;

Block::make('paragraph')
    ->icon(Heroicon::Bars3BottomLeft)
```

As well as allowing a static value, the ` icon() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




### Adding icons to the header of blocks

By default, blocks in the builder don't have an icon next to the header label, just in the dropdown to add new blocks. You may enable this using the ` blockIcons() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->blockIcons()
```

Optionally, you may pass a boolean value to the ` blockIcons() ` method to control if the icons are displayed in the block headers:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->blockIcons(FeatureFlag::active())
```

As well as allowing a static value, the ` blockIcons() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




## Previewing blocks

If you prefer to render read-only previews in the builder instead of the blocks' forms, you can use the ` blockPreviews() ` method. This will render each block's ` preview() ` instead of the form. Block data will be passed to the preview Blade view in a variable with the same name:

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;

Builder::make('content')
    ->blockPreviews()
    ->blocks([
        Block::make('heading')
            ->schema([
                TextInput::make('text')
                    ->placeholder('Default heading'),
            ])
            ->preview('filament.content.block-previews.heading'),
    ])
```

In ` /resources/views/filament/content/block-previews/heading.blade.php `, you can access the block data like so:

```blade
<h1>
    {{ $text ?? 'Default heading' }}
</h1>
```

Optionally, the ` blockPreviews() ` method accepts a boolean value to control if the builder should render block previews or not:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->blockPreviews(FeatureFlag::active())
```

As well as allowing static values, the ` blockPreviews() ` and ` preview() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




### Interactive block previews

By default, preview content is not interactive, and clicking it will open the Edit modal for that block to manage its settings. If you have links and buttons that you'd like to remain interactive in the block previews, you can use the ` areInteractive: true ` argument of the ` blockPreviews() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blockPreviews(areInteractive: true)
    ->blocks([
        //
    ])
```

As well as allowing a static value, the ` areInteractive ` argument also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Adding items

An action button is displayed below the builder to allow the user to add a new item.

## Setting the add action button's label

You may set a label to customize the text that should be displayed in the button for adding a builder item, using the ` addActionLabel() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->addActionLabel('Add a new block')
```

As well as allowing a static value, the ` addActionLabel() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Aligning the add action button

By default, the add action is aligned in the center. You may adjust this using the ` addActionAlignment() ` method, passing an ` Alignment ` option of ` Alignment::Start ` or ` Alignment::End `:

```php
use Filament\Forms\Components\Builder;
use Filament\Support\Enums\Alignment;

Builder::make('content')
    ->schema([
        // ...
    ])
    ->addActionAlignment(Alignment::Start)
```

As well as allowing a static value, the ` addActionAlignment() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




### Preventing the user from adding items

You may prevent the user from adding items to the builder using the ` addable(false) ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->addable(false)
```

As well as allowing a static value, the ` addable() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Deleting items

An action button is displayed on each item to allow the user to delete it.

### Preventing the user from deleting items

You may prevent the user from deleting items from the builder using the ` deletable(false) ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->deletable(false)
```

As well as allowing a static value, the ` deletable() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Reordering items

Blocks can be reordered by dragging. To provide visible controls for keyboard users, enable [reordering with buttons](https://filamentphp.com/docs/5.x/forms/builder.md#reordering-items-with-buttons).

When some blocks are hidden, reordering places the visible blocks first and retains the hidden blocks after them in the stored state.

### Preventing the user from reordering items

You may prevent the user from reordering items from the builder using the ` reorderable(false) ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->reorderable(false)
```

As well as allowing a static value, the ` reorderable() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Reordering items with buttons

You may use ` reorderableWithButtons() ` to display move up and move down buttons:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->reorderableWithButtons()
```



Optionally, you may pass a boolean value to control if the builder should be ordered with buttons or not:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->reorderableWithButtons(FeatureFlag::active())
```

As well as allowing a static value, the ` reorderableWithButtons() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Preventing reordering with drag and drop

You may use the ` reorderableWithDragAndDrop(false) ` method to prevent items from being ordered with drag and drop:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->reorderableWithDragAndDrop(false)
```

This also removes the visually hidden fallback buttons. Explicitly enabled visible move buttons remain available. Use ` reorderable(false) ` to prevent all reordering.

As well as allowing a static value, the ` reorderableWithDragAndDrop() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Collapsing items

The builder may be ` collapsible() ` to optionally hide content in long forms:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->collapsible()
```



You may also collapse all items by default:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->collapsed()
```



Optionally, the ` collapsible() ` and ` collapsed() ` methods accept a boolean value to control if the builder should be collapsible and collapsed or not:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->collapsible(FeatureFlag::active())
    ->collapsed(FeatureFlag::active())
```

As well as allowing static values, the ` collapsible() ` and ` collapsed() ` methods also accept functions to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


If collapsed items contain components that are expensive to render, you can [lazy load their block schemas](https://filamentphp.com/docs/5.x/forms/builder.md#lazy-loading-block-schemas) when they are expanded.

## Cloning items

You may allow builder items to be duplicated using the ` cloneable() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->cloneable()
```



## Customizing the block picker

### Grouping blocks

You may group blocks under headings by using named arrays in ` blocks() `:

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Textarea;

Builder::make('content')
    ->blocks([
        'Content' => [
            Block::make('heading')
                ->schema([TextInput::make('text')]),
            Block::make('paragraph')
                ->schema([Textarea::make('text')]),
        ],
        'Media' => [
            Block::make('video')
                ->schema([TextInput::make('url')->url()]),
        ],
    ])
```

Groups appear in the order they are defined. You may include ungrouped blocks alongside named groups; ungrouped blocks appear first without a heading. Grouping only affects the picker, not the order or stored state of the blocks you add.

Use group names that PHP keeps as string array keys. Integer keys (including numeric strings such as ` '2026' `, which PHP converts to integers) are treated as ungrouped lists of blocks.



When you configure multiple columns using ` blockPickerColumns() `, groups flow down each column before moving to the next. Groups stay together, and their heights are balanced across the columns. Otherwise, groups are stacked vertically. Searching hides groups with no matching blocks.

### Changing the number of columns in the block picker

The block picker has only 1 column. You may customize it by passing a number of columns to ` blockPickerColumns() `:

```php
use Filament\Forms\Components\Builder;

Builder::make()
    ->blockPickerColumns(2)
    ->blocks([
        // ...
    ])
```

This method can be used in a couple of different ways:

- You can pass an integer like ` blockPickerColumns(2) `. This integer is the number of columns used on the ` lg ` breakpoint and higher. All smaller devices will have just 1 column.
- You can pass an array, where the key is the breakpoint and the value is the number of columns. For example, ` blockPickerColumns(['md' => 2, 'xl' => 4]) ` will create a 2 column layout on medium devices, and a 4 column layout on extra large devices. The default breakpoint for smaller devices uses 1 column, unless you use a ` default ` array key.

Breakpoints (` sm `, ` md `, ` lg `, ` xl `, ` 2xl `) are defined by Tailwind, and can be found in the [Tailwind documentation](https://tailwindcss.com/docs/responsive-design#overview).

As well as allowing a static value, the ` blockPickerColumns() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |




### Increasing the width of the block picker

When you [increase the number of columns](https://filamentphp.com/docs/5.x/forms/builder.md#changing-the-number-of-columns-in-the-block-picker), the width of the dropdown should increase incrementally to handle the additional columns. If you'd like more control, you can manually set a maximum width for the dropdown using the ` blockPickerWidth() ` method. Options correspond to [Tailwind's max-width scale](https://tailwindcss.com/docs/max-width). The options are ` xs `, ` sm `, ` md `, ` lg `, ` xl `, ` 2xl `, ` 3xl `, ` 4xl `, ` 5xl `, ` 6xl `, ` 7xl `:

```php
use Filament\Forms\Components\Builder;

Builder::make()
    ->blockPickerColumns(3)
    ->blockPickerWidth('2xl')
    ->blocks([
        // ...
    ])
```

As well as allowing a static value, the ` blockPickerWidth() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Searching blocks

If you have many blocks, you may allow users to search them in the block picker using the ` searchable() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->searchable()
    ->blocks([
        // ...
    ])
```

The search matches block labels in the browser, without making a server request, and is case-insensitive. You may customize the placeholder of the search field using the ` searchPrompt() ` method, and the message displayed when no blocks match the search using the ` noSearchResultsMessage() ` method:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->searchable()
    ->searchPrompt('Search for a block')
    ->noSearchResultsMessage('No blocks found.')
    ->blocks([
        // ...
    ])
```

As well as allowing static values, the ` searchable() `, ` searchPrompt() ` and ` noSearchResultsMessage() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


The search prompt is displayed as plain text. If you pass an ` HtmlString ` to ` searchPrompt() `, its tags are removed and its HTML entities are decoded.

#### Tweaking the search debounce

By default, the block picker filters blocks immediately as the user types. You may debounce the search using the ` searchDebounce() ` method, which accepts the number of milliseconds to wait:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->searchable()
    ->searchDebounce(500)
    ->blocks([
        // ...
    ])
```

As well as allowing a static value, the ` searchDebounce() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Limiting the number of times a block can be used

By default, each block can be used in the builder an unlimited number of times. You may limit this using the ` maxItems() ` method on a block:

```php
use Filament\Forms\Components\Builder\Block;

Block::make('heading')
    ->schema([
        // ...
    ])
    ->maxItems(1)
```

As well as allowing a static value, the ` maxItems() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


## Using ` $get() ` to access parent field values

All form components are able to [use ` $get() ` and ` $set() `](https://filamentphp.com/docs/5.x/forms/overview.md#injecting-the-state-of-another-field) to access another field's value. However, you might experience unexpected behavior when using this inside the builder's schema.

This is because ` $get() ` and ` $set() `, by default, are scoped to the current builder item's ` data ` array. This means that you are able to interact with another field inside that builder item easily without knowing which builder item the current form component belongs to.

The consequence of this is that you may be confused when you are unable to interact with a field outside the builder. We use ` ../ ` syntax to solve this problem - ` $get('../parent_field_name') `.

Consider your form has this data structure:

```php
[
    'client_id' => 1,

    'builder' => [
        'item1' => [
            'type' => 'service',
            'data' => [
                'service_id' => 2,
            ],
        ],
    ],
]
```

You are trying to retrieve the value of ` client_id ` from inside the builder item.

` $get() ` is relative to the current builder item's ` data ` array, so ` $get('client_id') ` looks for ` builder.item1.data.client_id ` in the form data.

You can use ` ../ ` to go up a level in the data structure:

- ` $get('../client_id') ` looks for ` builder.item1.client_id `.
- ` $get('../../client_id') ` looks for ` builder.client_id `.
- ` $get('../../../client_id') ` reaches ` client_id ` at the root of the form data shown above and returns ` 1 `.

If the form has its own state path, these paths remain relative to that form's data, not the entire Livewire component.

The special case of ` $get() ` with no arguments, or ` $get('') ` or ` $get('./') `, returns the current block's ` data ` array, ` ['service_id' => 2] `, not the enclosing item with its ` type ` and ` data ` keys.

## Builder validation

As well as all rules listed on the [validation](https://filamentphp.com/docs/5.x/forms/validation.md) page, there are additional rules that are specific to builders.

### Number of items validation

You can validate the minimum and maximum number of items that you can have in a builder by setting the ` minItems() ` and ` maxItems() ` methods:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->minItems(1)
    ->maxItems(5)
```

As well as allowing static values, the ` minItems() ` and ` maxItems() ` methods also accept a function to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


> [!NOTE]
> ` maxItems() ` is a validation rule. Filament can build and render item schemas before validation rejects excessive item counts. To avoid long processing times if your application accidentally creates too many items, you can [limit item processing](https://filamentphp.com/docs/5.x/forms/builder.md#limiting-item-processing) separately.

## Limiting item processing

If your application's JavaScript accidentally creates a large state array, building and rendering a schema for every block can cause a long wait. You can opt in to a processing limit using ` maxItemsForProcessing() `. If the raw state exceeds this limit, Filament aborts with an HTTP 413 response before building the builder's item schemas, without truncating the data. All raw items count towards the limit, including items with unrecognized block types:

```php
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->maxItems(5)
    ->maxItemsForProcessing(100)
```

The processing limit is independent of ` maxItems() ` validation and is disabled by default. It accepts an integer, or ` null ` to disable it. It limits the number of items in each builder, not the total number of nested items or fields in a request.

> [!CAUTION]
> The processing limit also applies to existing data loaded from your database. A record above the limit cannot be opened through that form until you raise the limit or correct its data elsewhere. Choose a limit that accommodates existing records you need to edit, including records above your validation limit.

This is an opt-in performance safeguard, not a security boundary or a guarantee of request duration. See the shared [guidance on configuring processing limits globally](https://filamentphp.com/docs/5.x/forms/repeater.md#applying-processing-limits-globally) for repeaters, builders, and repeatable entries, including increasing, decreasing, or disabling the limit on individual components and the scope of the processing limit.

## Lazy loading block schemas

If a block's schema is expensive to render, you can pass a ` Schema ` object to ` schema() ` and use ` lazyLoaded() `. This is particularly useful when items are [collapsed](https://filamentphp.com/docs/5.x/forms/builder.md#collapsing-items) by default. Each block item schema will be loaded independently when its item is expanded and enters the viewport:

```php
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Schema;

Builder::make('content')
    ->blocks([
        Block::make('heading')
            ->schema(
                Schema::make()
                    ->components([
                        TextInput::make('content')
                            ->label('Heading')
                            ->required(),
                    ])
                    ->lazyLoaded(),
            ),
        // ...
    ])
    ->collapsed()
```

Builder block item schemas automatically receive unique keys from their item state paths. You can learn more about lazy schemas in the [schema overview](https://filamentphp.com/docs/5.x/schemas/overview.md#lazy-loading-a-child-schema).

## Customizing the builder item actions

This field uses action objects for easy customization of buttons within it. You can customize these buttons by passing a function to an action registration method. The function has access to the ` $action ` object, which you can use to [customize it](https://filamentphp.com/docs/5.x/actions/overview.md). The following methods are available to customize the actions:

- ` addAction() `
- ` addBetweenAction() `
- ` cloneAction() `
- ` collapseAction() `
- ` collapseAllAction() `
- ` deleteAction() `
- ` expandAction() `
- ` expandAllAction() `
- ` moveDownAction() `
- ` moveUpAction() `
- ` reorderAction() `

Here is an example of how you might customize an action:

```php
use Filament\Actions\Action;
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->collapseAllAction(
        fn (Action $action) => $action->label('Collapse all content'),
    )
```

The action registration methods can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/forms/overview.md#field-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The action object to customize. |
| Field | ` Filament\Forms\Components\Field ` | ` $component ` | The current field component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current form data. Validation is not run. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Raw state | ` mixed ` | ` $rawState ` | The current value of the field, before state casts were applied. Validation is not run. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the field. Validation is not run. |


### Confirming builder actions with a modal

You can confirm actions with a modal by using the ` requiresConfirmation() ` method on the action object. You may use any [modal customization method](https://filamentphp.com/docs/5.x/actions/modals.md) to change its content and behavior:

```php
use Filament\Actions\Action;
use Filament\Forms\Components\Builder;

Builder::make('content')
    ->blocks([
        // ...
    ])
    ->deleteAction(
        fn (Action $action) => $action->requiresConfirmation(),
    )
```

> [!NOTE]
> The ` addAction() `, ` addBetweenAction() `, ` collapseAction() `, ` collapseAllAction() `, ` expandAction() ` and ` expandAllAction() ` methods do not support confirmation modals, as clicking their buttons does not make the network request that is required to show the modal.

Completing a drag that changes the block order invokes ` reorderAction() `, which supports ` requiresConfirmation() `. Clicking the drag handle alone does not invoke the action.

### Adding extra item actions to a builder

You may add new [action buttons](https://filamentphp.com/docs/5.x/actions) to the header of each builder item by passing ` Action ` objects into ` extraItemActions() `:

```php
use Filament\Actions\Action;
use Filament\Forms\Components\Builder;
use Filament\Forms\Components\Builder\Block;
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;
use Illuminate\Support\Facades\Mail;

Builder::make('content')
    ->blocks([
        Block::make('contactDetails')
            ->schema([
                TextInput::make('email')
                    ->label('Email address')
                    ->email()
                    ->required(),
                // ...
            ]),
        // ...
    ])
    ->extraItemActions([
        Action::make('sendEmail')
            ->icon(Heroicon::Square2Stack)
            ->action(function (array $arguments, Builder $component): void {
                $itemData = $component->getItemState($arguments['item']);
                
                Mail::to($itemData['email'])
                    ->send(
                        // ...
                    );
            }),
    ])
```

In this example, ` $arguments['item'] ` gives you the ID of the current builder item. You can validate the data in that builder item using the ` getItemState() ` method on the builder component. This method returns the validated data for the item. If the item is not valid, it will cancel the action and show an error message for that item in the form.

If you want to get a snapshot of the current item's state without validating it, you can use ` $component->getItemStateSnapshot($arguments['item']) ` instead. The snapshot still applies state transformations.

If you want to manipulate the raw data for the entire builder, for example, to add, remove or modify items, you can use ` $component->getState() ` to get the data, and ` $component->state($state) ` to set it again:

```php
use Illuminate\Support\Str;

// Get the raw data for the entire builder
$state = $component->getState();

// Add an item, with a random UUID as the key
$state[Str::uuid()] = [
    'type' => 'contactDetails',
    'data' => [
        'email' => auth()->user()->email,
    ],
];

// Set the new data for the builder
$component->state($state);
```
