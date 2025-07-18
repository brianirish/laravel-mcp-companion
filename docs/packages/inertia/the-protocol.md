# Inertia - The Protocol

Source: https://inertiajs.com/the-protocol

# The protocol

## HTML responses

## Inertia responses

## The page object

## Asset versioning

## Partial reloads

This page contains a detailed specification of the Inertia protocol. Be sure to read the how it works page first for a high-level overview.

The very first request to an Inertia app is just a regular, full-page browser request, with no special Inertia headers or data. For these requests, the server returns a full HTML document.

This HTML response includes the site assets (CSS, JavaScript) as well as a root in the page's body. The root serves as a mounting point for the client-side app, and includes a data-page attribute with a JSON encoded page object for the initial page. Inertia uses this information to boot your client-side framework and display the initial page component.

Once the Inertia app has been booted, all subsequent requests to the site are made via XHR with a X-Inertia header set to true. This header indicates that the request is being made by Inertia and isn't a standard full-page visit.

When the server detects the X-Inertia header, instead of responding with a full HTML document, it returns a JSON response with an encoded page object.

Inertia shares data between the server and client via a page object. This object includes the necessary information required to render the page component, update the browser's history state, and track the site's asset version. The page object includes the following four properties:

On standard full page visits, the page object is JSON encoded into the data-page attribute in the root . On Inertia visits, the page object is returned as the JSON payload.

One common challenge with single-page apps is refreshing site assets when they've been changed. Inertia makes this easy by optionally tracking the current version of the site's assets. In the event that an asset changes, Inertia will automatically make a full-page visit instead of an XHR visit.

The Inertia page object includes a version identifier. This version identifier is set server-side and can be a number, string, file hash, or any other value that represents the current "version" of your site's assets, as long as the value changes when the site's assets have been updated.

Whenever an Inertia request is made, Inertia will include the current asset version in the X-Inertia-Version header. When the server receives the request, it compares the asset version provided in the X-Inertia-Version header with the current asset version. This is typically handled in the middleware layer of your server-side framework.

If the asset versions are the same, the request simply continues as expected. However, if the asset versions are different, the server immediately returns a 409 Conflict response, and includes the URL in a X-Inertia-Location header. This header is necessary, since server-side redirects may have occurred. This tells Inertia what the final intended destination URL is.

Note, 409 Conflict responses are only sent for GET requests, and not for POST/PUT/PATCH/DELETE requests. That said, they will be sent in the event that a GET redirect occurs after one of these requests.

If "flash" session data exists when a 409 Conflict response occurs, Inertia's server-side framework adapters will automatically reflash this data.

You can read more about this on the asset versioning page.

When making Inertia requests, the partial reload option allows you to request a subset of the props (data) from the server on subsequent visits to the same page component. This can be a helpful performance optimization if it's acceptable that some page data becomes stale.

When a partial reload request is made, Inertia includes two additional headers with the request: X-Inertia-Partial-Data and X-Inertia-Partial-Component.

The X-Inertia-Partial-Data header is a comma separated list of the desired props (data) keys that should be returned.

The X-Inertia-Partial-Component header includes the name of the component that is being partially reloaded. This is necessary, since partial reloads only work for requests made to the same page component. If the final destination is different for some reason (eg. the user was logged out and is now on the login page), then no partial reloading will occur.

`data-page`
`true`
`X-Inertia`
`The page object Inertia shares data between the server and client via a page object. This object includes the necessary information required to render the page component, update the browser's history state, and track the site's asset version. The page object includes the following four properties: component: The name of the JavaScript page component. props: The page props (data). url: The page URL. version: The current asset version. encryptHistory: Whether or not to encrypt the current page's history state. clearHistory: Whether or not to clear any encrypted history state. On standard full page visits, the page object is JSON encoded into the data-page`
`version`
`X-Inertia-Version`
`409 Conflict`
`X-Inertia-Location`
`GET`
`POST/PUT/PATCH/DELETE`
`X-Inertia-Partial-Data`
`X-Inertia-Partial-Component`
**component:**
**props:**
**url:**
**version:**
**encryptHistory:**
**clearHistory:**
[how it works](/how-it-works)
[page object](#the-page-object)
[asset versioning](/asset-versioning)
Come out and celebrate Jonathan&apos;s 36th birthday party!
