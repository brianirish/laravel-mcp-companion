# Laravel Learn - Getting Started with Laravel: Our first model

Source: https://laravel.com/learn/getting-started-with-laravel/our-first-model

---

Build your first Eloquent model to interact with the database elegantly. Learn how models represent database tables as PHP objects with powerful features.

Like we explored in the last lesson, now that you have a database, there's a number of different ways that you can interact with that database. You can use a GUI like TablePlus or DBeaver to interact with your database, even insert new things, delete things. That's a little bit more hands-on where you have a more manual approach. Within php artisan tinker, you could use maybe raw SQL, which sounds a little crazy and a little strange and maybe a little scary.

But you can also use something like the DB facade, which Laravel gives out of the box to say, "Hey, here's a little bit easier way of working within a database." But don't worry, it gets even easier. Right now, this lesson we're going to talk about models.

If we're going back to our restaurant analogy, the M in MVC—model—is our kitchen. It prepares the food, it organizes your data structure. It keeps everything nice and neat. And in a Laravel application, you can use models to interact with your database in a really, really beautiful way—an eloquent way.

## Step 1: Explore the User Model

So, as you can see here (I'm going to zoom out a little bit), we already have a model created for us. That's the User model. So why don't we take a look at what this actually looks like. Open `app/Models/User.php`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    // ... more code
}
```

There's a few things I want to point out. First, there's things like it can use specific things within Laravel, like HasFactory or Notifiable. We won't dive into either of those this course, but it's helpful to know that there are things that can interact with a model as a whole.

Next we have this `$fillable` array. This is just to show Laravel that people can, within your application, enter a name, an email, and a password into this table in your database. So this fillable array is the one that we're going to focus on as we create a new model for our chirps.

There are other additional arrays like `$hidden` or `$casts`, and what this does is allow you to interact with your model in even more depth. We won't touch those just yet. Models are PHP classes that represent your database tables.

## Step 2: Create the Chirp Model

So let's go ahead and create our own model. Opening up our terminal again:

```bash
php artisan make:model Chirp
```

And then we're going to pass it a singular capitalized name for our model. In this case: Chirp. Again, if we want to just leave that off, it gives us a little indicator of what that should be named (in this case "Flight"). But I'm not using flights, I'm using chirps.

Now before I run this make:model command for our Chirp, I did want to make a note that Laravel has these time-saving flags for models. If we were to create a model but add a dash parameter of `-mrc`, this would do everything that we've already done within this course:

```bash
php artisan make:model Chirp -mrc
```

- It would create the Chirp model, of course
- `m` creates a migration (like we did in lesson 6)
- `rc` creates a resource controller (like we did in lesson 5)

But since we already have those, we're just going to make the model.

Open `app/Models/Chirp.php`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Chirp extends Model
{
    //
}
```

Pretty minimal! But this simple class already knows it's connected to the `chirps` table (Eloquent automatically converts the class name to plural, lowercase).

Heading into that Chirp model, just like I said, we want to first focus on that fillable array.

## Step 3: Define Fillable Properties

Remember that `$fillable` array in the User model? Let's add one for Chirp:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Chirp extends Model
{
    protected $fillable = [
        'message',
    ];
}
```

So in this protected fillable array, we're just going to have our message, and this is because this is the only field in our model that we need to enter into the database. This protects against mass assignment vulnerabilities.

## Step 4: Define Relationships

Next, Laravel Eloquent allows us to attach these relationships between different models. That's going to be great for us because we have users that are associated to chirps and chirps that are associated to a single user. So we can do just that.

Here's where Eloquent shines. Let's define the relationship between users and chirps:

In `app/Models/Chirp.php`, add:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Chirp extends Model
{
    protected $fillable = [
        'message',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

Now in `app/Models/User.php`, add this method after the existing code:

```php
use Illuminate\Database\Eloquent\Relations\HasMany;

public function chirps(): HasMany
{
    return $this->hasMany(Chirp::class);
}
```

We can create a public function of user and here's where we can type hint this to say "this belongs to." We're pulling that in—this `use Illuminate\\\\Database\\\\Eloquent\\\\Relations\\\\BelongsTo` type. We're going to return this, which is this model belongs to, and then we can pass in the User class. So in this case, the User model.

This is letting Laravel know throughout this application, anytime we call the user on our chirps, we'll be able to grab the user's information that's associated to that single instance of a chirp or multiple chirps.

Now we want to do the inverse for what we already have within our Laravel application for our user. If I want to grab a single user's chirps, then this would be helpful.

These relationships let you do magical things like `$user->chirps` to get all of a user's chirps, or `$chirp->user` to get the chirp's author!

## Step 5: Eloquent in Action

Let's test our model in Tinker:

```bash
php artisan tinker
```

```php
// Create a new user
$user = \App\Models\User::create([
    'name' => 'Eloquent Expert',
    'email' => 'eloquent@expert.com',
    'password' => bcrypt('password')
]);

// Create a chirp for this user
$chirp = $user->chirps()->create([
    'message' => 'Eloquent makes database work a breeze!'
]);

