# Laravel Learn - Getting Started with Laravel: What is MVC?

Source: https://laravel.com/learn/getting-started-with-laravel/what-is-mvc

---

Understand the Model-View-Controller pattern that keeps Laravel code organized. Create your first controller and see how MVC separates concerns in web applications.

So what is MVC? Well, right now, your route in this `web.php` routes file—it's doing everything. It's handling the request, it's preparing data, it's returning a view. And it might not seem like it's doing that much, mostly because Laravel does all that for you in this Route facade that's getting this slash directory and returning a view. It's simple, but it's doing a lot under the hood.

As your application grows, you'll want a better way to organize things. And that's where the MVC model comes in. MVC stands for Model-View-Controller, and it's the pattern that keeps your code clean and your sanity intact.

## The Restaurant Analogy

If we're going to take this into an analogy, let's think of a restaurant. While MVC is not necessarily the order that everything happens in terms of model and then view and then controller within Laravel, let's talk about the controller first.

Imagine a restaurant:

- **The Waiter (Controller)**: This is what you would think of as the waiter in a restaurant. It takes your order, it coordinates everything, and then it brings you the food.
- **The Kitchen (Model)**: Well, the kitchen would then be the model. This is what prepares the food, it manages the ingredients—your data, I guess, in an application.
- **The Presentation (View)**: And then there's the presentation—how the food looks on the plate when it arrives. It's your view.

What this looks like in Laravel terms:

- **Controllers** handle your requests and coordinate responses
- **Models** manage your data and your business logic
- **Views** actually display the information to your users

Now, we've already seen what a view looks like. Each one has its own job, but your controller and your model haven't necessarily been shown to you in this course just yet. So let's go ahead and create your first controller!

## Step 1: Creating Your First Controller

Just for simplicity's sake, why don't we move everything that we have in this routes file—Route::get and then return view of home—why don't we move this logic to a controller? That way you have a little bit more insight as to how this all fits within a Laravel application.

Right now in `routes/web.php`, you have:

```php
Route::get('/', function () {
    return view('home');
});
```

We're going to generate a controller. Now we can do this in our terminal for our application, or we can actually just do it in the terminal built into your code editor if there is one. I'm going to do that here just for simplicity's sake:

```bash
php artisan make:controller ChirpController
```

Now I'm going to tell you what this command is, and then we're going to take a look at why this command actually exists. We're saying `php artisan make:controller`. But what is this `php artisan`? That is Laravel's way of running specific commands. It's Laravel's command line tool. It's your Swiss Army knife, I guess, for Laravel development.

We use it a lot to create things—not just controllers, but there are a ton of artisan commands that are available to be able to run anything within Laravel. And the cool thing is you can actually create your own as well! For right now, we're just going to be using a lot in this "make" directory of php artisan commands, mostly to make controllers, and later we'll make models, maybe database migrations as well. Artisan commands are incredibly powerful, so there's so much to dive into.

