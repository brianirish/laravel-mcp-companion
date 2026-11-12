# Laravel Learn - Getting Started with Laravel: Deploying your app

Source: https://laravel.com/learn/getting-started-with-laravel/deploying-your-app

---

Deploy your Laravel application to the internet with Laravel Cloud. Learn Git basics and get your app live with automatic deployments.

Alright, congratulations! You have your first Laravel application running locally. We used `composer run dev` to set up our local development server, and we used layouts to compose what the start of our application looks like. We haven't really touched the full power of Laravel just yet, but don't worry—we'll get there.

But here's the thing: Laravel is about the whole package of an application from start to finish. And what good is an application if only you can see it in your browser on your machine? Let's get this Chirper application live on the internet with Laravel Cloud! It's the easiest way to deploy a Laravel application, and it's made by Laravel itself.

## Prerequisites

Before we deploy, there's a few things you'll need (or at least knowledge of things you'll need):

- A GitHub account—you can create that free at [github.com](http://github.com)
- Some basic Git knowledge—but don't worry, we'll walk through those commands together
- Your Laravel application from the previous lessons—you should have that ready to go

Now, it's possible your machine doesn't have Git installed. If that's the case, [git-scm.com](http://git-scm.com) is probably the best resource to get it installed.

## Step 1: Initialize Git and Push to GitHub

Alright, let's get your code into a Git repository. In your terminal, in the directory of your Laravel Chirper application, we're going to initialize a new Git repository:

```bash
git init
```

That way we have a repository ready for us to push to GitHub. Now let's add all of our files:

```bash
git add .
```

This adds everything to that Git commit. And now let's commit:

```bash
git commit -m "Our first Laravel app"
```

And because Laravel has `.gitignore` set up for us out of the box, we don't have to worry about pushing something that shouldn't be pushed to GitHub.

Now on [GitHub.com](http://GitHub.com), we're going to create a new repository:

1. Go to [github.com/new](http://github.com/new)
2. Select yourself as the owner
3. Name it "chirper" (or whatever you like)
4. You don't have to put a description if you don't want
5. Keep it public or private—your choice (I'm going to make mine private for now)
6. Don't initialize with any files—we already have our code
7. Click "Create repository"

All the other default settings should be fine.

GitHub gives us some commands that we can use—and this is exactly what we want. Copy these commands and paste them in your terminal:

```bash
git remote add origin <https://github.com/YOUR_USERNAME/chirper.git>
git branch -M main
git push -u origin main
```

If you refresh that GitHub repository page, you should see—yes!—there's all of our code, ready to be deployed on Laravel Cloud.

## Step 2: Sign Up for Laravel Cloud

So I'm going to head to [cloud.laravel.com](http://cloud.laravel.com). If you don't have a Laravel Cloud account already, you can sign up for one for free. It is free to get started—you do have to enter a credit card, which just means it's pay-as-you-go. So the amount of usage that your application uses, that's what you're going to be paying for.

Now, we're going to make this as cheap as possible for you when you push this application, but this is just to show you how easy it is to get this up and running. And it's great to see your application live out in the wild!

Once you're signed in, you'll see the Laravel Cloud dashboard. Time to deploy!

## Step 3: Create Your First Application

I'm going to click "New Application" and then you'll see any repositories that have been recently pushed to your GitHub account. And there it is—Chirper! I'm going to select that and create the application.

While there shouldn't be too much that you have to change here, let me explain a few things:

**Hibernation Settings:** If you're on the Growth plan (the paid plan) of Laravel Cloud, then your app cluster isn't going to be hibernated by default. You can see that would be $5 per month in compute for these particular settings. Now, if you're on the Starter plan (the pay-as-you-go plan that you sign up with), you'll have hibernation enabled by default. I'm going to turn that on and set it to 5 minutes. What that does is say "Hey, this could cost up to $5 a month if it doesn't hibernate throughout the month." Feel free to change that "hibernate after" number to as low as you'd like. That startup time is probably going to be around 30 seconds if no one has actually hit your application after it's been hibernating.

**Database Setup:** Now the only thing we have to do is add a resource. While we haven't used our database in our local environment yet, we're going to get a database up and running so it's ready for us when we do push these changes into production.

Click "Create and connect a database" → "Create new database cluster"

I'm going to use Laravel Serverless Postgres just so we can hibernate this database—because we're not going to be using it much, and it's just a fun application. That way it costs less for us. You can select a specific region (I'm just going to select US East), and then we have "Dev" which will hibernate after 300 seconds. This database cluster will cost between $0 and $25.55 per month. And since this is just a fun application, you probably won't even get close to that upper number.

If you did want to select the Laravel MySQL database, that's a flat fee—so the dev would be a flat fee of $6 per month. But again, just to get started, we're going to use the Serverless Postgres.

## Step 4: Deploy Your App

Now I'm going to click "Save and Deploy". So now that we have a database configured, Laravel Cloud is going to deploy our application—the code that we pushed to that GitHub repository. It's going to:

1. Configure everything
2. Install the dependencies
3. Set up that database and connect to it so we're ready to go
4. Configure our web server so this application is publicly accessible
5. Give us a domain—a URL that we can actually change if we want

While Laravel Cloud deploys this fairly quickly, you can also watch the progress in real-time. It's oddly satisfying!

And just like that—in about 39 seconds in my case—we have our application deployed!

## Step 5: Visit Your Live App

If I go to our environment, we'll see that Chirper URL that's automatically generated for us. Clicking on that brings us to our application.

And there we go! This is our application deployed to the cloud, and it looks identical to our development server. Boom! Your Laravel app is live on the internet. Share it with friends, family, or that neighbor who never believed you could build a web app.

## Auto-Deploy Magic

The neat part is Laravel Cloud has already set up this magic for us. So anytime we make any change and push it to GitHub, Laravel Cloud will grab those changes and make them available for us in our public version.

So why don't we do that right now? In your code, let's add another line. Make a small change to your `home.blade.php` file:

```html
<p>This is your brand new Laravel app. Time to make it sing (or chirp)!</p>
<p class="mt-2 text-sm text-gray-600">Now this is live on the internet! 🎉</p>
```

If we look at our local version, yes, we see this is available. But let's push it live! In your terminal:

```bash
git status  # Just to see that there's something that needs to be pushed
git add .
git commit -m "Our first Cloud auto deployment"
git push
```

What Laravel Cloud is doing now is taking that change and adding it to a new Laravel Cloud deployment. You can see that happen live at [cloud.laravel.com](http://cloud.laravel.com). You can see your latest deployment getting ready to be pushed up.

And then once this has completed—again in just under a minute—we should be able to refresh our live page and see that change. It's as simple as that!

## What Just Happened?

So we've taken our code and put it onto GitHub using Git version control. It's there ready for deployment, as well as safekeeping and collaboration. And then we pushed this code through that GitHub repository to Laravel Cloud. It's a live application that now exists on the internet for your friends, family, and loved ones to see!

You've just:

- Put your code under version control with Git
- Pushed it to GitHub for safekeeping and collaboration
- Deployed a real Laravel app to the internet
- Set up automatic deployments for future changes

And the great thing is, because of those automatic deployments, anytime you push new changes to your GitHub repository—more features that we add throughout this bootcamp—those changes will automatically be updated live on your site. No FTP, no manual server management, no headaches.

Next up: Let's look at how Laravel organizes code with what's known as the MVC pattern. It's time to level up from "it works" to "it works *beautifully*."
