# Inertia - Progress Indicators

Source: https://inertiajs.com/progress-indicators

# Progress indicators

## Default

## Custom

### Handling cancelled visits

### File upload progress

### Loading indicator delay

### Complete example

## Visit Options

### showProgress

### async

Since Inertia requests are made via XHR, there would typically not be a browser loading indicator when navigating from one page to another. To solve this, Inertia displays a progress indicator at the top of the page whenever you make an Inertia visit. However, asynchronous requests do not show the progress indicator unless explicitly configured.

Of course, if you prefer, you can disable Inertia's default loading indicator and provide your own custom implementation. We'll discuss both approaches below.

Inertia's default progress indicator is a light-weight wrapper around the NProgress library. You can customize it via the progress property of the createInertiaApp() function.

You can disable Inertia's default loading indicator by setting the progress property to false.

It's also possible to setup your own custom page loading indicators using Inertia events. Let's explore how to do this using the NProgress library as an example.

First, disable Inertia's default loading indicator.

Next, install the NProgress library.

After installation, you'll need to add the NProgress styles to your project. You can do this using a CDN hosted copy of the styles.

Next, import both NProgress and the Inertia router into your application.

Next, let's add a start event listener. We'll use this listener to show the progress bar when a new Inertia visit begins.

Then, let's add a finish event listener to hide the progress bar when the page visit finishes.

That's it! Now, as you navigate from one page to another, the progress bar will be added and removed from the page.

While this custom progress implementation works great for page visits that finish properly, it would be nice to handle cancelled visits as well. First, for interrupted visits (those that get cancelled as a result of a new visit), the progress bar should simply be reset back to the start position. Second, for manually cancelled visits, the progress bar should be immediately removed from the page.

We can accomplish this by inspecting the event.detail.visit object that's provided to the finish event.

Let's take this a step further. When files are being uploaded, it would be great to update the loading indicator to reflect the upload progress. This can be done using the progress event.

Now, instead of the progress bar "trickling" while the files are being uploaded, it will actually update it's position based on the progress of the request. We limit the progress here to 90%, since we still need to wait for a response from the server.

The last thing we're going to implement is a loading indicator delay. It's often preferable to delay showing the loading indicator until a request has taken longer than 250-500 milliseconds. This prevents the loading indicator from appearing constantly on quick page visits, which can be visually distracting.

To implement the delay behavior, we'll use the setTimeout and clearTimeout functions. Let's start by defining a variable to keep track of the timeout.

Next, let's update the start event listener to start a new timeout that will show the progress bar after 250 milliseconds.

Next, we'll update the finish event listener to clear any existing timeouts in the event that the page visit finishes before the timeout does.

In the finish event listener, we need to determine if the progress bar has actually started displaying progress, otherwise we'll inadvertently cause it to show before the timeout has finished.

And, finally, we need to do the same check in the progress event listener.

That's it, you now have a beautiful custom page loading indicator!

For convenience, here is the full source code of the final version of our custom loading indicator.

In addition to these configurations, Inertia.js provides two visit options to control the loading indicator on a per-request basis: showProgress and async. These options offer greater control over how Inertia.js handles asynchronous requests and manages progress indicators.

The showProgress option provides fine-grained control over the visibility of the loading indicator during requests.

The async option allows you to perform asynchronous requests without displaying the default progress indicator. It can be used in combination with the showProgress option.

`progress`
`createInertiaApp()`
`You can disable Inertia's default loading indicator by setting the progress`
`false`
`Custom It's also possible to setup your own custom page loading indicators using Inertia events. Let's explore how to do this using the NProgress library as an example. First, disable Inertia's default loading indicator. Next, install the NProgress library. After installation, you'll need to add the NProgress styles to your project. You can do this using a CDN hosted copy of the styles. Next, import both NProgress`
`router`
`start`
`clearTimeout`
`Next, let's update the start`
`async`
`showProgress`
`async The async`
[asynchronous requests](#visit-options)
[NProgress](https://ricostacruz.com/nprogress/)
[events](/events)
[styles](https://github.com/rstacruz/nprogress/blob/master/nprogress.css)
// Disable the progress indicator
          router.get(
