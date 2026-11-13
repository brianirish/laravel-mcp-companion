Source: https://filamentphp.com/docs/5.x/infolists/image-entry.md

# Image entry

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/infolists/image-entry.md

## Introduction

Infolists can render images, based on the path in the state of the entry:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
```

In this case, the ` header_image ` state could contain ` posts/header-images/4281246003439.jpg `, which is relative to the root directory of the storage disk. The storage disk is defined in the [configuration file](https://filamentphp.com/docs/5.x/introduction/installation.md#publishing-configuration), ` local ` by default. You can also set the ` FILESYSTEM_DISK ` environment variable to change this.

Alternatively, the state could contain an absolute URL to an image, such as ` https://example.com/images/header.jpg `.



## Setting the alt text

You should set descriptive alt text on your images so that screen reader users understand what each image shows. Use the ` alt() ` method:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->alt('Article header image')
```

As well as allowing a static value, the ` alt() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters, including the ` $state ` of the current image, which is useful when the entry renders multiple images.

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
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |


If you do not set any alt text, the image is rendered with an empty ` alt ` attribute, which marks it as decorative for assistive technology.

> [!WARNING]
> When an image [links to a URL](https://filamentphp.com/docs/5.x/infolists/overview.md#opening-a-url-when-an-entry-is-clicked), its alt text becomes the accessible name of the link. Always set meaningful ` alt() ` text on linked images, otherwise screen reader users will encounter a link with no name.

## Managing the image disk

The default storage disk is defined in the [configuration file](https://filamentphp.com/docs/5.x/introduction/installation.md#publishing-configuration), ` local ` by default. You can also set the ` FILESYSTEM_DISK ` environment variable to change this. If you want to deviate from the default disk, you may pass a custom disk name to the ` disk() ` method:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->disk('s3')
```

As well as allowing a static value, the ` disk() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |


## Public images

By default, images use ` private ` visibility unless the [disk](https://filamentphp.com/docs/5.x/infolists/image-entry.md#managing-the-image-disk) is named ` public `. Filament attempts to generate temporary URLs for private images if the disk supports them, falling back to permanent URLs if it cannot. The default visibility depends on the disk's name, not its filesystem configuration.

> [!NOTE]
> If your application uses the ` local ` disk, you may need to [enable local temporary URLs](https://laravel.com/docs/filesystem#enabling-local-temporary-urls) by adding ` 'serve' => true ` to the disk's configuration in ` config/filesystems.php `.

If your images are already publicly accessible, you can set ` visibility('public') ` to use permanent URLs. This does not change the disk or make private files publicly accessible:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->visibility('public')
```

As well as allowing a static value, the ` visibility() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |


## Customizing the size

You may customize the image size by passing a ` imageWidth() ` and ` imageHeight() `, or both with ` imageSize() `:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->imageWidth(200)

ImageEntry::make('header_image')
    ->imageHeight(50)

ImageEntry::make('author.avatar')
    ->imageSize(40)
```

As well as allowing a static values, the ` imageWidth() `, ` imageHeight() ` and ` imageSize() ` methods also accept functions to dynamically calculate them. You can inject various utilities into the function as parameters.

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




### Square images

You may display the image using a 1:1 aspect ratio:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->square()
```



Optionally, you may pass a boolean value to control if the image should be square or not:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->square(FeatureFlag::active())
```

As well as allowing a static value, the ` square() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Circular images

You may make the image fully rounded, which is useful for rendering avatars:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->circular()
```



Optionally, you may pass a boolean value to control if the image should be circular or not:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('author.avatar')
    ->imageHeight(40)
    ->circular(FeatureFlag::active())
```

As well as allowing a static value, the ` circular() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Adding a default image URL

You can display a placeholder image if one doesn't exist yet, by passing a URL to the ` defaultImageUrl() ` method:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('header_image')
    ->defaultImageUrl(url('storage/posts/header-images/default.jpg'))
```

As well as allowing a static value, the ` defaultImageUrl() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Stacking images

You may display multiple images as a stack of overlapping images by using ` stacked() `:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
```



Optionally, you may pass a boolean value to control if the images should be stacked or not:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked(FeatureFlag::active())
```

As well as allowing a static value, the ` stacked() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


### Customizing the stacked ring width

No ring is displayed by default, but you may add one with a width from ` 0 ` to ` 8 `:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->ring(5)
```



As well as allowing a static value, the ` ring() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


### Customizing the stacked overlap

The default overlap is ` 2 `, but you may customize it to be from ` 0 ` to ` 8 `:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->overlap(4)
```



As well as allowing a static value, the ` overlap() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


## Setting a limit

You may limit the maximum number of images you want to display by passing ` limit() `:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
```

As well as allowing a static value, the ` limit() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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




### Showing the remaining images count

When you set a limit you may also display the count of remaining images by passing ` limitedRemainingText() `.

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText()
```



Optionally, you may pass a boolean value to control if the remaining text should be displayed or not:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(FeatureFlag::active())
```

As well as allowing a static value, the ` limitedRemainingText() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


#### Customizing the limited remaining text size

By default, the size of the remaining text is ` TextSize::Small `. You can customize this to be ` TextSize::ExtraSmall `, ` TextSize::Medium ` or ` TextSize::Large ` using the ` size ` parameter:

```php
use Filament\Infolists\Components\ImageEntry;
use Filament\Support\Enums\TextSize;

ImageEntry::make('colleagues.avatar')
    ->imageHeight(40)
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText(size: TextSize::Large)
```

As well as allowing a static value, the ` limitedRemainingText() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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


#### Adding a tooltip to the remaining images count

You can add a tooltip to the ` +N ` count using ` limitedRemainingTextTooltip() `. This is separate from ` tooltip() `, which applies to each visible image:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('colleagues.avatar')
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText()
    ->limitedRemainingTextTooltip('More colleagues')
```

As well as allowing a static value, the ` limitedRemainingTextTooltip() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters. The ` $state ` contains the full entry state, including images hidden by the limit.

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


The tooltip is only displayed when the remaining images count is visible. Pass ` null ` to disable it.

## Prevent file existence checks

When the schema is loaded, it will automatically detect whether the images exist to prevent errors for missing files. This is all done on the backend. When using remote storage with many images, this can be time-consuming. You can use the ` checkFileExistence(false) ` method to disable this feature:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('attachment')
    ->checkFileExistence(false)
```

As well as allowing a static value, the ` checkFileExistence() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |


## Adding extra HTML attributes to the image

You can pass extra HTML attributes to the ` <img> ` element via the ` extraImgAttributes() ` method. The attributes should be represented by an array, where the key is the attribute name and the value is the attribute value:

```php
use Filament\Infolists\Components\ImageEntry;

ImageEntry::make('logo')
    ->extraImgAttributes([
        'alt' => 'Logo',
        'loading' => 'lazy',
    ])
```

As well as allowing a static value, the ` extraImgAttributes() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

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
| Related record | ` Illuminate\Database\Eloquent\Model ` | ` $relatedRecord ` | The current related Eloquent record for the rendered item. |
| State | ` mixed ` | ` $state ` | The current value of the entry. |


Calling ` extraImgAttributes() ` multiple times will overwrite the previous attributes.
