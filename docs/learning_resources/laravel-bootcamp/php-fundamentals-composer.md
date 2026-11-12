# Laravel Learn - PHP Fundamentals: Composer

Source: https://laravel.com/learn/php-fundamentals/composer

---

Learn about PHP's package manager, how to manage dependencies, and set up projects professionally.

Composer is PHP's package manager and an essential tool for modern PHP development. It helps you manage your project's dependencies and autoload your classes. Almost every modern PHP project uses Composer - Laravel itself is installed via Composer, and popular packages like Guzzle (for HTTP requests), Carbon (for date handling), and PHPUnit (for testing) are all distributed through Composer.

You can find these packages and many more on [Packagist.org](http://Packagist.org), PHP's main package repository with over 300,000 packages available. Think of it as npm for PHP - it's where developers share and distribute their code.

Let's see how it works.

**Installing Composer**

First, you need Composer on your machine. If you followed our setup video, you already have it installed. You can verify this by running:

```bash
composer --version
```

**Creating a New Project**

Every PHP project with Composer starts with a composer.json file. You can create one manually or use:

```bash
composer init
```

This will walk you through a setup process to create your next composer project.

**Installing Dependencies**

To install a package, you can either:

```bash
composer require guzzlehttp/guzzle
```

Or add it to composer.json and run:

```bash
composer install
```

**Autoloading**

One of Composer's best features is autoloading. It automatically loads your PHP classes without requiring manual includes. You just have to tell composer about it. In your composer.json:

```json
{
  "autoload": {
    "psr-4": {
      "App\\\\": "src/"
    }
  }
}
```

Now your classes will be autoloaded:

```php
// src/User.php
namespace App;

class User {
    // Your code
}
```

When you start working with Laravel, you'll see that Composer is used extensively for managing packages and autoloading. It's a fundamental tool that makes modern PHP development possible.

In fact, Laravel itself is installed via Composer, which we'll cover in our Laravel series!
