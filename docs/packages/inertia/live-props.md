Source: https://inertiajs.com/docs/v3/data-props/live-props.md

# Live Props

Sometimes you may wish to keep a prop in sync with your server without any user interaction. Live props listen for your broadcast events and refresh the props those events affect, making them ideal for order statuses, unread counts, or dashboard metrics.

Live props are refreshed using [partial reloads](https://inertiajs.com/docs/v3/data-props/partial-reloads.md), so the client receives whatever your controller returns at that moment. Events may also [carry the new values](#broadcasting-values) themselves.

## Creating Live Props

To create a live prop, use the `Inertia::live()` method and pass the event that should refresh it.

```php theme={null}
use App\Events\OrderUpdated;

return Inertia::render('Orders/Show', [
    'order' => Inertia::live(fn () => $order, on: new OrderUpdated($order)),
]);
```

Inertia reads the channels from the event's `broadcastOn()` method, and the client reloads the `order` prop whenever the event is broadcast.

Live props may be combined with [deferred](https://inertiajs.com/docs/v3/data-props/deferred-props.md), [once](https://inertiajs.com/docs/v3/data-props/once-props.md), [optional](https://inertiajs.com/docs/v3/data-props/partial-reloads.md#lazy-data-evaluation), and always props. An optional live prop is only refreshed after the page has loaded it. [Merge props](https://inertiajs.com/docs/v3/data-props/merging-props.md) may not be live.

```php theme={null}
return Inertia::render('Orders/Show', [
    'metrics' => Inertia::defer(fn () => $order->metrics())->live(on: new OrderUpdated($order)),
]);
```

## Client Setup

Live props receive events through a transport, which you pass to the `live` option of `createInertiaApp()`. Inertia includes transports for [Laravel Echo](https://laravel.com/docs/broadcasting#client-side-installation), `pusher-js`, and Action Cable, and subscribes and unsubscribes automatically as the user navigates.

### Echo

Configure Echo as usual, then pass the `echo()` transport.

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from "@inertiajs/vue3";
import { echo } from "@inertiajs/vue3/echo";
import { configureEcho } from "@laravel/echo-vue";

configureEcho({ broadcaster: "reverb" });

createInertiaApp({
  live: echo(),
  // ...
});
```

```js React icon="react" theme={null}
import { createInertiaApp } from "@inertiajs/react";
import { echo } from "@inertiajs/react/echo";
import { configureEcho } from "@laravel/echo-react";

configureEcho({ broadcaster: "reverb" });

createInertiaApp({
  live: echo(),
  // ...
});
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from "@inertiajs/svelte";
import { echo } from "@inertiajs/svelte/echo";
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({ broadcaster: "reverb" });

createInertiaApp({
  live: echo(),
  // ...
});
```

You may pass a `resolve` callback to `echo()` to use a different Echo instance, such as one created with `laravel-echo` directly.

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from "@inertiajs/vue3";
import { echo } from "@inertiajs/vue3/echo";

createInertiaApp({
  live: echo({ resolve: () => window.Echo }),
  // ...
});
```

```js React icon="react" theme={null}
import { createInertiaApp } from "@inertiajs/react";
import { echo } from "@inertiajs/react/echo";

createInertiaApp({
  live: echo({ resolve: () => window.Echo }),
  // ...
});
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from "@inertiajs/svelte";
import { echo } from "@inertiajs/svelte/echo";

createInertiaApp({
  live: echo({ resolve: () => window.Echo }),
  // ...
});
```

### Pusher

The `pusher()` transport accepts a `pusher-js` client, which works with any Pusher-compatible server, such as [Reverb](https://laravel.com/framework/docs/reverb). You are responsible for configuring the client, including channel authorization.

```js theme={null}
import { pusher } from "@inertiajs/core/pusher";
import Pusher from "pusher-js";

const client = new Pusher("pusher-app-key", {
  // ...
});

createInertiaApp({
  live: pusher({ client }),
  // ...
});
```

### Action Cable

Rails applications may use the `actionCable()` transport for [Action Cable](https://guides.rubyonrails.org/action_cable_overview.html). Pass a function that creates the consumer, so Inertia only opens the connection once a page subscribes, and never during server-side rendering.

```js theme={null}
import { actionCable } from "@inertiajs/core/actionCable";
import { createConsumer } from "@rails/actioncable";

createInertiaApp({
  live: actionCable({ consumer: () => createConsumer() }),
  // ...
});
```

[AnyCable](https://anycable.io) is also supported. Import `createConsumer()` from `@anycable/web` instead of `@rails/actioncable`.

## Listening for Multiple Events

You may pass an array of events to refresh a prop from more than one event. Each event uses its own channels.

```php theme={null}
return Inertia::render('Orders/Show', [
    'order' => Inertia::live(fn () => $order, on: [
        new OrderUpdated($order),
        new OrderShipped($order),
    ]),
]);
```

Props listening for the same event are refreshed together in a single request.

## Channels

Live props listen on every channel your event [broadcasts on](https://laravel.com/docs/broadcasting#defining-broadcast-events). An event broadcasting on both `orders.1` and `orders` therefore refreshes the prop whenever any order changes. You may pass the `channel` argument to listen on a specific channel instead.

```php theme={null}
return Inertia::render('Dashboard', [
    'metrics' => Inertia::live(fn () => Metrics::today(), on: OrderUpdated::class, channel: new PrivateChannel('orders')),
]);
```

You may also pass an event class name instead of an instance, as long as its channels and `broadcastAs()` name don't depend on the event's data, since Inertia creates the event without calling its constructor.

```php theme={null}
class OrderUpdated implements ShouldBroadcast
{
    public function broadcastOn(): PrivateChannel
    {
        return new PrivateChannel('orders');
    }
}

Inertia::live(fn () => $order, on: OrderUpdated::class);
```

A bare string is a public channel, and each channel class defines its own type.

```php theme={null}
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\EncryptedPrivateChannel;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;

$channel = 'stats';                                   // public
$channel = new Channel('stats');                      // public
$channel = new PrivateChannel('orders.1');            // private
$channel = new PresenceChannel('room.1');             // presence
$channel = new EncryptedPrivateChannel('orders.1');   // encrypted private

Inertia::live($value, on: $event, channel: $channel);
```

Channels returned from `broadcastOn()` follow the same rules, so wrap non-public channel names in the appropriate channel class.

```php theme={null}
public function broadcastOn(): array
{
    return [
        'stats',                        // public
        new PrivateChannel('orders.1'), // private
    ];
}
```

Private, presence, and encrypted private channels are [authorized](https://laravel.com/docs/broadcasting#authorizing-channels) through your `channels.php` routes as usual.

## Throttling

By default, each live prop refreshes at most once per second. You may change this default using the `throttle` option, in milliseconds, of `echo()`, `pusher()`, or `actionCable()`.

```js Vue icon="vuejs" theme={null}
import { createInertiaApp } from "@inertiajs/vue3";
import { echo } from "@inertiajs/vue3/echo";

createInertiaApp({
  live: echo({ throttle: 2000 }),
  // ...
});
```

```js React icon="react" theme={null}
import { createInertiaApp } from "@inertiajs/react";
import { echo } from "@inertiajs/react/echo";

createInertiaApp({
  live: echo({ throttle: 2000 }),
  // ...
});
```

```js Svelte icon="s" theme={null}
import { createInertiaApp } from "@inertiajs/svelte";
import { echo } from "@inertiajs/svelte/echo";

createInertiaApp({
  live: echo({ throttle: 2000 }),
  // ...
});
```

A prop may also define its own throttle.

```php theme={null}
return Inertia::render('Dashboard', [
    'metrics' => Inertia::live(fn () => Metrics::today(), on: new MetricsUpdated, throttle: 5000),
]);
```

Each prop is throttled separately, so a busy prop never delays the rest of the page. Events received during the throttle window are collected into a single request once the window ends. Manual reloads using `router.reload()` are never throttled.

A single action often broadcasts several events at once, so Inertia waits a few milliseconds before refreshing and collects every affected prop into one request.

Refreshes pause while the browser tab is hidden and resume when the user returns. You may disable this using the `pauseWhenHidden` option.

## Broadcasting Values

By default, every listening page requests the new value from the server, so a dashboard open in a thousand tabs turns one event into a thousand requests. To avoid these requests, the event may broadcast the values itself using `Inertia::broadcastProps()`.

```php theme={null}
class OrderUpdated implements ShouldBroadcast
{
    public function __construct(public Order $order) {}

    public function broadcastOn(): PrivateChannel
    {
        return new PrivateChannel("orders.{$this->order->id}");
    }

    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            ...Inertia::broadcastProps([
                'order' => OrderResource::make($this->order),
            ]),
        ];
    }
}
```

Inertia writes these values into the page without making a request. Keys are prop names, using dot notation for nested props. Values are resolved like page props, so resources, `Arrayable` objects, and closures all work, but prop types such as `Inertia::optional()` do not.

Props that don't listen for the event ignore its values, and props the event carries no value for are reloaded as usual. A prop that is already being reloaded also ignores the value, since that request may return newer data.

> [!WARNING]
>
> Every subscriber of a channel receives the same payload, and channel authorization only runs when a user subscribes. Only broadcast values that every subscriber may see, and leave anything that depends on the user to a reload. Prefer resources over models, since a model broadcasts every attribute that isn't `$hidden`.

## Tracking Refreshes

The `useProp` hook returns a prop's value and whether it is being refreshed, making it ideal for subtle loading indicators.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { useProp } from "@inertiajs/vue3";

const { value: order, loading } = useProp("order");
</script>

<template>
  <div :class="{ 'opacity-50': loading }">
    {{ order.status }}
  </div>
</template>
```

```jsx React icon="react" theme={null}
import { useProp } from "@inertiajs/react";

export default () => {
  const order = useProp("order");

  return <div className={order.loading ? "opacity-50" : ""}>{order.value.status}</div>;
};
```

```svelte Svelte icon="s" theme={null}
<script>
  import { useProp } from "@inertiajs/svelte";

  const order = useProp("order");
</script>

<div class={order.loading ? "opacity-50" : ""}>
  {order.value.status}
</div>
```

The hook also returns a `loaded` value, which is useful for live props that are also [deferred](https://inertiajs.com/docs/v3/data-props/deferred-props.md).

## Live Events

Inertia fires a cancelable [`live` event](https://inertiajs.com/docs/v3/advanced/events#live) before updating a live prop. Returning `false` skips the update, allowing you to show a "New data available" button instead. You may apply the update later using `router.reload({ only: event.detail.props })`.

```js theme={null}
router.on("live", (event) => {
  console.log(event.detail.props); // the props about to be refreshed
  console.log(event.detail.channel); // { name, type }
  console.log(event.detail.event); // the broadcast event name
  console.log(event.detail.payload); // the broadcast payload

  return false;
});
```

## Skipping the Current Connection

Inertia sends the socket ID as an `X-Socket-Id` header on same-origin requests, so the user who triggers a broadcast using `toOthers()` doesn't receive it.

```php theme={null}
broadcast(new OrderUpdated($order))->toOthers();
```

You may provide your own socket ID using `socketId.resolveUsing()`, which takes precedence over the transport's. Passing `null` disables the header.

```js Vue icon="vuejs" theme={null}
import { socketId } from "@inertiajs/vue3";

socketId.resolveUsing(() => mySocket.id);
socketId.resolveUsing(null);
```

```js React icon="react" theme={null}
import { socketId } from "@inertiajs/react";

socketId.resolveUsing(() => mySocket.id);
socketId.resolveUsing(null);
```

```js Svelte icon="s" theme={null}
import { socketId } from "@inertiajs/svelte";

socketId.resolveUsing(() => mySocket.id);
socketId.resolveUsing(null);
```

## Custom Transports

You may pass any object implementing the `LiveTransport` interface to the `live` option, allowing you to receive events from your own WebSocket client, server-sent events, or a `BroadcastChannel`.

```ts theme={null}
import type { LiveTransport } from "@inertiajs/core";

const transport: LiveTransport = {
  subscribe(channel, event, handler) {
    // Called once per channel and event pair. Return a function that unsubscribes.
    return () => {};
  },

  // Optional. Lets Inertia send the socket ID so `toOthers()` works.
  socketId: () => connection.id,

  // Optional. Inertia refreshes every live prop after a dropped connection
  // returns, since events that fired while it was down never arrived.
  onStatusChange(callback) {
    return () => {};
  },
};

createInertiaApp({
  live: transport,
  // ...
});
```

Channels arrive unprefixed with their type, such as `{ name: "orders.1", type: "private" }`, so `subscribe()` should apply any prefix your broadcaster expects. A broadcaster that subscribes per channel rather than per event should join the channel on its first listener and leave it after its last. Since `subscribe()` runs during a page swap, avoid throwing from it, as an error aborts the swap.

The `onStatusChange()` callback receives a boolean indicating whether the connection is up. Inertia ignores repeated statuses and only acts when a dropped connection is restored.

```ts theme={null}
onStatusChange(callback) {
  const handler = (state: string) => callback(state === "connected");

  connection.on("state_change", handler);

  return () => connection.off("state_change", handler);
}
```

Review the [pusher.ts](https://github.com/inertiajs/inertia/blob/3.x/packages/core/src/pusher.ts) source for a reference implementation. It relies on a few internal helpers, such as prefixing channel names and counting the listeners on each channel, which your transport implements for its own broadcaster.

### Channel Transports

Some broadcasters can't route messages by event name. Their transports may implement `subscribeToChannel()` instead, which is called once per channel. Inertia then reads the event name from each message's `__inertia.event` key. Review the [actionCable.ts](https://github.com/inertiajs/inertia/blob/3.x/packages/core/src/actionCable.ts) source for a reference implementation, which also uses internal helpers you'd write yourself.

```ts theme={null}
import type { LiveChannelTransport } from "@inertiajs/core";

const transport: LiveChannelTransport = {
  subscribeToChannel(channel, handler) {
    const stream = socket.subscribe(channel.name, handler);

    return () => stream.close();
  },

  // Optional. Reads the event name from somewhere other than `__inertia.event`.
  eventName: (payload) => (payload as { type?: string }).type,
};
```
