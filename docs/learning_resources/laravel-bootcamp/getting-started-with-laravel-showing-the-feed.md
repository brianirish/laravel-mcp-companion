# Laravel Learn - Getting Started with Laravel: Showing the feed

Source: https://laravel.com/learn/getting-started-with-laravel/showing-the-feed

---

Transform your app with proper styling using Blade components. Create reusable UI components and format timestamps to build a polished social media feed.

Alright! Our application is starting to take shape, but let's be honest—it looks pretty basic right now. This is just the start of having our full Chirper application, but let's give it some TLC. We're going to add user avatars, format some timestamps, and use DaisyUI's components to make this look just a little bit nicer.

Let's transform this into something that actually looks like a social media feed!

## Step 1: Create a Chirp Component

The first thing I want to tackle is this home.blade.php file. It's great, but it'd be nice if we could get every chirp as its own component. That way we only have one place where we're modifying how chirps are displayed.

Blade components aren't just for layouts—they're perfect for reusable UI pieces like this! Let's create a component for displaying individual chirps:

Create a new file at `resources/views/components/chirp.blade.php`:

```html
@props(['chirp'])

<div class="card bg-base-100 shadow">
    <div class="card-body">
        <div class="flex space-x-3">
            @if($chirp->user)
                <div class="avatar">
                    <div class="size-10 rounded-full">
                        <img src="<https://avatars.laravel.cloud/>{{ urlencode($chirp->user->email) }}"
                             alt="{{ $chirp->user->name }}'s avatar"
                             class="rounded-full" />
                    </div>
                </div>
            @else
                <div class="avatar placeholder">
                    <div class="size-10 rounded-full">
                        <img src="<https://avatars.laravel.cloud/f61123d5-0b27-434c-a4ae-c653c7fc9ed6?vibe=stealth>"
                        alt="Anonymous User"
                        class="rounded-full" />
                    </div>
                </div>
            @endif

            <div class="min-w-0">
                <div class="flex items-center gap-1">
                    <span class="text-sm font-semibold">{{ $chirp->user ? $chirp->user->name : 'Anonymous' }}</span>
                    <span class="text-base-content/60">·</span>
                    <span class="text-sm text-base-content/60">{{ $chirp->created_at->diffForHumans() }}</span>
                </div>

                <p class="mt-1">
                    {{ $chirp->message }}
                </p>
            </div>
        </div>
    </div>
</div>
```

Let me walk you through what we changed here. This is pretty close to what we had previously, but now we're just making it a little bit cleaner.

Notice a few key things:

- **Avatar magic**: If there is a chirp user, we're using `avatars.laravel.cloud`, which is a free service that generates these neat little gradients for you whenever you need avatars for your application. We're just passing in the user's email to generate them specifically for that user.
- **Anonymous fallback**: We have a default avatar for anonymous users too.
- **Props power**: Here's the neat thing about Blade components—we can pass in a prop (in this case, a chirp model instance). This prop then allows us to access `$chirp->user`, `$chirp->message`, `$chirp->created_at`, and so on when we use this component in our views.

> Note: We're handling both authenticated and anonymous chirps. In lesson 11, we'll add authentication so every chirp has a real user!

## Step 2: Update the Feed View

Now that we have our chirp component, let's update `home.blade.php` to use it. We're still looping through all the chirps like we did before—we're just doing it with our new component instead.

