# Laravel Learn - PHP Fundamentals: Arrays

Source: https://laravel.com/learn/php-fundamentals/arrays

---

Explore PHP's versatile arrays, which can serve as both numbered lists and key-value stores. Perfect for handling structured data.

Arrays are one of PHP's most powerful features. If you're coming from JavaScript, you'll find them particularly interesting as they combine the functionality of both JavaScript arrays and objects. While PHP also uses objects for holding data (which we'll explore in our Classes video), arrays are incredibly versatile and widely used. Let's explore how they work.

**Basic Array Types**

In PHP, we have two main types of arrays. First, there are numeric arrays (similar to JavaScript arrays), which use numbers as their keys starting from 0. Then we have associative arrays, which use named keys (similar to JavaScript objects). The great thing about PHP arrays is that they can also mix both styles.

Let's look at some examples:

```php
// Numeric array
$colors = ['red', 'blue', 'green'];

// Associative array
$user = [
	'name' => 'John',
	'age' => 25
];

// Mixed array
$mixed = [
	42,                  // index 0
	'key' => 'value',    // key 'key'
	'another value'      // index 1
];
```

**Creating Arrays**

PHP gives us multiple ways to create arrays. While the square bracket syntax [] is most common in modern PHP, you might also see the array() syntax in older code:

```php
// Modern syntax
$array1 = ['a', 'b', 'c'];

// Creating with specific keys
$user = [
	'name' => 'John',
	'age' => 25
];
```

**Working with Arrays**

Accessing array elements is straightforward. For numeric arrays, we use the index number, and for associative arrays, we use the key name:

```php
$colors = ['red', 'blue', 'green'];
echo $colors[0];    // outputs: red

$user = ['name' => 'John', 'age' => 25];
echo $user['name']; // outputs: John
```

Arrays can also be nested, allowing you to create more complex data structures:

```php
$blogPost = [
    'title' => 'Getting Started with PHP',
    'author' => [
        'name' => 'John',
        'role' => 'editor'
    ],
    'comments' => [
        ['user' => 'Jane', 'text' => 'Great article!'],
        ['user' => 'Bob', 'text' => 'Thanks for sharing']
    ]
];

echo $blogPost['title'];                  // outputs: Getting Started with PHP
echo $blogPost['author']['name'];         // outputs: John
echo $blogPost['comments'][0]['text'];    // outputs: Great article!
```

**Common Operations**

PHP provides many ways to work with arrays. Here are some operations you'll use frequently

```php
// Adding elements
$colors[] = 'yellow';           // Add to numeric array
$user['email'] = 'john@example.com';  // Add to associative array

// Checking elements
isset($user['email']);          // Check if key exists
in_array('red', $colors);       // Check if value exists

// Array size
count($colors);                 // Get number of elements

// Remove elements
unset($user['email']);          // Remove specific element
```

**Real World Example**

Let's look at a practical example that you might encounter when working with data in a web application:

```php
$post = [
	'title' => 'Getting Started with PHP',
	'author' => [
		'name' => 'John Doe',
		'role' => 'editor'
	],
	'tags' => ['php', 'beginner', 'tutorial'],
	'published' => true,
	'comments' => [
		[
			'user' => 'Jane',
			'message' => 'Great article!'
		],
		[
			'user' => 'Mike',
			'message' => 'Thanks for sharing'
		]
	]
];
```

This structure shows how arrays can handle complex data with different types and nested information - something you'll often use when working with databases, APIs, or configuration files.
