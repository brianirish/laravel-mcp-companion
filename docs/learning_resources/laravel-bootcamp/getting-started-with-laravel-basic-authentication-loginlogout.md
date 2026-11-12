# Laravel Learn - Getting Started with Laravel: Basic authentication: Login/Logout

Source: https://laravel.com/learn/getting-started-with-laravel/basic-authentication-loginlogout

---

Complete the authentication system with login and logout functionality. Learn about sessions, middleware, and protecting routes from unauthorized access.

I've created at least two accounts now, mostly because I don't have a sign-in page just yet. So let's fix that—we're almost done!

Users can register, but what happens when they come back tomorrow? They need to log in! Let's complete our authentication system with login and logout functionality. This is the final piece to make Chirper a real multi-user application.

## Step 1: Create the Login Form

Let's make it so we don't see that 404 Not Found error again when we try to visit the login page.

In our resources/views, we have the auth directory for register. I'm going to create a new file for `login.blade.php`. We can start with the register page itself and just make changes, or you can just paste in what's in the lesson. There's nothing too crazy here—it's exactly what the register page is, just with fewer fields and directing to a login method.

Create `resources/views/auth/login.blade.php`:

```html
<x-layout>
    <x-slot:title>
        Sign In
    </x-slot:title>

    <div class="hero min-h-[calc(100vh-16rem)]">
        <div class="hero-content flex-col">
            <div class="card w-96 bg-base-100">
                <div class="card-body">
                    <h1 class="text-3xl font-bold text-center mb-6">Welcome Back</h1>

                    <form method="POST" action="/login">
                        @csrf

                        <!-- Email -->
                        <label class="floating-label mb-6">
                            <input type="email"
                                   name="email"
                                   placeholder="[mail@example.com](<mailto:mail@example.com>)"
                                   value="{{ old('email') }}"
                                   class="input input-bordered @error('email') input-error @enderror"
                                   required
                                   autofocus>
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

                        <!-- Remember Me -->
                        <div class="form-control mt-4">
                            <label class="label cursor-pointer justify-start">
                                <input type="checkbox"
                                       name="remember"
                                       class="checkbox">
                                <span class="label-text ml-2">Remember me</span>
                            </label>
                        </div>

                        <!-- Submit Button -->
                        <div class="form-control mt-8">
                            <button type="submit" class="btn btn-primary btn-sm w-full">
                                Sign In
                            </button>
                        </div>
                    </form>

                    <div class="divider">OR</div>
                    <p class="text-center text-sm">
                        Don't have an account?
                        <a href="/register" class="link link-primary">Register</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</x-layout>
```

You can start to tell how a lot of this is repeatable in the sense of once you get the hang of what a form looks like, especially if it's a form that has similar fields, the next time you implement that form, it's going to be a lot easier. And Laravel just makes it easier too.

## Step 2: Create Login and Logout Controllers

We created an `Auth/Logout` class already in the previous lesson for demonstration. Now we just need our `Auth/Login`. Following Laravel's single action controller pattern, let's create separate controllers for login and logout:

```bash
php artisan make:controller Auth/Login --invokable
php artisan make:controller Auth/Logout --invokable
```

If we go to our Login auth controller, this is our invokable single-class controller. This is going to be one of the few controllers that's a little bit different, but only slightly. We're going to pull in that Auth facade.

In `app/Http/Controllers/Auth/Login.php`:

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class Login extends Controller
{
    public function __invoke(Request $request)
    {
        // Validate the input
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        // Attempt to log in
        if (Auth::attempt($credentials, $request->boolean('remember'))) {
            // Regenerate session for security
            $request->session()->regenerate();

            // Redirect to intended page or home
            return redirect()->intended('/')->with('success', 'Welcome back!');
        }

        // If login fails, redirect back with error
        return back()
            ->withErrors(['email' => 'The provided credentials do not match our records.'])
            ->onlyInput('email');
    }
}
```

What this Auth facade is doing is we're using the `attempt` helper with this facade. We're taking the credentials that we've been given (this email and password), we're attaching the Remember checkbox if they gave that, and we're requesting a new session—we're regenerating that new session.

This `attempt` helper automatically has that remember variable. If it's false, it's false by default. Otherwise, if we pass that in, then it's true. This is doing all the heavy lifting for us.

Then we'll return back. Otherwise, if the auth attempt fails for whatever reason, then we're going to return back with errors. This is a neat little return helper to say, "Hey, we're returning to the previous page, regardless of where that was."

In `app/Http/Controllers/Auth/Logout.php`:

```php
<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class Logout extends Controller
{
    public function __invoke(Request $request)
    {
        Auth::logout();

        // Invalidate session
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/')->with('success', 'You have been logged out.');
    }
}
```

And seeing that we're requesting this session to be regenerated, it reminded me that I think we want to invalidate the session as well in the logout controller. So instead of just logging out this user, we can actually simplify this with `Auth::logout()` because we already know the authenticated user. Then we can say we need the request session and we're going to invalidate that, as well as regenerate a new token, so that way the user who is then not logged in still has a fresh token.

## Step 3: Add Login/Logout Routes

Let's go ahead and add this login route to our web routes. In `routes/web.php`:

```php
use App\Http\Controllers\Auth\Login;
use App\Http\Controllers\Auth\Logout;

// Login routes
Route::view('/login', 'auth.login')
    ->middleware('guest')
    ->name('login');

Route::post('/login', Login::class)
    ->middleware('guest');

// Logout route
Route::post('/logout', Logout::class)
    ->middleware('auth')
    ->name('logout');
```

We want this to be a named route because we are using named routes. What we do need is the `Route::view()` to be able to pass in the `/login` page to the login view. And this is where we can have the middleware of guest and the named login route.

Why don't we name the logout as well, even though I don't think we're using it anywhere, but it's also helpful just in case we wanted to use it.

Note: Laravel automatically redirects to `/login` when an unauthenticated user tries to access a protected route. That's why we name it `login`.

## Step 4: Update Chirp Component for Auth

Now we have this login page, and we should be able to log in with our previous email that we created. The logout button should work even with the named route.

If you haven't already, let's make sure we update `resources/views/components/chirp.blade.php` to properly check ownership so that way we know if the user `can` or cannot update or delete a chirp:

```html
@props(['chirp'])

<div class="card bg-base-100 shadow">
    <div class="card-body">
        <div class="flex space-x-3">
            @if ($chirp->user)
                <div class="avatar">
                    <div class="size-10 rounded-full">
                        <img src="https://avatars.laravel.cloud/{{ urlencode($chirp->user->email) }}"
                            alt="{{ $chirp->user->name }}'s avatar" class="rounded-full" />
                    </div>
                </div>
            @else
                <div class="avatar placeholder">
                    <div class="size-10 rounded-full">
                        <img src="https://avatars.laravel.cloud/f61123d5-0b27-434c-a4ae-c653c7fc9ed6?vibe=stealth"
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
                        @if ($chirp->updated_at->gt($chirp->created_at->addSeconds(5)))
                            <span class="text-base-content/60">·</span>
                            <span class="text-sm text-base-content/60 italic">edited</span>
                        @endif
                    </div>

                    <!-- Replace the temporary @php block and $canEdit check with: -->
                    @can('update', $chirp)
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
                    @endcan
                </div>
                <p class="mt-1">{{ $chirp->message }}</p>
            </div>
        </div>
    </div>
