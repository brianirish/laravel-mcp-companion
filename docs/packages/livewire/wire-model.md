# Livewire - Wire Model

Source: https://livewire.laravel.com/docs/wire-model

Version 3.x

Version 3.x
Version 2.x
Version 1.x

* ##### Getting Started

  + Quickstart
  + Installation
  + Upgrade Guide

UI Components →

* ##### Essentials

  + Components
  + Properties
  + Actions
  + Forms
  + Events
  + Lifecycle Hooks
  + Nesting Components
  + Testing
* ##### Features

  + Alpine
  + Navigate
  + Lazy Loading
  + Validation
  + File Uploads
  + Pagination
  + URL Query Parameters
  + Computed Properties
  + Session Properties
  + Redirecting
  + File Downloads
  + Locked Properties
  + Request Bundling
  + Offline States
  + Teleport
* ##### HTML Directives

  + wire:click
  + wire:submit
  + wire:model
  + wire:loading
  + wire:navigate
  + wire:current
  + wire:cloak
  + wire:dirty
  + wire:confirm
  + wire:transition
  + wire:init
  + wire:poll
  + wire:offline
  + wire:ignore
  + wire:replace
  + wire:show
  + wire:stream
  + wire:text
* ##### Concepts

  + Morphing
  + Hydration
  + Nesting
* ##### Advanced

  + Troubleshooting
  + Security
  + JavaScript
  + Synthesizers
  + Contribution Guide
* ##### Packages

  + Volt

wire:model
==========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire makes it easy to bind a component property's value with form inputs using `wire:model`.

Here is a simple example of using `wire:model` to bind the `$title` and `$content` properties with form inputs in a "Create Post" component:

```php

use Livewire\Component;

use App\Models\Post;

class CreatePost extends Component

{

public $title = '';

public $content = '';

public function save()

{

$post = Post::create([

'title' => $this->title

'content' => $this->content

]);

// ...

}

}

```
```php

<form wire:submit="save">

<label>

<span>Title</span>

<input type="text" wire:model="title">

</label>

<label>

<span>Content</span>

<textarea wire:model="content"></textarea>

</label>

<button type="submit">Save</button>

</form>

```
Because both inputs use `wire:model`, their values will be synchronized with the server's properties when the "Save" button is pressed.

"Why isn't my component live updating as I type?"

If you tried this in your browser and are confused why the title isn't automatically updating, it's because Livewire only updates a component when an "action" is submitted—like pressing a submit button—not when a user types into a field. This cuts down on network requests and improves performance. To enable "live" updating as a user types, you can use `wire:model.live` instead. Learn more about data binding.

#Customizing update timing
--------------------------

By default, Livewire will only send a network request when an action is performed (like `wire:click` or `wire:submit`), NOT when a `wire:model` input is updated.

This drastically improves the performance of Livewire by reducing network requests and provides a smoother experience for your users.

However, there are occasions where you may want to update the server more frequently for things like real-time validation.

### #Live updating

To send property updates to the server as a user types into an input-field, you can append the `.live` modifier to `wire:model`:

```php

<input type="text" wire:model.live="title">

```
#### #Customizing the debounce

By default, when using `wire:model.live`, Livewire adds a 150 millisecond debounce to server updates. This means if a user is continually typing, Livewire will wait until the user stops typing for 150 milliseconds before sending a request.

You can customize this timing by appending `.debounce.Xms` to the input. Here is an example of changing the debounce to 250 milliseconds:

```php

<input type="text" wire:model.live.debounce.250ms="title">

```
### #Updating on "blur" event

By appending the `.blur` modifier, Livewire will only send network requests with property updates when a user clicks away from an input, or presses the tab key to move to the next input.

Adding `.blur` is helpful for scenarios where you want to update the server more frequently, but not as a user types. For example, real-time validation is a common instance where `.blur` is helpful.

```php

<input type="text" wire:model.blur="title">

```
### #Updating on "change" event

There are times when the behavior of `.blur` isn't exactly what you want and instead `.change` is.

For example, if you want to run validation every time a select input is changed, by adding `.change`, Livewire will send a network request and validate the property as soon as a user selects a new option. As opposed to `.blur` which will only update the server after the user tabs away from the select input.

```php

<select wire:model.change="title">

<!-- ... -->

</select>

```
Any changes made to the text input will be automatically synchronized with the `$title` property in your Livewire component.

#All available modifiers
------------------------

| Modifier | Description |
| --- | --- |
| `.live` | Send updates as a user types |
| `.blur` | Only send updates on the `blur` event |
| `.change` | Only send updates on the the `change` event |
| `.lazy` | An alias for `.change` |
| `.debounce.[?]ms` | Debounce the sending of updates by the specified millisecond delay |
| `.throttle.[?]ms` | Throttle network request updates by the specified millisecond interval |
| `.number` | Cast the text value of an input to `int` on the server |
| `.boolean` | Cast the text value of an input to `bool` on the server |
| `.fill` | Use the initial value provided by a "value" HTML attribute on page-load |

#Input fields
-------------

Livewire supports most native input elements out of the box. Meaning you should just be able to attach `wire:model` to any input element in the browser and easily bind properties to them.

Here's a comprehensive list of the different available input types and how you use them in a Livewire context.

### #Text inputs

