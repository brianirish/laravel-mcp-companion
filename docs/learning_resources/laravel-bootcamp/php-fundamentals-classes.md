# Laravel Learn - PHP Fundamentals: Classes

Source: https://laravel.com/learn/php-fundamentals/classes

---

Get started with object-oriented programming in PHP, learning about classes, properties, and methods with real-world examples.

Classes are a fundamental part of modern PHP development. Think of a class as a blueprint - it defines what properties (data) and methods (functions) your objects will have. Objects in PHP help you organize related data and functionality together in a reusable way.

**Basic Class Structure**

Let's start with a simple example:

```php
class Product
{
    public string $name;
    public float $price;
    
    public function isExpensive(): bool
    {
        return $this->price > 100;
    }
}

$product = new Product();
$product->name = "Phone";
$product->price = 99.99;

echo $product->name; // returns “Phone”
var_dump($product->isExpensive());  // returns false
```

This simple example shows the basic components of a class: • Properties ($name, $price) store data

• Methods (isExpensive()) define behavior

• The $this keyword refers to the current object

**Constructor Method**

We can make our class better by using a constructor - a special method that runs when creating a new object. It lets you add data while creating a new object instance:

```php
class Product
{
	public function __construct(
		public string $name,
		public float $price
    ) {}
}

$product = new Product("Phone", 99.99);
```

**Access Levels**

PHP provides three visibility levels for properties and methods:

```php
class Product
{
	public string $name;      // Accessible from anywhere
	private float $price;     // Only inside this class
	protected bool $active;   // Inside this class and child classes
}
```

**Inheritance**

Classes can inherit properties and methods from other classes. This is useful when you have similar types of objects that share common features but need some additional functionality. Instead of duplicating code, you can extend a base class:

```php
class Product 
{
    public function __construct(
        public string $name,
        public float $price
    ) {}

    public function hasDiscount(): bool 
    {
        return $this->price < 100;
    }

    public function getDescription(): string 
    {
        return "{$this->name} costs {$this->price}€";
    }
}

class DigitalProduct extends Product 
{
    public function __construct(
        public string $name,
        public float $price,
        public string $downloadLink
    ) {}

    public function download(): string 
    {
        return "Downloading {$this->name} from {$this->downloadLink}";
    }
}

$course = new DigitalProduct('PHP Course', 99.99, 'course.zip');
echo $course->getDescription();  // inherited method
echo $course->hasDiscount();     // inherited method
echo $course->download();        // new method
```

When you start working with Laravel, you'll use classes extensively. Every model, controller, and service in Laravel is a class. This foundation will help you understand Laravel's structure better.
