# Livewire - Events

Source: https://livewire.laravel.com/docs/events

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

Events
======

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

Livewire offers a robust event system that you can use to communicate between different components on the page. Because it uses browser events under the hood, you can also use Livewire's event system to communicate with Alpine components or even plain, vanilla JavaScript.

To trigger an event, you may use the `dispatch()` method from anywhere inside your component and listen for that event from any other component on the page.

#Dispatching events
-------------------

To dispatch an event from a Livewire component, you can call the `dispatch()` method, passing it the event name and any additional data you want to send along with the event.

Below is an example of dispatching a `post-created` event from a `CreatePost` component:

```php

use Livewire\Component;

class CreatePost extends Component

{

public function save()

{

// ...

$this->dispatch('post-created');

}

}

```
In this example, when the `dispatch()` method is called, the `post-created` event will be dispatched, and every other component on the page that is listening for this event will be notified.

You can pass additional data with the event by passing the data as the second parameter to the `dispatch()` method:

```php

$this->dispatch('post-created', title: $post->title);

```
#Listening for events
---------------------

To listen for an event in a Livewire component, add the `#[On]` attribute above the method you want to be called when a given event is dispatched:

Make sure you import attribute classes

Make sure you import any attribute classes. For example, the below `#[On()]` attributes requires the following import `use Livewire\Attributes\On;`.

```php

use Livewire\Component;

use Livewire\Attributes\On;

class Dashboard extends Component

{

#[On('post-created')]

public function updatePostList($title)

{

// ...

}

}

```
Now, when the `post-created` event is dispatched from `CreatePost`, a network request will be triggered and the `updatePostList()` action will be invoked.

As you can see, additional data sent with the event will be provided to the action as its first argument.

### #Listening for dynamic event names

Occasionally, you may want to dynamically generate event listener names at run-time using data from your component.

For example, if you wanted to scope an event listener to a specific Eloquent model, you could append the model's ID to the event name when dispatching like so:

```php

use Livewire\Component;

class UpdatePost extends Component

{

public function update()

{

// ...

$this->dispatch("post-updated.{$post->id}");

}

}

```
And then listen for that specific model:

```php

use Livewire\Component;

use App\Models\Post;

use Livewire\Attributes\On;

class ShowPost extends Component

{

public Post $post;

#[On('post-updated.{post.id}')]

public function refreshPost()

{

// ...

}

}

```
If the above `$post` model had an ID of `3`, the `refreshPost()` method would only be triggered by an event named: `post-updated.3`.

### #Listening for events from specific child components

Livewire allows you to listen for events directly on individual child components in your Blade template like so:

```php

<div>

<livewire:edit-post @saved="$refresh">

<!-- ... -->

</div>

```
In the above scenario, if the `edit-post` child component dispatches a `saved` event, the parent's `$refresh` will be called and the parent will be refreshed.

Instead of passing `$refresh`, you can pass any method you normally would to something like `wire:click`. Here's an example of calling a `close()` method that might do something like close a modal dialog:

```php

<livewire:edit-post @saved="close">

```
If the child dispatched parameters along with the request, for example `$this->dispatch('saved', postId: 1)`, you can forward those values to the parent method using the following syntax:

```php

<livewire:edit-post @saved="close($event.detail.postId)">

```
#Using JavaScript to interact with events
-----------------------------------------

Livewire's event system becomes much more powerful when you interact with it from JavaScript inside your application. This unlocks the ability for any other JavaScript in your app to communicate with Livewire components on the page.

### #Listening for events inside component scripts

You can easily listen for the `post-created` event inside your component's template from a `@script` directive like so:

```php

@script

<script>

$wire.on('post-created', () => {

//

});

</script>

@endscript

```
The above snippet would listen for the `post-created` from the component it's registered within. If the component is no longer on the page, the event listener will no longer be triggered.

Read more about using JavaScript inside your Livewire components →

### #Dispatching events from component scripts

Additionally, you can dispatch events from within a component's `@script` like so:

```php

@script

<script>

$wire.dispatch('post-created');

</script>

@endscript

```
When the above `@script` is run, the `post-created` event will be dispatched to the component it's defined within.

To dispatch the event only to the component where the script resides and not other components on the page (preventing the event from "bubbling" up), you can use `dispatchSelf()`:

```php

$wire.dispatchSelf('post-created');

```
You can pass any additional parameters to the event by passing an object as a second argument to `dispatch()`:

```php

@script

<script>

$wire.dispatch('post-created', { refreshPosts: true });

</script>

@endscript

```
You can now access those event parameters from both your Livewire class and also other JavaScript event listeners.

Here's an example of receiving the `refreshPosts` parameter within a Livewire class:

