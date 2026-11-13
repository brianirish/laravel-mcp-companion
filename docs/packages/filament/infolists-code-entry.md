Source: https://filamentphp.com/docs/5.x/infolists/code-entry.md

# Code entry

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/infolists/code-entry.md

## Introduction

The code entry allows you to present a highlighted code snippet in your infolist. It uses [Phiki](https://github.com/phikiphp/phiki) for code highlighting on the server:

```php
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('code')
    ->grammar(Grammar::Php)
```



To use the code entry, you need to first install the [` phiki/phiki `](https://github.com/phikiphp/phiki) Composer package. Filament does not include it by default to allow you to choose which major version of Phiki to use explicitly, since major versions can have different grammars and themes available. You can install the latest version of Phiki using the following command:

```bash
composer require phiki/phiki
```

## Changing the code's grammar (language)

You may change the grammar (language) of the code using the ` grammar() ` method. Over 200 grammars are available, and you can open the ` Phiki\Grammar\Grammar ` enum class to see the full list. To switch to use JavaScript as the grammar, you can use the ` Grammar::Javascript ` enum value:

```php
use Filament\Infolists\Components\CodeEntry;
use Phiki\Grammar\Grammar;

CodeEntry::make('code')
    ->grammar(Grammar::Javascript)
```

As well as allowing a static value, the ` grammar() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/infolists/overview.md#entry-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Entry | ` Filament\Infolists\Components\Entry ` | ` $component ` | The current entry component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |




> [!TIP]
> If your code entry's content is a PHP array, it will automatically be converted to a JSON string, and the grammar will be set to ` Grammar::Json `. You can customize the ` JSON_ ` flags used during conversion with the ` jsonFlags() ` method.

## Changing the code's theme (highlighting)

You may change the theme of the code using the ` lightTheme() ` and ` darkTheme() ` methods. Over 50 themes are available, and you can open the ` Phiki\Theme\Theme ` enum class to see the full list. To use the popular ` Dracula ` theme, you can use the ` Theme::Dracula ` enum value:

```php
use Filament\Infolists\Components\CodeEntry;
use Phiki\Theme\Theme;

CodeEntry::make('code')
    ->lightTheme(Theme::Dracula)
    ->darkTheme(Theme::Dracula)
```

As well as allowing static values, the ` lightTheme() ` and ` darkTheme() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the functions as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/infolists/overview.md#entry-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Entry | ` Filament\Infolists\Components\Entry ` | ` $component ` | The current entry component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |




## Allowing the code to be copied to the clipboard

You may make the code copyable, such that clicking on it copies the code to the clipboard, and optionally specify a custom confirmation message and duration in milliseconds. This feature only works when SSL is enabled for the app.

```php
use Filament\Infolists\Components\CodeEntry;

CodeEntry::make('code')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500)
```

Optionally, you may pass a boolean value to control if the code should be copyable or not:

```php
use Filament\Infolists\Components\CodeEntry;

CodeEntry::make('code')
    ->copyable(FeatureFlag::active())
```

As well as allowing static values, the ` copyable() `, ` copyMessage() `, and ` copyMessageDuration() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/infolists/overview.md#entry-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Entry | ` Filament\Infolists\Components\Entry ` | ` $component ` | The current entry component instance. |
| Get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $get ` | A function for retrieving values from the current schema data. Validation is not run on form fields. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current schema. |
| Operation | ` string ` | ` $operation ` | The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Parent repeater item index | ` int ` | ` $parentRepeaterItemIndex ` | The zero-based index of the nearest containing repeater item or builder block, or ` 0 ` when neither exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current schema. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |
