# Forge - Sdk

*Source: https://forge.laravel.com/docs/sdk*

---

## On this page
- [Introduction](#introduction)
- [Installation](#installation)
- [Upgrading](#upgrading)
- [Basic usage](#basic-usage)
Get Started
# Laravel Forge SDK
Copy page
A PHP SDK for interacting with Laravel Forge.
Copy page
## Laravel Forge SDK
View the Laravel Forge SDK on GitHub
## Laravel Forge API
View the Laravel Forge API documentation
## [​](#introduction) Introduction
The [Laravel Forge SDK](https://github.com/laravel/forge-sdk) provides an expressive interface for interacting with Forge’s API and managing Laravel Forge servers.
## [​](#installation) Installation
To install the SDK in your project you need to require the package via composer:
```
composer require laravel/forge-sdk
```
## [​](#upgrading) Upgrading
When upgrading to a new major version of Laravel Forge SDK, it’s important that you carefully review [the upgrade guide](https://github.com/laravel/forge-sdk/blob/master/UPGRADE.md).
## [​](#basic-usage) Basic usage
You can create an instance of the SDK like so:
```
$forge = new Laravel\Forge\Forge(TOKEN_HERE);
```
Using the `Forge` instance you may perform multiple actions as well as retrieve the different resources Forge’s API provides:
```
$servers = $forge->servers();
```
This will give you an array of servers that you have access to, where each server is represented by an instance of `Laravel\Forge\Resources\Server`, this instance has multiple public properties like `$name`, `$id`, `$size`, `$region`, and others.
You may also retrieve a single server using:
```
$server = $forge->server(SERVER_ID_HERE);
```
On multiple actions supported by this SDK you may need to pass some parameters, for example when creating a new server:
```
$server = $forge->createServer([
    "provider"=> ServerProviders::DIGITAL_OCEAN,
    "credential_id"=> 1,
    "name"=> "test-via-api",
    "type"=> ServerTypes::APP,
    "size"=> "01",
    "database"=> "test123",
    "database_type" => InstallableServices::POSTGRES,
    "php_version"=> InstallableServices::PHP_84,
    "region"=> "ams2"
]);
```
These parameters will be used in the POST request sent to Laravel Forge servers, you can find more information about the parameters needed for each action on
[Laravel Forge’s official API documentation](https://forge.laravel.com/api-documentation).
Notice that this request for example will only start the server creation process, your server might need a few minutes before it completes provisioning, you’ll need to check the server’s `$isReady` property to know if it’s ready or not yet.
Some SDK methods however wait for the action to complete on Laravel Forge’s end, we do this by periodically contacting Forge servers and checking if our action has completed, for example:
```
$forge->createSite(SERVER_ID, [SITE_PARAMETERS]);
```
This method will ping Laravel Forge servers every 5 seconds and see if the newly created Site’s status is `installed` and only return when it’s so, in case the waiting exceeded 30 seconds a `Laravel\Forge\Exceptions\TimeoutException` will be thrown.
You can easily stop this behavior by setting the `$wait` argument to false:
```
$forge->createSite(SERVER_ID, [SITE_PARAMETERS], false);
```
You can also set the desired timeout value:
```
$forge->setTimeout(120)->createSite(SERVER_ID, [SITE_PARAMETERS]);
```
Was this page helpful?
YesNo
[Laravel Forge CLI](/docs/cli)[Organizations](/docs/organizations)
⌘I