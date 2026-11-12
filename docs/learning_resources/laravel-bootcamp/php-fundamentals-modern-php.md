# Laravel Learn - PHP Fundamentals: Modern PHP

Source: https://laravel.com/learn/php-fundamentals/modern-php

---

Explore PHP's modern features like constructor property promotion, match expressions, and nullsafe operators.

PHP has evolved significantly in recent years. Let's look at some modern features that make PHP code cleaner, safer, and more enjoyable to write. These features are especially relevant when working with frameworks like Laravel.

**Performance Improvements**

PHP 8 brought significant performance improvements through various optimizations in its core engine. Modern PHP applications run noticeably faster, making PHP a strong choice for web development in 2025.

**Constructor Property Promotion (PHP 8.0)**

One of the most welcome improvements in modern PHP is constructor property promotion. It eliminates the boilerplate code of declaring properties and then assigning them in the constructor. This is particularly useful for data objects and simple classes:

```php
// Old way
class User {
	public string $name;
	public string $email;

	public function __construct(string $name, string $email) {
	    $this->name = $name;
	    $this->email = $email;
	}

}

// Modern way
class User {
	public function __construct(
		public string $name,
		public string $email,
	) {}
}
```

**Readonly Properties (PHP 8.1)**

Readonly properties add an extra layer of safety to your code. Once a property is set in the constructor, it cannot be changed. This is great for values that should remain constant throughout an object's lifetime, like IDs, dates of creation, or configuration values:

```php
class Price {
	public function __construct(
		public readonly float $amount,
		public readonly string $currency
	) {}
}
```

**Match Expression (PHP 8.0)**

The match expression is a modern replacement for the switch statement. It's more concise, returns values directly, and does strict comparisons by default. It's perfect for mapping values or handling different cases:

```php
// Old way with switch
switch ($status) {
    case 200:
        $result = 'success';
        break;
    case 404:
        $result = 'not found';
        break;
    case 500:
        $result = 'server error';
        break;
    default:
        $result = 'unknown status';
}

// Modern way with match
$result = match ($status) {
    200 => 'success',
    404 => 'not found',
    500 => 'server error',
    default => 'unknown status'
};
```

**Nullsafe Operator (PHP 8.0)**

The nullsafe operator (?->) helps prevent null reference errors when accessing properties or methods in a chain. It's particularly useful when working with optional relationships or nested data structures:

```php
// Old way
$country = null;

if ($user !== null) {
	if ($user->getAddress() !== null) {
		$country = $user->getAddress()->getCountry();
	}
}

// Modern way
$country = $user?->getAddress()?->getCountry();
```

**Named Arguments (PHP 8.0)**

Named arguments make function and method calls more explicit and self-documenting. They're especially useful when dealing with multiple optional parameters or when the parameter names are important for understanding:

```php
$user = new User("John", "[john@example.com](<mailto:john@example.com>)");

// Works the same
$user = new User(
	name: "John",
	email: "[john@example.com](<mailto:john@example.com>)"
);
```

**Typed Properties (PHP 7.4)**

Type declarations for properties help catch errors early and make code more reliable. PHP will ensure that only values of the correct type can be assigned to these properties:

```php
class User {
	public string $name;
	public int $age;
	public ?string $email = null;  // Nullable string
}
```

These modern features make PHP code:

- More concise and expressive
- Safer with better type checking
- Easier to read and maintain
- Less prone to errors
