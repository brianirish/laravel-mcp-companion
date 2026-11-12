# Laravel Learn - Getting Started with Laravel: Setting up your Laravel project

Source: https://laravel.com/learn/getting-started-with-laravel/setting-up-your-laravel-project

---

Install Laravel, PHP, and create your first Laravel project. Learn about Laravel's AI-friendly design and get your development environment ready.

Alright, let's start by setting up your first Laravel project! I know you're excited to start coding, and trust me, we're going to get there fast. Whether you're on macOS, Windows, or Linux, the [official Laravel docs](https://laravel.com/docs/12.x#installing-php) at [laravel.com](http://laravel.com) have you covered with clean instructions and a one-line command that you can paste into your terminal to get started. No need to hunt down PHP or Composer separately—this single command handles everything for you.

## A Quick Note About Laravel and AI

Before we dive in, I want to take a quick timeout to talk about Laravel and AI. Laravel is designed to work beautifully with AI assistants. In fact, the framework includes Laravel Boost, which is a powerful tool that bridges the gap between AI coding agents and Laravel applications. It detects what's installed in your application and then allows those AI assistants to work with Laravel exactly the way you'd expect.

While I won't be using AI assistants or even AI auto-complete for this course (I want you to see and understand every line we write), Laravel and AI do make a fantastic pairing. You can ask AI to help explain concepts, debug issues, or even generate boilerplate code. Just remember: the easiest way to learn is by writing it out yourself, or at least understanding what the code does if AI is helping you write it. Understanding what the code does is always more important than who writes it!

## Step 1: Install Laravel and PHP

Head over to the [installation section](https://laravel.com/docs/12.x#installing-php) of the Laravel documentation and follow the instructions for your operating system. What's great about this is that the single command there will install PHP, Composer, and the Laravel installer all in one go—everything you need to get started.

After running that command, and this is important, **quit and restart your terminal session** to make sure everything that was installed is available globally. Trust me, this saves a lot of "command not found" headaches.

Want to check if everything worked? Try these commands:

```
php -v
```

This shows your PHP version, and:

```
laravel -v
```

This confirms the Laravel installer is ready (I'm running version 5.17 in the video).

Now, if you already had PHP and Composer installed previously, you could just install the Laravel installer globally with:

```
composer global require laravel/installer
```

For a fully-featured, graphical PHP installation and management experience, check out Laravel Herd—it's a fantastic tool that makes PHP management a breeze.

## Step 2: Create a New Laravel Application

With everything installed, you're ready to create your Laravel application! I have a `Code` directory where I like to put all my projects, but you can run the Laravel installer wherever you see fit. Here's the magic command:

```
laravel new chirper
```

The installer's going to ask you a few questions. Here's what to pick (and yes, we're sticking with the defaults for most of this):

- **Starter Kit:** Choose "None"—we're going to build things ourselves for now so you understand what's happening under the hood
- **Testing framework:** Just leave it with the default options (we won't be touching testing in this course, but it's good to have)
- **Database:** Select `sqlite`—it's perfect for getting started quickly, no configuration needed
- **Run** `npm install`**?** Say "yes" to let Laravel install the JavaScript dependencies for our application

Once that's done (and you'll see "Application ready!" in your terminal), jump into your new project folder:

```
cd chirper
```

That's it! The application is ready in the chirper directory.

## Step 3: Set Up Your Editor

I'm going to be using VS Code as my editor of choice for this bootcamp, but here's the good news—it doesn't really matter what you use. You can use any text editor or IDE you like, and Laravel works great with all of them.

Some popular choices include:

- **VS Code and Cursor**: Both have an official Laravel extension for syntax highlighting and productivity boosts. The Laravel official extension works great with VS Code or any VS Code forks like Cursor.
- **PHPStorm**: If you prefer a more dedicated IDE, PHPStorm is a favorite among PHP and Laravel developers. It even has its own Laravel Idea plugin, which is free for PHPStorm users.

No matter what you pick, you're set for a smooth ride. Pick what you're comfortable with!

## Step 4: Explore the Project Structure

Now that we have our Laravel application up and running, let's take a quick, high-level overview of the project structure that the Laravel installer generated for us—even without selecting a starter kit, there's quite a bit here!

Inside your `chirper` folder, here are the main directories you'll be working with:

- `app/` — This is where your PHP code lives—things like models and controllers are going to go here. We'll talk a lot more about those as the course progresses.
- `resources/views/` — This is where your views are going to go. In other words, where does your HTML go? You can think of these Blade templates as HTML with a little bit of extra magic and superpowers on top.
- `routes/` — This is where we define our application's URLs. When a user hits a particular page in your application, what should happen? This is where you define that behavior.
- `database/` — Everything database-related lives here. The neat thing about this directory is because we selected SQLite in the application installer, we have a database specifically just as this one file: `database.sqlite`. But this directory is also where things like our migrations are going to go, telling our database what structure it should have.

All of this might look like a lot now, but you'll be navigating these folders with ease very soon. I just wanted to let you know that there's really only going to be a couple of them that we'll spend the majority of our time in, so don't check out just yet!

## Step 5: Start Your App

Alright, moment of truth! Let's get this application up and running. Since all your dependencies are already built (remember when we said yes to npm install?), we can kickstart the development process with one beautiful command:

```
composer run dev
```

What this does is magic—it starts the development server for us. You might have noticed in the output that not only do we have our assets ready to go at a specific Vite port, but we also have our app URL for this Laravel application.

This command gets everything moving at once:

- Laravel's local development server
- The queue worker (for background jobs)
- Vite development server (for your frontend assets)

Open up <http://localhost:8000> in your browser, and you should see the Laravel welcome page. We're using Laravel 12 for this current version of the Laravel Bootcamp, and if you see that welcome page, congratulations—you're ready to start building!

We have our application, we have it open in our text editor, and we have our development server up and running to see any of the changes that we make. I think we're ready to get building!

Next up: you'll create your very first route and view, and get something custom showing up on your new Laravel site.
