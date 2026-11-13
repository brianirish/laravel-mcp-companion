Source: https://nightwatch.laravel.com/docs/webhooks.md

# Webhooks

> Configure webhooks to receive HTTP POST notifications when events occur in your application

## Setup

**1. Open your application settings**

Navigate to your application's Issues settings in the Nightwatch dashboard.

**2. Add a webhook**

In the **Webhooks** section, configure your webhook:

* **Name**: A descriptive label for your reference (e.g., "Slack notifications", "Internal API")
* **URL**: An HTTPS endpoint that accepts POST requests

> [!NOTE]
>
> Only one webhook per application is allowed. To change the URL or name, edit the existing webhook configuration.

***

## Request format

Every webhook request is an HTTP POST with a JSON body of this shape:

| Field | Type | Description |
| - | - | - |
| `event` | string | Event type (e.g. `issue.opened`, `issue.resolved`) |
| `timestamp` | string | ISO 8601 datetime when the event was sent (e.g. `2026-02-18T12:00:00.000000Z`) |
| `payload` | object | Event data (see below) plus metadata |

The `payload` object always includes:

| Field | Type | Description |
| - | - | - |
| `webhook_id` | string | UUID of the webhook |
| `application_id` | string | UUID of the application |
| `organization_id` | string | UUID of the organization |

Plus the event-specific fields described for each event below.

***

## Events

### `issue.opened`

Sent when a new issue is created (first time the exception or performance problem is detected).

**When it fires:** A new issue is created for the application (e.g. new exception group or new slow route/job).

**Payload (in addition to metadata):**