If we press enter (and if you didn't add the controller name), it's automatically going to prompt for what that controller should be named. You can even see what that looks like typically in terms of casing and in terms of how it should be spelled. Because we are going to be creating chirps, we want a ChirpController.

We're going to stick with an empty controller for now, but later we'll go back and look at what "resource" actually provides for us.

And you can see it created a specific file for us: `app/Http/Controllers/ChirpController.php`. Let's go ahead and open up that new file:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ChirpController extends Controller
{
    //
}
```

## Step 2: Add an Index Method

It's just a blank file, but let's go ahead and add the things that we had in our web route here. How do we do that? We're going to add an index method to handle our homepage:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ChirpController extends Controller
{
    public function index()
    {
        return view('home');
    }
}
```

Don't forget the semicolon! And you can see here that if you're using the VS Code Laravel extension, it still takes us directly to that view that we have.

The `index` method is a convention for displaying a list of things (or in our case, the main page).

## Step 3: Update Your Route

So in our web routes, how do we change this to instead point to our index method in our ChirpController?

Let's go ahead and clear this out. Instead of returning a view here, we're actually going to use the ChirpController. Update `routes/web.php` to use your controller:

```php
use App\Http\Controllers\ChirpController;

Route::get('/', [ChirpController::class, 'index']);
```

We're importing it in as a class, and then we can pass it a particular method. In this case, I'm going to be direct and pass it that index method.

Let's take a look at our browser... refresh, everything still works great! This is just a cleaner way of writing what we were doing directly in our routes file. But now all of this lives in our controller. Now we can slowly start to add to this controller as we build out our application.

## Step 4: Passing Data to Views

Now controllers really shine when you need to prepare data and then serve that data. Again, similar to how a waiter might do this in a restaurant. We're going to add some sample chirps to see this in action:

```php
public function index()
{
    $chirps = [
        [
            'author' => 'Jane Doe',
            'message' => 'Just deployed my first Laravel app! 🚀',
            'time' => '5 minutes ago'
        ],
        [
            'author' => 'John Smith',
            'message' => 'Laravel makes web development fun again!',
            'time' => '1 hour ago'
        ],
        [
            'author' => 'Alice Johnson',
            'message' => 'Working on something cool with Chirper...',
            'time' => '3 hours ago'
        ]
    ];

    return view('home', ['chirps' => $chirps]);
}
```

Now, how do we pass this into this view? Our second parameter is going to be an array. We're saying that 'chirps' is going to be equal to the $chirps array variable.

Now, how do we display these chirps in our view? Again, if we're talking about the MVC model-view-controller structure, we have our controller and we're passing these chirps to our view. Now, how do we display them here?

Well, this is where that Blade templating comes into play. So our `home.blade.php` file is not just HTML, it is Blade, and we can add some templating structure to this. Update your `home.blade.php` to display these chirps:

```html
<x-layout>
    <x-slot:title>
        Welcome
    </x-slot:title>
    <div class="max-w-2xl mx-auto">
        @foreach ($chirps as $chirp)
            <div class="card bg-base-100 shadow mt-8">
                <div class="card-body">
                    <div>
                        <div class="font-semibold">{{ $chirp['author'] }}</div>
                        <div class="mt-1">{{ $chirp['message'] }}</div>
                        <div class="text-sm text-gray-500 mt-2">{{ $chirp['time'] }}</div>
                    </div>
                </div>
            </div>
        @endforeach
    </div>
</x-layout>
```

In this case, for every chirp we can say `@foreach ($chirps as $chirp)`, and then every single instance of chirps that we have in that array that is being passed in from this ChirpController, we're going to iterate over whatever HTML that we're passing in here. Don't forget the `@endforeach` to say that this is the end of that foreach loop.

Now we have available the $chirps array. We have the chirp author, the chirp message, and the chirp time to coincide with what we're passing in from the ChirpController.

Let's see what this looks like in our browser... Alright! That looks pretty good. Now you can see how our controller is going to allow us to pass additional data to different views, and we can also have different methods.

## Step 5: Resource Controllers

Let's take a look at what resource controllers offer. What I'm going to do is I'm actually going to copy all of this and delete this ChirpController, because when we used that initial method to create a controller, we just selected empty.

What happens if we then create a ChirpController that is a resource controller? This is what you might typically use in a standard MVC structure. This resource allows for an optional model that you might have. We don't have a Chirp model just yet, so I'm not going to select anything there.

```bash
php artisan make:controller ChirpController --resource
```

Just a hint—anytime we use an artisan command, we don't necessarily need to leave it blank. We could write ChirpController and then even pass it additional options or parameters. Most artisan commands have this ability where I could pass it `--resource` and it would automatically complete what we just had completed for us.

Now, in that ChirpController, we have seven different methods:

- `index()` - Displaying a listing of all resources. It's listing all of the chirps, this home page.
- `create()` - Might be showing a form to create a new chirp. In our demo application, we're doing this on the same page, so we likely won't use this.
- `store()` - Where we're creating and saving a new chirp
- `show()` - To be able to display one single chirp
- `edit()` - Displaying a form for editing a single chirp
- `update()` - Would be to update that single chirp
- `destroy()` - Deleting a chirp

We're going to be using most of, if not all of these, eventually throughout our application, but for now, we're just using the index method. So just update the `index` method with our sample data from before.

## The MVC Flow

So to recap, here's what happens when someone visits your site:

1. **Route** - This slash parameter, this root of your application, receives the request
2. **Route** calls the ChirpController, specifically the index method of this ChirpController class
3. **Controller** prepares the data—it's waiting at our table to decide how are we going to present this data (our sample chirps)
4. **Controller** passes all this information to the view—in this case, that home.blade.php
5. **View** then renders that HTML with the data
6. User sees this page!

## Why This Matters

So why does all this matter? Well, right now we're using fake data, but imagine when we have thousands of real chirps in a database:

- The **Controller** that we just set up is going to decide which chirps to show. It's going to take our order and then decide how to present them.
- The **Model** (which we're going to learn about in the next lesson) fetches them from the database.
- The **View** (that home.blade.php, at least for our index) displays them nicely.

So each piece has its job in the MVC structure—Model, View, Controller. Your code stays organized, and then future you will thank current you for how things are organized and displayed to your user.

## What's Next?

Our chirps are just arrays in memory right now. So in our next lesson, let's start working with real data to see how your app might remember things permanently. We'll set up a real database and create our first Model to manage actual data!
