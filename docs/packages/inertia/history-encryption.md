Source: https://inertiajs.com/docs/v3/security/history-encryption.md

# History Encryption

Imagine a scenario where your user is authenticated, browses privileged information on your site, then logs out. If they press the back button, they can still see the privileged information that is stored in the window's history state. This is a security risk. To prevent this, Inertia.js provides a history encryption feature.

## How It Works

When you instruct Inertia to encrypt your app's history, it uses the browser's built-in [`Crypto` API](https://developer.mozilla.org/en-US/docs/Web/API/Crypto) to encrypt the current page's data before pushing it to the history state. We store the corresponding key in the browser's session storage. When the user navigates back to a page, we decrypt the data using the key stored in the session storage.

Once you instruct Inertia to clear your history state, it clears the existing key from session storage and generates a new one. If it attempts to decrypt the history state with the new key, it will fail and Inertia will make a fresh request back to your server for the page data.

History encryption relies on `window.crypto.subtle` which is only available in secure environments (sites with SSL enabled).

## Opting in

History encryption is an opt-in feature. There are several methods for enabling it:

### Global Encryption

If you'd like to enable history encryption globally, set the `inertia.history.encrypt` config value to `true`.

You are able to opt out of encryption on specific pages by calling the `Inertia::encryptHistory()`method before returning the response.

```php theme={null}
Inertia::encryptHistory(false);
```

### Per-request Encryption

To encrypt the history of an individual request, simply call the `Inertia::encryptHistory()` method before returning the response.

```php theme={null}
Inertia::encryptHistory();
```

### Encrypt Middleware

To encrypt a group of routes, you may use Inertia's included `EncryptHistory` middleware.

```php theme={null}
Route::middleware([Inertia\Middleware\EncryptHistory::class])->get('/', function() {
    //
});

Route::middleware(['inertia::encrypt'])->get('/', function() {
    //
});
```

## Clearing History

To clear the history state, you can call the `Inertia::clearHistory()` method before returning the response.

```php theme={null}
Inertia::clearHistory();
```

Once the response has rendered on the client, the encryption key will be rotated, rendering the previous history state unreadable.

You can also clear history on the client side by calling `router.clearHistory()`.
