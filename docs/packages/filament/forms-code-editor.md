Source: https://filamentphp.com/docs/5.x/forms/code-editor.md

# Code editor

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/forms/code-editor.md

## Introduction

The code editor component allows you to write code in a textarea with line numbers. By default, no syntax highlighting is applied.

```php
use Filament\Forms\Components\CodeEditor;

CodeEditor::make('code')
```



## Using language syntax highlighting

You may change the language syntax highlighting of the code editor using the ` language() ` method. The editor supports the following languages:

- C++
- CSS
- Go
- HTML
- Java
- JavaScript
- JSON
- Markdown
- PHP
- Python
- SQL
- XML
- YAML

You can open the ` Filament\Forms\Components\CodeEditor\Enums\Language ` enum class to see this list. To switch to using JavaScript syntax highlighting, you can use the ` Language::JavaScript ` enum value:

```php
use Filament\Forms\Components\CodeEditor;
use Filament\Forms\Components\CodeEditor\Enums\Language;

CodeEditor::make('code')
    ->language(Language::JavaScript)
```

As well as allowing a static value, the ` language() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




## Allowing lines to wrap

By default, long lines in the code editor will create a horizontal scrollbar. If you would like to allow long lines to wrap instead, you may use the ` wrap() ` method:

```php
use Filament\Forms\Components\CodeEditor;

CodeEditor::make('code')
    ->wrap()
```
