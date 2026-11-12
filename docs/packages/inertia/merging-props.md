Source: https://inertiajs.com/docs/v3/data-props/merging-props.md

# Merging Props

Inertia overwrites props with the same name when reloading a page. However, you may need to merge new data with existing data instead. For example, when implementing a "load more" button for paginated results. The [Infinite scroll](https://inertiajs.com/docs/v3/data-props/infinite-scroll.md) component uses prop merging under the hood.

Prop merging only works during [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md). Full page visits will always replace props entirely, even if you've marked them for merging.

## Merge Methods

To merge a prop instead of overwriting it, you may use the `Inertia::merge()` method when returning your response.

```php theme={null}
Route::get('/items', function () {
    // Static array of tags...
    $allTags = [
        'Laravel', 'React', 'Vue', 'Tailwind', 'Inertia',
        'PHP', 'JavaScript', 'TypeScript', 'Docker', 'Vite',
    ];

    // Get chunk of tags by page...
    $page = request()->input('page', 1);
    $perPage = 5;
    $offset = ($page - 1) * $perPage;
    $tags = array_slice($allTags, $offset, $perPage);

    return Inertia::render('Tags/Index', [
        'tags' => Inertia::merge($tags),
    ]);
});
```

The `Inertia::merge()` method will append new items to existing arrays at the root level. You may change this behavior to prepend items instead.

```php theme={null}
// Append at root level (default)...
Inertia::merge($items);

// Prepend at root level...
Inertia::merge($items)->prepend();
```

For more precise control, you can target specific nested properties for merging while replacing the rest of the object.

```php theme={null}
// Only append to the 'data' array, replace everything else...
Inertia::merge(User::paginate())->append('data');

// Prepend to the 'messages' array...
Inertia::merge($chatData)->prepend('messages');
```

You can combine multiple operations and target several properties at once.

```php theme={null}
Inertia::merge($forumData)
    ->append('posts')
    ->prepend('announcements');

// Target multiple properties...
Inertia::merge($dashboardData)
    ->append(['notifications', 'activities']);
```

On the client side, Inertia handles all the merging automatically according to your server-side configuration.

## Matching Items

When merging arrays, you may use the `matchOn` parameter to match existing items by a specific field and update them instead of appending new ones.

```php theme={null}
// Match posts by ID, update existing ones...
Inertia::merge($postData)->append('data', matchOn: 'id');

// Multiple properties with different match fields...
Inertia::merge($complexData)->append([
    'users.data' => 'id',
    'messages' => 'uuid',
]);
```

In the first example, Inertia will iterate over the `data` array and attempt to match each item by its `id` field. If a match is found, the existing item will be replaced. If no match is found, the new item will be appended.

## Deep Merge

Instead of specifying which nested paths should be merged, you may use `Inertia::deepMerge()` to ensure a deep merge of the entire structure.

```php theme={null}
Route::get('/chat', function () {
    $chatData = [
        'messages' => [
            ['id' => 4, 'text' => 'Hello there!', 'user' => 'Alice'],
            ['id' => 5, 'text' => 'How are you?', 'user' => 'Bob'],
        ],
        'online' => 12,
    ];

    return Inertia::render('Chat', [
        'chat' => Inertia::deepMerge($chatData)->matchOn('messages.id'),
    ]);
});
```

`Inertia::deepMerge()` was introduced before `Inertia::merge()` had support for prepending and targeting nested paths. In most cases, `Inertia::merge()` with its append and prepend methods should be sufficient.

## Client-Side Visits

You can also merge props directly on the client side without making a server request using [client side visits](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#client-side-visits). Inertia provides [prop helper methods](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#prop-helpers) that allow you to append, prepend, or replace prop values.

## Combining with Deferred Props

You may combine [deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props.md) with mergeable props to defer the loading of the prop and ultimately mark it as mergeable once it's loaded.

```php theme={null}
Route::get('/users', function () {
    $page = request()->input('page', 1);
    $perPage = request()->input('per_page', 10);

    return Inertia::render('Users/Index', [
        'results' => Inertia::defer(fn() => User::paginate($perPage, page: $page))->deepMerge(),
    ]);
});
```

## Combining with Once Props

You may chain the `once()` modifier onto a merge prop to ensure the data is resolved only once and remembered by the client across subsequent navigations.

```php theme={null}
return Inertia::render('Users/Index', [
    'activity' => Inertia::merge(fn () => $user->recentActivity())->once(),
]);
```

For more information on once props, see the [once props](https://inertiajs.com/docs/v3/data-props/once-props.md) documentation.

## Resetting Props

On the client side, you can indicate to the server that you would like to reset the prop. This is useful when you want to clear the prop value before merging new data, such as when the user enters a new search query on a paginated list.

The `reset` request option accepts an array of the prop keys you would like to reset.

```js theme={null}
router.reload({
  reset: ["results"],
  // ...
});
```
