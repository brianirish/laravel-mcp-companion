# Laravel Learn - PHP Fundamentals: Functions

Source: https://laravel.com/learn/php-fundamentals/functions

---

Master function creation and usage in PHP, including modern features like type declarations and anonymous functions.

Functions are essential building blocks in PHP. They help us organize code, make it reusable, and prevent repetition. Let's explore how they work and what makes them special in PHP.

**Basic Function Syntax**

Creating a function in PHP starts with the ⁠function keyword, followed by the name and parentheses. The name should describe what the function does:

```php
function sayHello() {
	echo "Hello!";
}

// Call the function
sayHello();
```

**Parameters and Arguments**

Functions become more useful when they can work with different values. We can pass data to functions through parameters:

```php
function greet($name) {
	echo "Hello, $name!";
}

greet("John");    // outputs: Hello, John!

// Multiple parameters
function add($a, $b) {
	return $a + $b;
}

$result = add(5, 3);    // returns: 8
```

**Return Values**

Functions can send back results using the ⁠return statement. A function can return any type of data - numbers, strings, arrays, or even other functions:

```php
function getStatus($score) {
	if ($score >= 75) {
		return "Passed";
	}
	
	return "Failed";
}

$status = getStatus(80);    // returns: "Passed"
```

**Default Parameter Values**

PHP allows you to set default values for parameters. If an argument isn't provided, the default value is used:

```php
function greet($name = "Guest") {
	echo "Hello, $name!";
}

greet();          // outputs: Hello, Guest!
greet("John");    // outputs: Hello, John!
```

**Type Declarations**

Since PHP 7, you can specify types for parameters and return values. This helps catch errors early and makes code more reliable:

```php
function add(int $a, int $b): int {
	return $a + $b;
}

function getUserName(array $user): string {
	return $user['name'];
}
```

**Anonymous Functions (Closures)**

PHP also supports anonymous functions, often used for callbacks or when a function is used only once:

```php
$greet = function($name) {
echo "Hello, $name!";
};

$greet("John");    // outputs: Hello, John!
```
