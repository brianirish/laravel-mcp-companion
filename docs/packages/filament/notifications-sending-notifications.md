# Filament - Notifications/Sending Notifications

Source: https://filamentphp.com/docs/3.x/notifications/sending-notifications

#Overview
---------

> To start, make sure the package is installed - `@livewire('notifications')` should be in your Blade layout somewhere.

Notifications are sent using a `Notification` object that’s constructed through a fluent API. Calling the `send()` method on the `Notification` object will dispatch the notification and display it in your application. As the session is used to flash notifications, they can be sent from anywhere in your code, including JavaScript, not just Livewire components.

```php
<?php

namespace App\Livewire;

use Filament\Notifications\Notification;
use Livewire\Component;

class EditPost extends Component
{
    public function save(): void
    {
        // ...

        Notification::make()
            ->title('Saved successfully')
            ->success()
            ->send();
    }
}

```
![Success notification](/docs/3.x/images/light/notifications/success.jpg) ![Success notification](/docs/3.x/images/dark/notifications/success.jpg)

#Setting a title
----------------

The main message of the notification is shown in the title. You can set the title as follows:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->send();

```
The title text can contain basic, safe HTML elements. To generate safe HTML with Markdown, you can use the `Str::markdown()` helper: `title(Str::markdown('Saved **successfully**'))`

Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .send()

```
#Setting an icon
----------------

Optionally, a notification can have an icon that’s displayed in front of its content. You may also set a color for the icon, which is gray by default:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->icon('heroicon-o-document-text')
    ->iconColor('success')
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .icon('heroicon-o-document-text')
    .iconColor('success')
    .send()

```
![Notification with icon](/docs/3.x/images/light/notifications/icon.jpg) ![Notification with icon](/docs/3.x/images/dark/notifications/icon.jpg)

Notifications often have a status like `success`, `warning`, `danger` or `info`. Instead of manually setting the corresponding icons and colors, there’s a `status()` method which you can pass the status. You may also use the dedicated `success()`, `warning()`, `danger()` and `info()` methods instead. So, cleaning up the above example would look like this:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .send()

```
![Notifications with various statuses](/docs/3.x/images/light/notifications/statuses.jpg) ![Notifications with various statuses](/docs/3.x/images/dark/notifications/statuses.jpg)

#Setting a background color
---------------------------

Notifications have no background color by default. You may want to provide additional context to your notification by setting a color as follows:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->color('success')
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .color('success')
    .send()

```
![Notification with background color](/docs/3.x/images/light/notifications/color.jpg) ![Notification with background color](/docs/3.x/images/dark/notifications/color.jpg)

#Setting a duration
-------------------

By default, notifications are shown for 6 seconds before they’re automatically closed. You may specify a custom duration value in milliseconds as follows:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->duration(5000)
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .duration(5000)
    .send()

```
If you prefer setting a duration in seconds instead of milliseconds, you can do so:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->seconds(5)
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .seconds(5)
    .send()

```
You might want some notifications to not automatically close and require the user to close them manually. This can be achieved by making the notification persistent:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->persistent()
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .persistent()
    .send()

```
#Setting body text
------------------

Additional notification text can be shown in the `body()`:

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->send();

```
The body text can contain basic, safe HTML elements. To generate safe HTML with Markdown, you can use the `Str::markdown()` helper: `body(Str::markdown('Changes to the **post** have been saved.'))`

Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .send()

```
![Notification with body text](/docs/3.x/images/light/notifications/body.jpg) ![Notification with body text](/docs/3.x/images/dark/notifications/body.jpg)

#Adding actions to notifications
--------------------------------

Notifications support Actions, which are buttons that render below the content of the notification. They can open a URL or dispatch a Livewire event. Actions can be defined as follows:

```php
use Filament\Notifications\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button(),
        Action::make('undo')
            ->color('gray'),
    ])
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button(),
        new FilamentNotificationAction('undo')
            .color('gray'),
    ])
    .send()

```
![Notification with actions](/docs/3.x/images/light/notifications/actions.jpg) ![Notification with actions](/docs/3.x/images/dark/notifications/actions.jpg)

