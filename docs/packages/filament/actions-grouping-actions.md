Source: https://filamentphp.com/docs/5.x/actions/grouping-actions.md

# Grouping actions

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/actions/grouping-actions.md

## Introduction

You may group actions together into a dropdown menu by using an ` ActionGroup ` object. Groups may contain many actions, or other groups:

```php
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;

ActionGroup::make([
    Action::make('view'),
    Action::make('edit'),
    Action::make('delete'),
])
```



This page is about customizing the look of the group's trigger button and dropdown.

## Customizing the group trigger style

The button which opens the dropdown may be customized in the same way as a normal action. [All the methods available for trigger buttons](https://filamentphp.com/docs/5.x/actions/overview.md) may be used to customize the group trigger button:

```php
use Filament\Actions\ActionGroup;
use Filament\Support\Enums\Size;

ActionGroup::make([
    // Array of actions
])
    ->label('More actions')
    ->icon('heroicon-m-ellipsis-vertical')
    ->size(Size::Small)
    ->color('primary')
    ->button()
```





When you render multiple groups together, use distinct ` label() ` values so users can distinguish their triggers, including when only icons are visible.

### Adding a tooltip to the group trigger button

You may add a tooltip to the group trigger button using the ` tooltip() ` method:

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->tooltip('Actions')
```



### Using a grouped button design

Instead of a dropdown, an action group can render itself as a group of buttons. This design works with and without button labels. To use this feature, use the ` buttonGroup() ` method:

```php
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;
use Filament\Support\Icons\Heroicon;

ActionGroup::make([
    Action::make('edit')
        ->color('gray')
        ->icon(Heroicon::PencilSquare)
        ->hiddenLabel(),
    Action::make('delete')
        ->color('gray')
        ->icon(Heroicon::Trash)
        ->hiddenLabel(),
])
    ->buttonGroup()
```



## Setting the placement of the dropdown

The dropdown may be positioned relative to the trigger button by using the ` dropdownPlacement() ` method:

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownPlacement('top-start')
```

The ` dropdownPlacement() ` method also accepts a function to dynamically calculate the value. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action group | ` Filament\Actions\ActionGroup ` | ` $group ` | The current action group instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action group, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action group, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Action groups in schemas only\] The schema object that this action group belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Action groups in schemas only\] The schema component that this action group belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Action groups in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Action groups in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Action groups in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Action groups in schemas only\] The current value of the schema that this action group belongs to, like the current repeater item. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Action groups in tables only\] The table object that this action group belongs to. |




Alternatively, you may let the dropdown position be automatically determined based on the available space using the ` dropdownAutoPlacement() ` method:

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownAutoPlacement()
```

## Adding dividers between actions

You may add dividers between groups of actions by using nested ` ActionGroup ` objects:

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    ActionGroup::make([
        // Array of actions
    ])->dropdown(false),
    // Array of actions
])
```

The ` dropdown(false) ` method puts the actions inside the parent dropdown, instead of a new nested dropdown.

The ` dropdown() ` method also accepts a function to dynamically calculate the value. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action group | ` Filament\Actions\ActionGroup ` | ` $group ` | The current action group instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action group, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action group, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Action groups in schemas only\] The schema object that this action group belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Action groups in schemas only\] The schema component that this action group belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Action groups in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Action groups in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Action groups in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Action groups in schemas only\] The current value of the schema that this action group belongs to, like the current repeater item. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Action groups in tables only\] The table object that this action group belongs to. |




## Setting the width of the dropdown

The dropdown may be set to a width by using the ` dropdownWidth() ` method. Options correspond to [Tailwind's max-width scale](https://tailwindcss.com/docs/max-width). The options are ` ExtraSmall `, ` Small `, ` Medium `, ` Large `, ` ExtraLarge `, ` TwoExtraLarge `, ` ThreeExtraLarge `, ` FourExtraLarge `, ` FiveExtraLarge `, ` SixExtraLarge ` and ` SevenExtraLarge `:

```php
use Filament\Actions\ActionGroup;
use Filament\Support\Enums\Width;

ActionGroup::make([
    // Array of actions
])
    ->dropdownWidth(Width::ExtraSmall)
```



The ` dropdownWidth() ` method also accepts a function to dynamically calculate the value. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action group | ` Filament\Actions\ActionGroup ` | ` $group ` | The current action group instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action group, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action group, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Action groups in schemas only\] The schema object that this action group belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Action groups in schemas only\] The schema component that this action group belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Action groups in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Action groups in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Action groups in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Action groups in schemas only\] The current value of the schema that this action group belongs to, like the current repeater item. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Action groups in tables only\] The table object that this action group belongs to. |


## Controlling the dropdown offset

You may control the offset of the dropdown using the ` dropdownOffset() ` method, by default the offset is set to ` 8 `.

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownOffset(16)
```

The ` dropdownOffset() ` method also accepts a function to dynamically calculate the value. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action group | ` Filament\Actions\ActionGroup ` | ` $group ` | The current action group instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action group, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action group, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Action groups in schemas only\] The schema object that this action group belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Action groups in schemas only\] The schema component that this action group belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Action groups in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Action groups in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Action groups in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Action groups in schemas only\] The current value of the schema that this action group belongs to, like the current repeater item. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Action groups in tables only\] The table object that this action group belongs to. |


## Controlling the maximum height of the dropdown

The dropdown content can have a maximum height using the ` dropdownMaxHeight() ` method, so that it scrolls. You can pass a [CSS length](https://developer.mozilla.org/en-US/docs/Web/CSS/length):

```php
use Filament\Actions\ActionGroup;

ActionGroup::make([
    // Array of actions
])
    ->dropdownMaxHeight('400px')
```

The ` dropdownMaxHeight() ` method also accepts a function to dynamically calculate the value. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action group | ` Filament\Actions\ActionGroup ` | ` $group ` | The current action group instance. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action group, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action group, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Action groups in schemas only\] The schema object that this action group belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Action groups in schemas only\] The schema component that this action group belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Action groups in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Action groups in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Action groups in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Action groups in schemas only\] The current value of the schema that this action group belongs to, like the current repeater item. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Action groups in tables only\] The table object that this action group belongs to. |
