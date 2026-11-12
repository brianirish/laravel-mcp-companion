Source: https://inertiajs.com/docs/v3/advanced/testing.md

# Testing

There are many different ways to test an Inertia application. This page provides a quick overview of the tools available.

## End-to-end Tests

One popular approach to testing your JavaScript page components is to use an end-to-end testing tool like [Cypress](https://www.cypress.io/) or [Pest](https://pestphp.com). These are browser automation tools that allow you to run real simulations of your app in the browser. These tests are known to be slower; however, since they test your application at the same layer as your end users, they can provide a lot of confidence that your app is working correctly. And, since these tests are run in the browser, your JavaScript code is actually executed and tested as well.

## Client-Side Unit Tests

Another approach to testing your page components is to use a client-side unit testing framework, such as [Vitest](https://vitest.dev/), [Jest](https://jestjs.io/), or [Mocha](https://mochajs.org/). This approach allows you to test your JavaScript page components in isolation using Node.js.

## Endpoint Tests

In addition to testing your JavaScript page components, you will likely want to also test the Inertia responses that are returned by your server-side framework. A popular approach to doing this is using endpoint tests, where you make requests to your application and examine the responses. Laravel [provides tooling](https://laravel.com/docs/http-tests) for executing these types of tests.

However, to make this process even easier, Inertia's Laravel adapter provides additional HTTP testing tools. Let's take a look at an example.

```php theme={null}
use Inertia\Testing\AssertableInertia as Assert;

class PodcastsControllerTest extends TestCase
{
    public function test_can_view_podcast()
    {
        $this->get('/podcasts/41')
            ->assertInertia(fn (Assert $page) => $page
                ->component('Podcasts/Show')
                ->has('podcast', fn (Assert $page) => $page
                    ->where('id', $podcast->id)
                    ->where('subject', 'The Laravel Podcast')
                    ->where('description', 'The Laravel Podcast brings you Laravel and PHP development news and discussion.')
                    ->has('seasons', 4)
                    ->has('seasons.4.episodes', 21)
                    ->has('host', fn (Assert $page) => $page
                        ->where('id', 1)
                        ->where('name', 'Matt Stauffer')
                    )
                    ->has('subscribers', 7, fn (Assert $page) => $page
                        ->where('id', 2)
                        ->where('name', 'Claudio Dekker')
                        ->where('platform', 'Apple Podcasts')
                        ->etc()
                        ->missing('email')
                        ->missing('password')
                    )
                )
            );
    }
}
```

As you can see in the example above, you may use these assertion methods to assert against the content of the data provided to the Inertia response. In addition, you may assert that array data has a given length as well as scope your assertions.

You may use the `inertiaProps` method to retrieve the props returned in the response. You can pass a key to retrieve a specific property, and nested properties are supported using "dot" notation.

```php theme={null}
$response = $this->get('/podcasts/41');

// Returns all props...
$response->inertiaProps();

// Returns a specific prop...
$response->inertiaProps('podcast');

// Returns a nested prop using "dot" notation...
$response->inertiaProps('podcast.id');
```

Let's dig into the `assertInertia` method and the available assertions in detail. First, to assert that the Inertia response has a property, you may use the `has` method. You can think of this method as being similar to PHP's `isset` function.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    // Checking if a root-level property has 7 items...
    ->has('podcasts', 7)

    // Checking nested properties using "dot" notation...
    ->has('podcast.subscribers', 7)
);
```

To assert that an Inertia property has a specified number of items, you may provide the expected size as the second argument to the `has` method.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    // Checking if a root-level property has 7 items...
    ->has('podcasts', 7)

    // Checking nested properties using "dot" notation...
    ->has('podcast.subscribers', 7)
);
```

The `has` method may also be used to scope properties in order to lessen repetition when asserting against nested properties.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    // Creating a single-level property scope...
    ->has('message', fn (Assert $page) => $page
        // We can now continue chaining methods...
        ->has('subject')
        ->has('comments', 5)

        // And can even create a deeper scope using "dot" notation...
        ->has('comments.0', fn (Assert $page) => $page
            ->has('body')
            ->has('files', 1)
            ->has('files.0', fn (Assert $page) => $page
                ->has('url')
            )
        )
    )
);
```

When scoping into Inertia properties that are arrays or collections, you may also assert that a specified number of items are present in addition to scoping into the first item.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    // Assert that there are 5 comments and automatically scope into the first comment...
    ->has('comments', 5, fn (Assert $page) => $page
        ->has('body')
        // ...
    )
);
```

To assert that an Inertia property has an expected value, you may use the `where` assertion.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('message', fn (Assert $page) => $page
        // Assert that the subject prop matches the given message...
        ->where('subject', 'This is an example message')

        // Or, assert against deeply nested values...
        ->where('comments.0.files.0.name', 'example-attachment.pdf')
    )
);
```

Inertia's testing methods will automatically fail when you haven't interacted with at least one of the props in a scope. While this is generally useful, you might run into situations where you're working with unreliable data (such as from an external feed), or with data that you really don't want interact with in order to keep your test simple. For these situations, the `etc` method exists.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('message', fn (Assert $page) => $page
        ->has('subject')
        ->has('comments')
        ->etc()
    )
);
```

