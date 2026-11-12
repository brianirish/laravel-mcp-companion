Source: https://filamentphp.com/docs/5.x/components/notifications.md

# Rendering notifications outside of a panel

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/components/notifications.md

> **Warning**
>
> Before proceeding, make sure ` filament/notifications ` is installed in your project. You can check by running:
> 
> ```bash
> composer show filament/notifications
> ```
> 
> If it's not installed, consult the [installation guide](https://filamentphp.com/docs/5.x/introduction/installation.md#installing-the-individual-components) and configure the **individual components** according to the instructions.


## Introduction

To render notifications in your app, make sure the ` notifications ` Livewire component is rendered in your layout:

```blade
<div>
    @livewire('notifications')
</div>
```

Now, when [sending a notification](https://filamentphp.com/docs/5.x/notifications) from a Livewire request, it will appear for the user.
