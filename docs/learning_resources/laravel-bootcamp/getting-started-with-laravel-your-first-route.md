# Laravel Learn - Getting Started with Laravel: Your first route

Source: https://laravel.com/learn/getting-started-with-laravel/your-first-route

---

Create your first Laravel route and view. Learn how routes connect URLs to code and build a basic homepage with Blade templates.

Alright, let's dive into some actual code! When you first opened up that URL—that's <http://127.0.0.1:8000> on port 8000 where your development server is running—you were greeted by Laravel's friendly default welcome page (at least for Laravel 12 at the time of this recording).

But how does Laravel know what to show you? That's thanks to the route in `routes/web.php`. Let's take a look at what's happening:

```php
Route::get('/', function () {
    return view('welcome');
});
```

This little bit of code tells Laravel: "When someone visits the homepage (that slash route), show them the `welcome` view." That's what this Route facade is doing—it's defining what happens when a user goes to the root directory of your application.

And since I'm using VS Code with the official Laravel extension, I can actually option-click (or ctrl-click on Windows) to follow that `welcome` view to `resources/views/welcome.blade.php`. That's where this view lives, and that's what you're seeing in your browser.

## Step 1: Change the Rendered View

Let's take control! Update the route to render a view called `home` instead:

```php
Route::get('/', function () {
    return view('home');
});
```

If you refresh your browser now, you'll get an error—Laravel can't find the `home` view yet.

If you're using the Laravel VS Code extension, not only will it show you this error right in the editor (the view `home` is not found), but it also gives you an easy way to fix this—it can create the missing `home.blade.php` file for you. Handy!

## Step 2: Create the Home View

So what can we do about this missing view? Let's create it! In the `resources/views` directory, create a new file named `home.blade.php`.

