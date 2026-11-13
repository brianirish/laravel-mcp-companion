Source: https://laravel.com/cloud/docs/resources/websockets/pusher.md

# Connecting with Pusher SDKs

Publish and receive events using Pusher SDKs with Laravel Cloud WebSockets.

## Introduction

Laravel Cloud WebSocket clusters speak the Pusher protocol, so you may connect to them using Pusher's official SDKs. You can publish events from PHP, JavaScript, Python, Go, Ruby, and Java applications using Pusher's HTTP SDKs, then receive those events using Pusher's WebSocket SDKs. You do not need a Pusher account.

## Connection variables

To get started, [create a WebSocket cluster](https://laravel.com/cloud/docs/resources/websockets#creating-clusters), attach a WebSocket application to your environment, and redeploy. Laravel Cloud injects the following variables into JavaScript, Python, Go, Ruby, and Java applications, as well as PHP applications that don't use Laravel or Symfony:

```dotenv theme={null}
PUSHER_APP_ID=10001
PUSHER_APP_KEY=********
PUSHER_APP_SECRET=********
PUSHER_HOST=ws-********-reverb.laravel.cloud
PUSHER_PORT=443
PUSHER_SCHEME=https
```

These variables point to your Laravel Cloud cluster rather than Pusher's hosted service, so you need to pass `PUSHER_HOST` to each SDK. Laravel Cloud accepts HTTPS requests for publishing and secure WebSocket (`wss`) connections for subscribing, both on port `443`.

For PHP applications, Laravel Cloud writes these variables to an injected `.env` file, and your application is responsible for loading it. The [PHP example](#php) uses [PHP dotenv](https://github.com/vlucas/phpdotenv) to load the file. The other examples read their variables directly from the process environment.

Laravel and Symfony applications receive `REVERB_*` variables instead. If you're using one of those frameworks, follow the [connection instructions](https://laravel.com/cloud/docs/resources/websockets#connecting-your-application) for your framework.

## Publishing events

Pusher's HTTP SDKs publish events by sending signed requests from your server to your WebSocket application. The SDKs sign these requests with `PUSHER_APP_SECRET`, so always publish events from your server.

### PHP

To publish events from PHP, install Pusher's [PHP HTTP SDK](https://github.com/pusher/pusher-http-php) along with PHP dotenv:

```sh theme={null}
composer require pusher/pusher-php-server vlucas/phpdotenv
```

Then, place the following script in your project's root directory, next to the injected `.env` file and your `vendor` directory:

```php theme={null}
<?php

require __DIR__.'/vendor/autoload.php';

Dotenv\Dotenv::createImmutable(__DIR__)->load();

$pusher = new Pusher\Pusher(
    $_ENV['PUSHER_APP_KEY'],
    $_ENV['PUSHER_APP_SECRET'],
    $_ENV['PUSHER_APP_ID'],
    [
        'host' => $_ENV['PUSHER_HOST'],
        'port' => (int) $_ENV['PUSHER_PORT'],
        'scheme' => $_ENV['PUSHER_SCHEME'],
        'useTLS' => $_ENV['PUSHER_SCHEME'] === 'https',
    ],
);

$pusher->trigger('notifications', 'message-sent', [
    'message' => 'Hello from Laravel Cloud',
]);
```

If your application already loads its `.env` file, you may remove the `Dotenv` call and use your existing configuration instead.

### Node.js

To publish events from Node.js, install Pusher's [Node.js HTTP SDK](https://github.com/pusher/pusher-http-node):

```sh theme={null}
npm install pusher
```

Then, save the following script as `publish.cjs` and run it using `node publish.cjs`:

```javascript theme={null}
const Pusher = require('pusher');

const pusher = new Pusher({
    appId: process.env.PUSHER_APP_ID,
    key: process.env.PUSHER_APP_KEY,
    secret: process.env.PUSHER_APP_SECRET,
    host: process.env.PUSHER_HOST,
    port: process.env.PUSHER_PORT,
    useTLS: process.env.PUSHER_SCHEME === 'https',
});

async function publish() {
    await pusher.trigger('notifications', 'message-sent', {
        message: 'Hello from Laravel Cloud',
    });
}

publish().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
```

The `pusher` package only publishes events from your server. To receive events in the browser, use the separate `pusher-js` package, as shown in the [JavaScript WebSocket client](#javascript-websocket-client) example.

### Python

To publish events from Python, install Pusher's [Python HTTP SDK](https://github.com/pusher/pusher-http-python):

```sh theme={null}
pip install pusher
```

Then, create a client using the injected variables and trigger an event:

```python theme={null}
import os

import pusher

client = pusher.Pusher(
    app_id=os.environ["PUSHER_APP_ID"],
    key=os.environ["PUSHER_APP_KEY"],
    secret=os.environ["PUSHER_APP_SECRET"],
    host=os.environ["PUSHER_HOST"],
    port=int(os.environ["PUSHER_PORT"]),
    ssl=os.environ["PUSHER_SCHEME"] == "https",
)

client.trigger("notifications", "message-sent", {
    "message": "Hello from Laravel Cloud",
})
```

### Go

To publish events from Go, install Pusher's [Go HTTP SDK](https://github.com/pusher/pusher-http-go):

```sh theme={null}
go get github.com/pusher/pusher-http-go/v5
```

The Go SDK expects the port to be included in its `Host` field, so the following example joins `PUSHER_HOST` and `PUSHER_PORT` together:

```go theme={null}
package main

import (
	"log"
	"net"
	"os"

	"github.com/pusher/pusher-http-go/v5"
)

func main() {
	client := pusher.Client{
		AppID:  os.Getenv("PUSHER_APP_ID"),
		Key:    os.Getenv("PUSHER_APP_KEY"),
		Secret: os.Getenv("PUSHER_APP_SECRET"),
		Host:   net.JoinHostPort(os.Getenv("PUSHER_HOST"), os.Getenv("PUSHER_PORT")),
		Secure: os.Getenv("PUSHER_SCHEME") == "https",
	}

	err := client.Trigger("notifications", "message-sent", map[string]string{
		"message": "Hello from Laravel Cloud",
	})
	if err != nil {
		log.Fatal(err)
	}
}
```

### Ruby

To publish events from Ruby, add Pusher's [Ruby HTTP SDK](https://github.com/pusher/pusher-http-ruby) to your application's `Gemfile` and run `bundle install`:

```ruby theme={null}
gem "pusher"
```

Then, create a client using the injected variables and trigger an event:

```ruby theme={null}
require "pusher"

client = Pusher::Client.new(
  app_id: ENV.fetch("PUSHER_APP_ID"),
  key: ENV.fetch("PUSHER_APP_KEY"),
  secret: ENV.fetch("PUSHER_APP_SECRET"),
  host: ENV.fetch("PUSHER_HOST"),
  port: Integer(ENV.fetch("PUSHER_PORT")),
  use_tls: ENV.fetch("PUSHER_SCHEME") == "https"
)

client.trigger("notifications", "message-sent", {
  message: "Hello from Laravel Cloud"
})
```

### Java

To publish events from Java, add Pusher's [Java HTTP SDK](https://github.com/pusher/pusher-http-java) to your Maven dependencies:

```xml theme={null}
<dependency>
    <groupId>com.pusher</groupId>
    <artifactId>pusher-http-java</artifactId>
    <version>1.3.5</version>
</dependency>
```

Then, configure the client's host and encryption settings and trigger an event:

```java theme={null}
import com.pusher.rest.Pusher;
import com.pusher.rest.data.Result;
import java.util.Collections;

public class Publish {
    public static void main(String[] args) {
        Pusher pusher = new Pusher(
            System.getenv("PUSHER_APP_ID"),
            System.getenv("PUSHER_APP_KEY"),
            System.getenv("PUSHER_APP_SECRET")
        );
        pusher.setHost(System.getenv("PUSHER_HOST"));
        pusher.setEncrypted("https".equals(System.getenv("PUSHER_SCHEME")));

        Result result = pusher.trigger(
            "notifications",
            "message-sent",
            Collections.singletonMap("message", "Hello from Laravel Cloud")
        );

        if (result.getStatus() != Result.Status.SUCCESS) {
            throw new IllegalStateException(result.getMessage());
        }
    }
}
```

You may notice that the example doesn't configure a port. The Java HTTP SDK doesn't offer a port setting. It always uses the default HTTPS port of `443`, which is the port Laravel Cloud listens on.

## Receiving events

While the HTTP SDKs can only publish events, Pusher's WebSocket SDKs hold open a persistent connection to your WebSocket application and receive events as they are published. The following examples use Pusher's JavaScript and Java clients. Pusher also offers WebSocket clients for other platforms, such as Swift and .NET.

### JavaScript WebSocket client

To receive events in the browser, install Pusher's [JavaScript WebSocket SDK](https://github.com/pusher/pusher-js):

```sh theme={null}
npm install pusher-js
```

Then, create a client in your browser application. In the following example, replace the placeholder key and hostname with the `PUSHER_APP_KEY` and `PUSHER_HOST` values from your attached WebSocket application:

```javascript theme={null}
import Pusher from 'pusher-js';

const pusher = new Pusher('your-app-key', {
    cluster: 'mt1',
    wsHost: 'ws-your-cluster-reverb.laravel.cloud',
    wssPort: 443,
    forceTLS: true,
    enabledTransports: ['ws'],
});

const channel = pusher.subscribe('notifications');

channel.bind('message-sent', (data) => {
    console.log(data.message);
});
```

The SDK requires a `cluster` option. Because `wsHost` is set and only the `ws` transport is enabled, `mt1` is only a placeholder and does not select a Pusher or Laravel Cloud region. The `forceTLS` option makes the connection use secure WebSockets.

Your application key and hostname are safe to share with the browser. For stacks other than Laravel, Laravel Cloud does not create frontend variables such as `VITE_PUSHER_*`. You need to render these values into your frontend's configuration or define them through your build tool yourself. Your `PUSHER_APP_SECRET` should never leave your server, so take care not to expose your server's full environment to browser code.

Laravel Cloud automatically allows connections from your attached environments. If your browser application is hosted on another domain, add its URL (for example, `https://frontend.example.com`) to your WebSocket application's **Allowed origins** before connecting.

### Java WebSocket client

Pusher's Java WebSocket SDK doesn't send an `Origin` header, nor does it provide a way to set one. As a result, Laravel Cloud rejects its connections unless your WebSocket application's **Allowed origins** is set to `*`.

> [!WARNING]
>
> Setting **Allowed origins** to `*` allows connections from any origin, including browsers on other sites. Anyone with your public application key can subscribe to your public channels, so use private or presence channels for any data that requires access control.

Once your allowed origins are updated, add Pusher's [Java WebSocket SDK](https://github.com/pusher/pusher-websocket-java) to your Maven dependencies:

```xml theme={null}
<dependency>
    <groupId>com.pusher</groupId>
    <artifactId>pusher-java-client</artifactId>
    <version>2.4.4</version>
</dependency>
```

Then, connect using your application's key and WebSocket host and subscribe to the channel:

```java theme={null}
import com.pusher.client.Pusher;
import com.pusher.client.PusherOptions;
import com.pusher.client.channel.Channel;
import java.util.concurrent.CountDownLatch;

public class Subscribe {
    public static void main(String[] args) throws InterruptedException {
        PusherOptions options = new PusherOptions()
            .setHost(System.getenv("PUSHER_HOST"))
            .setWssPort(Integer.parseInt(System.getenv("PUSHER_PORT")))
            .setUseTLS("https".equals(System.getenv("PUSHER_SCHEME")));

        Pusher pusher = new Pusher(System.getenv("PUSHER_APP_KEY"), options);
        Channel channel = pusher.subscribe("notifications");
        channel.bind("message-sent", event -> System.out.println(event.getData()));

        Runtime.getRuntime().addShutdownHook(new Thread(pusher::disconnect));
        pusher.connect();

        new CountDownLatch(1).await();
    }
}
```

The `CountDownLatch` keeps this standalone example running so that it can continue listening for events. In an existing application, tie the connection to your application's lifecycle instead.

## Private and presence channels

The examples in this guide use a public channel, which anyone may subscribe to without authorization. Private and presence channels require your application to provide an authorization endpoint. The endpoint should authenticate the user, verify that they may access the requested channel, and then use your HTTP SDK to sign and return an authorization response. You also need to configure your WebSocket client's authorization options so that it calls the endpoint when subscribing.

Pusher's [authorizing users](https://pusher.com/docs/channels/server_api/authorizing-users/) documentation covers the authorization API for each SDK. Keep your application secret on your server. Return only the signed authorization response to the client.
