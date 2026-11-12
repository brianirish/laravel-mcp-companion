Source: https://filamentphp.com/docs/5.x/schemas/empty-states.md

# Empty states

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/schemas/empty-states.md

## Introduction

You can display an empty state in your schema to communicate that there is no content to show yet, and to guide the user towards the next action. An empty state requires a heading, but can also have a ` description() `, [` icon() `](https://filamentphp.com/docs/5.x/schemas/empty-states.md#adding-an-icon-to-the-empty-state) and [` footer() `](https://filamentphp.com/docs/5.x/schemas/empty-states.md#inserting-actions-and-other-components-in-the-footer-of-an-empty-state):

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->icon(Heroicon::OutlinedUser)
    ->footer([
        Action::make('createUser')
            ->icon(Heroicon::Plus),
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




## Adding an icon to the empty state

You may add an [icon](https://filamentphp.com/docs/5.x/styling/icons.md) to the empty state using the ` icon() ` method:

```php
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->icon(Heroicon::OutlinedUser)
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


## Inserting actions and other components in the footer of an empty state

You may insert [actions](https://filamentphp.com/docs/5.x/actions) and any other schema component (usually [prime components](https://filamentphp.com/docs/5.x/schemas/primes.md)) into the footer of an empty state by passing an array of components to the ` footer() ` method:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\EmptyState;
use Filament\Support\Icons\Heroicon;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->footer([
        Action::make('createUser')
            ->icon(Heroicon::Plus),
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


## Removing the empty state container

By default, empty states have a background color, shadow and border. You may remove these styles and just render the content of the empty state without the container using ` contained(false) `:

```php
use Filament\Schemas\Components\EmptyState;

EmptyState::make('No users yet')
    ->description('Get started by creating a new user.')
    ->contained(false)
```

As well as allowing a static value, the ` contained() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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