You can learn more about how to style action buttons here.

### #Opening URLs from notification actions

You can open a URL, optionally in a new tab, when clicking on an action:

```php
use Filament\Notifications\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray'),
    ])
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray'),
    ])
    .send()

```
### #Dispatching Livewire events from notification actions

Sometimes you want to execute additional code when a notification action is clicked. This can be achieved by setting a Livewire event which should be dispatched on clicking the action. You may optionally pass an array of data, which will be available as parameters in the event listener on your Livewire component:

```php
use Filament\Notifications\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray')
            ->dispatch('undoEditingPost', [$post->id]),
    ])
    ->send();

```
You can also `dispatchSelf` and `dispatchTo`:

```php
Action::make('undo')
    ->color('gray')
    ->dispatchSelf('undoEditingPost', [$post->id])

Action::make('undo')
    ->color('gray')
    ->dispatchTo('another_component', 'undoEditingPost', [$post->id])

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray')
            .dispatch('undoEditingPost'),
    ])
    .send()

```
Similarly, `dispatchSelf` and `dispatchTo` are also available:

```php
new FilamentNotificationAction('undo')
    .color('gray')
    .dispatchSelf('undoEditingPost')

new FilamentNotificationAction('undo')
    .color('gray')
    .dispatchTo('another_component', 'undoEditingPost')

```
### #Closing notifications from actions

After opening a URL or dispatching an event from your action, you may want to close the notification right away:

```php
use Filament\Notifications\Actions\Action;
use Filament\Notifications\Notification;

Notification::make()
    ->title('Saved successfully')
    ->success()
    ->body('Changes to the post have been saved.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $post), shouldOpenInNewTab: true),
        Action::make('undo')
            ->color('gray')
            ->dispatch('undoEditingPost', [$post->id])
            ->close(),
    ])
    ->send();

```
Or with JavaScript:

```php
new FilamentNotification()
    .title('Saved successfully')
    .success()
    .body('Changes to the post have been saved.')
    .actions([
        new FilamentNotificationAction('view')
            .button()
            .url('/view')
            .openUrlInNewTab(),
        new FilamentNotificationAction('undo')
            .color('gray')
            .dispatch('undoEditingPost')
            .close(),
    ])
    .send()

```
#Using the JavaScript objects
-----------------------------

The JavaScript objects (`FilamentNotification` and `FilamentNotificationAction`) are assigned to `window.FilamentNotification` and `window.FilamentNotificationAction`, so they are available in on-page scripts.

You may also import them in a bundled JavaScript file:

```php
import { Notification, NotificationAction } from '../../vendor/filament/notifications/dist/index.js'

// ...

```
#Closing a notification with JavaScript
---------------------------------------

Once a notification has been sent, you can close it on demand by dispatching a browser event on the window called `close-notification`.

The event needs to contain the ID of the notification you sent. To get the ID, you can use the `getId()` method on the `Notification` object:

```php
use Filament\Notifications\Notification;

$notification = Notification::make()
    ->title('Hello')
    ->persistent()
    ->send()

$notificationId = $notification->getId()

```
To close the notification, you can dispatch the event from Livewire:

```php
$this->dispatch('close-notification', id: $notificationId);

```
Or from JavaScript, in this case Alpine.js:

```php
<button x-on:click="$dispatch('close-notification', { id: notificationId })" type="button">
    Close Notification
</button>

```
If you are able to retrieve the notification ID, persist it, and then use it to close the notification, that is the recommended approach, as IDs are generated uniquely, and you will not risk closing the wrong notification. However, if it is not possible to persist the random ID, you can pass in a custom ID when sending the notification:

```php
use Filament\Notifications\Notification;

Notification::make('greeting')
    ->title('Hello')
    ->persistent()
    ->send()

```
In this case, you can close the notification by dispatching the event with the custom ID:

```php
<button x-on:click="$dispatch('close-notification', { id: 'greeting' })" type="button">
    Close Notification
</button>

```
Please be aware that if you send multiple notifications with the same ID, you may experience unexpected side effects, so random IDs are recommended.

Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion