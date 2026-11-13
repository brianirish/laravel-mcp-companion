Source: https://filamentphp.com/docs/5.x/components/link.md

# Link Blade component

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/components/link.md

## Introduction

The link component is used to render a clickable link that can perform an action:

```blade
<x-filament::link :href="route('users.create')">
    New user
</x-filament::link>
```



> [!CAUTION]
> If you are passing user-controlled data to the ` href ` attribute, validate its scheme using [` Str::sanitizeUrl() `](https://filamentphp.com/docs/5.x/advanced/security.md#validating-user-input) before rendering it. HTML escaping alone does not prevent a ` javascript: ` URL from executing code when clicked.

## Using a link as a button

By default, a link's underlying HTML tag is ` <a> `. You can change it to be a ` <button> ` tag by using the ` tag ` attribute:

```blade
<x-filament::link
    wire:click="openNewUserModal"
    tag="button"
>
    New user
</x-filament::link>
```

## Setting the size of a link

By default, the size of a link is ` md ` (medium). The built-in sizes are ` xs `, ` sm `, ` md `, ` lg `, and ` xl `, which you can select using the ` size ` attribute. In the default theme, ` md `, ` lg `, and ` xl ` use the same text size:

```blade
<x-filament::link size="xs">
    New user
</x-filament::link>

<x-filament::link size="sm">
    New user
</x-filament::link>

<x-filament::link size="lg">
    New user
</x-filament::link>

<x-filament::link size="xl">
    New user
</x-filament::link>
```



## Setting the font weight of a link

By default, the font weight of links is ` medium `. You can make it ` thin `, ` extralight `, ` light `, ` normal `, ` semibold `, ` bold `, ` extrabold ` or ` black ` by using the ` weight ` attribute:

```blade
<x-filament::link weight="thin">
    New user
</x-filament::link>

<x-filament::link weight="extralight">
    New user
</x-filament::link>

<x-filament::link weight="light">
    New user
</x-filament::link>

<x-filament::link weight="normal">
    New user
</x-filament::link>

<x-filament::link weight="medium">
    New user
</x-filament::link>

<x-filament::link weight="semibold">
    New user
</x-filament::link>
   
<x-filament::link weight="bold">
    New user
</x-filament::link>

<x-filament::link weight="black">
    New user
</x-filament::link> 
```

Alternatively, you can pass in a custom CSS class to define the weight:

```blade
<x-filament::link weight="md:font-[650]">
    New user
</x-filament::link>
```



## Changing the color of a link

By default, the color of a link is "primary". You can change it to be ` danger `, ` gray `, ` info `, ` success ` or ` warning ` by using the ` color ` attribute:

```blade
<x-filament::link color="danger">
    New user
</x-filament::link>

<x-filament::link color="gray">
    New user
</x-filament::link>

<x-filament::link color="info">
    New user
</x-filament::link>

<x-filament::link color="success">
    New user
</x-filament::link>

<x-filament::link color="warning">
    New user
</x-filament::link>
```



## Adding an icon to a link

You can add an [icon](https://filamentphp.com/docs/5.x/styling/icons.md) to a link by using the ` icon ` attribute:

```blade
<x-filament::link icon="heroicon-m-sparkles">
    New user
</x-filament::link>
```

You can also change the icon's position to be after the text instead of before it, using the ` icon-position ` attribute:

```blade
<x-filament::link
    icon="heroicon-m-sparkles"
    icon-position="after"
>
    New user
</x-filament::link>
```



## Adding a tooltip to a link

You can add a tooltip to a link by using the ` tooltip ` attribute:

```blade
<x-filament::link tooltip="Register a user">
    New user
</x-filament::link>
```

## Adding a badge to a link

You can render a [badge](https://filamentphp.com/docs/5.x/components/badge.md) on top of a link by using the ` badge ` slot:

```blade
<x-filament::link>
    Mark notifications as read

    <x-slot name="badge">
        3
    </x-slot>
</x-filament::link>
```

You can [change the color](https://filamentphp.com/docs/5.x/components/badge.md#changing-the-color-of-the-badge) of the badge using the ` badge-color ` attribute:

```blade
<x-filament::link badge-color="danger">
    Mark notifications as read

    <x-slot name="badge">
        3
    </x-slot>
</x-filament::link>
```
