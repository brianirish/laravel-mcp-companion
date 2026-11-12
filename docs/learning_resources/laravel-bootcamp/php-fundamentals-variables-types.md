# Laravel Learn - PHP Fundamentals: Variables & Types

Source: https://laravel.com/learn/php-fundamentals/variables-types

---

Learn about PHP's basic types, variable declarations, and type handling. See how PHP manages strings, numbers, and other data types.

PHP variables always start with a $ symbol. This makes them easy to spot in your code. PHP variables can hold any type of data, and you don't need to declare types upfront - you can change a variable's type simply by assigning a different kind of value to it.

```php
$status = 404;  // integer      

$status = "active"; // sting

$status = true; // boolean
```

**Strings**

Strings in PHP are similar to what you might know from other languages. You can create them with single or double quotes. The main difference is that double quotes allow you to embed variables directly in your string, while single quotes treat everything as literal text. Strings can be combined using the dot (.) operator:

```php
$name = 'John'; // John
$greeting = "Hello $name";    // Hello John
$greeting = 'Hello $name';    // Hello $name

// You can chain multiple strings
$fullName = 'John' . ' ' . 'Doe';   // Results in: John Doe
```

**Numbers**

PHP has two numeric types you'll commonly use:

```php
$age = 25;           // Integer
$price = 19.99;      // Float (also called double)
```

**Booleans**

In PHP, like in many other programming languages, a boolean represents two possible values: true or false.

```php
$isActive = true;
$isDeleted = false;
```

**Type Casting**

PHP allows you to explicitly convert (cast) variables from one type to another. This is similar to JavaScript's parseInt or toString, but PHP uses a simpler syntax:

```php
$price = "19.99";    // string
$age = (int) $price;   // converts to 19
$isActive = (bool) 1;  // converts to true
$text = (string) 42;   // converts to "42"
```

PHP also performs automatic type coercion, similar to JavaScript. This means PHP will automatically convert types when needed:

```php
$result = "123" + 456;    // "123" becomes integer, result is 579
$sum = 42 . " items";     // 42 becomes string "42 items"
if ("hello") {            // string is coerced to true
	// this runs
}
```
