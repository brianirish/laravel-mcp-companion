# Filament - Forms/Fields/Markdown Editor

Source: https://filamentphp.com/docs/3.x/forms/fields/markdown-editor

#Overview
---------

The markdown editor allows you to edit and preview markdown content, as well as upload images using drag and drop.

```php
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')

```
![Markdown editor](/docs/3.x/images/light/forms/fields/markdown-editor/simple.jpg) ![Markdown editor](/docs/3.x/images/dark/forms/fields/markdown-editor/simple.jpg)

#Security
---------

By default, the editor outputs raw Markdown and HTML, and sends it to the backend. Attackers are able to intercept the value of the component and send a different raw HTML string to the backend. As such, it is important that when outputting the HTML from a Markdown editor, it is sanitized; otherwise your site may be exposed to Cross-Site Scripting (XSS) vulnerabilities.

When Filament outputs raw HTML from the database in components such as `TextColumn` and `TextEntry`, it sanitizes it to remove any dangerous JavaScript. However, if you are outputting the HTML from a Markdown editor in your own Blade view, this is your responsibility. One option is to use Filament’s `sanitizeHtml()` helper to do this, which is the same tool we use to sanitize HTML in the components mentioned above:

```php
{!! str($record->content)->markdown()->sanitizeHtml() !!}

```
#Customizing the toolbar buttons
--------------------------------

You may set the toolbar buttons for the editor using the `toolbarButtons()` method. The options shown here are the defaults:

```php
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->toolbarButtons([
        'attachFiles',
        'blockquote',
        'bold',
        'bulletList',
        'codeBlock',
        'heading',
        'italic',
        'link',
        'orderedList',
        'redo',
        'strike',
        'table',
        'undo',
    ])

```
Alternatively, you may disable specific buttons using the `disableToolbarButtons()` method:

```php
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
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
use Filament\Forms\Components\MarkdownEditor;

MarkdownEditor::make('content')
    ->fileAttachmentsDisk('s3')
    ->fileAttachmentsDirectory('attachments')
    ->fileAttachmentsVisibility('private')

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion