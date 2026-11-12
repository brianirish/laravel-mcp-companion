# Laravel Learn - Getting Started with Laravel: Edit and delete Chirps

Source: https://laravel.com/learn/getting-started-with-laravel/edit-and-delete-chirps

---

Complete CRUD operations by adding edit and delete functionality. Learn about RESTful routing and build a full-featured content management system.

No one's perfect and everyone makes mistakes, typos, you name it. So let's start the day with a nice cup of coffee and add the ability for our users to edit their chirps.

The neat part is this completes the whole CRUD operations within an MVC structure in a Laravel application. So CRUD: Create, Read, Update, and Delete. We've got Create and Read down—now let's do the Update and Delete parts!

## Step 1: Add Edit and Delete UI

In our chirp.blade.php component (that's our component for each chirp that we're looping through), let's add edit and delete buttons. We'll add the UI first, but we won't hook it up just yet.

Update `resources/views/components/chirp.blade.php`:

```html
@props(['chirp'])

<div class="card bg-base-100 shadow">
    <div class="card-body">
        <div class="flex space-x-3">
            @if ($chirp->user)
                <div class="avatar">
                    <div class="size-10 rounded-full">
                        <img src="<https://avatars.laravel.cloud/>{{ urlencode($chirp->user->email) }}"
                            alt="{{ $chirp->user->name }}'s avatar" class="rounded-full" />
                    </div>
                </div>
            @else
                <div class="avatar placeholder">
                    <div class="size-10 rounded-full">
                        <img src="<https://avatars.laravel.cloud/f61123d5-0b27-434c-a4ae-c653c7fc9ed6?vibe=stealth>"
                            alt="Anonymous User" class="rounded-full" />
                    </div>
                </div>
            @endif

            <div class="min-w-0 flex-1">
                <div class="flex justify-between w-full">
                    <div class="flex items-center gap-1">
                        <span class="text-sm font-semibold">{{ $chirp->user ? $chirp->user->name : 'Anonymous' }}</span>
                        <span class="text-base-content/60">·</span>
                        <span class="text-sm text-base-content/60">{{ $chirp->created_at->diffForHumans() }}</span>
                    </div>

                    <div class="flex gap-1">
                        <a href="/chirps/{{ $chirp->id }}/edit" class="btn btn-ghost btn-xs">
                            Edit
                        </a>
                        <form method="POST" action="/chirps/{{ $chirp->id }}">
                            @csrf
                            @method('DELETE')
                            <button type="submit"
                                onclick="return confirm('Are you sure you want to delete this chirp?')"
                                class="btn btn-ghost btn-xs text-error">
                                Delete
                            </button>
                        </form>
                    </div>
                </div>
                <p class="mt-1">{{ $chirp->message }}</p>
            </div>
        </div>
    </div>
</div>
```

Notice a few important things here:

- **Edit button**: We're passing in the chirp ID. We want to target a particular, singular chirp, and this is a way to do that within Blade. The route looks like `/chirps/{chirp_id}/edit`.
- **Delete form**: We have another form with `@csrf` and `@method('DELETE')`. This is necessary because HTML forms don't have a standard method of delete, so Laravel gives us this handy directive.
- **Confirmation**: Notice that "onclick" on the delete button—it pops up with a browser modal asking "Are you sure you want to delete this chirp?" Just a neat little touch!

This might seem a little bit complicated, but bear with me. Most of everything we're going to look at when it comes to editing and deleting means that we have to do it within a single instance of a chirp. That's why we have this chirp ID inputted into these routes—because we need to find which chirp we need to edit and which chirp we need to delete.

## Step 2: Add Routes

In our web routes, we can just continue to add those route parameters. Let's add routes for edit, update, and delete:

```php
use App\Http\Controllers\ChirpController;

Route::get('/', [ChirpController::class, 'index']);
Route::post('/chirps', [ChirpController::class, 'store']);
Route::get('/chirps/{chirp}/edit', [ChirpController::class, 'edit']);
Route::put('/chirps/{chirp}', [ChirpController::class, 'update']);
Route::delete('/chirps/{chirp}', [ChirpController::class, 'destroy']);
```