```php

use Livewire\Attributes\On;

// ...

#[On('post-created')]

public function handleNewPost($refreshPosts = false)

{

//

}

```
You can also access the `refreshPosts` parameter from a JavaScript event listener from the event's `detail` property:

```php

@script

<script>

$wire.on('post-created', (event) => {

let refreshPosts = event.detail.refreshPosts

// ...

});

</script>

@endscript

```
Read more about using JavaScript inside your Livewire components →

### #Listening for Livewire events from global JavaScript

Alternatively, you can listen for Livewire events globally using `Livewire.on` from any script in your application:

```php

<script>

document.addEventListener('livewire:init', () => {

Livewire.on('post-created', (event) => {

//

});

});

</script>

```
The above snippet would listen for the `post-created` event dispatched from any component on the page.

If you wish to remove this event listener for any reason, you can do so using the returned `cleanup` function:

```php

<script>

document.addEventListener('livewire:init', () => {

let cleanup = Livewire.on('post-created', (event) => {

//

});

// Calling "cleanup()" will un-register the above event listener...

cleanup();

});

</script>

```
#Events in Alpine
-----------------

Because Livewire events are plain browser events under the hood, you can use Alpine to listen for them or even dispatch them.

### #Listening for Livewire events in Alpine

For example, we may easily listen for the `post-created` event using Alpine:

```php

<div x-on:post-created="..."></div>

```
The above snippet would listen for the `post-created` event from any Livewire components that are children of the HTML element that the `x-on` directive is assigned to.

To listen for the event from any Livewire component on the page, you can add `.window` to the listener:

```php

<div x-on:post-created.window="..."></div>

```
If you want to access additional data that was sent with the event, you can do so using `$event.detail`:

```php

<div x-on:post-created="notify('New post: ' + $event.detail.title)"></div>

```
The Alpine documentation provides further information on listening for events.

### #Dispatching Livewire events from Alpine

Any event dispatched from Alpine is capable of being intercepted by a Livewire component.

For example, we may easily dispatch the `post-created` event from Alpine:

```php

<button @click="$dispatch('post-created')">...</button>

```
Like Livewire's `dispatch()` method, you can pass additional data along with the event by passing the data as the second parameter to the method:

```php

<button @click="$dispatch('post-created', { title: 'Post Title' })">...</button>

```
To learn more about dispatching events using Alpine, consult the Alpine documentation.

You might not need events

If you are using events to call behavior on a parent from a child, you can instead call the action directly from the child using `$parent` in your Blade template. For example:

```php

<button wire:click="$parent.showCreatePostForm()">Create Post</button>

```
Learn more about $parent.

#Dispatching directly to another component
------------------------------------------

If you want to use events for communicating directly between two components on the page, you can use the `dispatch()->to()` modifier.

Below is an example of the `CreatePost` component dispatching the `post-created` event directly to the `Dashboard` component, skipping any other components listening for that specific event:

```php

use Livewire\Component;

class CreatePost extends Component

{

public function save()

{

// ...

$this->dispatch('post-created')->to(Dashboard::class);

}

}

```
#Dispatching a component event to itself
----------------------------------------

Using the `dispatch()->self()` modifier, you can restrict an event to only being intercepted by the component it was triggered from:

```php

use Livewire\Component;

class CreatePost extends Component

{

public function save()

{

// ...

$this->dispatch('post-created')->self();

}

}

```
#Dispatching events from Blade templates
----------------------------------------

You can dispatch events directly from your Blade templates using the `$dispatch` JavaScript function. This is useful when you want to trigger an event from a user interaction, such as a button click:

```php

<button wire:click="$dispatch('show-post-modal', { id: {{ $post->id }} })">

EditPost

</button>

```
In this example, when the button is clicked, the `show-post-modal` event will be dispatched with the specified data.

If you want to dispatch an event directly to another component you can use the `$dispatchTo()` JavaScript function:

```php

<button wire:click="$dispatchTo('posts', 'show-post-modal', { id: {{ $post->id }} })">

EditPost

</button>

```
In this example, when the button is clicked, the `show-post-modal` event will be dispatched directly to the `Posts` component.

#Testing dispatched events
--------------------------

To test events dispatched by your component, use the `assertDispatched()` method in your Livewire test. This method checks that a specific event has been dispatched during the component's lifecycle:

```php

<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;

use App\Livewire\CreatePost;

use Livewire\Livewire;

class CreatePostTest extends TestCase

{

use RefreshDatabase;

/** @test */

public function it_dispatches_post_created_event()

{

Livewire::test(CreatePost::class)

->call('save')

->assertDispatched('post-created');

}

}

```
In this example, the test ensures that the `post-created` event is dispatched with the specified data when the `save()` method is called on the `CreatePost` component.

### #Testing Event Listeners

To test event listeners, you can dispatch events from the test environment and assert that the expected actions are performed in response to the event:

