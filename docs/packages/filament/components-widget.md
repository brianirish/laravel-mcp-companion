Source: https://filamentphp.com/docs/5.x/components/widget.md

# Rendering a widget in a Blade view

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/components/widget.md

> [!WARNING]
> Before proceeding, make sure ` filament/widgets ` is installed in your project. You can check by running:
> 
> ```bash
> composer show filament/widgets
> ```
> 
> If it's not installed, consult the [installation guide](https://filamentphp.com/docs/5.x/introduction/installation.md#installing-the-individual-components) and configure the **individual components** according to the instructions.

## Creating a widget

Use the ` make:filament-widget ` command to generate a new widget. For details on customization and usage, see the [widgets section](https://filamentphp.com/docs/5.x/widgets).

## Adding the widget

Since widgets are Livewire components, you can easily render a widget in any Blade view using the ` @livewire ` directive:

```blade
<div>
    @livewire(\App\Livewire\Dashboard\PostsChart::class)
</div>
```

> [!NOTE]
> If you're using a [table widget](https://filamentphp.com/docs/5.x/widgets/overview.md#table-widgets), make sure to install ` filament/tables ` as well.  
> Refer to the [installation guide](https://filamentphp.com/docs/5.x/introduction/installation.md#installing-the-individual-components) and follow the steps to configure the **individual components** properly.
