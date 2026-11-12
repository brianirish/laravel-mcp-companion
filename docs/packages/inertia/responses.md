Source: https://inertiajs.com/docs/v3/the-basics/responses.md

# Responses

## Creating Responses

Creating an Inertia response is simple. To get started, invoke the `Inertia::render()` method within your controller or route, providing both the name of the [JavaScript page component](https://inertiajs.com/docs/v3/the-basics/pages.md) that you wish to render, as well as any properties (data) for the page.

In the example below, we will pass a single property (`event`) which contains four attributes (`id`, `title`, `start_date` and `description`) to the `Event/Show` page component.

```php theme={null}
use Inertia\Inertia;

class EventsController extends Controller
{
    public function show(Event $event)
    {
        return Inertia::render('Event/Show', [
            'event' => $event->only(
                'id',
                'title',
                'start_date',
                'description'
            ),
        ]);

        // Alternatively, you can use the inertia() helper...
        return inertia('Event/Show', [
            'event' => $event->only(
                'id',
                'title',
                'start_date',
                'description'
            ),
        ]);
    }
}
```

The component name may also be a Backed Enum, which is useful for organizing page components with type-safe references.

```php theme={null}
enum Page: string
{
    case EventShow = 'Event/Show';
    case EventIndex = 'Event/Index';
}

return Inertia::render(Page::EventShow, [
    'event' => $event,
]);
```

> [!TIP]
>
> To ensure that pages load quickly, only return the minimum data required for
> the page.

> [!NOTE]
>
> Be aware that all data returned from the controllers will be visible
> client-side, so be sure to omit sensitive information.

## Properties

To pass data from the server to your page components, you can use properties. You can pass various types of values as props, including primitive types, arrays, objects, and several Laravel-specific types that are automatically resolved:

```php theme={null}
use App\Models\User;
use Illuminate\Http\Resources\Json\JsonResource;

Inertia::render('Dashboard', [
    // Primitive values
    'title' => 'Dashboard',
    'count' => 42,
    'active' => true,

    // Arrays and objects
    'settings' => ['theme' => 'dark', 'notifications' => true],

    // Arrayable objects (Collections, Models, etc.)
    'user' => auth()->user(), // Eloquent model
    'users' => User::all(), // Eloquent collection

    // API Resources
    'profile' => new UserResource(auth()->user()),

    // Responsable objects
    'data' => new JsonResponse(['key' => 'value']),

    // Closures
    'timestamp' => fn() => now()->timestamp,
]);
```

Arrayable objects like Eloquent models and collections are automatically converted using their `toArray()` method. Responsable objects like API resources and JSON responses are resolved through their `toResponse()` method.

Integers outside JavaScript's safe range lose precision in the browser. You may preserve them as native `BigInt` values using [big integer support](https://inertiajs.com/docs/v3/advanced/big-integers.md).

## `ProvidesInertiaProperty` Interface

When passing props to your components, you may want to create custom classes that can transform themselves into the appropriate data format. While Laravel's `Arrayable` interface simply converts objects to arrays, Inertia offers the more powerful `ProvidesInertiaProperty` interface for context-aware transformations.

This interface requires a `toInertiaProperty` method that receives a `PropertyContext` object containing the property key (`$context->key`), all props for the page (`$context->props`), and the request instance (`$context->request`).

```php theme={null}
use Inertia\PropertyContext;
use Inertia\ProvidesInertiaProperty;

class UserAvatar implements ProvidesInertiaProperty
{
    public function __construct(protected User $user, protected int $size = 64)
    {
        //
    }

    public function toInertiaProperty(PropertyContext $context): mixed
    {
        return $this->user->avatar
            ? Storage::url($this->user->avatar)
            : "https://ui-avatars.com/api/?name={$this->user->name}&size={$this->size}";
    }
}
```

Once defined, you can use this class directly as a prop value.

```php theme={null}
Inertia::render('Profile', [
    'user' => $user,
    'avatar' => new UserAvatar($user, 128),
]);
```

The `PropertyContext` gives you access to the property key, which enables powerful patterns like merging with shared data.

```php theme={null}
use Inertia\Inertia;
use Inertia\PropertyContext;
use Inertia\ProvidesInertiaProperty;

class MergeWithShared implements ProvidesInertiaProperty
{
    public function __construct(protected array $items = [])
    {
        //
    }

    public function toInertiaProperty(PropertyContext $context): mixed
    {
        // Access the property key to get shared data
        $shared = Inertia::getShared($context->key, []);

        // Merge with the new items
        return array_merge($shared, $this->items);
    }
}

// Usage
Inertia::share('notifications', ['Welcome back!']);

return Inertia::render('Dashboard', [
    'notifications' => new MergeWithShared(['New message received']),
    // Result: ['Welcome back!', 'New message received']
]);
```

## `ProvidesInertiaProperties` Interface

In some situations you may want to group related props together for reusability across different pages. You can accomplish this by implementing the `ProvidesInertiaProperties` interface.

This interface requires a `toInertiaProperties` method that returns an array of key-value pairs. The method receives a `RenderContext` object containing the component name (`$context->component`) and request instance (`$context->request`).

```php theme={null}
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;
use Inertia\RenderContext;
use Inertia\ProvidesInertiaProperties;

class UserPermissions implements ProvidesInertiaProperties
{
    public function __construct(#[CurrentUser] protected User $user)
    {
        //
    }

    public function toInertiaProperties(RenderContext $context): array
    {
        return [
            'canEdit' => $this->user->can('edit'),
            'canDelete' => $this->user->can('delete'),
            'canPublish' => $this->user->can('publish'),
            'isAdmin' => $this->user->hasRole('admin'),
        ];
    }
}
```

You can use these prop classes directly in the `render()` and `with()` methods.

```php theme={null}
public function index(UserPermissions $permissions)
{
    return Inertia::render('UserProfile', $permissions);

    // or...

    return Inertia::render('UserProfile')->with($permissions);
}
```

You can also combine multiple prop classes with other props in an array:

```php theme={null}
public function index(UserPermissions $permissions)
{
    return Inertia::render('UserProfile', [
        'user' => auth()->user(),
        $permissions,
    ]);

    // or using method chaining...

    return Inertia::render('UserProfile')
        ->with('user', auth()->user())
        ->with($permissions);
}
```

## Root Template Data

There are situations where you may want to access your prop data in your application's root Blade template. For example, you may want to add a meta description tag, Twitter card meta tags, or Facebook Open Graph meta tags. You can access this data via the `$page` variable.

```blade theme={null}
<meta name="twitter:title" content="{{ $page['props']['event']->title }}">
```

Sometimes you may even want to provide data to the root template that will not be sent to your JavaScript page component. This can be accomplished by invoking the `withViewData` method.

```php theme={null}
return Inertia::render('Event', ['event' => $event])
    ->withViewData(['meta' => $event->meta]);
```

After invoking the `withViewData` method, you can access the defined data as you would typically access a Blade template variable.

```blade theme={null}
<meta name="description" content="{{ $meta }}">
```

## Maximum Response Size

To enable client-side history navigation, all Inertia server responses are stored in the browser's history state. However, keep in mind that some browsers impose a size limit on how much data can be saved within the history state.

For example, [Firefox](https://developer.mozilla.org/en-US/docs/Web/API/History/pushState) has a size limit of 16 MiB and throws a `NS_ERROR_ILLEGAL_VALUE` error if you exceed this limit. Typically, this is much more data than you'll ever practically need when building applications.