```html
<x-layout>
    <x-slot:title>
        Home Feed
    </x-slot:title>

    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold mt-8">Latest Chirps</h1>

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

Notice that we're passing in the `:chirp` prop to our `<x-chirp>` component—that colon indicates it's a prop we can pass into the component. Pretty neat, right?

## Step 3: Add Sample Data

Now that we're cruising along, why don't we get some more sample data without having to open `php artisan tinker` every time we want to create chirps? Laravel gives us an easy way to do this with something called seeders.

Let's create a seeder to generate some sample chirps. Run:

```bash
php artisan make:seeder ChirpSeeder
```

Now, let's edit `database/seeders/ChirpSeeder.php`. Seeders are a great way to make sample data so we can make sure our application is looking and feeling and working the way we expect.

We won't get into factories in this particular course, but factories are a great way to make random data. Seeders, on the other hand, are going to be a little bit more specific—they're basically just telling our database to run particular commands. You can think of seeders as an automated way to run `php artisan tinker` commands, so you don't have to type it all out.

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Chirp;
use Illuminate\Database\Seeder;

class ChirpSeeder extends Seeder
{
    public function run(): void
    {
        // Create a few sample users if they don't exist
        $users = User::count() < 3
				    ? collect([
				        User::create([
				            'name' => 'Alice Developer',
				            'email' => 'alice@example.com',
				            'password' => bcrypt('password'),
				        ]),
				        User::create([
				            'name' => 'Bob Builder',
				            'email' => 'bob@example.com',
				            'password' => bcrypt('password'),
				        ]),
				        User::create([
				            'name' => 'Charlie Coder',
				            'email' => 'charlie@example.com',
				            'password' => bcrypt('password'),
				        ]),
				    ])
				    : User::take(3)->get();

        // Sample chirps
        $chirps = [
            'Just discovered Laravel - where has this been all my life? 🚀',
            'Building something cool with Chirper today!',
            'Laravel\'s Eloquent ORM is pure magic ✨',
            'Deployed my first app with Laravel Cloud. So smooth!',
            'Who else is loving Blade components?',
            'Friday deploys with Laravel? No problem! 😎',
        ];

        // Create chirps for random users
        foreach ($chirps as $message) {
            $users->random()->chirps()->create([
                'message' => $message,
                'created_at' => now()->subMinutes(rand(5, 1440)),
            ]);
        }
    }
}
```

These are just some sample chirps in an array, and we're saying if there are fewer than three users (which there currently are in the database), let's go ahead and create some new users with this information. Again, this is exactly what we would do within tinker—this is just making it a little bit easier for us.

For each chirp message, every user is going to get a random chirp based off of this chirps array. Pretty cool, right?

Now let's run the seeder:

```bash
php artisan db:seed --class=ChirpSeeder
```

Running the seeder command is as simple as that! A database was successfully seeded.

Again, a seeder is just an easier way to have all those tinker commands run for us, but within a way that Laravel expects. In this case, we're just running all that PHP code, but seeding the database with it.

## Step 4: Real-time Updates (Preview)

Your feed looks great, but I want to make you aware of something we're not going to touch in this course, but something you might want to look into in the future: keeping this form up to date in real-time.

Right now, you can see that when we post a chirp, it says "0 seconds ago." But if anyone else accesses this page, they won't see new chirps until they actually refresh the page. Laravel has some great options for this, such as WebSockets with something like Laravel Reverb, which can notify all users when a new chirp comes in.

Here's what Laravel offers for real-time features:

- **Laravel Broadcasting** - Push updates to browsers in real-time
- **Laravel Echo** - JavaScript library for receiving broadcasts
- **Pusher or Laravel Reverb** - WebSocket servers for real-time communication

Again, not something we're going to be touching on in this course, but it's helpful to know that those options are out there and might be a great way to build on top of what we're building here with Chirper!

## What We've Built

Look at that! Your feed now has:

- A reusable Blade component for chirps
- Beautiful user avatars generated specifically for each user based on their email
- User information and formatted timestamps
- A polished, professional design with DaisyUI
- Handles empty states gracefully
- A clean way of generating sample data with seeders

So we're really moving right along! We now have a reusable Blade component for chirps, a way to generate chirps if we ever need to reset the database and start it up again, and a clean way of showing user information.

But it's still read-only. Next up: since it's still read-only, we're going to let users create their own chirps. Time to make this social network actually social!