```php

<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;

use App\Livewire\Dashboard;

use Livewire\Livewire;

class DashboardTest extends TestCase

{

use RefreshDatabase;

/** @test */

public function it_updates_post_count_when_a_post_is_created()

{

Livewire::test(Dashboard::class)

->assertSee('Posts created: 0')

->dispatch('post-created')

->assertSee('Posts created: 1');

}

}

```
In this example, the test dispatches the `post-created` event, then checks that the `Dashboard` component properly handles the event and displays the updated count.

#Real-time events using Laravel Echo
------------------------------------

Livewire pairs nicely with Laravel Echo to provide real-time functionality on your web-pages using WebSockets.

Installing Laravel Echo is a prerequisite

This feature assumes you have installed Laravel Echo and the `window.Echo` object is globally available in your application. For more information on installing echo, check out the Laravel Echo documentation.

### #Listening for Echo events

Imagine you have an event in your Laravel application named `OrderShipped`:

```php

<?php

namespace App\Events;

use App\Models\Order;

use Illuminate\Broadcasting\Channel;

use Illuminate\Broadcasting\InteractsWithSockets;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;

use Illuminate\Foundation\Events\Dispatchable;

use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldBroadcast

{

use Dispatchable, InteractsWithSockets, SerializesModels;

public Order $order;

public function broadcastOn()

{

return new Channel('orders');

}

}

```
You might dispatch this event from another part of your application like so:

```php

use App\Events\OrderShipped;

OrderShipped::dispatch();

```
If you were to listen for this event in JavaScript using only Laravel Echo, it would look something like this:

```php

Echo.channel('orders')

.listen('OrderShipped', e => {

console.log(e.order)

})

```
Assuming you have Laravel Echo installed and configured, you can listen for this event from inside a Livewire component.

Below is an example of an `OrderTracker` component that is listening for the `OrderShipped` event in order to show users a visual indication of a new order:

```php

<?php

namespace App\Livewire;

use Livewire\Attributes\On;

use Livewire\Component;

class OrderTracker extends Component

{

public $showNewOrderNotification = false;

#[On('echo:orders,OrderShipped')]

public function notifyNewOrder()

{

$this->showNewOrderNotification = true;

}

// ...

}

```
If you have Echo channels with variables embedded in them (such as an Order ID), you can define listeners via the `getListeners()` method instead of the `#[On]` attribute:

```php

<?php

namespace App\Livewire;

use Livewire\Attributes\On;

use Livewire\Component;

use App\Models\Order;

class OrderTracker extends Component

{

public Order $order;

public $showOrderShippedNotification = false;

public function getListeners()

{

return [

"echo:orders.{$this->order->id},OrderShipped" => 'notifyShipped',

];

}

public function notifyShipped()

{

$this->showOrderShippedNotification = true;

}

// ...

}

```
Or, if you prefer, you can use the dynamic event name syntax:

```php

#[On('echo:orders.{order.id},OrderShipped')]

public function notifyNewOrder()

{

$this->showNewOrderNotification = true;

}

```
If you need to access the event payload, you can do so via the passed in `$event` parameter:

```php

#[On('echo:orders.{order.id},OrderShipped')]

public function notifyNewOrder($event)

{

$order = Order::find($event['orderId']);

//

}

```
### #Private & presence channels

You may also listen to events broadcast to private and presence channels:

Before proceeding, ensure you have defined Authentication Callbacks for your broadcast channels.

```php

<?php

namespace App\Livewire;

use Livewire\Component;

class OrderTracker extends Component

{

public $showNewOrderNotification = false;

public function getListeners()

{

return [

// Public Channel

"echo:orders,OrderShipped" => 'notifyNewOrder',

// Private Channel

"echo-private:orders,OrderShipped" => 'notifyNewOrder',

// Presence Channel

"echo-presence:orders,OrderShipped" => 'notifyNewOrder',

"echo-presence:orders,here" => 'notifyNewOrder',

"echo-presence:orders,joining" => 'notifyNewOrder',

"echo-presence:orders,leaving" => 'notifyNewOrder',

];

}

public function notifyNewOrder()

{

$this->showNewOrderNotification = true;

}

}

```
On this page

* Dispatching events
* Listening for events
  + Listening for dynamic event names
  + Listening for events from specific child components
* Using JavaScript to interact with events
  + Listening for events inside component scripts
  + Dispatching events from component scripts
  + Listening for Livewire events from global JavaScript
* Events in Alpine
  + Listening for Livewire events in Alpine
  + Dispatching Livewire events from Alpine
* Dispatching directly to another component
* Dispatching a component event to itself
* Dispatching events from Blade templates
* Testing dispatched events
  + Testing Event Listeners
* Real-time events using Laravel Echo
  + Listening for Echo events
  + Private & presence channels

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.