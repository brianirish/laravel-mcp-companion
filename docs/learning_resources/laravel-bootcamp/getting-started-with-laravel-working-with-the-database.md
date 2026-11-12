# Laravel Learn - Getting Started with Laravel: Working with the database

Source: https://laravel.com/learn/getting-started-with-laravel/working-with-the-database

---

Set up your database with migrations and learn Laravel's database tools. Create tables programmatically and explore different ways to interact with data.

Alright, we have these sample chirps that we're passing to our view layer. Again, this is our controller—the C of the MVC structure—and we're passing this to our V, our view layer. But these chirps are just hardcoded values that we're passing from this controller. They don't actually exist in the database.

So when you're creating an application, when you're putting it out onto the web, most of the time you need a database in order to save things that can then live forever—or at least until someone deletes their chirp.

## Laravel's Database Magic

Good news: Laravel already set up a database for you! Remember when you chose SQLite during installation? It's been waiting patiently at `database/database.sqlite`. SQLite is perfect for learning—it's a real database that lives in a single file, no server required and it works with your local development environment seamlessly.

## Step 1: Meet Migrations

Migrations are like version control for your database. Instead of manually creating tables, you write PHP code that describes your database structure. Laravel can then create, modify, or rollback your database changes automatically.

Let's create a migration for our chirps table:

```bash
php artisan make:migration create_chirps_table
```

This creates a new file in `database/migrations/` with a timestamp and name. Open it up:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('chirps', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('chirps');
    }
};
```

## Step 2: Design Your Table

Let's add the columns we need for chirps:

```php
public function up(): void
{
    Schema::create('chirps', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->nullable()->constrained()->cascadeOnDelete();
        $table->string('message', 255);
        $table->timestamps();
    });
}
```

What's happening here:

- `id()` - Creates an auto-incrementing ID (primary key)
- `foreignId('user_id')` - Links each chirp to a user
- `nullable()` - Makes the user\_id optional for now (we'll fix this when we add authentication)
- `constrained()` - Creates a foreign key constraint
- `cascadeOnDelete()` - If a user is deleted, delete their chirps too
- `string('message', 255)` - The chirp text (max 255 characters)
- `timestamps()` - Adds created\_at and updated\_at columns automatically

> Note: Making user\_id nullable isn't recommended for production, but it lets us see our app working in the browser before we tackle authentication. Laravel gives us a User model out of the box, but to keep things simple, we'll build up to authentication gradually. We'll make this field required when we add user registration and login.

## Step 3: Run the Migration

Time to create the table:

```bash
php artisan migrate
```

You'll see output like:

```
INFO  Running migrations.

2024_01_15_123456_create_chirps_table ................... 28ms DONE
```

Your database now has a chirps table! 🎉

## Step 4: Explore Your Database

Want to see what you just created? You can use any SQLite viewer, but Laravel provides a handy tool called Tinker:

```bash
php artisan tinker
```

Then type:

```php
\DB::select('SELECT * FROM chirps');
```

You'll see an empty array `[]` because we haven't added any chirps yet. Type `exit` to leave Tinker.

For a visual approach, tools like TablePlus, DBeaver, or even VS Code extensions can open your `database/database.sqlite` file and show you the tables.

## Step 5: Understanding the Users Table

Notice that `user_id` column? It references the `users` table. Good news—Laravel already created this table for you! Check out `database/migrations/` and you'll see a create\_users\_table migration that ran when you first set up the project.

The users table has:

- id
- name
- email
- password
- remember\_token
- timestamps

This is why we can link chirps to users—the infrastructure is already there!

## Manual Data (Just to See It Work)

Before we move forward, I do want to manually create a chirp with php artisan tinker, mostly to show you that there's an easier way to do it in the next lesson—an easier way to interact with our database, even with the tools that Laravel gives us through models.

But also to show you that Tinker or any way that we're interacting with our database is a great use case for something like AI. Within Laravel Boost, there's tools that allow you to work with Tinker or allow your AI assistants to work with Tinker. You don't need to know all of this syntax for how to interact with the database through Tinker, but it's helpful to know what your AI, or even what specific commands might do.

Let's manually add a test chirp:

```bash
php artisan tinker
```

```php
// We're entering into the chirps table for selecting the chirps table
// and then inserting a message
\DB::table('chirps')->insert([
    'user_id' => null,  // Because we don't have a user, we can just leave it off
    'message' => 'My first chirp in the database!',
    'created_at' => now(),  // Laravel doesn't give these by default when using DB
    'updated_at' => now()
]);

// And we get this true back. So that means that this was successful,
// this chirp was now entered into the database!

// Check it worked (all chirps)
\DB::table('chirps')->get();
```

And there we go. Here's our first chirp. Congratulations! You just entered something into the database using a command line tool. Type `exit` to leave Tinker.

> Note: This might seem tedious to interact with the database in this way. The good news is we will explore easier ways to interact (even within Tinker) in the next lesson. Laravel Boost also provides AI Assistants an easy tool to use Tinker within your Laravel application.

## Migration Rollbacks

Made a mistake? Migrations can be reversed:

```bash
php artisan migrate:rollback
```

This runs the `down()` method, dropping the chirps table. You can then modify your migration and run `php artisan migrate` again.

**Warning**: Rolling back will delete any data in those tables!

## What We've Built

You now have:

- A real database (SQLite)
- A chirps table with proper structure
- A foreign key relationship to users
- Version-controlled database changes

But typing SQL queries is no fun. Next, we'll create a Model that lets us work with chirps using beautiful, expressive PHP code. No more SQL strings!

## Pro Tips

1. **Migration files are timestamped** - This ensures they run in the correct order
2. **Never edit old migrations** - Create new ones to modify existing tables
3. **Keep migrations in version control** - Your team needs them too!
4. `php artisan migrate:fresh` - Drops all tables and re-runs migrations (careful in production!)

Ready to make working with the database feel like writing poetry? Let's create our Chirp model!
