Source: https://inertiajs.com/docs/v3/advanced/big-integers.md

# Big Integers

v3.8.0+Laravel Adapter v3.5.0+

Sometimes you may wish to pass integers that exceed JavaScript's safe integer range, such as IDs from a 64-bit database column. JavaScript rounds those values while parsing JSON, so `900719925474099988` reaches your components as `900719925474100000`. Big integer support keeps them exact by delivering them as native `BigInt` values, following the JSON convention [documented on MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt#use_within_json).

## Enabling Big Integers

Big integer support is disabled by default and is enabled entirely on the server, so there is nothing to configure on the client. You may enable it for every response in your `config/inertia.php` file, or through the `INERTIA_PRESERVE_BIG_INTEGERS` environment variable.

```php config/inertia.php theme={null}
'preserve_big_integers' => true,
```

Alternatively, you may enable it for a single response using the `preserveBigIntegers` method. This is useful when only a few pages of your application deal with large integers.

```php theme={null}
return Inertia::render('Orders/Show', [
    'order' => $order,
])->preserveBigIntegers();
```

Passing `false` opts a single response out, which is useful once the feature is enabled in your configuration file.

```php theme={null}
return Inertia::render('Reports/Index', $props)->preserveBigIntegers(false);
```

## How Values Are Transported

Integers outside the safe range are wrapped in a marker object before the response is encoded. The client turns that marker back into a `BigInt`, so your component receives the exact value.

```php theme={null}
return Inertia::render('Users/Show', [
    'id' => 900719925474099988,
]);

// The response carries {"$bigint": "900719925474099988"}
```

```vue Vue icon="vuejs" theme={null}
<script setup>
defineProps({ id: BigInt });
</script>

<template>
  <p>User {{ id }}</p>
  <!-- User 900719925474099988 -->
</template>
```

```jsx React icon="react" theme={null}
export default function Show({ id }) {
  return <p>User {String(id)}</p>;
  // User 900719925474099988
}
```

```svelte Svelte icon="s" theme={null}
<script>
  let { id } = $props();
</script>

<p>User {id}</p>
<!-- User 900719925474099988 -->
```

Integers within the safe range are left as regular numbers, so only the values that need it become a `BigInt`. The same prop may therefore arrive as a number or a `BigInt`, depending on its value. [Flash data](https://inertiajs.com/docs/v3/data-props/flash-data.md) receives the same treatment as props.

Markers are only revived on pages that enable big integer support, so applications that already send their own `{"$bigint": "..."}` objects continue to receive them as plain objects everywhere else.

## Objects and Classes

Arrays, plain objects, Eloquent models, collections, API resources, and values implementing `JsonSerializable` are all inspected for large integers, as are the public properties of your own classes. Built-in PHP classes such as `DateTime`, along with classes extending them, are passed through untouched, since they serialize through their own handlers.

## Submitting Big Integers

A `BigInt` submitted through the router, a form, or [Precognition](https://inertiajs.com/docs/v3/the-basics/forms.md#precognition) is sent as its digits, the same way form data and query strings send numbers. Your controller receives a numeric string, which validation rules such as `integer` and the request's `integer` method handle as usual.

```js theme={null}
router.post("/orders", { id: props.order.id });
```

```php theme={null}
public function store(Request $request)
{
    $request->validate(['id' => ['required', 'integer']]);

    $request->integer('id'); // 900719925474099988
}
```

The [`useHttp`](https://inertiajs.com/docs/v3/the-basics/http-requests) hook does not handle `BigInt` values, since it is commonly used to call third-party APIs. Convert those values to a string before sending them.

## Testing

Inertia's [testing helpers](https://inertiajs.com/docs/v3/advanced/testing.md#endpoint-tests) turn markers back into integers, so you may assert against the same values you passed to the response.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->where('order.id', 900719925474099988)
);

$response->inertiaProps('order.id'); // 900719925474099988
```
