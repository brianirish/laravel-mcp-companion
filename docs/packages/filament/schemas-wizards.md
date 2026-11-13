Source: https://filamentphp.com/docs/5.x/schemas/wizards.md

# Wizards

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/schemas/wizards.md

## Introduction

Similar to [tabs](https://filamentphp.com/docs/5.x/schemas/tabs.md), you may want to use a multistep wizard to reduce the number of components that are visible at once. These are especially useful if your form has a definite chronological order, in which you want each step to be validated as the user progresses.

```php
use Filament\Schemas\Components\Wizard;
use Filament\Schemas\Components\Wizard\Step;

Wizard::make([
    Step::make('Order')
        ->schema([
            // ...
        ]),
    Step::make('Delivery')
        ->schema([
            // ...
        ]),
    Step::make('Billing')
        ->schema([
            // ...
        ]),
])
```



> [!TIP]
> We have different setup instructions if you're looking to add a wizard to the creation process inside a [panel resource](https://filamentphp.com/docs/5.x/resources/creating-records.md#using-a-wizard) or an [action modal](https://filamentphp.com/docs/5.x/actions/modals.md#rendering-a-wizard-in-a-modal). Following that documentation will ensure that the ability to submit the form is only available on the last step of the wizard.

## Rendering a submit button on the last step

You may use the ` submitAction() ` method to render submit button HTML or a view at the end of the wizard, on the last step. This provides a clearer UX than displaying a submit button below the wizard at all times:

```php
use Filament\Schemas\Components\Wizard;
use Illuminate\Support\HtmlString;

Wizard::make([
    // ...
])->submitAction(view('order-form.submit-button'))

Wizard::make([
    // ...
])->submitAction(new HtmlString('<button type="submit">Submit</button>'))
```

Alternatively, you can use the built-in Filament button Blade component:

```php
use Filament\Schemas\Components\Wizard;
use Illuminate\Support\Facades\Blade;
use Illuminate\Support\HtmlString;

Wizard::make([
    // ...
])->submitAction(new HtmlString(Blade::render(<<<BLADE
    <x-filament::button
        type="submit"
        size="sm"
    >
        Submit
    </x-filament::button>
BLADE)))
```

You could extract this component to a separate Blade view if you prefer.



## Setting a step icon

Steps may have an [icon](https://filamentphp.com/docs/5.x/styling/icons.md), which you can set using the ` icon() ` method:

```php
use Filament\Schemas\Components\Wizard\Step;
use Filament\Support\Icons\Heroicon;

Step::make('Order')
    ->icon(Heroicon::ShoppingBag)
    ->schema([
        // ...
    ]),
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




## Customizing the icon for completed steps

You may customize the [icon](https://filamentphp.com/docs/5.x/schemas/wizards.md#setting-a-step-icon) of a completed step using the ` completedIcon() ` method:

```php
use Filament\Schemas\Components\Wizard\Step;
use Filament\Support\Icons\Heroicon;

Step::make('Order')
    ->completedIcon(Heroicon::HandThumbUp)
    ->schema([
        // ...
    ]),
```

As well as allowing a static value, the ` completedIcon() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Adding descriptions to steps

You may add a short description after the title of each step using the ` description() ` method:

```php
use Filament\Schemas\Components\Wizard\Step;

Step::make('Order')
    ->description('Review your basket')
    ->schema([
        // ...
    ]),
```

As well as allowing a static value, the ` description() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Setting the default active step

You may use the ` startOnStep() ` method to load a specific step in the wizard:

```php
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])->startOnStep(2)
```

As well as allowing a static value, the ` startOnStep() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Allowing steps to be skipped

If you'd like to allow free navigation, so all steps are skippable, use the ` skippable() ` method:

```php
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])->skippable()
```

Optionally, the ` skippable() ` method accepts a boolean value to control if the steps are skippable or not:

```php
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])->skippable(FeatureFlag::active())
```

As well as allowing a static value, the ` skippable() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Persisting the current step in the URL's query string

By default, the current step is not persisted in the URL's query string. You can change this behavior using the ` persistStepInQueryString() ` method:

```php
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])->persistStepInQueryString()
```

When enabled, the current step is persisted in the URL's query string using the ` step ` key. You can change this key by passing it to the ` persistStepInQueryString() ` method:

```php
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])->persistStepInQueryString('wizard-step')
```

As well as allowing a static value, the ` persistStepInQueryString() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Step lifecycle hooks

You may use the ` afterValidation() ` and ` beforeValidation() ` methods to run code before and after validation occurs on the step:

```php
use Filament\Schemas\Components\Wizard\Step;

Step::make('Order')
    ->afterValidation(function () {
        // ...
    })
    ->beforeValidation(function () {
        // ...
    })
    ->schema([
        // ...
    ]),
```

You can inject various utilities into the ` afterValidation() ` and ` beforeValidation() ` functions as parameters.

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


### Preventing the next step from being loaded

Inside ` afterValidation() ` or ` beforeValidation() `, you may throw ` Filament\Support\Exceptions\Halt `, which will prevent the wizard from loading the next step:

```php
use Filament\Schemas\Components\Wizard\Step;
use Filament\Support\Exceptions\Halt;

Step::make('Order')
    ->afterValidation(function () {
        // ...

        if (true) {
            throw new Halt();
        }
    })
    ->schema([
        // ...
    ]),
```

## Using grid columns within a step

You may use the ` columns() ` method to customize the [grid](https://filamentphp.com/docs/5.x/schemas/layouts.md#grid-system) within the step:

```php
use Filament\Schemas\Components\Wizard;
use Filament\Schemas\Components\Wizard\Step;

Wizard::make([
    Step::make('Order')
        ->columns(2)
        ->schema([
            // ...
        ]),
    // ...
])
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


## Customizing the wizard action objects

This component uses action objects for easy customization of buttons within it. You can customize these buttons by passing a function to an action registration method. The function has access to the ` $action ` object, which you can use to [customize it](https://filamentphp.com/docs/5.x/actions/overview.md). The following methods are available to customize the actions:

- ` nextAction() `
- ` previousAction() `

Here is an example of how you might customize an action:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Wizard;

Wizard::make([
    // ...
])
    ->nextAction(
        fn (Action $action) => $action->label('Next step'),
    )
```

The action registration methods can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/schemas/overview.md#component-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The action object to customize. |
| Component | ` Filament\Schemas\Components\Component ` | ` $component ` | The current component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |


## Lazy loading step content

If the content of a wizard step is expensive to render, you can pass a ` Schema ` object to its ` schema() ` method and use ` lazyLoaded() `. The content of the active step will be loaded when it enters the viewport. The content of a later step will not be loaded until the user reaches it:

```php
use Filament\Forms\Components\TextInput;
use Filament\Schemas\Components\Wizard;
use Filament\Schemas\Components\Wizard\Step;
use Filament\Schemas\Schema;

Wizard::make([
    Step::make('Account')
        ->key('accountStep')
        ->schema(
            Schema::make()
                ->components([
                    TextInput::make('name'),
                ])
                ->lazyLoaded(),
        ),
    Step::make('Confirmation')
        ->key('confirmationStep')
        ->schema(
            Schema::make()
                ->components([
                    // ...
                ])
                ->lazyLoaded(),
        ),
])
    ->key('accountWizard')
```

Every lazy schema must have a unique key. In this example, the keys on the steps are inherited by their child schemas, while the key on the ` Wizard ` component namespaces them from other steps in the same schema. You can learn more in the [schema overview](https://filamentphp.com/docs/5.x/schemas/overview.md#lazy-loading-a-child-schema).
