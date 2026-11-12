# Laravel Learn - Getting Started with Laravel: Creating and storing Chirps

Source: https://laravel.com/learn/getting-started-with-laravel/creating-and-storing-chirps

---

Build forms to let users create content and store it in the database. Learn about Laravel's form handling, validation, and mass assignment protection.

Our Chirper application is showing chirps that we have stored in the database, but we still don't have a way for our users to actually create their own chirps and store them in the database. A social network where you can only read? That's just a newspaper!

So that's what we're going to do in this lesson. We're going to build a form, handle the validation with that form, and store those chirps that users create in the database—all with the things that are built into Laravel. We're still saving the actual user authentication for a later lesson, but we are going to allow our users as anonymous users to create those chirps.

## Step 1: Add a Create Form

Why don't we add the form at the top of our feed and we can get going from there. We really just want a form right after the "Latest Chirps" header, and before we actually list the chirps.

Let's update `home.blade.php`:

```html
<x-layout>
    <x-slot:title>
        Home Feed
    </x-slot:title>

    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold mt-8">Latest Chirps</h1>

        <!-- Chirp Form -->
        <div class="card bg-base-100 shadow mt-8">
            <div class="card-body">
                <form method="POST" action="/chirps">
                    @csrf
                    <div class="form-control w-full">
                        <textarea
                            name="message"
                            placeholder="What's on your mind?"
                            class="textarea textarea-bordered w-full resize-none"
                            rows="4"
                            maxlength="255"
                            required
                        ></textarea>
                    </div>

                    <div class="mt-4 flex items-center justify-end">
                        <button type="submit" class="btn btn-primary btn-sm">
                            Chirp
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Feed -->
        <div class="space-y-4 mt-8">
            @forelse ($chirps as $chirp)
                <x-chirp :chirp="$chirp" />
            @empty
                <div class="hero py-12">
                    <div class="hero-content text-center">
                        <div>
                            <svg class="mx-auto h-12 w-12 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                            </svg>
                            <p class="mt-4 text-base-content/60">No chirps yet. Be the first to chirp!</p>
                        </div>
                    </div>
                </div>
            @endforelse
        </div>
    </div>
</x-layout>
```

There's nothing too special about this form right now—just one textarea and a button. But notice a couple of important things:

- `@csrf` - Laravel's CSRF protection (prevents cross-site request forgery)
- POST to `/chirps` route (which we'll create next)

If you tried to submit this form right now, nothing would actually happen because we haven't hooked it up on the Laravel side yet.

## Step 2: Add the Store Route

So let's hook this up! In `routes/web.php`, add a route to handle form submission:

```php
use App\Http\Controllers\ChirpController;

Route::get('/', [ChirpController::class, 'index']);
Route::post('/chirps', [ChirpController::class, 'store']);
```

## Step 3: Create the Store Method

First, I want to create the method that we're going to be submitting this form to in our controller. Let's go to our `ChirpController` and add the store method. This store method is perfect for this because we're creating a resource (in this case, a chirp), and this is what the store method is intended for in a resource controller.

```php
public function store(Request $request)
{
    // Validate the request
    $validated = $request->validate([
        'message' => 'required|string|max:255',
    ]);

    // Create the chirp (no user for now - we'll add auth later)
    \App\Models\Chirp::create([
        'message' => $validated['message'],
        'user_id' => null, // We'll add authentication in lesson 11
    ]);

    // Redirect back to the feed
    return redirect('/')->with('success', 'Chirp created!');
}
```

Let me break this down:

1. **Validation**: We're validating the request and storing it in the `$validated` parameter. We're saying the message that we're receiving from this request is required, should be a string, and have a max of 255 characters. Notice we now have two places where this max is indicated—our validation as well as in the database itself.
2. **Creation**: We're using the Chirp model to create this with a message from the validated data and a user\_id of null (for now).
3. **Redirect**: We're returning a redirect back to the homepage with a specific success message. In Laravel, this `with` function returns with a flash of data to the session—so after we redirect back, that initial load flashes a piece of data to the session with this success message.

> Note: We're creating chirps without a user for now to keep things simple. In lesson 11, we'll add proper authentication so each chirp belongs to the logged-in user!

## Step 4: Show Success Messages

Now, how can we grab this flash session information and display it to our user? In our app.css, we added that `animate-fade-out` parameter earlier—this is going to make things a lot easier when we create a notification component for any success messages.

We're not going to put this success message in our home.blade.php. Instead, we're going to put it in the layout so it can be used everywhere. Add this to your layout component (`resources/views/components/layout.blade.php`) right after the `</nav>`:

```html
<!-- Success Toast -->
@if (session('success'))
    <div class="toast toast-top toast-center">
        <div class="alert alert-success animate-fade-out">
            <svg xmlns="<http://www.w3.org/2000/svg>" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ session('success') }}</span>
        </div>
    </div>
@endif
```

In this case, if the session has a parameter of 'success', we're going to show a toast. The toast is using DaisyUI classes, but we also have that animate-fade-out class that we added to our app.css. This is saying we're just going to take that session value, the success message, regardless of if this is from posting a chirp or if we use this for logging in and registering later.

The toast will appear at the top center and automatically fade away after a few seconds!

## Step 5: Display Validation Errors

Now let's test this out! But first, what if someone tries to submit an empty chirp? We have client-side validation with that `required` attribute, but we also have server-side validation in our chirp controller. Let's make sure we can show validation errors properly.

Laravel gives us an `errors` variable that gets passed to the view if there are any errors within the session. Let's update the form section in `home.blade.php` to handle this:

```html
<!-- Chirp Form -->
<div class="card bg-base-100 shadow mt-8">
    <div class="card-body">
        <form method="POST" action="/chirps">
            @csrf
            <div class="form-control w-full">
                <textarea
                    name="message"
                    placeholder="What's on your mind?"
                    class="textarea textarea-bordered w-full resize-none @error('message') textarea-error @enderror"
                    rows="4"
                    maxlength="255"
                    required
                >{{ old('message') }}</textarea>

                @error('message')
                    <div class="label">
                        <span class="label-text-alt text-error">{{ $message }}</span>
                    </div>
                @enderror
            </div>

            <div class="mt-4 flex items-center justify-end">
                <button type="submit" class="btn btn-primary btn-sm">
                    Chirp
                </button>
            </div>
        </form>
    </div>
</div>
```

Notice a few things here:

- If there is an error with the message parameter (that's what we're validating in the controller), we add the `textarea-error` class
- We use `@error('message')` to show the error message
- DaisyUI gives us the ability to have the textarea show as an error state with that CSS class
- We use `{{ old('message') }}` so when we flash back after an error, the textarea displays the old input so the user doesn't have to retype everything

Laravel's validation automatically:

- Redirects back on error
- Provides error messages via `@error`
- Preserves old input with `old('message')`

## Step 6: Better Validation Messages

Now, to add just a little bit of UI nicety, let's customize our validation messages to be more "chirpy" and user-friendly. To show off the power of Laravel, we can actually customize these validation messages easily:

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'message' => 'required|string|max:255',
    ], [
        'message.required' => 'Please write something to chirp!',
        'message.max' => 'Chirps must be 255 characters or less.',
    ]);

    \App\Models\Chirp::create([
        'message' => $validated['message'],
        'user_id' => null,
    ]);

    return redirect('/')->with('success', 'Your chirp has been posted!');
}
```

Now all of a sudden, within a couple of seconds, because of what Laravel gives to us, we have the ability to modify something as simple as error messages without having to do hardly anything!

## Step 7: Test It Out!

Let's test our form:

1. **Try submitting an empty form** - You'll see our custom validation error: "Please write something to chirp!"
2. **Type more than 255 characters** - The client-side `maxlength` attribute prevents it, but if someone bypassed that, our server-side validation would catch it with "Chirps must be 255 characters or less."
3. **Submit a valid chirp** - You'll see the success message and your new chirp at the top of the feed!

Because we are redirecting, we automatically receive that new chirp because the `/` route is automatically getting all of the latest chirps and pushing them into our view.

## Security Features We Get for Free

Laravel automatically protects you from:

- **CSRF attacks** - That `@csrf` token ensures forms come from your site
- **SQL injection** - Eloquent parameterizes all queries
- **Mass assignment** - Only fields in `$fillable` can be set
- **XSS attacks** - Blade `{{ }}` automatically escapes output

## What About Rate Limiting?

Now, it is helpful to know that while we won't touch on it in this particular course, there's so much more that you could add here. What if you don't want your users to post five times within a second, or maybe a hundred times within a second? There are some bad eggs out there—really, you can't trust anyone on the web.

Well, Laravel has the ability to rate limit. What that means is that you can, within a matter of minutes, say "Hey, this particular chirp method can only be done by a user maybe one time every 60 seconds."

You could also prevent duplicate chirps if you wanted:

```php
$validated = $request->validate([
    'message' => [
        'required',
        'string',
        'max:255',
        Rule::unique('chirps')->where(function ($query) use ($user) {
            return $query->where('user_id', $user->id);
        })
    ],
]);
```

This would ensure each user's chirps are unique. But before we get into something like that...

## What We've Accomplished

Look at what we've built! Your app can now:

- Accept user input through a beautiful form
- Validate that input on both client and server side
- Store chirps in the database
- Show custom success and error messages with nice toasts
- Protect against common security threats automatically
- Redirect users back with flash messages

We have this form and it works! We're submitting anonymous data for now, but the validation works perfectly. Laravel automatically gives us both client-side validation and server-side validation.

But users can only create chirps—they can't edit or delete them yet. In the next lesson, we'll start working on editing and deleting chirps, even before we get to the user authentication piece. Let's check out how you can edit and delete chirps!
