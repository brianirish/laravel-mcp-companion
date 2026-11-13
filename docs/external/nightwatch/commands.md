Source: https://nightwatch.laravel.com/docs/commands.md

# Commands

> Artisan commands executed in your Laravel application

Nightwatch automatically captures all Artisan commands, including those run via `php artisan`, programmatically via `Artisan::call()`, and scheduled commands.

Commands are one of the primary execution contexts in Nightwatch, alongside requests and scheduled tasks. Each command execution becomes the starting point of a new trace, where all subsequent events such as database queries, queued jobs, and exceptions are captured and linked together to provide a complete picture of your application’s behavior.

## Command List

View all commands for an application from the **Commands** panel. Each command is displayed with its name, success and failure statistics and average and p95 execution times.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of commands. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Command Details

Click any command in the list to open its details page, where you can view its performance over time. The page also shows every individual execution of that command, and selecting one opens the full trace so you can see the command and all of its associated child events.

## Sampling

### Global Sampling

You can configure global sampling for Artisan commands using the `NIGHTWATCH_COMMAND_SAMPLE_RATE` environment variable. When a command is sampled in, Nightwatch captures the full execution context, including related database queries, queued jobs, and exceptions.

```bash theme={null}
NIGHTWATCH_COMMAND_SAMPLE_RATE=1.0 # Sample 100% of commands
```

### Sampling Specific Commands

You can exclude specific commands from sampling by listening for the `CommandStarting` event:

```php AppServiceProvider.php theme={null}
use Illuminate\Console\Events\CommandStarting;
use Illuminate\Support\Facades\Event;
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Event::listen(function (CommandStarting $event) {
        if (in_array($event->command, [
            'schedule:finish',
            // ...
        ])) {
            Nightwatch::dontSample();
        }
    });
}
```

### Sampling vendor commands

For convenience, Nightwatch won't automatically sample some commands from the Laravel framework or first-party packages. These are framework commands that are not typically of interest to most applications. This includes:

* Laravel framework internals (e.g. scheduler, queue worker)
* Laravel Horizon
* Laravel Nightwatch
* Laravel Reverb
* Inertia SSR

You can inspect the full list of ignored commands by running `php artisan tinker` and calling `Nightwatch::defaultVendorCommands()`.

You can opt in to collecting these using `captureDefaultVendorCommands`, but be cautioned that this can increase the number of events captured:

```php AppServiceProvider.php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;

public function boot(): void
{
    Nightwatch::captureDefaultVendorCommands();
}
```

## Filtering

There are no specific filtering methods for commands. To conditionally exclude commands from collection, you can use the sampling mechanisms described above.

## Redaction

You can manually redact command arguments that may contain sensitive information using the `redactCommands` callback:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Command;

Nightwatch::redactCommands(function (Command $command) {
    $command->command = str_replace('secret', '***', $command->command);
});
```
