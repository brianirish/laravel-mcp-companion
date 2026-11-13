Source: https://filamentphp.com/docs/5.x/components/icon-button.md

# Icon button Blade component

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/components/icon-button.md

## Introduction

The button component is used to render a clickable button that can perform an action:

```blade
<x-filament::icon-button
    icon="heroicon-m-plus"
    wire:click="openNewUserModal"
    label="New label"
/>
```



## Using an icon button as an anchor link

By default, an icon button's underlying HTML tag is ` <button> `. You can change it to be an ` <a> ` tag by using the ` tag ` attribute:

```blade
<x-filament::icon-button
    icon="heroicon-m-arrow-top-right-on-square"
    href="https://filamentphp.com"
    tag="a"
    label="Filament"
/>
```

> [!CAUTION]
> If you are passing user-controlled data to the ` href ` attribute, validate its scheme using [` Str::sanitizeUrl() `](https://filamentphp.com/docs/5.x/advanced/security.md#validating-user-input) before rendering it. HTML escaping alone does not prevent a ` javascript: ` URL from executing code when clicked.

## Setting the size of an icon button

By default, the size of an icon button is "medium". You can make it "extra small", "small", "large" or "extra large" by using the ` size ` attribute:

```blade
<x-filament::icon-button
    icon="heroicon-m-plus"
    size="xs"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-m-plus"
    size="sm"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-s-plus"
    size="lg"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-s-plus"
    size="xl"
    label="New label"
/>
```



## Changing the color of an icon button

By default, the color of an icon button is "primary". You can change it to be ` danger `, ` gray `, ` info `, ` success ` or ` warning ` by using the ` color ` attribute:

```blade
<x-filament::icon-button
    icon="heroicon-m-plus"
    color="danger"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-m-plus"
    color="gray"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-m-plus"
    color="info"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-m-plus"
    color="success"
    label="New label"
/>

<x-filament::icon-button
    icon="heroicon-m-plus"
    color="warning"
    label="New label"
/>
```



## Adding a tooltip to an icon button

You can add a tooltip to an icon button by using the ` tooltip ` attribute:

```blade
<x-filament::icon-button
    icon="heroicon-m-plus"
    tooltip="Register a user"
    label="New label"
/>
```

## Adding a badge to an icon button

You can render a [badge](https://filamentphp.com/docs/5.x/components/badge.md) on top of an icon button by using the ` badge ` slot:

```blade
<x-filament::icon-button
    icon="heroicon-m-x-mark"
    label="Mark notifications as read"
>
    <x-slot name="badge">
        3
    </x-slot>
</x-filament::icon-button>
```

You can [change the color](https://filamentphp.com/docs/5.x/components/badge.md#changing-the-color-of-the-badge) of the badge using the ` badge-color ` attribute:

```blade
<x-filament::icon-button
    icon="heroicon-m-x-mark"
    label="Mark notifications as read"
    badge-color="danger"
>
    <x-slot name="badge">
        3
    </x-slot>
</x-filament::icon-button>
```
