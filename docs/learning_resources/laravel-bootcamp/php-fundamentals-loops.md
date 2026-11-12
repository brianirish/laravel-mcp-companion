# Laravel Learn - PHP Fundamentals: Loops

Source: https://laravel.com/learn/php-fundamentals/loops

---

Understand different ways to iterate through data in PHP, with focus on the powerful foreach loop and practical use cases.

Loops are fundamental in any programming language, allowing us to repeat actions and work with collections of data. Let's explore the different types of loops in PHP and see how they're commonly used.

**The foreach Loop**

Let's start with ⁠foreach, as it's the most commonly used loop in modern PHP, especially when working with arrays:

```php
$colors = ['red', 'blue', 'green'];

foreach ($colors as $color) {
	echo $color;
}

// Or...
$invoiceItems = [
    ['item' => 'Laptop', 'price' => 1200],
    ['item' => 'Mouse', 'price' => 75],
    ['item' => 'Keyboard', 'price' => 100]
];

$total = 0;
foreach ($invoiceItems as $item) {
    $total += $item['price']; // shortcut for $total = $total + $item['price'];
}
```

**The for Loop**

When you need more control over the iteration process, the ⁠for loop is your friend:

```php
for ($i = 0; $i < 5; $i++) {
	echo $i;
}

// Counting backwards (like for a countdown)
for ($i = 10; $i > 0; $i--) {
    echo "$i seconds remaining...";
}
```

**While and Do-While Loops**

These loops continue as long as a condition is true:

```php
$count = 0;
while ($count < 5) {
	echo $count;
	
	$count++;
}

// Do-while executes at least once
do {
	echo $count;
	$count++;
} while ($count < 5);
```

**Breaking and Continuing**

You can control loop execution with ⁠break and ⁠continue:

```php
$users = [
    ['name' => 'John', 'newsletter' => true],
    ['name' => 'Jane', 'newsletter' => false],
    ['name' => 'Bob', 'newsletter' => true]
];

foreach ($users as $user) {
    if (!$user['newsletter']) {
        continue;    // Skip users who didn't subscribe
    }
    
    sendNewsletter($user);
}

// Simple break example
$numbers = [1, 2, 3, 4, 5];
foreach ($numbers as $number) {
    if ($number === 3) {
        break;    // Stop the loop
    }
    echo $number;
}
```

While break exists and is shown here for completeness, in modern PHP you'll often find better approaches using array functions or early returns in functions.

**A Glimpse into Laravel Collections**

When you start working with Laravel, you'll discover Collections, which provide a more elegant way to work with arrays. Here's a little teaser:

```php
// Regular PHP loop
$numbers = [1, 2, 3, 4, 5];
$doubled = [];

foreach ($numbers as $number) {
	$doubled[] = $number * 2;
}

// With Laravel Collections
$doubled = collect([1, 2, 3, 4, 5])->map(fn($number) => $number * 2);
```

Here's another example showing more Collection power:

```php
$users = collect([
	['name' => 'John', 'active' => false],
	['name' => 'Jane', 'active' => true],
	['name' => 'Bob', 'active' => true]
]);

$users
	->filter(fn($user) => $user['active'])
	->each(fn($user) => User::create($user));
```

In this example, we filter out inactive users and create database entries only for active ones - all in just two lines of code. This is the power of Collections: they make complex operations readable and concise.

Collections make data manipulation more readable and maintainable. We'll explore them in detail when we get to Laravel, but it's good to understand the basic loops first as they're the foundation.
