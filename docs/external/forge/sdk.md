Source: https://laravel.com/forge/docs/sdk.md

# Laravel Forge SDK

> A PHP SDK for interacting with the Laravel Forge API.

> [card] [Laravel Forge SDK](https://github.com/laravel/forge-sdk)
>
> View the Laravel Forge SDK on GitHub

> [card] [Laravel Forge API](https://forge.laravel.com/api-documentation)
>
> View the Laravel Forge API documentation

## Introduction

The [Laravel Forge SDK](https://github.com/laravel/forge-sdk) provides an expressive PHP interface for interacting with the Laravel Forge API and managing your servers, sites, and other resources programmatically.

The SDK targets the Forge API and provides access to platform resources such as servers, sites, databases, scheduled jobs, background processes, integrations, teams, roles, and more.

## Installation

To install the SDK in your project, you should require the package via Composer:

```bash theme={null}
composer require laravel/forge-sdk
```

## Upgrading From v3.x

> [!WARNING]
>
> Forge SDK v4.0 targets the Forge API v2 and contains significant breaking changes. Every resource endpoint now requires an organization slug as the first argument. Several action traits have been renamed, and a handful of legacy features have been removed.

When upgrading from v3.x, we recommend carefully reviewing the [v4.0 upgrade guide](https://github.com/laravel/forge-sdk/blob/4.x/UPGRADE-4.0.md) on GitHub. The upgrade guide details every method signature change, the renamed action traits, and the migration strategy you should follow.

## Basic Usage

You may create an instance of the SDK by passing an API token generated from [Forge's API dashboard](https://forge.laravel.com/profile/api):

```php theme={null}
$forge = new Laravel\Forge\Forge($token);
```

### The Organization Slug

Starting in v4.0, every resource endpoint is scoped to an [organization](https://forge.laravel.com/docs/organizations.md). Before making most calls, you must determine the slug of the organization you want to interact with by listing the authenticated user's organizations:

```php theme={null}
$organizations = $forge->organizations();

$organizationSlug = $organizations[0]->slug;
```

The following endpoints are examples of methods that do not require an organization slug:

* `$forge->user()` / `$forge->me()`
* `$forge->organizations()`
* `$forge->providers()`
* `$forge->permissions()`
* `$forge->predefinedRoles()`

> [!TIP]
>
> We recommend caching the organization slug in your application configuration rather than resolving it on every request.

### Retrieving Resources

Once you have an organization slug, you may retrieve resources scoped to that organization:

```php theme={null}
$servers = $forge->servers($organizationSlug);

$server = $forge->server($organizationSlug, $serverId);
```

Each resource is represented by a class such as `Laravel\Forge\Resources\Server`. Resource instances expose public properties such as `$name`, `$id`, `$size`, and `$region`.

### Paginated Collections

Collection methods such as `servers()`, `serverSites()`, and `recipes()` return a `Laravel\Forge\CursorPaginator` rather than a plain array. The paginator may be iterated directly for the current page, iterated lazily to fetch additional pages on demand, or converted to an array:

```php theme={null}
// Iterate the current page
foreach ($forge->servers($organizationSlug) as $server) {
    echo $server->name;
}

// Lazily iterate across every page — the next cursor is fetched on demand
foreach ($forge->servers($organizationSlug)->lazy() as $server) {
    echo $server->name;
}

// Snapshot the current page as a plain array
$page = $forge->servers($organizationSlug)->toArray();
```

### Creating Resources

When creating resources, you should pass the organization slug as the first argument and the request payload as the second:

```php theme={null}
use Laravel\Forge\ServerProviders;
use Laravel\Forge\InstallableServices;

$server = $forge->createServer($organizationSlug, [
    'provider' => ServerProviders::DIGITAL_OCEAN,
    'credential_id' => 1,
    'name' => 'test-via-api',
    'type' => 'app',
    'size' => '01',
    'database' => 'test123',
    'database_type' => InstallableServices::POSTGRES,
    'php_version' => InstallableServices::PHP_84,
    'region' => 'ams2',
]);
```

For a full list of parameters accepted by each endpoint, consult the [official Forge API documentation](https://forge.laravel.com/api-documentation).

### Waiting for Asynchronous Operations

Some operations, such as creating a server or a site, are processed asynchronously by Forge. By default, the SDK will poll the API every few seconds until the resource has finished provisioning, up to a maximum of 30 seconds:

```php theme={null}
$site = $forge->createSite($organizationSlug, $serverId, [
    'domain' => 'example.com',
    'type' => 'php',
]);
```

If you do not wish to wait, you may pass `false` as the final argument:

```php theme={null}
$site = $forge->createSite($organizationSlug, $serverId, $data, false);
```

You may customize the timeout in seconds using the `setTimeout` method:

```php theme={null}
$site = $forge->setTimeout(120)->createSite($organizationSlug, $serverId, $data);
```

If the timeout is exceeded, a `Laravel\Forge\Exceptions\TimeoutException` will be thrown.

## Managing Organizations

```php theme={null}
$organizations = $forge->organizations();
$organization = $forge->organization($organizationSlug);

// Server credentials
$credentials = $forge->serverCredentials($organizationSlug);
$credential = $forge->serverCredential($organizationSlug, $credentialId);
```

## Managing Servers

```php theme={null}
$servers = $forge->servers($organizationSlug);
$server = $forge->server($organizationSlug, $serverId);

$server = $forge->createServer($organizationSlug, $data);

$forge->deleteServer($organizationSlug, $serverId);

// Server actions, such as reboot
$forge->createServerAction($organizationSlug, $serverId, [
    'action' => 'reboot',
]);

// Archived servers
$archivedServers = $forge->archivedServers($organizationSlug);
```

### Server Service Actions

```php theme={null}
$forge->performNginxAction($organizationSlug, $serverId, ['action' => 'restart']);
$forge->performMySQLAction($organizationSlug, $serverId, ['action' => 'restart']);
$forge->performPostgresAction($organizationSlug, $serverId, ['action' => 'restart']);
$forge->performRedisAction($organizationSlug, $serverId, ['action' => 'restart']);
$forge->performPHPAction($organizationSlug, $serverId, ['action' => 'restart']);
$forge->performSupervisorAction($organizationSlug, $serverId, ['action' => 'restart']);
```

## Managing Sites

```php theme={null}
$sites = $forge->serverSites($organizationSlug, $serverId);
$site = $forge->organizationSite($organizationSlug, $siteId);

$site = $forge->createSite($organizationSlug, $serverId, $data);
$site = $forge->updateSite($organizationSlug, $serverId, $siteId, $data);

$forge->deleteSite($organizationSlug, $serverId, $siteId);
```

### Site Domains and Certificates

```php theme={null}
$domains = $forge->domains($organizationSlug, $serverId, $siteId);
$domain = $forge->createDomain($organizationSlug, $serverId, $siteId, $data);
$forge->deleteDomain($organizationSlug, $serverId, $siteId, $domainId);

$certificates = $forge->domainCertificates($organizationSlug, $serverId, $siteId, $domainId);
$active = $forge->activeDomainCertificate($organizationSlug, $serverId, $siteId, $domainId);
$certificate = $forge->certificate($organizationSlug, $serverId, $siteId, $domainId, $certificateId);

$forge->createCertificate($organizationSlug, $serverId, $siteId, $domainId, $data);
$forge->deleteCertificate($organizationSlug, $serverId, $siteId, $domainId, $certificateId);
```

### Site Deployments

```php theme={null}
$webhooks = $forge->webhooks($organizationSlug, $serverId, $siteId);
$forge->createWebhook($organizationSlug, $serverId, $siteId, $data);

$script = $forge->deploymentScript($organizationSlug, $serverId, $siteId);
$forge->updateDeploymentScript($organizationSlug, $serverId, $siteId, $content);

$deployment = $forge->createDeployment($organizationSlug, $serverId, $siteId);

$forge->createPushToDeploy($organizationSlug, $serverId, $siteId, $data);
$forge->deletePushToDeploy($organizationSlug, $serverId, $siteId);
```

### Laravel Integrations

The SDK exposes first-class support for managing Laravel ecosystem integrations on each site, including Horizon, Octane, Reverb, Pulse, Inertia, Laravel Maintenance Mode, and the Laravel Scheduler:

```php theme={null}
$forge->getHorizon($organizationSlug, $serverId, $siteId);
$forge->createHorizon($organizationSlug, $serverId, $siteId, $data);
$forge->deleteHorizon($organizationSlug, $serverId, $siteId);

$forge->getOctane($organizationSlug, $serverId, $siteId);
$forge->createOctane($organizationSlug, $serverId, $siteId, $data);

$forge->getReverb($organizationSlug, $serverId, $siteId);
$forge->createReverb($organizationSlug, $serverId, $siteId, $data);

$forge->getPulse($organizationSlug, $serverId, $siteId);
$forge->createPulse($organizationSlug, $serverId, $siteId, $data);
```

### Site Workers

```php theme={null}
$workers = $forge->workers($organizationSlug, $serverId, $siteId);
$worker = $forge->createWorker($organizationSlug, $serverId, $siteId, $data);

$forge->createWorkerAction($organizationSlug, $serverId, $siteId, $workerId, [
    'action' => 'restart',
]);
```

### Site Configuration

```php theme={null}
// Environment file
$forge->siteEnvironment($organizationSlug, $serverId, $siteId);
$forge->updateSiteEnvironment($organizationSlug, $serverId, $siteId, $content);

// Nginx configuration
$forge->siteNginx($organizationSlug, $serverId, $siteId);
$forge->updateSiteNginx($organizationSlug, $serverId, $siteId, $content);

// PHP version
$forge->sitePhp($organizationSlug, $serverId, $siteId);
$forge->updateSitePhp($organizationSlug, $serverId, $siteId, ['version' => 'php84']);
```

## Managing Databases

```php theme={null}
$databases = $forge->databases($organizationSlug, $serverId);
$database = $forge->database($organizationSlug, $serverId, $databaseId);

$database = $forge->createDatabase($organizationSlug, $serverId, $data);
$forge->deleteDatabase($organizationSlug, $serverId, $databaseId);

// Database users
$users = $forge->databaseUsers($organizationSlug, $serverId);
$user = $forge->createDatabaseUser($organizationSlug, $serverId, $data);
$forge->deleteDatabaseUser($organizationSlug, $serverId, $userId);
```

## Background Processes

> [!NOTE]
>
> Background processes were referred to as "daemons" in v3.x of the SDK. The `ManagesDaemons` trait has been renamed to `ManagesBackgroundProcesses` and every method has been renamed accordingly.

```php theme={null}
$processes = $forge->backgroundProcesses($organizationSlug, $serverId);
$process = $forge->createBackgroundProcess($organizationSlug, $serverId, $data);

$forge->deleteBackgroundProcess($organizationSlug, $serverId, $processId);
```

## Scheduled Jobs

```php theme={null}
$jobs = $forge->scheduledJobs($organizationSlug, $serverId);
$job = $forge->createScheduledJob($organizationSlug, $serverId, $data);

$forge->deleteScheduledJob($organizationSlug, $serverId, $jobId);
```

## PHP Version Management

```php theme={null}
$versions = $forge->phpVersions($organizationSlug, $serverId);

$forge->installPhpVersion($organizationSlug, $serverId, ['version' => 'php84']);

$forge->phpFpmConfig($organizationSlug, $serverId, $phpVersion);
$forge->updatePhpFpmConfig($organizationSlug, $serverId, $phpVersion, $content);
```

## Teams, Roles, and Permissions

```php theme={null}
// Teams
$teams = $forge->teams($organizationSlug);
$team = $forge->createTeam($organizationSlug, $data);

$members = $forge->teamMembers($organizationSlug, $teamId);
$invitations = $forge->teamInvitations($organizationSlug, $teamId);

// Roles
$roles = $forge->roles($organizationSlug);
$role = $forge->createRole($organizationSlug, $data);

// Permissions
$permissions = $forge->permissions();
$predefinedRoles = $forge->predefinedRoles();
```

## Recipes

```php theme={null}
// Organization recipes
$recipes = $forge->recipes($organizationSlug);
$recipe = $forge->createRecipe($organizationSlug, $data);

$run = $forge->createRecipeRun($organizationSlug, $recipeId, $data);

// Forge-provided recipes
$forgeRecipes = $forge->forgeRecipes();
```

## Providers

```php theme={null}
$providers = $forge->providers();
$provider = $forge->provider($providerId);

$sizes = $forge->providerSizes($providerId);
$regions = $forge->providerRegions($providerId);
```

## Error Handling

The SDK throws dedicated exception classes that you may catch to handle specific error states:

* `Laravel\Forge\Exceptions\ValidationException`
* `Laravel\Forge\Exceptions\NotFoundException`
* `Laravel\Forge\Exceptions\ForbiddenException`
* `Laravel\Forge\Exceptions\FailedActionException`
* `Laravel\Forge\Exceptions\RateLimitExceededException`
* `Laravel\Forge\Exceptions\TimeoutException`

> [!TIP]
>
> If you are looking for application performance monitoring for the Laravel applications you deploy with Forge, take a look at [Laravel Nightwatch](https://nightwatch.laravel.com). If you prefer fully managed Laravel hosting, consider [Laravel Cloud](https://cloud.laravel.com).
