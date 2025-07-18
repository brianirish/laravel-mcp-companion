# Inertia - Testing

Source: https://inertiajs.com/testing

# Testing

## End-to-end tests

## Client-side unit tests

## Endpoint tests

### Testing Partial Reloads

There are many different ways to test an Inertia application. This page provides a quick overview of the tools available.

One popular approach to testing your JavaScript page components is to use an end-to-end testing tool like Cypress or Laravel Dusk. These are browser automation tools that allow you to run real simulations of your app in the browser. These tests are known to be slower; however, since they test your application at the same layer as your end users, they can provide a lot of confidence that your app is working correctly. And, since these tests are run in the browser, your JavaScript code is actually executed and tested as well.

Another approach to testing your page components is using a client-side unit testing framework, such as Jest or Mocha. This approach allows you to test your JavaScript page components in isolation using Node.js.

In addition to testing your JavaScript page components, you will likely want to also test the Inertia responses that are returned by your server-side framework. A popular approach to doing this is using endpoint tests, where you make requests to your application and examine the responses. Laravel provides tooling for executing these types of tests.

However, to make this process even easier, Inertia's Laravel adapter provides additional HTTP testing tools. Let's take a look at an example.

As you can see in the example above, you may use these assertion methods to assert against the content of the data provided to the Inertia response. In addition, you may assert that array data has a given length as well as scope your assertions.

You may use the inertiaProps method to retrieve the props returned in the response. You can pass a key to retrieve a specific property, and nested properties are supported using "dot" notation.

Let's dig into the assertInertia method and the available assertions in detail. First, to assert that the Inertia response has a property, you may use the has method. You can think of this method as being similar to PHP's isset function.

To assert that an Inertia property has a specified amount of items, you may provide the expected size as the second argument to the has method.

The has method may also be used to scope properties in order to lessen repetition when asserting against nested properties.

When scoping into Inertia properties that are arrays or collections, you may also assert that a specified number of items are present in addition to scoping into the first item.

To assert that an Inertia property has an expected value, you may use the where assertion.

Inertia's testing methods will automatically fail when you haven't interacted with at least one of the props in a scope. While this is generally useful, you might run into situations where you're working with unreliable data (such as from an external feed), or with data that you really don't want interact with in order to keep your test simple. For these situations, the etc method exists.

The missing method is the exact opposite of the has method, ensuring that the property does not exist. This method makes a great companion to the etc method.

You may use the reloadOnly and reloadExcept methods to test how your application responds to partial reloads. These methods perform a follow-up request and allow you to make assertions against the response.

Instead of passing a single prop as a string, you may also pass an array of props to reloadOnly or reloadExcept.

`has`
`isset`
`etc`
`reloadExcept`
[Cypress](https://www.cypress.io/)
[Laravel Dusk](https://laravel.com/docs/dusk)
[Jest](https://jestjs.io/)
[Mocha](https://mochajs.org/)
[provides tooling](https://laravel.com/docs/http-tests)
[partial reloads](/partial-reloads)
)

              // Checking nested properties using

, 7)

              // Checking nested properties using

, 5)

                  // And can even create a deeper scope using
