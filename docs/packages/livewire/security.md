# Livewire - Security

Source: https://livewire.laravel.com/docs/security

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

Security
========

Are you a visual learner?

Master Livewire with our in-depth screencasts

Watch now

It's important to make sure your Livewire apps are secure and don't expose any application vulnerabilities. Livewire has internal security features to handle many cases, however, there are times when it's up to your application code to keep your components secure.

#Authorizing action parameters
------------------------------

Livewire actions are extremely powerful, however, any parameters passed to Livewire actions are mutable on the client and should be treated as un-trusted user input.

Arguably the most common security pitfall in Livewire is failing to validate and authorize Livewire action calls before persisting changes to the database.

Here is an example of an insecurity resulting from a lack of authorization:

```php

<?php

use App\Models\Post;

use Livewire\Component;

class ShowPost extends Component

{

// ...

public function delete($id)

{

// INSECURE!

$post = Post::find($id);

$post->delete();

}

}

```
```php

<button wire:click="delete({{ $post->id }})">Delete Post</button>

```
The reason the above example is insecure is that `wire:click="delete(...)"` can be modified in the browser to pass ANY post ID a malicious user wishes.

Action parameters (like `$id` in this case) should be treated the same as any untrusted input from the browser.

Therefore, to keep this application secure and prevent a user from deleting another user's post, we must add authorization to the `delete()` action.

First, let's create a Laravel Policy for the Post model by running the following command:

```php

php artisan make:policy PostPolicy --model=Post

```
After running the above command, a new Policy will be created inside `app/Policies/PostPolicy.php`. We can then update its contents with a `delete` method like so:

```php

<?php

namespace App\Policies;

use App\Models\Post;

use App\Models\User;

class PostPolicy

{

/**

* Determine if the given post can be deleted by the user.

*/

public function delete(?User $user, Post $post): bool

{

return $user?->id === $post->user_id;

}

}

```
Now, we can use the `$this->authorize()` method from the Livewire component to ensure the user owns the post before deleting it:

```php

public function delete($id)

{

$post = Post::find($id);

// If the user doesn't own the post,

// an AuthorizationException will be thrown...

$this->authorize('delete', $post);

$post->delete();

}

```
Further reading:

* Laravel Gates
* Laravel Policies

#Authorizing public properties
------------------------------

Similar to action parameters, public properties in Livewire should be treated as un-trusted input from the user.

Here is the same example from above about deleting a post, written insecurely in a different manner:

```php

<?php

use App\Models\Post;

use Livewire\Component;

class ShowPost extends Component

{

public $postId;

public function mount($postId)

{

$this->postId = $postId;

}

public function delete()

{

// INSECURE!

$post = Post::find($this->postId);

$post->delete();

}

}

```
```php

<button wire:click="delete">Delete Post</button>

```
As you can see, instead of passing the `$postId` as a parameter to the `delete` method from `wire:click`, we are storing it as a public property on the Livewire component.

The problem with this approach is that any malicious user can inject a custom element onto the page such as:

```php

<input type="text" wire:model="postId">

```
This would allow them to freely modify the `$postId` before pressing "Delete Post". Because the `delete` action doesn't authorize the value of `$postId`, the user can now delete any post in the database, whether they own it or not.

To protect against this risk, there are two possible solutions:

### #Using model properties

When setting public properties, Livewire treats models differently than plain values such as strings and integers. Because of this, if we instead store the entire post model as a property on the component, Livewire will ensure the ID is never tampered with.

Here is an example of storing a `$post` property instead of a simple `$postId` property:

```php

<?php

use App\Models\Post;

use Livewire\Component;

class ShowPost extends Component

{

public Post $post;

public function mount($postId)

{

$this->post = Post::find($postId);

}

public function delete()

{

$this->post->delete();

}

}

```
```php

<button wire:click="delete">Delete Post</button>

```
This component is now secured because there is no way for a malicious user to change the `$post` property to a different Eloquent model.

### #Locking the property

Another way to prevent properties from being set to unwanted values is to use locked properties. Locking properties is done by applying the `#[Locked]` attribute. Now if users attempt to tamper with this value an error will be thrown.

Note that properties with the Locked attribute can still be changed in the back-end, so care still needs to taken that untrusted user input is not passed to the property in your own Livewire functions.

```php

<?php

use App\Models\Post;

use Livewire\Component;

use Livewire\Attributes\Locked;

class ShowPost extends Component

{

#[Locked]

public $postId;

public function mount($postId)

{

$this->postId = $postId;

}

public function delete()

{

$post = Post::find($this->postId);

$post->delete();

}

}

```
### #Authorizing the property

If using a model property is undesired in your scenario, you can of course fall-back to manually authorizing the deletion of the post inside the `delete` action:

```php

<?php

use App\Models\Post;

use Livewire\Component;

class ShowPost extends Component

{

public $postId;

public function mount($postId)

{

$this->postId = $postId;

}

public function delete()

{

$post = Post::find($this->postId);

$this->authorize('delete', $post);

$post->delete();

}

}

```
```php

<button wire:click="delete">Delete Post</button>

```
Now, even though a malicious user can still freely modify the value of `$postId`, when the `delete` action is called, `$this->authorize()` will throw an `AuthorizationException` if the user does not own the post.

Further reading:

* Laravel Gates
* Laravel Policies

#Middleware
-----------

When a Livewire component is loaded on a page containing route-level Authorization Middleware, like so:

```php

Route::get('/post/{post}', App\Livewire\UpdatePost::class)

->middleware('can:update,post');

```
Livewire will ensure those middlewares are re-applied to subsequent Livewire network requests. This is referred to as "Persistent Middleware" in Livewire's core.

Persistent middleware protects you from scenarios where the authorization rules or user permissions have changed after the initial page-load.

Here's a more in-depth example of such a scenario:

```php

Route::get('/post/{post}', App\Livewire\UpdatePost::class)

->middleware('can:update,post');

```
```php

<?php

use App\Models\Post;

use Livewire\Component;

use Livewire\Attributes\Validate;

class UpdatePost extends Component

{

public Post $post;

#[Validate('required|min:5')]

public $title = '';

public $content = '';

public function mount()

{

$this->title = $this->post->title;

$this->content = $this->post->content;

}

public function update()

{

$this->post->update([

'title' => $this->title,

'content' => $this->content,

]);

}

}

```
As you can see, the `can:update,post` middleware is applied at the route-level. This means that a user who doesn't have permission to update a post cannot view the page.

However, consider a scenario where a user:

* Loads the page
* Loses permission to update after the page loads
* Tries updating the post after losing permission

Because Livewire has already successfully loaded the page you might ask yourself: "When Livewire makes a subsequent request to update the post, will the `can:update,post` middleware be re-applied? Or instead, will the un-authorized user be able to update the post successfully?"

Because Livewire has internal mechanisms to re-apply middleware from the original endpoint, you are protected in this scenario.

### #Configuring persistent middleware

By default, Livewire persists the following middleware across network requests:

```php

\Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,

\Laravel\Jetstream\Http\Middleware\AuthenticateSession::class,

\Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,

\Illuminate\Routing\Middleware\SubstituteBindings::class,

\App\Http\Middleware\RedirectIfAuthenticated::class,

\Illuminate\Auth\Middleware\Authenticate::class,

\Illuminate\Auth\Middleware\Authorize::class,

```
If any of the above middlewares are applied to the initial page-load, they will be persisted (re-applied) to any future network requests.

However, if you are applying a custom middleware from your application on the initial page-load, and want it persisted between Livewire requests, you will need to add it to this list from a Service Provider in your app like so:

```php

<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

use Livewire;

class AppServiceProvider extends ServiceProvider

{

/**

* Bootstrap any application services.

*/

public function boot(): void

{

Livewire::addPersistentMiddleware([

App\Http\Middleware\EnsureUserHasRole::class,

]);

}

}

```
If a Livewire component is loaded on a page that uses the `EnsureUserHasRole` middleware from your application, it will now be persisted and re-applied to any future network requests to that Livewire component.

Middleware arguments are not supported

Livewire currently doesn't support middleware arguments for persistent middleware definitions.

```php

// Bad...

Livewire::addPersistentMiddleware(AuthorizeResource::class.':admin');

// Good...

Livewire::addPersistentMiddleware(AuthorizeResource::class);

```
### #Applying global Livewire middleware

Alternatively, if you wish to apply specific middleware to every single Livewire update network request, you can do so by registering your own Livewire update route with any middleware you wish:

```php

Livewire::setUpdateRoute(function ($handle) {

return Route::post('/livewire/update', $handle)

->middleware(App\Http\Middleware\LocalizeViewPaths::class);

});

```
Any Livewire AJAX/fetch requests made to the server will use the above endpoint and apply the `LocalizeViewPaths` middleware before handling the component update.

Learn more about customizing the update route on the Installation page.

#Snapshot checksums
-------------------

Between every Livewire request, a snapshot is taken of the Livewire component and sent to the browser. This snapshot is used to re-build the component during the next server round-trip.

Learn more about Livewire snapshots in the Hydration documentation.

Because fetch requests can be intercepted and tampered with in a browser, Livewire generates a "checksum" of each snapshot to go along with it.

This checksum is then used on the next network request to verify that the snapshot hasn't changed in any way.

If Livewire finds a checksum mismatch, it will throw a `CorruptComponentPayloadException` and the request will fail.

This protects against any form of malicious tampering that would otherwise result in granting users the ability to execute or modify unrelated code.

On this page

* Authorizing action parameters
* Authorizing public properties
  + Using model properties
  + Locking the property
  + Authorizing the property
* Middleware
  + Configuring persistent middleware
  + Applying global Livewire middleware
* Snapshot checksums

![Flux Ad](/images/flux_ad.jpg)

Pro UI Components

Flux · The official Livewire component library

Built by the folks behind Livewire and Alpine.