| Field | Type | Description |
| - | - | - |
| `issue` | object | The issue (see [Issue object](#issue-object)) |
| `environment` | object | Environment where the issue was detected (see [Environment object](#environment-object)) |

### `issue.reopened`

Sent when an issue that was previously resolved is seen again and reopened.

**When it fires:** The same exception or performance issue is detected again after the issue was closed.

**Payload (in addition to metadata):**

| Field | Type | Description |
| - | - | - |
| `issue` | object | The issue (see [Issue object](#issue-object)) |
| `environment` | object | Environment where the issue was detected (see [Environment object](#environment-object)) |

### `issue.ignored`

Sent when an issue’s status is set to **Ignored**.

**When it fires:** A user (or automation) marks the issue as ignored.

**Payload (in addition to metadata):**

| Field | Type | Description |
| - | - | - |
| `issue` | object | The issue (see [Issue object](#issue-object)) |
| `actor` | object | User who performed the action, if any (see [Actor object](#actor-object)) |

### `issue.resolved`

Sent when an issue’s status is set to **Resolved**.

**When it fires:** A user (or automation) marks the issue as resolved.

**Payload (in addition to metadata):**

| Field | Type | Description |
| - | - | - |
| `issue` | object | The issue (see [Issue object](#issue-object)) |
| `actor` | object | User who performed the action, if any (see [Actor object](#actor-object)) |

## Shared payload objects

### Issue object

| Field | Type | Description |
| - | - | - |
| `id` | string | Issue UUID |
| `ref` | int | Display number (e.g. issue #123) |
| `type` | string | `"exception"` or `"performance"` |
| `title` | string | Issue title |
| `status` | string | `"open"`, `"resolved"`, or `"ignored"` |
| `priority` | string | `"none"`, `"low"`, `"medium"`, or `"high"` |
| `url` | string | Link to the issue in the dashboard |
| `details` | object | Details about the issue (see [Issue details object](#issue-details-object)) |

### Issue details object

#### Exception

| Field | Type | Description |
| - | - | - |
| `type` | `exception` | Type of issue |
| `handled` | boolean | Whether the exception was caught |
| `class` | string | Fully qualified exception class (e.g. `"Illuminate\Database\QueryException"`) |
| `message` | string | Exception message |
| `file` | string | Application file path where the exception was thrown |
| `line` | int | Line number in that file |
| `laravel_version` | string | Laravel version when the exception occurred |
| `php_version` | string | PHP version when the exception occurred |

#### Request performance issue

| Field | Type | Description |
| - | - | - |
| `type` | `slow-route` | Type of performance issue |
| `methods` | array | HTTP methods (e.g. `["GET", "HEAD"]`) |
| `path` | string | Route path (e.g. `"/flights/{id}"`) |
| `action` | string | Controller action (e.g. `"App\Http\Controllers\FlightController@index"`) |
| `duration` | string | Request duration in milliseconds (e.g. `"7,237ms"`) |
| `threshold` | string | Configured threshold in milliseconds (e.g. `"1,000ms"`) |

#### Job performance issue

| Field | Type | Description |
| - | - | - |
| `type` | `slow-job` | Type of performance issue |
| `name` | string | Job class (e.g. `App\Jobs\ProcessRefund`) |
| `duration` | string | Request duration in milliseconds (e.g. `"7,237ms"`) |
| `threshold` | string | Configured threshold in milliseconds (e.g. `"1,000ms"`) |

#### Command performance issue

| Field | Type | Description |
| - | - | - |
| `type` | `slow-command` | Type of performance issue |
| `name` | string | Command name (e.g. `reminders:send`) |
| `duration` | string | Request duration in milliseconds (e.g. `"7,237ms"`) |
| `threshold` | string | Configured threshold in milliseconds (e.g. `"1,000ms"`) |

#### Scheduled task performance issue

| Field | Type | Description |
| - | - | - |
| `type` | `slow-scheduled-task` | Type of performance issue |
| `name` | string | Task name (e.g. `"php artisan reminders:send"`) |
| `cron` | string | Cron schedule (e.g. `"* * * * *"` for every minute) |
| `timezone` | string | Timezone (e.g. "UTC") |
| `duration` | string | Request duration in milliseconds (e.g. `"7,237ms"`) |
| `threshold` | string | Configured threshold in milliseconds (e.g. `"1,000ms"`) |

### Environment object

| Field | Type | Description |
| - | - | - |
| `id` | string | Environment UUID |
| `name` | string | Environment name |

### Actor object

Present when the action was performed by a user.

| Field | Type | Description |
| - | - | - |
| `id` | string | User UUID |
| `name` | string | User display name |
| `email` | string | User email |
| `type` | string | Always `"user"` |

***

## Example request

```json theme={null}
{
  "event": "issue.resolved",
  "timestamp": "2026-02-18T12:00:00.000000Z",
  "payload": {
    "issue": {
      "id": "9d4e2c1a-1234-5678-abcd-ef0123456789",
      "ref": 42,
      "type": "exception",
      "title": "Illuminate\\Database\\QueryException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '1' for key 'flights_id_unique' (Connection: mysql, SQL: insert into \"flights\" (\"id\", \"name\", \"created_at\", \"updated_at\") values (?, ?, ?, ?))",
      "status": "resolved",
      "priority": "high",
      "url": "https://nightwatch.laravel.com/us/applications/cf592d1a-5f91-4f3c-9c10-8c67013c4469/issues/42",
      "details": {
        "type": "exception",
        "handled": false,
        "class": "Illuminate\\Database\\QueryException",
        "message": "SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '1' for key 'flights_id_unique' (Connection: mysql, SQL: insert into \"flights\" (\"id\", \"name\", \"created_at\", \"updated_at\") values (?, ?, ?, ?))",
        "file": "app/Actions/ProcessFlight.php",
        "line": 123,
        "laravel_version": "12.52.0",
        "php_version": "8.4.11"
      }
    },
    "actor": {
      "id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
      "name": "Jane Doe",
      "email": "jane@example.com",
      "type": "user"
    },
    "webhook_id": "fa2d5c2d-3b8c-41ad-8cf6-52f80d446818",
    "application_id": "cf592d1a-5f91-4f3c-9c10-8c67013c4469",
    "organization_id": "9cfeeac6-d449-4924-852b-c3a3294db9c2"
  }
}
```

***

## Verifying signatures

Each webhook request includes a `Nightwatch-Signature` header that allows you to verify the request came from Nightwatch and has not been tampered with.

**1. Get your signing secret**

You can find and copy the signing secret at any time in your application's Issues settings > Webhooks > Edit.

**2. Compute the expected signature**

Using the raw request body (the exact JSON string received) and your signing secret, compute an HMAC-SHA256 signature:

* **Algorithm:** HMAC-SHA256
* **Message:** Raw request body
* **Key:** Your webhook signing secret

**3. Compare signatures**

Compare the computed signature with the `Nightwatch-Signature` header using a constant-time comparison to prevent timing attacks. If they match, the request is authentic.

> [!NOTE]
>
> Store your webhook signing secret in your application's configuration file or environment variables for security.

**Laravel example:**

```php theme={null}
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;

class NightwatchWebhookController extends Controller
{
    public function handle(Request $request): Response
    {
        $payload = $request->getContent();
        $signature = $request->header('Nightwatch-Signature');
        $secret = config('services.nightwatch.webhook_secret');
        
        $expectedSignature = hash_hmac('sha256', $payload, $secret);
        
        if (! hash_equals($expectedSignature, $signature)) {
            abort(401, 'Invalid signature');
        }
        
        // Process the verified webhook payload
        $data = json_decode($payload, true);
        
        // Handle the webhook event based on $data['event']
        match ($data['event']) {
            'issue.opened' => $this->handleIssueOpened($data['payload']),
            'issue.resolved' => $this->handleIssueResolved($data['payload']),
            'issue.reopened' => $this->handleIssueReopened($data['payload']),
            'issue.ignored' => $this->handleIssueIgnored($data['payload']),
            default => logger()->info('Unknown webhook event', ['event' => $data['event']]),
        };
        
        return response()->json(['status' => 'success']);
    }
    
    private function handleIssueOpened(array $payload): void
    {
        // Handle new issue notification
    }
    
    private function handleIssueResolved(array $payload): void
    {
        // Handle issue resolution notification
    }
    
    private function handleIssueReopened(array $payload): void
    {
        // Handle issue reopening notification
    }
    
    private function handleIssueIgnored(array $payload): void
    {
        // Handle issue ignored notification
    }
}
```

**Configuration example (`config/services.php`):**

```php theme={null}
return [
    // Other service configurations...
    
    'nightwatch' => [
        'webhook_secret' => env('NIGHTWATCH_WEBHOOK_SECRET'),
    ],
];
```