</div>
```

This ensures that we only show the edit and delete buttons for chirps that the current user owns.

## Step 5: What is this "Remember Me" Functionality

Laravel's "Remember Me" feature:

- Creates a long-lived cookie
- Allows users to stay logged in between browser sessions
- Automatically re-authenticates users when they return

The `remember_token` column in the users table stores this securely.

## Testing the Complete Flow

Let's test the complete authentication flow:

1. **Logout** if you're logged in (click logout in the nav)
2. **Try to create a chirp** - you'll be redirected to login because of our middleware protection
3. **Log in** with your credentials
4. **Check "Remember me"** to stay logged in
5. **Create a chirp** - it works and shows your avatar!
6. **Close your browser** and come back - still logged in thanks to the remember token!

We are using the default authentication, the auth helper, and facade that Laravel gives, which includes remembering us and remembering that session.

## Security Features

Laravel automatically protects you from:

- **Session hijacking** - Sessions are regenerated on login
- **CSRF attacks** - All forms require CSRF tokens
- **Password exposure** - Passwords are hashed with bcrypt
- **Timing attacks** - Password comparison is constant-time
- **Session fixation** - Session IDs change after login

## What We've Built

Just to recap what we've accomplished: if we try to create a chirp, because we have middleware attached to any of the POST methods for creating a chirp, editing a chirp, or anything like that, we can't do it unless we're authenticated. It takes us directly to the login page. We can register a new account if we'd like, or log back in with existing credentials.

Congratulations! You now have a complete authentication system:

- ✅ User registration
- ✅ Login with "remember me" functionality
- ✅ Logout with session cleanup
- ✅ Protected routes with middleware
- ✅ User-specific content and permissions

Your Chirper app is now a real multi-user application where:

- Anyone can view the chirp feed
- Only registered users can create chirps
- Users can only edit/delete their own chirps
- Each chirp shows the user's avatar and name

We have the ability to add new chirps, and we can see that each chirp is attached to our particular user with our avatar. Logging out and signing in with a different email means that I cannot edit or delete chirps that another user created, but I can definitely edit and delete my own chirps. Full CRUD functionality!

## Quick Design Update

Thankfully, the Laravel team has a TON of incredible designers who can help us make this look a lot better with just a small handful of changes. Now, the majority of these changes are all done in the `app.css` file for simplicity sake. Typically, within a modern application that uses TailwindCSS, you would modify the markup (HTML) itself. However, since I want to have you change as little as possible within your application, we are doing some things that wouldn't be considered "best practice."

That being said, the benefit of modern CSS with Laravel by using something like TailwindCSS is that everything just works. After all, Blade template files like we mentioned at the start is just HTML with some added niceties. All of Laravel's starter kits have TailwindCSS included out of the box so it's nice to learn to embrace it when at all possible.

In your `resources/css/app.css` file, we can add the following changes after the existing code:

```css
/* CHIRPER CUSTOM LARAVEL THEME */
:root:has(input.theme-controller[value=laravelChirper]:checked),
[data-theme="laravelChirper"] {
  color-scheme: light;

  /* Canvas + text (neutral / cooler beige balance) */
  --color-base-50:  #fafafa;  /* almost pure white, very faint gray */
  --color-base-100: #f7f7f8;  /* neutral canvas */
  --color-base-200: #ededee;  /* light neutral gray (still contrasty w/ border) */
  --color-base-300: #e0e1e3;  /* mid gray, cooler but not blue */
  --color-base-content: #1a1a1c; /* neutral dark, softer than #111113 */

  /* Text tones */
  --text-12: var(--color-base-content);
  --text-10: color-mix(in oklab, var(--color-base-content) 64%, transparent);

  /* Brand / actions */
  --color-primary: #5580d2;            /* cooler button blue */
  --color-primary-content: #ffffff;
  --color-secondary: #2f3136;          /* neutral charcoal */
  --color-secondary-content: #ffffff;
  --link: #5580d2;
  --link-hover: color-mix(in oklab, #5580d2 80%, black);

  /* Borders / elevation */
  --border: 1px;
  --border-color-soft: rgba(0, 0, 0, 0.08); /* slightly stronger for visibility */

  /* Radii + misc */
  --radius-xs: 3px;
  --radius-sm: 5px;
  --radius-field: 8px;
  --radius-box: 10px;

  --radius-selector: var(--radius-sm);
  --radius-field: var(--radius-field);
  --radius-box: var(--radius-box);

  --depth: 1;
  --noise: 0;
}

/* Page background & base text */
html[data-theme="laravelChirper"],
:root:has(input.theme-controller[value=laravelChirper]:checked) body {
    color: var(--text-12);
}

/* Navbar = sand + hairline bottom */
.navbar {
    background: var(--color-base-100);
    border-bottom: var(--border) solid var(--border-color-soft);
    backdrop-filter: saturate(140%) blur(6px);
}

/* Cards — no shadow, soft border, tidy radius */
:where(.card) {
    background: var(--color-base-100);
    color: var(--text-12);
    border-radius: var(--radius-box);
    border: var(--border) solid var(--border-color-soft);
    box-shadow: none !important;
    /* kill all shadows */
    transition: none;
    /* no hover lift */
}

:where(.card:hover),
:where(.card.shadow),
:where(.card.shadow:hover) {
    box-shadow: none !important;
}

:where(.card .card-body) {
    padding: .875rem .875rem 1.125rem;
}

/* a hair more breathing room */

/* INPUTS / TEXTAREAS */
:where(.input, .textarea) {
    border-radius: var(--radius-field);
    border: var(--border) solid var(--border-color-soft);
    background: #fff;
}

/* reduce default textarea padding a touch */
:where(.textarea) {
    padding: .625rem .75rem;
}

/* inside cards, a hair tighter */
.card :where(.textarea) {
    padding: .5625rem .75rem;
}

:where(.input:focus, .textarea:focus) {
    outline: 2px solid color-mix(in oklab, var(--color-primary) 25%, transparent);
    outline-offset: 2px;
}

/* LINKS (site-wide) */
a {
    color: var(--link);
}

a:hover {
    color: var(--link-hover);
}

/* Fix: anchor-buttons should NOT be blue like links */
:where(a.btn) {
    color: inherit;
    text-decoration: none;
}

/* BUTTONS */
:where(.btn) {
    border-radius: 5px;
    box-shadow: none;
    font-weight: 500;
    /* medium */
    font-size: 0.875rem;
    /* Tailwind text-base */
    line-height: 1.25rem;
    /* align with text-base */
    padding-inline: 1rem;
    /* a bit more horizontal breathing room */
}

:where(.btn-primary),
:where(a.btn-primary) {
    background: var(--color-primary);
    color: var(--color-primary-content);
    border: none;
}

:where(.btn-primary:hover),
:where(a.btn-primary:hover) {
    background: color-mix(in oklab, var(--color-primary) 85%, black);
}

:where(.btn-ghost),
:where(a.btn-ghost) {
    color: var(--text-12);
    border: var(--border) solid var(--border-color-soft);
    background: transparent;
}

:where(.btn-ghost:hover),
:where(a.btn-ghost:hover) {
    background: rgba(0, 0, 0, 0.03);
}

:where(.btn-sm) {
    height: 2rem;
    min-height: 2rem;
    padding-inline: .75rem;
}

:where(.btn-xs) {
    height: 1.5rem;
    min-height: 1.5rem;
    padding-inline: .5rem;
    font-size: .75rem;
}

/* Toast-only success color */
:where(.toast) {
    --color-success: #598b6e;
    --color-success-content: #ffffff;
}

/* Hairline border + ensure text/icons pick up the content color */
:where(.toast .alert-success) {
    background: var(--color-success);
    color: var(--color-success-content);
    border: var(--border) solid rgba(0, 0, 0, 0.08);
}

:where(.link-primary) {
    color: var(--color-primary) !important;
}

:where(.link-primary:hover) {
    color: color-mix(in oklab, var(--color-primary) 85%, black) !important;
}

/* Timestamps / separators (like your `·` and “ago”) */
.text-base-content\\/60 {
    color: var(--text-10) !important;
}

/* Footer strip */
footer.footer {
    background: var(--color-base-200);
    color: var(--text-10);
}

/* 1) Links shouldn't style buttons (fixes blue anchor-buttons) */
a:not(.btn) {
    color: var(--link);
}

a:not(.btn):hover {
    color: var(--link-hover);
}

/* Anchor buttons keep button colors in all states */
a.btn,
a.btn:visited {
    color: inherit !important;
    text-decoration: none;
}

a.btn-ghost,
a.btn-ghost:visited {
    color: var(--text-12) !important;
}

a.btn-primary,
a.btn-primary:visited {
    color: var(--color-primary-content) !important;
}

/* keep ghost text from turning blue on hover */
a.btn-ghost:hover {
    color: var(--text-12) !important;
}

/* 2) Auth inputs full width inside cards/labels */
.card .input,
.card .textarea,
.floating-label>input,
.floating-label>.input,
.floating-label>.textarea {
    width: 100%;
}

/* 3) Slightly rounder cards & fields*/
:root:has(input.theme-controller[value=laravelChirper]:checked),
[data-theme="laravelChirper"] {
    --radius-box: 10px;
    /* was 8px */
    --radius-field: 8px;
    /* was 6px */
    --noise: 0;
    /* was 1; Community look is clean */
}

/* ensure cards pick up the token over defaults */
.card {
    border-radius: var(--radius-box) !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    font-weight: 400 !important;
}
```

Next, we added some Favicons and an OG image and referenced them in our `resources/views/components/layout.blade.php` file. If you would like to use those for your application you can find them in the [Github repository here.](https://github.com/laravel/bootcamp)

In that same Layout file, we have a new logo to add. This can replace the existing `button` logo that we were using with our cute little bird emoji and our existing footer respectively.

```php
<a href="/">
   <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 312 69"
      class="h-7 w-auto px-4">
      <path fill="#D9D9D9"
         d="M40.97.446c22.091 0 40 17.909 40 40a39.805 39.805 0 0 1-6.56 21.95c-.61.928-1.87 1.105-2.825.541a18.92 18.92 0 0 0-9.651-2.63c-.787 0-1.563.048-2.325.141a19.108 19.108 0 0 0-7.03-9.607 18.57 18.57 0 0 0 5.996-11.778l8.493-7.543a.931.931 0 0 0-.43-1.607l-10.423-2.138c-3.207-5.575-9.218-9.329-16.103-9.329-10.256 0-18.57 8.33-18.571 18.605 0 1.274.128 2.519.372 3.721-6.58.032-12.37 3.407-15.764 8.517-1.07 1.61-3.854 1.582-4.265-.306a40.101 40.101 0 0 1-.914-8.537c0-22.091 17.908-40 40-40Z" />
      <path fill="url(#a)"
         d="M40.97.446c22.091 0 40 17.909 40 40a39.805 39.805 0 0 1-6.56 21.95c-.61.928-1.87 1.105-2.825.541a18.92 18.92 0 0 0-9.651-2.63c-.787 0-1.563.048-2.325.141a19.108 19.108 0 0 0-7.03-9.607 18.57 18.57 0 0 0 5.996-11.778l8.493-7.543a.931.931 0 0 0-.43-1.607l-10.423-2.138c-3.207-5.575-9.218-9.329-16.103-9.329-10.256 0-18.57 8.33-18.571 18.605 0 1.274.128 2.519.372 3.721-6.58.032-12.37 3.407-15.764 8.517-1.07 1.61-3.854 1.582-4.265-.306a40.101 40.101 0 0 1-.914-8.537c0-22.091 17.908-40 40-40Z" />
      <path fill="#D9D9D9"
         d="M45.065 28.834a3.718 3.718 0 0 1 3.714 3.72 3.719 3.719 0 0 1-3.715 3.722 3.719 3.719 0 0 1-3.713-3.721 3.718 3.718 0 0 1 3.714-3.721Z" />
      <path fill="url(#b)"
         d="M45.065 28.834a3.718 3.718 0 0 1 3.714 3.72 3.719 3.719 0 0 1-3.715 3.722 3.719 3.719 0 0 1-3.713-3.721 3.718 3.718 0 0 1 3.714-3.721Z" />
      <path fill="#1B1B18"
         d="m299.633 26.19 1.798 8.246v22.01h-7.192V26.19h5.394Zm.496 11.656-1.488-.682V31.77l.558-.744c.413-.702 1.074-1.488 1.984-2.356a13.566 13.566 0 0 1 3.162-2.232c1.24-.62 2.5-.93 3.782-.93.62 0 1.198.042 1.736.124.578.083 1.012.228 1.302.434v6.51h-1.984c-2.728 0-4.774.434-6.138 1.302-1.364.827-2.336 2.15-2.914 3.968ZM273.838 57.066c-2.976 0-5.58-.64-7.812-1.922-2.232-1.322-3.989-3.162-5.27-5.518-1.24-2.356-1.86-5.104-1.86-8.246 0-3.182.62-5.952 1.86-8.308 1.281-2.397 3.038-4.257 5.27-5.58 2.232-1.322 4.836-1.984 7.812-1.984 3.017 0 5.642.682 7.874 2.046 2.273 1.323 4.03 3.183 5.27 5.58 1.24 2.356 1.86 5.084 1.86 8.184 0 .372-.021.744-.062 1.116 0 .372-.021.703-.062.992H265.22V37.66h18.166l-1.488 3.286c0-2.852-.661-5.187-1.984-7.006-1.323-1.818-3.327-2.728-6.014-2.728-2.439 0-4.381.765-5.828 2.294-1.405 1.488-2.108 3.472-2.108 5.952v3.286c0 2.563.703 4.609 2.108 6.138 1.447 1.488 3.431 2.232 5.952 2.232 2.273 0 4.03-.475 5.27-1.426a13.445 13.445 0 0 0 3.286-3.534l5.146 3.1c-1.364 2.563-3.183 4.506-5.456 5.828-2.273 1.323-5.084 1.984-8.432 1.984ZM242.175 57.128c-2.728 0-5.104-.64-7.13-1.922-1.984-1.281-3.534-3.1-4.65-5.456-1.116-2.356-1.674-5.146-1.674-8.37 0-3.224.558-6.014 1.674-8.37 1.158-2.397 2.728-4.236 4.712-5.518 2.026-1.322 4.382-1.984 7.068-1.984 2.811 0 5.25.662 7.316 1.984 2.108 1.323 3.741 3.183 4.898 5.58 1.158 2.356 1.736 5.126 1.736 8.308 0 3.1-.578 5.849-1.736 8.246-1.157 2.356-2.79 4.196-4.898 5.518-2.108 1.323-4.546 1.984-7.316 1.984Zm-15.81 11.098V26.19h5.394l1.798 6.634h-.62v16.182h.62v19.22h-7.192Zm14.632-17.546c2.315 0 4.196-.847 5.642-2.542 1.447-1.736 2.17-3.988 2.17-6.758 0-2.81-.723-5.084-2.17-6.82-1.446-1.736-3.327-2.604-5.642-2.604-2.273 0-4.154.868-5.642 2.604-1.446 1.695-2.17 3.948-2.17 6.758 0 2.811.724 5.084 2.17 6.82 1.488 1.695 3.369 2.542 5.642 2.542ZM209.902 26.19l1.798 8.246v22.01h-7.192V26.19h5.394Zm.496 11.656-1.488-.682V31.77l.558-.744c.413-.702 1.075-1.488 1.984-2.356a13.566 13.566 0 0 1 3.162-2.232c1.24-.62 2.501-.93 3.782-.93.62 0 1.199.042 1.736.124.579.083 1.013.228 1.302.434v6.51h-1.984c-2.728 0-4.774.434-6.138 1.302-1.364.827-2.335 2.15-2.914 3.968ZM196.93 56.446h-7.192V26.19h7.192v30.256Zm-8.122-39.68c0-1.322.392-2.397 1.178-3.224.826-.868 1.942-1.302 3.348-1.302 1.322 0 2.397.434 3.224 1.302.826.827 1.24 1.902 1.24 3.224 0 1.323-.414 2.398-1.24 3.224-.827.827-1.902 1.24-3.224 1.24-1.406 0-2.522-.413-3.348-1.24-.786-.826-1.178-1.901-1.178-3.224ZM155.405 56.446V14.224h7.192v42.222h-7.192Zm19.902 0V37.598c0-2.025-.434-3.368-1.302-4.03-.827-.702-1.86-1.054-3.1-1.054-1.158 0-2.356.248-3.596.744a11.427 11.427 0 0 0-3.286 1.922 10.082 10.082 0 0 0-2.418 2.728l-1.426-6.138a20.156 20.156 0 0 1 3.782-3.286 16.408 16.408 0 0 1 4.34-2.17 14.833 14.833 0 0 1 4.836-.806c2.149 0 3.844.352 5.084 1.054 1.24.703 2.17 1.674 2.79 2.914.62 1.199 1.012 2.563 1.178 4.092.206 1.488.31 3.038.31 4.65v18.228h-7.192ZM131.034 57.128c-4.299 0-8.06-.93-11.284-2.79-3.224-1.901-5.725-4.484-7.502-7.75-1.736-3.306-2.604-7.047-2.604-11.222 0-3.141.516-6.034 1.55-8.68 1.074-2.686 2.562-5.001 4.464-6.944 1.942-1.942 4.216-3.451 6.82-4.526 2.604-1.074 5.456-1.612 8.556-1.612 4.836 0 8.804 1.013 11.904 3.038 3.1 2.026 5.58 4.816 7.44 8.37l-6.82 2.294c-1.736-2.521-3.638-4.278-5.704-5.27-2.026-.992-4.299-1.488-6.82-1.488-2.687 0-5.084.64-7.192 1.922-2.108 1.24-3.782 2.976-5.022 5.208-1.24 2.232-1.86 4.795-1.86 7.688 0 2.894.62 5.456 1.86 7.688 1.24 2.232 2.914 3.989 5.022 5.27 2.108 1.24 4.505 1.86 7.192 1.86 2.521 0 4.794-.496 6.82-1.488 2.066-.992 3.968-2.748 5.704-5.27l6.82 2.294c-1.86 3.555-4.34 6.345-7.44 8.37-3.1 2.026-7.068 3.038-11.904 3.038Z" />
      <defs>
         <linearGradient id="a" x1=".97" x2="72.586" y1=".446" y2="80.006"
            gradientUnits="userSpaceOnUse">
            <stop stop-color="#45B8FF" />
            <stop offset="1" stop-color="#4B2A99" />
         </linearGradient>
         <linearGradient id="b" x1=".97" x2="72.586" y1=".446" y2="80.006"
            gradientUnits="userSpaceOnUse">
            <stop stop-color="#45B8FF" />
            <stop offset="1" stop-color="#4B2A99" />
         </linearGradient>
      </defs>
   </svg>
</a>
```

```php
<footer class="w-full mt-24">
    <div class="mx-auto w-full max-w-[1400px] px-4 xl:px-16">
        <svg class="block w-full h-auto text-base-content opacity-8" viewBox="0 0 1280 308" aria-hidden="true"
            focusable="false">
            <path d="M50.2753 0H0V308.689H144.713V263.27H50.2753V0Z" fill="currentColor" />
            <path
                d="M322.209 130.973C315.796 120.684 306.688 112.602 294.883 106.718C283.081 100.84 271.201 97.8969 259.253 97.8969C243.798 97.8969 229.665 100.764 216.843 106.496C204.014 112.228 193.015 120.099 183.834 130.091C174.654 140.088 167.51 151.628 162.412 164.706C157.308 177.792 154.761 191.54 154.761 205.94C154.761 220.645 157.308 234.457 162.412 247.39C167.508 260.332 174.652 271.796 183.834 281.788C193.015 291.785 204.017 299.647 216.843 305.379C229.665 311.111 243.798 313.978 259.253 313.978C271.201 313.978 283.081 311.038 294.883 305.159C306.688 299.282 315.796 291.197 322.209 280.904V308.685H369.865V103.186H322.209V130.973ZM317.837 231.076C314.922 239.016 310.841 245.925 305.598 251.804C300.35 257.687 294.009 262.389 286.579 265.917C279.146 269.445 270.905 271.208 261.875 271.208C252.837 271.208 244.676 269.445 237.391 265.917C230.104 262.389 223.839 257.687 218.593 251.804C213.345 245.925 209.335 239.016 206.57 231.076C203.794 223.138 202.417 214.759 202.417 205.942C202.417 197.12 203.794 188.742 206.57 180.804C209.335 172.866 213.345 165.961 218.593 160.078C223.839 154.201 230.102 149.493 237.391 145.965C244.676 142.437 252.837 140.674 261.875 140.674C270.908 140.674 279.146 142.437 286.579 145.965C294.009 149.493 300.35 154.199 305.598 160.078C310.844 165.961 314.922 172.866 317.837 180.804C320.748 188.742 322.209 197.12 322.209 205.942C322.209 214.759 320.748 223.138 317.837 231.076Z"
                fill="currentColor" />
            <path
                d="M709.568 130.973C703.155 120.684 694.047 112.602 682.242 106.718C670.44 100.84 658.56 97.8969 646.612 97.8969C631.157 97.8969 617.024 100.764 604.202 106.496C591.373 112.228 580.374 120.099 571.193 130.091C562.013 140.088 554.869 151.628 549.771 164.706C544.666 177.792 542.12 191.54 542.12 205.94C542.12 220.645 544.666 234.457 549.771 247.39C554.867 260.332 562.01 271.796 571.193 281.788C580.374 291.785 591.375 299.647 604.202 305.379C617.024 311.111 631.157 313.978 646.612 313.978C658.56 313.978 670.44 311.038 682.242 305.159C694.047 299.282 703.155 291.197 709.568 280.904V308.685H757.224V103.186H709.568V130.973ZM705.198 231.076C702.283 239.016 698.202 245.925 692.959 251.804C687.711 257.687 681.37 262.389 673.94 265.917C666.507 269.445 658.266 271.208 649.236 271.208C640.198 271.208 632.037 269.445 624.752 265.917C617.465 262.389 611.2 257.687 605.954 251.804C600.706 245.925 596.696 239.016 593.931 231.076C591.155 223.138 589.778 214.759 589.778 205.942C589.778 197.12 591.155 188.742 593.931 180.804C596.696 172.866 600.706 165.961 605.954 160.078C611.2 154.201 617.463 149.493 624.752 145.965C632.037 142.437 640.198 140.674 649.236 140.674C658.269 140.674 666.507 142.437 673.94 145.965C681.37 149.493 687.711 154.199 692.959 160.078C698.205 165.961 702.283 172.866 705.198 180.804C708.109 188.742 709.57 197.12 709.57 205.942C709.568 214.759 708.107 223.138 705.198 231.076Z"
                fill="currentColor" />
            <path d="M1280 1.12315e-05H1232.35V308.689H1280V1.12315e-05Z" fill="currentColor" />
            <path d="M407.466 308.689H455.117V150.486H536.876V103.192H407.466V308.689Z" fill="currentColor" />
            <path
                d="M948.281 103.192L888.386 260.557L828.489 103.192H780.224L858.441 308.689H918.331L996.546 103.192H948.281Z"
                fill="currentColor" />
            <path
                d="M1100.48 97.908C1042.13 97.908 995.937 146.279 995.937 205.944C995.937 271.9 1040.64 313.98 1106.59 313.98C1143.5 313.98 1167.06 299.745 1195.85 268.746L1163.66 243.621C1163.64 243.646 1139.36 275.802 1103.1 275.802C1060.96 275.802 1043.22 241.533 1043.22 223.803H1201.32C1209.62 155.913 1165.37 97.908 1100.48 97.908ZM1043.35 188.085C1043.71 184.13 1049.2 136.086 1100.1 136.086C1151.01 136.086 1157.19 184.123 1157.55 188.085H1043.35Z"
                fill="currentColor" />
        </svg>
        </p>
    </div>
</footer>
```

Next, to better match the new design, we can remove the `shadow` styles from our card elements in our `resources/views/components/chirp.blade.php` and the `resources/views/chirps/edit.blade.php` files.

Lastly, we can modify the h1's of the Register and Login view files to use `text-xl mt-1` instead of the previous `text-3xl`.

Looking good!

## Laravel Auth Starter Kits

Building auth manually taught you how it works, but in real projects, you'd often use:

- **Laravel Starter Kits** - Ready-to-use authentication scaffolding with complete user interfaces
- **Laravel Fortify** - Headless authentication backend for building authentication from scratch with your own UI
- **Laravel Socialite** - OAuth authentication with providers like GitHub, Google, Facebook, Twitter, and more

These provide production-ready auth with email verification, password resets, two-factor authentication, and more!

Now, it might seem simple, but give yourself a round of applause—we just created your first Laravel application with complete authentication! Next up: Let's wrap up and talk about what's next in your Laravel journey!
