# Filament - Forms/Fields/Textarea

Source: https://filamentphp.com/docs/3.x/forms/fields/textarea

#Overview
---------

The textarea allows you to interact with a multi-line string:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')

```
![Textarea](/docs/3.x/images/light/forms/fields/textarea/simple.jpg) ![Textarea](/docs/3.x/images/dark/forms/fields/textarea/simple.jpg)

#Resizing the textarea
----------------------

You may change the size of the textarea by defining the `rows()` and `cols()` methods:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->rows(10)
    ->cols(20)

```
### #Autosizing the textarea

You may allow the textarea to automatically resize to fit its content by setting the `autosize()` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->autosize()

```
#Making the field read-only
---------------------------

Not to be confused with disabling the field, you may make the field “read-only” using the `readOnly()` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->readOnly()

```
There are a few differences, compared to `disabled()`:

* When using `readOnly()`, the field will still be sent to the server when the form is submitted. It can be mutated with the browser console, or via JavaScript. You can use `dehydrated(false)` to prevent this.
* There are no styling changes, such as less opacity, when using `readOnly()`.
* The field is still focusable when using `readOnly()`.

#Disabling Grammarly checks
---------------------------

If the user has Grammarly installed and you would like to prevent it from analyzing the contents of the textarea, you can use the `disableGrammarly()` method:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->disableGrammarly()

```
#Textarea validation
--------------------

As well as all rules listed on the validation page, there are additional rules that are specific to textareas.

### #Length validation

You may limit the length of the textarea by setting the `minLength()` and `maxLength()` methods. These methods add both frontend and backend validation:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('description')
    ->minLength(2)
    ->maxLength(1024)

```
You can also specify the exact length of the textarea by setting the `length()`. This method adds both frontend and backend validation:

```php
use Filament\Forms\Components\Textarea;

Textarea::make('question')
    ->length(100)

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion