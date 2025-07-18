# Filament - Forms/Fields/Rich Editor

Source: https://filamentphp.com/docs/3.x/forms/fields/rich-editor

#Overview
---------

The rich editor allows you to edit and preview HTML content, as well as upload images.

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')

```
![Rich editor](/docs/3.x/images/light/forms/fields/rich-editor/simple.jpg) ![Rich editor](/docs/3.x/images/dark/forms/fields/rich-editor/simple.jpg)

#Security
---------

By default, the editor outputs raw HTML, and sends it to the backend. Attackers are able to intercept the value of the component and send a different raw HTML string to the backend. As such, it is important that when outputting the HTML from a rich editor, it is sanitized; otherwise your site may be exposed to Cross-Site Scripting (XSS) vulnerabilities.

When Filament outputs raw HTML from the database in components such as `TextColumn` and `TextEntry`, it sanitizes it to remove any dangerous JavaScript. However, if you are outputting the HTML from a rich editor in your own Blade view, this is your responsibility. One option is to use Filament’s `sanitizeHtml()` helper to do this, which is the same tool we use to sanitize HTML in the components mentioned above:

```php
{!! str($record->content)->sanitizeHtml() !!}

```
#Customizing the toolbar buttons
--------------------------------

You may set the toolbar buttons for the editor using the `toolbarButtons()` method. The options shown here are the defaults. In addition to these, `'h1'` is also available:

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')
    ->toolbarButtons([
        'attachFiles',
        'blockquote',
        'bold',
        'bulletList',
        'codeBlock',
        'h2',
        'h3',
        'italic',
        'link',
        'orderedList',
        'redo',
        'strike',
        'underline',
        'undo',
    ])

```
Alternatively, you may disable specific buttons using the `disableToolbarButtons()` method:

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')
    ->disableToolbarButtons([
        'blockquote',
        'strike',
    ])

```
To disable all toolbar buttons, set an empty array with `toolbarButtons([])` or use `disableAllToolbarButtons()`.

#Uploading images to the editor
-------------------------------

You may customize how images are uploaded using configuration methods:

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')
    ->fileAttachmentsDisk('s3')
    ->fileAttachmentsDirectory('attachments')
    ->fileAttachmentsVisibility('private')

```
#Disabling Grammarly checks
---------------------------

If the user has Grammarly installed and you would like to prevent it from analyzing the contents of the editor, you can use the `disableGrammarly()` method:

```php
use Filament\Forms\Components\RichEditor;

RichEditor::make('content')
    ->disableGrammarly()

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion