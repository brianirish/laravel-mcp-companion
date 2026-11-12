# Laravel Learn - Getting Started with Laravel: Basic authentication: Registration

Source: https://laravel.com/learn/getting-started-with-laravel/basic-authentication-registration

---

Build user registration from scratch to understand authentication fundamentals. Create registration forms, hash passwords, and automatically log in new users.

We're finally going to make use of the Sign In and Sign Up buttons! Well, first the Sign Up button in this lesson.

We've been pretending that we can edit or delete any chirp that's added, and right now, anytime we add a new one, it's just an anonymous person creating this chirp. Time to change that!

Laravel offers complete authentication scaffolding with Laravel Starter Kits, but it's also helpful to know how to manually build it first to understand how things work under the hood. So let's start with user registration and learn what's happening behind the scenes.

## Step 1: Create the Registration Form

Let's start by creating a new page. We have our chirps directory where we have our edit page, so it makes sense to create a new directory that is an auth directory. So let's create `auth` and then we'll have `register.blade.php`.

Create a new file at `resources/views/auth/register.blade.php`:

```html
<x-layout>
    <x-slot:title>
        Register
    </x-slot:title>

    <div class="hero min-h-[calc(100vh-16rem)]">
        <div class="hero-content flex-col">
            <div class="card w-96 bg-base-100">
                <div class="card-body">
                    <h1 class="text-3xl font-bold text-center mb-6">Create Account</h1>

                    <form method="POST" action="/register">
                        @csrf

                        <!-- Name -->
                        <label class="floating-label mb-6">
                            <input type="text"
                                   name="name"
                                   placeholder="John Doe"
                                   value="{{ old('name') }}"
                                   class="input input-bordered @error('name') input-error @enderror"
                                   required>
                            <span>Name</span>
                        </label>
                        @error('name')
                            <div class="label -mt-4 mb-2">
                                <span class="label-text-alt text-error">{{ $message }}</span>
                            </div>
                        @enderror

                        <!-- Email -->
                        <label class="floating-label mb-6">
                            <input type="email"
                                   name="email"
                                   placeholder="[mail@example.com](<mailto:mail@example.com>)"
                                   value="{{ old('email') }}"
                                   class="input input-bordered @error('email') input-error @enderror"
                                   required>
                            <span>Email</span>
                        </label>
                        @error('email')
                            <div class="label -mt-4 mb-2">
                                <span class="label-text-alt text-error">{{ $message }}</span>
                            </div>
                        @enderror

                        <!-- Password -->
                        <label class="floating-label mb-6">
                            <input type="password"
                                   name="password"
                                   placeholder="••••••••"
                                   class="input input-bordered @error('password') input-error @enderror"
                                   required>
                            <span>Password</span>
                        </label>
                        @error('password')
                            <div class="label -mt-4 mb-2">
                                <span class="label-text-alt text-error">{{ $message }}</span>
                            </div>
                        @enderror

                        <!-- Password Confirmation -->
                        <label class="floating-label mb-6">
                            <input type="password"
                                   name="password_confirmation"
                                   placeholder="••••••••"
                                   class="input input-bordered"
                                   required>
                            <span>Confirm Password</span>
                        </label>

                        <!-- Submit Button -->
                        <div class="form-control mt-8">
                            <button type="submit" class="btn btn-primary btn-sm w-full">
                                Register
                            </button>
                        </div>
                    </form>

                    <div class="divider">OR</div>
                    <p class="text-center text-sm">
                        Already have an account?
                        <a href="/login" class="link link-primary">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</x-layout>
```

The majority of things we're seeing here are not new. We've seen them throughout our time together. We have a slot where we're saying this is the register page. We're using a layout. We're using a bunch of different forms. We're gathering any errors that we might have. We're showing those error messages, and then we're using old inputs if we have any errors. So again, not much new here!

## Step 2: Create the Registration Controller

We could create a new authentication controller, but what we're going to do is kind of split this up into different controllers. We're going to go against the grain just a little bit here.

Laravel recommends using single action controllers (invokable controllers) for actions that don't fit the standard resource pattern. Let's create a dedicated controller for registration:

```bash
php artisan make:controller Auth/Register --invokable
```

This creates a single action controller in the auth namespace: `/Http/Controllers/Auth/Register.php`. What this looks like is a single class, an invokable controller, which just means that usually you only have one method per controller. Instead of having a resource controller that has multiple (seven different) methods.

This is really personal preference, but I wanted to show two different ways that you might do it. Everything that we're doing within auth, we're going to have invokable controllers instead of one massive authentication controller that has weird method names.

This creates a single action controller in `app/Http/Controllers/Auth/Register.php`:

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class Register extends Controller
{
    public function __invoke(Request $request)
    {
        // Validate the input
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        // Create the user
        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        // Log them in
        Auth::login($user);

        // Redirect to home
        return redirect('/')->with('success', 'Welcome to Chirper!');
    }
}
```

We just pretend that this `__invoke` is whatever method we normally would use in our ChirpController, for example. But this is just our register auth controller, and when we call it, it's going to use this invokable function.

Here's what's happening (almost identical to any other method or form that we've done):

1. **Validate the input** - We get the name, email, and password. We're making sure the password is confirmed (that's what the `password_confirmation` field is for).
2. **Create the user** - With a hash of that particular password.
3. **Log them in** - Using the Auth facade helper method to log in the user we just created.
4. **Redirect** - To home with a success status.

It looks like this shouldn't be as easy as it is, right? But it is mostly because of the helper methods that Laravel provides—not just the authentication helper method to log in the user, but also things like Hash to make passwords secure. And because we already have a User model given to us out of the box within Laravel, this becomes incredibly easy to get authentication up and running.

## Step 3: Add Routes

Let's add this to our web routes. In `routes/web.php`, add the registration routes:

```php
use App\Http\Controllers\Auth\Register;

// Registration routes
Route::view('/register', 'auth.register')
    ->middleware('guest')
    ->name('register');

Route::post('/register', Register::class)
    ->middleware('guest');
```

There's something I want to add right now. I want to make sure that these routes should be able to be accessed by anyone, even if they're not logged in. This is where middleware comes into play, and Laravel has middleware built out of the box for us. In this case, for the register route, I want to make sure that this is accessible by guests.

I also want to show what a named route looks like. We can pass in a name, and I'm going to call this the register route. We can do the same thing with our POST method as well.

Note: Since we're just showing a view for the GET route, we use `Route::view()` directly. For the POST route, we pass the invokable controller class.

The `guest` middleware ensures only non-authenticated users can access these routes. This name helps us—instead of knowing that it is the `/register` page, maybe we change this to `/new` for some reason. Well, then we automatically know that it's still under the named route of register.

## Step 4: Update the Navigation

We can actually update the navigation instead of that `href="/register"` to use a named route. But I also want to update this because when we're logged in, we shouldn't show the Sign In and Sign Up page. That's where the `@auth` directive comes in.

Let's update our layout to show the current user. In `resources/views/components/layout.blade.php`, update the navbar-end section:

```html
<div class="navbar-end gap-2">
    @auth
        <span class="text-sm">{{ auth()->user()->name }}</span>
        <form method="POST" action="/logout" class="inline">
            @csrf
            <button type="submit" class="btn btn-ghost btn-sm">Logout</button>
        </form>
    @else
        <a href="/login" class="btn btn-ghost btn-sm">Sign In</a>
        <a href="{{ route('register') }}" class="btn btn-primary btn-sm">Sign Up</a>
    @endauth
</div>
```

Instead of the Sign In and Sign Up buttons, we can say: if someone is authenticated into the application, then we're going to show the authenticated user's name and a logout button (we'll set this up in a bit). Otherwise, let's show the buttons like we had them previously.

## Step 5: Protect Routes

So just so we aren't stuck without being able to test, let's go ahead and protect the rest of our routes and update our controllers to use our user now. We can actually group routes with middleware.

Now let's make sure only authenticated users can create chirps. Update your routes:

```php
Route::get('/', [ChirpController::class, 'index']);

// Protected routes
Route::middleware('auth')->group(function () {
    Route::post('/chirps', [ChirpController::class, 'store']);
    Route::get('/chirps/{chirp}/edit', [ChirpController::class, 'edit']);
    Route::put('/chirps/{chirp}', [ChirpController::class, 'update']);
    Route::delete('/chirps/{chirp}', [ChirpController::class, 'destroy']);
});
```

Now everything that we see here is under the `auth` middleware. So I can't send a new chirp now unless I am authenticated. What does this look like? Well, if I try to send a chirp and I'm not logged in, Laravel gives you something out of the box that—because it knows you're not authenticated—it's going to try to authenticate you by redirecting to the login route.

## Step 6: Update ChirpController

Let's go ahead and update our ChirpController because now we're not just creating a new chirp—we're actually creating a new chirp with our users. Now we can use the real authenticated user! Update your controller methods:

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'message' => 'required|string|max:255',
    ]);

    // Use the authenticated user
    auth()->user()->chirps()->create($validated);

    return redirect('/')->with('success', 'Your chirp has been posted!');
}

public function edit(Chirp $chirp)
{
    $this->authorize('update', $chirp);

    return view('chirps.edit', compact('chirp'));
}

public function update(Request $request, Chirp $chirp)
{
    $this->authorize('update', $chirp);

    $validated = $request->validate([
        'message' => 'required|string|max:255',
    ]);

    $chirp->update($validated);

    return redirect('/')->with('success', 'Chirp updated!');
}

public function destroy(Chirp $chirp)
{
    $this->authorize('delete', $chirp);

    $chirp->delete();

    return redirect('/')->with('success', 'Chirp deleted!');
}
```

We're using the `auth()` helper and we can say that the user of this auth helper, we want to get their chirps, but we want to create them. We can actually create them with that validated parameter.

Since we set up that policy to authorize a user to update a particular chirp, we can add that here. This `$this->authorize()` method will check if they are authorized to update the chirp, then let's continue. We'll need the controller to have the `AuthorizesRequests` trait that it can use.

## Step 7: Update Chirp Component

Now we still see these edit and delete buttons when we're not logged in, but we've started to authorize if someone is able to edit or delete. How can we only show these edit and delete buttons when we are able to edit and delete them?

Instead of checking if the auth check exists and if the auth ID is equal to the chirp user ID, there's an easier way to do this. We just need to check that policy that we created. Can they update or can they delete a chirp?

Update the chirp component to use proper authentication. In `resources/views/components/chirp.blade.php`, replace the temporary auth check:

```html
@can('update', $chirp)
    <div class="flex gap-1">
        <a href="/chirps/{{ $chirp->id }}/edit" class="btn btn-ghost btn-xs"> Edit </a>
        <form method="POST" action="/chirps/{{ $chirp->id }}"> @csrf @method('DELETE') <button
                type="submit" onclick="return confirm('Are you sure you want to delete this chirp?')"
                class="btn btn-ghost btn-xs text-error"> Delete </button>
        </form>
    </div>
@endcan
```

We can use the Blade directive `@can` to check if they can update the chirp (in this case, the chirp that we're passing in), and then the `@endcan` directive. In this case, if I can't edit any of these chirps and I can't delete any of them because I'm not logged in, the buttons won't show. But if I sign up and create a new account, after I create a chirp I can actually edit and delete them.

## Step 8: Form Protection

While the chirp form is visible to everyone on the home page, the POST route to `/chirps` is protected by the `auth` middleware. This means:

- Guests can see the form but will be redirected to login if they try to submit
- Only authenticated users can successfully post chirps
- The middleware protection ensures security even if the form is visible

This approach lets visitors see what they could do if they sign up, encouraging registration.

## Understanding Laravel's Auth

Behind the scenes, Laravel:

- **Hashes passwords** using bcrypt (never store plain text!)
- **Creates a session** when users log in
- **Sets a cookie** to remember the session
- **Provides the** `auth()` **helper** to access the current user
- **Offers middleware** to protect routes

## Test Your Registration

Let's test this out!

1. Visit `/register`
2. Fill out the form with your name, email, and password
3. Submit it
4. You should be logged in and redirected to the home page with a "Welcome to Chirper!" message
5. Try creating a chirp—it now belongs to you and you can see your avatar!

You now have your user avatar associated with you because you're logged in, and you can see the edit and delete methods available for your own chirps.

## What About Email Verification?

Laravel makes email verification easy too! You'd just:

1. Implement `MustVerifyEmail` on your User model
2. Add the `verified` middleware to protected routes
3. Laravel handles sending verification emails

We'll skip this for now, but it's there when you need it!

## Next Up

Hopefully this shows you that authentication doesn't have to be too scary. Authentication within Laravel is actually incredibly easy because of the tools that it provides. While yes, it's great that you can just grab a starter kit from Laravel and you have authentication out of the box, you don't necessarily need to use it every single time.

That being said, starter kits are great because they have a lot that we're not going to even touch within Chirper, such as password reset pages.

But registration works great, and users need to log back in! In the next lesson, we'll add login and logout functionality to complete our authentication system. Almost there!