Now we won't get an error anymore, but if you refresh your browser, it's just a blank page. So let's actually build something! I'm going to paste in the entire code so we can get this up and running as quickly as possible (if you're following along on [laravel.com/learn](http://laravel.com/learn), you can find this code below the lesson):

```html
<!DOCTYPE html>
<html lang="en" data-theme="lofi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chirper - Home</title>
    <link rel="preconnect" href="<https://fonts.bunny.net>">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600,700" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css" />
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>

<body class="min-h-screen flex flex-col bg-base-200 font-sans">
    <nav class="navbar bg-base-100">
        <div class="navbar-start">
            <a href="/" class="btn btn-ghost text-xl">🐦 Chirper</a>
        </div>
        <div class="navbar-end gap-2">
            <a href="#" class="btn btn-ghost btn-sm">Sign In</a>
            <a href="#" class="btn btn-primary btn-sm">Sign Up</a>
        </div>
    </nav>

    <main class="flex-1 container mx-auto px-4 py-8">
        <div class="max-w-2xl mx-auto">
            <div class="card bg-base-100 shadow mt-8">
                <div class="card-body">
                    <div>
                        <h1 class="text-3xl font-bold">Welcome to Chirper!</h1>
                        <p class="mt-4 text-base-content/60">This is your brand new Laravel application. Time to make it
                            sing (or chirp)!</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer footer-center p-5 bg-base-300 text-base-content text-xs">
        <div>
            <p>© 2025 Chirper - Built with Laravel and ❤️</p>
        </div>
    </footer>
</body>

</html>
```

Now, a couple things to note here. First, Blade is just HTML! We could have a whole script tag in here if we wanted, or a style tag. Everything you see in this file is just HTML. Blade just has a little bit of templating magic on top that we'll get into.

Notice that `@vite` directive? That's telling Laravel we want to use the `app.css` and `app.js` files. Laravel gives us Tailwind CSS out of the box and it's already set up for our application. And just to keep things simple and focus on Laravel itself (not styling), we're including DaisyUI as one of the CDN links. It uses Tailwind CSS, so we're just building on top of what Laravel already gives us. You can see we're using the `data-theme="lofi"` for that clean, minimalist look.

Refresh your browser—you should now see your custom Chirper homepage, complete with a header and navigation links. It's starting to look a little bit better!

## Step 3: Extract a Layout with Blade Components

Alright, we have this HTML file here, our `home.blade.php`, and you can imagine this would get a little bit complex. If we were to add additional pages—like say a sign in or sign up page—we'd copy everything and then add it to a new sign in page and change what we needed to change. But then if something small changed that we needed to update everywhere... you see where this is going.

This is where Blade layouts come into play—or in this case, a layout component that is a Blade file. This is where the fun actually begins!

### What Are Blade Components?

Blade components let you take your content from these views, and that content gets injected into the layout via this special `$slot` variable. So any new page that uses that layout automatically gets all of the extra stuff attached to it from the get-go.

Let's see how this works:

### Defining the Layout Component

What we're going to do is create a new layout component. We'll take everything—let's say everything except what's in the main div—and put it in a reusable layout.

In your `resources` folder, in `views`, create a new folder called `components` (this is what Laravel looks for). In that components folder, create a new file called `layout.blade.php`:

```html
<!DOCTYPE html>
<html lang="en" data-theme="lofi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ isset($title) ? $title . ' - Chirper' : 'Chirper' }}</title>
    <link rel="preconnect" href="<https://fonts.bunny.net>">
    <link href="https://fonts.bunny.net/css?family=instrument-sans:400,500,600,700" rel="stylesheet" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5/themes.css" rel="stylesheet" type="text/css" />
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="min-h-screen flex flex-col bg-base-200 font-sans">
    <nav class="navbar bg-base-100">
        <div class="navbar-start">
            <a href="/" class="btn btn-ghost text-xl">🐦 Chirper</a>
        </div>
        <div class="navbar-end gap-2">
            <a href="#" class="btn btn-ghost btn-sm">Sign In</a>
            <a href="#" class="btn btn-primary btn-sm">Sign Up</a>
        </div>
    </nav>

    <main class="flex-1 container mx-auto px-4 py-8">
        {{ $slot }}
    </main>

    <footer class="footer footer-center p-5 bg-base-300 text-base-content text-xs">
        <div>
            <p>© {{ date('Y') }} Chirper - Built with Laravel and ❤️</p>
        </div>
    </footer>
</body>
</html>
```

Notice that `{{ $slot }}` in the main section? That's where the content from our individual pages will be injected. So basically, any other stuff that we add to a file using this layout will be put right there.

Also, look at how we're handling the title: `{{ isset($title) ? $title . ' - Chirper' : 'Chirper' }}`. We're using some PHP here to say: if this title variable is set, let's use it and append " - Chirper". If not, let's just revert to "Chirper". This gives us consistent branding across all pages!

### Configuring Tailwind v4 with app.css

With Tailwind CSS v4, we can customize our design system directly in `app.css`. Update `resources/css/app.css`:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
@source '../../storage/framework/views/*.php';
@source '../**/*.blade.php';
@source '../**/*.js';

@theme {
    --font-sans: 'Instrument Sans', ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',
        'Segoe UI Symbol', 'Noto Color Emoji';

    --animate-fade-out: fade-out 4s ease-in-out forwards;

    @keyframes fade-out {
        0%, 70% {
            opacity: 1;
        }
        100% {
            opacity: 0;
            pointer-events: none;
        }
    }
}
```

This configuration:

- Sets Instrument Sans as our default sans-serif font (used when we apply `font-sans`)
- Creates a custom `animate-fade-out` animation for notifications
- Uses Tailwind v4's `@theme` directive to extend the design system

### Applying the Layout Component

Now comes the magic part. Let's update our `home.blade.php` to use this layout. We're going to take just the content within the main div and wrap it with our layout component:

```html
<x-layout>
    <x-slot:title>
        Welcome
    </x-slot:title>

    <div class="max-w-2xl mx-auto">
        <div class="card bg-base-100 shadow mt-8">
            <div class="card-body">
                <div>
                    <h1 class="text-3xl font-bold">Welcome to Chirper!</h1>
                    <p class="mt-4 text-base-content/60">This is your brand new Laravel application. Time to make it
                        sing (or chirp)!</p>
                </div>
            </div>
        </div>
    </div>
</x-layout>
```

Laravel knows to look for a layout in the `views/components` directory, and if you're using the Laravel extension, it'll even validate this for you automatically.

Now the content between the `x-layout` tags is injected into the layout's `$slot`. And see that `x-slot:title`? That's how we can pass the title prop to our layout. We're setting it to "Welcome", so in the browser you'll see "Welcome - Chirper" as the page title.

If we look at our browser and refresh, we shouldn't see any change visually—we just took one file and made it into two files to make it more composable for the future. But now we have an application that's ready to start adding pages. We just have to use this `x-layout` to get everything we'd expect: the nav, the footer, and a simple layout to add things to.

## Step 4: Routing to Your View

Your route in `routes/web.php` doesn't change:

```php
Route::get('/', function () {
    return view('home');
});
```

Visit <http://localhost:8000> and you'll see your home page, now using your shiny new layout component!

And there you have it! You've just learned how to create a custom view, build a reusable layout with Blade components, and wire everything up with a route. This is the foundation for every page you'll build in Laravel. With all this in mind, we now have an application that's ready to start growing. We're ready for the next lesson!