// Access the relationship
echo $chirp->user->name; // "Eloquent Expert"

// Get all chirps
\App\Models\Chirp::all();

// Get recent chirps
\App\Models\Chirp::latest()->get();
```

Type `exit` to leave Tinker.

So what do these relationships actually look like in code? I kind of talked through it with you, but why don't we actually write it out? If I want to grab a chirp's user, I could do `$chirp->user` and this would give me something like "Hey, this is Josh. Who is the user?"

Again, this is just handy to know how all this fits together. And while this is just muscle memory to be able to learn how Tinker works and how our model works, you could do this with something like AI or even within a graphical interface to create these new users or maybe even chirps associated with the user. But this lets us know how our model's relationships also work as well.

## Step 6: Update Your Controller

Now, let's go ahead and update our controller with our real data now, because if we remember in our ChirpController, we were just passing in fake chirp data. Well instead, instead of this chirps array, why don't we actually grab the chirps from the model?

Update `app/Http/Controllers/ChirpController.php`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Chirp;
use Illuminate\Http\Request;

class ChirpController extends Controller
{
    public function index()
    {
        $chirps = Chirp::with('user')
            ->latest()
            ->take(50)  // Limit to 50 most recent chirps
            ->get();

        return view('home', ['chirps' => $chirps]);
    }
}
```

What's happening:

- `Chirp::with('user')` - This is so that we can eager load that user relationship and it prevents N+1 queries—in that case, having to query the database multiple times for things that we already have
- `latest()` - We want to grab those chirps via the latest, ordering by created\_at, newest first
- `take(50)` - Let's say we want to take 50 of them. Maybe this is so that we don't have all of the chirps loaded on one screen. There's other ways around this, but for now, this is going to be the easiest
- `get()` - And then we're going to get those chirps

And we shouldn't have to change anything else because we're still passing that chirps variable to our home view.

## Step 7: Update Your View

Update `home.blade.php` to use real data:

```html
<x-layout>
    <x-slot:title>
        Welcome
    </x-slot:title>
    <div class="max-w-2xl mx-auto">
        @forelse ($chirps as $chirp)
            <div class="card bg-base-100 shadow mt-8">
                <div class="card-body">
                    <div>
                        <div class="font-semibold"> {{ $chirp->user ? $chirp->user->name : 'Anonymous' }}</div>
                        <div class="mt-1">{{ $chirp->message }}</div>
                        <div class="text-sm text-gray-500 mt-2">
                            {{ $chirp->created_at->diffForHumans() }}
                        </div>
                    </div>
                </div>
            </div>
        @empty
            <p class="text-gray-500">No chirps yet. Be the first to chirp!</p>
        @endforelse
    </div>
</x-layout>
```

So there's a few things that we need to change in order to update our view to accept this real data. First of all, it's not an array anymore, it's an actual model, and that's going to look a little bit different.

Notice:

- I changed things to `@forelse`. This is a little bit easier, but mostly so I can teach you something new. `@forelse` says "for all the chirps as chirp," this still exists in the same way, but if it's empty, then we can show an empty state: "There's no chirps yet. Be the first to chirp!"
- `$chirp->message` - Everything that we would have passed as an array in our PHP now is the chirp message. This is associated to that model.
- `$chirp->created_at->diffForHumans()` - This is a cool little Laravel helper "diffForHumans," which is going to tell us how long ago did this actually happen, that specific date. Laravel automatically converts timestamps to Carbon date objects with helpful methods!
- `$chirp->user ? $chirp->user->name : 'Anonymous'` - This is just showing that it's going to say the user name if that user exists. Otherwise, it'll be anonymous because again, we have the ability, at least right now, to say that no user has to create a chirp. We can create one without having an authenticated user.

> Note: We're checking if a user exists before showing their name. In lesson 11, we'll add authentication so every chirp has a real user!

## The Power of Eloquent

Look what we can do now without writing SQL:

```php
// Get all chirps
Chirp::all();

// Get chirp by ID
Chirp::find(1);

// Get first chirp matching criteria
Chirp::where('message', 'like', '%Laravel%')->first();

// Count chirps
Chirp::count();

// Get a user's chirps
$user->chirps;

// Create a chirp
$user->chirps()->create(['message' => 'Hello!']);

// Update a chirp
$chirp->update(['message' => 'Updated message']);

// Delete a chirp
$chirp->delete();
```

No SQL in sight, just readable PHP!

## What We've Accomplished

So what does this look like in the browser? Well, you can see this was a chirp that was created by us. We did that within Tinker. We're starting to see how this is turning into a real-world application. We're having things stored in the database, at least we're being able to then read them and also take relationships from them saying, "Hey, this is anonymous. There's no user associated with it, but this one has a user, and that user has a name."

Just to confirm how those relationships work, instead of showing user name, maybe I want to show user email here. And there we go! There's the email that I entered for my user that I created.

- Created a Chirp model that represents our database table
- Defined relationships between Users and Chirps
- Used Eloquent to query real data
- Displayed actual chirps from the database

So now your app has real data! But users can't create chirps yet. Next up: building a form to post new chirps. Time to make your app interactive!