The `missing` method is the exact opposite of the `has` method, ensuring that the property does not exist. This method makes a great companion to the `etc` method.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('message', fn (Assert $page) => $page
        ->has('subject')
        ->missing('published_at')
        ->etc()
    )
);
```

### Testing Partial Reloads

You may use the `reloadOnly` and `reloadExcept` methods to test how your application responds to [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md). These methods perform a follow-up request and allow you to make assertions against the response.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('orders')
    ->missing('statuses')
    ->reloadOnly('statuses', fn (Assert $reload) => $reload
        ->missing('orders')
        ->has('statuses', 5)
    )
);
```

Instead of passing a single prop as a string, you may also pass an array of props to `reloadOnly` or `reloadExcept`.

### Testing Deferred Props

You may use the `loadDeferredProps` method to test how your application responds to [deferred props](https://inertiajs.com/docs/v3/data-props/deferred-props.md). This method performs a follow-up request to load the deferred props and allows you to make assertions against the response.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('users')
    ->has('roles')
    ->missing('permissions') // Deferred prop not in initial response
    ->loadDeferredProps(fn (Assert $reload) => $reload
        ->has('permissions')
        ->where('permissions.0.name', 'edit users')
    )
);
```

You may also load specific deferred prop groups by passing the group name as the first argument to the `loadDeferredProps` method.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->has('users')
    ->missing('teams')
    ->missing('projects')
    ->loadDeferredProps('attributes', fn (Assert $reload) => $reload
        ->has('teams', 5)
        ->has('projects')
        ->missing('permissions') // Different group
    )
);
```

Instead of passing a single group as a string, you may also pass an array of groups to `loadDeferredProps`.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    ->loadDeferredProps(['default', 'attributes'], fn (Assert $reload) => $reload
        ->has('permissions')
        ->has('teams')
        ->has('projects')
    )
);
```

### Testing Flash Data

You may use the `hasFlash` and `missingFlash` methods to test [flash data](https://inertiajs.com/docs/v3/data-props/flash-data.md) in your Inertia responses.

```php theme={null}
$response->assertInertia(fn (Assert $page) => $page
    // Assert flash data exists...
    ->hasFlash('message')

    // Assert flash data has a specific value...
    ->hasFlash('message', 'Item saved!')

    // Nested values are supported using "dot" notation...
    ->hasFlash('notification.type', 'success')

    // Assert flash data does not exist...
    ->missingFlash('error')
);
```

#### Redirect Responses

The `hasFlash` and `missingFlash` methods above only work on rendered Inertia page responses. For redirect responses, you may use the `assertInertiaFlash` and `assertInertiaFlashMissing` methods directly on the test response to assert against the session's flash data.

```php theme={null}
$response = $this->post('/users');

$response->assertRedirect('/dashboard')
    ->assertInertiaFlash('message')
    ->assertInertiaFlash('message', 'User created!')
    ->assertInertiaFlash('notification.type', 'success')
    ->assertInertiaFlashMissing('error');
```

## Disabling SSR During Tests

Your application may have [SSR enabled](https://inertiajs.com/docs/v3/advanced/server-side-rendering.md) for development and production, but you might not need it during testing. You may set `INERTIA_SSR_ENABLED` to `false` in your `phpunit.xml` to prevent the Laravel adapter from dispatching SSR requests.

```xml theme={null}
<env name="INERTIA_SSR_ENABLED" value="false" />
```

Alternatively, you may use the `Inertia::disableSsr()` method in your test base class.

```php theme={null}
use Inertia\Inertia;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void
    {
        parent::setUp();

        Inertia::disableSsr();
    }
}
```

A boolean or closure may be passed to disable SSR conditionally. This is typically called from a service provider.

```php theme={null}
// Evaluated immediately...
Inertia::disableSsr(app()->runningUnitTests());

// Evaluated lazily...
Inertia::disableSsr(fn () => app()->runningUnitTests());
```