First and foremost, text inputs are the bedrock of most forms. Here's how to bind a property named "title" to one:

```php

<input type="text" wire:model="title">

```
### #Textarea inputs

Textarea elements are similarly straightforward. Simply add `wire:model` to a textarea and the value will be bound:

```php

<textarea type="text" wire:model="content"></textarea>

```
If the "content" value is initialized with a string, Livewire will fill the textarea with that value - there's no need to do something like the following:

```php

<!-- Warning: This snippet demonstrates what NOT to do... -->

<textarea type="text" wire:model="content">{{ $content }}</textarea>

```
### #Checkboxes

Checkboxes can be used for single values, such as when toggling a boolean property. Or, checkboxes may be used to toggle a single value in a group of related values. We'll discuss both scenarios:

#### #Single checkbox

At the end of a signup form, you might have a checkbox allowing the user to opt-in to email updates. You might call this property `$receiveUpdates`. You can easily bind this value to the checkbox using `wire:model`:

```php

<input type="checkbox" wire:model="receiveUpdates">

```
Now when the `$receiveUpdates` value is `false`, the checkbox will be unchecked. Of course, when the value is `true`, the checkbox will be checked.

#### #Multiple checkboxes

Now, let's say in addition to allowing the user to decide to receive updates, you have an array property in your class called `$updateTypes`, allowing the user to choose from a variety of update types:

```php

public $updateTypes = [];

```
By binding multiple checkboxes to the `$updateTypes` property, the user can select multiple update types and they will be added to the `$updateTypes` array property:

```php

<input type="checkbox" value="email" wire:model="updateTypes">

<input type="checkbox" value="sms" wire:model="updateTypes">

<input type="checkbox" value="notification" wire:model="updateTypes">

```
For example, if the user checks the first two boxes but not the third, the value of `$updateTypes` will be: `["email", "sms"]`

### #Radio buttons

To toggle between two different values for a single property, you may use radio buttons:

```php

<input type="radio" value="yes" wire:model="receiveUpdates">

<input type="radio" value="no" wire:model="receiveUpdates">

```
### #Select dropdowns

Livewire makes it simple to work with `<select>` dropdowns. When adding `wire:model` to a dropdown, the currently selected value will be bound to the provided property name and vice versa.

In addition, there's no need to manually add `selected` to the option that will be selected - Livewire handles that for you automatically.

Below is an example of a select dropdown filled with a static list of states:

```php

<select wire:model="state">

<option value="AL">Alabama</option>

<option value="AK">Alaska</option>

<option value="AZ">Arizona</option>

...

</select>

```
When a specific state is selected, for example, "Alaska", the `$state` property on the component will be set to `AK`. If you would prefer the value to be set to "Alaska" instead of "AK", you can leave the `value=""` attribute off the `<option>` element entirely.

Often, you may build your dropdown options dynamically using Blade:

```php

<select wire:model="state">

@foreach (\App\Models\State::all() as $state)

<option value="{{ $state->id }}">{{ $state->label }}</option>

@endforeach

</select>

```
If you don't have a specific option selected by default, you may want to show a muted placeholder option by default, such as "Select a state":

```php

<select wire:model="state">

<option disabled value="">Select a state...</option>

@foreach (\App\Models\State::all() as $state)

<option value="{{ $state->id }}">{{ $state->label }}</option>

@endforeach

</select>

```
As you can see, there is no "placeholder" attribute for a select menu like there is for text inputs. Instead, you have to add a `disabled` option element as the first option in the list.

### #Dependent select dropdowns

Sometimes you may want one select menu to be dependent on another. For example, a list of cities that changes based on which state is selected.

For the most part, this works as you'd expect, however there is one important gotcha: You must add a `wire:key` to the changing select so that Livewire properly refreshes its value when the options change.

Here's an example of two selects, one for states, one for cities. When the state select changes, the options in the city select will change properly:

```php

<!-- States select menu... -->

<select wire:model.live="selectedState">

@foreach (State::all() as $state)

<option value="{{ $state->id }}">{{ $state->label }}</option>

@endforeach

</select>

<!-- Cities dependent select menu... -->

<select wire:model.live="selectedCity" wire:key="{{ $selectedState }}">

@foreach (City::whereStateId($selectedState->id)->get() as $city)

<option value="{{ $city->id }}">{{ $city->label }}</option>

@endforeach

</select>

```
Again, the only thing non-standard here is the `wire:key` that has been added to the second select. This ensures that when the state changes, the "selectedCity" value will be reset properly.

### #Multi-select dropdowns

If you are using a "multiple" select menu, Livewire works as expected. In this example, states will be added to the `$states` array property when they are selected and removed if they are deselected:

```php

<select wire:model="states" multiple>

<option value="AL">Alabama</option>

<option value="AK">Alaska</option>

<option value="AZ">Arizona</option>

...

</select>

```
#Going deeper
-------------

For a more complete documentation on using `wire:model` in the context of HTML forms, visit the Livewire forms documentation page.

On this page

* Customizing update timing
  + Live updating
  + Updating on "blur" event
  + Updating on "change" event
* All available modifiers
* Input fields
  + Text inputs
  + Textarea inputs
  + Checkboxes
  + Radio buttons
  + Select dropdowns
  + Dependent select dropdowns
  + Multi-select dropdowns
* Going deeper

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.