Source: https://filamentphp.com/docs/5.x/schemas/callouts.md

# Callouts

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/schemas/callouts.md

## Introduction

Callouts are used to draw attention to important information or messages. They are often used for alerts, notices, or tips. You can create a callout using the ` Callout ` component:

```php
use Filament\Schemas\Components\Callout;

Callout::make('New version available')
    ->description('Filament v4 has been released with exciting new features and improvements.')
    ->info()
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




## Using status variants

Callouts have built-in status variants that automatically set the appropriate icon, icon color, and background color. You can use the ` danger() `, ` info() `, ` success() `, or ` warning() ` methods:

```php
use Filament\Schemas\Components\Callout;

Callout::make('Payment successful')
    ->description('Your order has been confirmed and is being processed.')
    ->success()

Callout::make('Session expiring soon')
    ->description('Your session will expire in 5 minutes. Save your work to avoid losing changes.')
    ->warning()

Callout::make('Connection failed')
    ->description('Unable to connect to the server. Please check your internet connection.')
    ->danger()
```



## Removing the background color

By default, status callouts have a colored background. You can remove the background color while keeping the status icon and icon color by using ` color(null) `:

```php
use Filament\Schemas\Components\Callout;

Callout::make('Scheduled maintenance')
    ->description('The system will be unavailable on Sunday from 2:00 AM to 4:00 AM.')
    ->warning()
    ->color(null)
```

As well as allowing a static value, the ` color() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Adding a custom icon

You can add a custom [icon](https://filamentphp.com/docs/5.x/styling/icons.md) to the callout using the ` icon() ` method:

```php
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->icon(Heroicon::OutlinedLightBulb)
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


### Changing the icon color

You can change the icon color using the ` iconColor() ` method:

```php
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->icon(Heroicon::OutlinedLightBulb)
    ->iconColor('primary')
```

As well as allowing a static value, the ` iconColor() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




### Changing the icon size

By default, the icon size is "large". You can change it to "small" or "medium" using the ` iconSize() ` method:

```php
use Filament\Schemas\Components\Callout;
use Filament\Support\Enums\IconSize;

Callout::make('Quick note')
    ->description('This callout has a smaller icon.')
    ->info()
    ->iconSize(IconSize::Small)
```

As well as allowing a static value, the ` iconSize() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Using a custom background color

You can set a custom background color using the ` color() ` method:

```php
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('Pro tip')
    ->description('You can use keyboard shortcuts to navigate faster. Press ? to see all available shortcuts.')
    ->color('primary')
    ->icon(Heroicon::OutlinedLightBulb)
    ->iconColor('primary')
```



## Adding actions to the callout footer

You can add [actions](https://filamentphp.com/docs/5.x/actions) to the callout footer using the ` actions() ` method:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;

Callout::make('Your trial ends in 3 days')
    ->description('Upgrade now to keep access to all premium features.')
    ->warning()
    ->actions([
        Action::make('upgrade')
            ->label('Upgrade to Pro')
            ->button(),
        Action::make('compare')
            ->label('Compare plans'),
    ])
```

You can pass functions inside the ` actions() ` array to dynamically calculate actions. You can inject various utilities into these functions as parameters.

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




### Changing the footer actions alignment

By default, actions are aligned to the start. You can change the alignment using the ` footerActionsAlignment() ` method:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Support\Enums\Alignment;

Callout::make('Updates available')
    ->description('New features and improvements are ready to install.')
    ->info()
    ->actions([
        Action::make('install')->label('Install Now'),
        Action::make('later')->label('Remind Me Later'),
    ])
    ->footerActionsAlignment(Alignment::End)
```

The available alignment options are ` Alignment::Start `, ` Alignment::Center `, ` Alignment::End `, and ` Alignment::Between `.

As well as allowing a static value, the ` footerActionsAlignment() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Adding custom footer content

You can add custom content to the footer using the ` footer() ` method. This accepts an array of schema components:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Schemas\Components\Text;

Callout::make('Backup complete')
    ->description('Your data has been successfully backed up to the cloud.')
    ->success()
    ->footer([
        Text::make('Last backup: 5 minutes ago')
            ->color('gray'),
        Action::make('viewBackups')
            ->label('View All Backups')
            ->button(),
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




## Adding custom control content

You can add custom content to the controls (top-right corner) using the ` controls() ` method. This accepts an array of schema components:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;

Callout::make('Backup complete')
    ->description('Your data has been successfully backed up to the cloud.')
    ->success()
    ->controls([
        Action::make('dismiss')
            ->icon('heroicon-m-x-mark')
            ->iconButton()
            ->color('gray'),
    ])
```

As well as allowing a static value, the ` controls() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Adding control actions to the callout

You can add control [actions](https://filamentphp.com/docs/5.x/actions) to the top-right corner of the callout using the ` controlActions() ` method. For example, you could add a dismiss button that hides the callout for the duration of the user's session:

```php
use Filament\Actions\Action;
use Filament\Schemas\Components\Callout;
use Filament\Support\Icons\Heroicon;

Callout::make('New version available')
    ->description('Filament v4 has been released with exciting new features and improvements.')
    ->info()
    ->controlActions([
        Action::make('dismiss')
            ->icon(Heroicon::XMark)
            ->iconButton()
            ->color('gray')
            ->action(fn () => session()->put('new-version-callout-dismissed', true)),
    ])
    ->visible(fn (): bool => ! session()->get('new-version-callout-dismissed'))
```



## Announcing dynamically revealed callouts

If you reveal a callout dynamically, for example after an action completes, use ` extraAttributes() ` to make it a live region for assistive technology. Status variants alone do not make a callout a live region:

```php
use Filament\Schemas\Components\Callout;

Callout::make('Changes saved')
    ->success()
    ->extraAttributes(['role' => 'status']) // Use `alert` instead of `status` for urgent messages
```