Notice those curly brackets with `{chirp}`? This is what we call **route model binding**. We know that we need to get an instance of a chirp, so this just gives Laravel an easy way of saying "Hey, within this route we need to look for something that we can identify as a chirp."

Now, Laravel does have a shorthand so that you don't have to do all of this. We're doing things a little bit differently just because we have a `GET` in the root directory and not a `GET` of `/chirps`. But what we could do is something like this:

```php
Route::get('/', [ChirpController::class, 'index']);

Route::resource('chirps', ChirpController::class)
    ->only(['store', 'edit', 'update', 'destroy']);
```

This resource route is identical to the four routes we wrote out explicitly above—just an easier way of putting it. For right now, I'm going to be extremely explicit so you can see exactly what's happening.

## Step 3: Create the Edit View

Now let's create the edit view that we will need because we are getting a new route `/chirps/{chirp}/edit`. In our views directory, since we don't actually have a directory for chirps (because our chirp index is technically the index of our whole application), I'm going to create one: `chirps`, and then in that chirps directory, we're going to have `edit.blade.php`.

Create a new file `resources/views/chirps/edit.blade.php`:

```html
<x-layout>
    <x-slot:title>
        Edit Chirp
    </x-slot:title>

    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold mt-8">Edit Chirp</h1>

        <div class="card bg-base-100 shadow mt-8">
            <div class="card-body">
                <form method="POST" action="/chirps/{{ $chirp->id }}">
                    @csrf
                    @method('PUT')

                    <div class="form-control w-full">
                        <textarea
                            name="message"
                            class="textarea textarea-bordered w-full resize-none @error('message') textarea-error @enderror"
                            rows="4"
                            maxlength="255"
                            required
                        >{{ old('message', $chirp->message) }}</textarea>

                        @error('message')
                            <div class="label">
                                <span class="label-text-alt text-error">{{ $message }}</span>
                            </div>
                        @enderror
                    </div>

                    <div class="card-actions justify-between mt-4">
                        <a href="/" class="btn btn-ghost btn-sm">
                            Cancel
                        </a>
                        <button type="submit" class="btn btn-primary btn-sm">
                            Update Chirp
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</x-layout>
```

This is the same layout that we're using throughout our application. The majority of this form is exactly the same as our home.blade.php, just with different buttons and a different form action. This form is using the PUT method for the `/chirps/{id}` action, which goes to our update method in the web routes.

Notice this textarea needs to have the chirp that we need to edit, right? We're passing in the old message (`{{ old('message', $chirp->message) }}`) so that when we are directed to this edit page, we see the actual chirp message that exists within this chirp instance from the get-go.

## Step 4: Implement Controller Methods

Now let's hook this up to our ChirpController. We need to add these methods. This edit method is showing the form for editing the specified resource. In a resource controller for a standard MVC Laravel application, this is just best practice.

```php
public function edit(Chirp $chirp)
{
    // We'll add authorization in lesson 11
    return view('chirps.edit', compact('chirp'));
}

public function update(Request $request, Chirp $chirp)
{
    // Validate
    $validated = $request->validate([
        'message' => 'required|string|max:255',
    ]);

    // Update
    $chirp->update($validated);

    return redirect('/')->with('success', 'Chirp updated!');
}

public function destroy(Chirp $chirp)
{
    $chirp->delete();

    return redirect('/')->with('success', 'Chirp deleted!');
}
```

Let me explain what's happening here:

**Edit Method**: Instead of using a string ID to find the existing chirp based off of maybe an ID, we can use route model binding. Because we know that the `{chirp}` parameter in our web routes is associated with the Chirp model, Laravel automatically assumes what chirp this is based off of that ID. We use the `compact` method to pass everything from this chirp into the view.

**Update Method**: This is similar to our store method where we need to validate something first and then update the chirp. We grab the chirp and update it with the validated info.

**Destroy Method**: We just delete the chirp and redirect back with a success message.

## Step 5: A Note About Authorization

You might notice a few things when you test this out. Like we can edit anyone's chirp. Well, that's not necessarily good. And we'll fix that when authentication comes into play in the next couple of lessons.

> Important: Right now, anyone can edit or delete any chirp. This isn't secure! In lesson 11, we'll add authentication so users can only edit and delete their own chirps. For now, we're focusing on getting the basic functionality working.

## Step 6: Laravel Policies (Preview)

I do want to give a sneak peek on what this will look like when we do implement authorization and authentication. When a user is logged in, how do we know that they're able to edit and delete their own chirps?

Laravel has a clean way to put all the authorization code we might need with something called Policies. Here's a preview:

```bash
php artisan make:policy ChirpPolicy --model=Chirp
```

In `app/Policies/ChirpPolicy.php`:

```php
public function update(User $user, Chirp $chirp): bool
{
    return $chirp->user()->is($user);
}

public function delete(User $user, Chirp $chirp): bool
{
    return $chirp->user()->is($user);
}
```

Then in your controller:

```php
public function update(Request $request, Chirp $chirp)
{
    if ($request->user()->cannot('update', $chirp)) {
        abort(403);
    }
    // ... rest of method
}
```

Or even simpler, we can use the authorize method:

```php
public function update(Request $request, Chirp $chirp)
{
    $this->authorize('update', $chirp);
    // ... rest of method
}
```

This `$this->authorize()` method will check: does this user have the authorization to delete this particular chirp? And in our ChirpPolicy, instead of returning false or true, we can just check if the chirp user is the user making the request: `$chirp->user->is($user)`.

We can't put this in the controller just yet because we don't have authentication set up, but once we do, then we can add that back in!

We'll use this pattern once we add proper authentication!

## Step 7: Add Edit Indication

Lastly, before we move on from this lesson, I want to change how something is shown when something is updated. If I edit a chirp, we don't know that this was actually edited. We don't know what the original was. It'd be nice to know that this was updated and not just posted some time ago.

Most social media platforms have this feature, so we might as well get ahead of it! Let's show when a chirp has been edited. Laravel automatically tracks both `created_at` and `updated_at` timestamps, so we can compare them to see if a chirp has been modified.

Update the chirp component (`resources/views/components/chirp.blade.php`) to show the edited indicator:

```html
<div class="flex items-center gap-1">
     <span class="text-sm font-semibold">{{ $chirp->user ? $chirp->user->name : 'Anonymous' }}</span>
     <span class="text-base-content/60">·</span>
     <span class="text-sm text-base-content/60">{{ $chirp->created_at->diffForHumans() }}</span>
    @if ($chirp->updated_at->gt($chirp->created_at->addSeconds(5)))
        <span class="text-base-content/60">·</span>
        <span class="text-sm text-base-content/60 italic">edited</span>
    @endif
</div>
```

If the chirp has been updated at, and if that updated\_at is different than when the chirp was created\_at by at least 5 seconds, then we'll show this little "edited" text. This checks if the `updated_at` timestamp is more than 5 seconds after `created_at` (to account for any small delays during creation).

When a chirp is edited, Laravel automatically updates the `updated_at` timestamp, and our component will show "edited" next to the timestamp. No database changes needed—Laravel's timestamps handle everything for us!

## What We've Built

Things are really coming along! Your Chirper app now has full CRUD functionality:

- **Create** - Users can post new chirps
- **Read** - Display chirps in a feed
- **Update** - Edit existing chirps with an edit form
- **Delete** - Remove chirps with confirmation
- **Edit indication** - Shows when chirps have been modified

We have a nice edit page that automatically knows what information to bring in thanks to route model binding. We can edit and delete chirps (though right now anyone can edit anyone's chirps, which we'll fix with authentication).

In the next lessons, we'll add proper authentication so users can actually register, log in, and manage their own chirps securely. We'll allow our users to register and create accounts, and you'll see how easy this can be even without a starter kit.

Ready to make this a real multi-user application? Let's add authentication!
