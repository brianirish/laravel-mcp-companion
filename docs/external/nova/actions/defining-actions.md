# Nova - Actions/Defining-Actions

*Source: https://nova.laravel.com/docs/v5/actions/defining-actions*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Actions
Defining Actions
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
- [Blog](https://blog.laravel.com)
##### Get Started
- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)
##### Resources
- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)
##### Search
- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)
##### Filters
- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)
##### Lenses
- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)
##### Actions
- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)
##### Metrics
- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)
##### Digging Deeper
- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)
On this page
- [Overview](#overview)
- [Action Titles](#action-titles)
- [Destructive Actions](#destructive-actions)
- [Action Callbacks](#action-callbacks)
- [Action Fields](#action-fields)
- [Action Fields Default Values](#action-fields-default-values)
- [Action Responses](#action-responses)
- [Redirect Responses](#redirect-responses)
- [Download Responses](#download-responses)
- [Emitting Client Side Events](#emitting-client-side-events)
- [Custom Modal Responses](#custom-modal-responses)
- [Queued Actions](#queued-actions)
- [Customizing the Connection and Queue](#customizing-the-connection-and-queue)
- [Job Batching](#job-batching)
- [Action Log](#action-log)
- [Disabling the Action Log](#disabling-the-action-log)
- [Queued Action Statuses](#queued-action-statuses)
- [Action Modal Customization](#action-modal-customization)
Actions
# Defining Actions
Defining actions in Nova
Nova actions allow you to perform custom tasks on one or more Eloquent models. For example, you might write an action that sends an email to a user containing account data they have requested. Or, you might write an action to transfer a group of records to another user.
Once an action has been attached to a resource definition, you may initiate it from the resource’s index or detail pages:
If an action is enabled for display on the resource’s table row, you may also initiate the action from the resource’s action dropdown menu via the resource index page. These actions are referred to as “Inline Actions”:
## [​](#overview) Overview
Nova actions may be generated using the `nova:action` Artisan command. By default, all actions are placed in the `app/Nova/Actions` directory:
Copy
Ask AI
```
php artisan nova:action EmailAccountProfile
```
You may generate a [destructive action](#destructive-actions) by passing the `--destructive` option:
Copy
Ask AI
```
php artisan nova:action DeleteUserData --destructive
```
To learn how to define Nova actions, let’s look at an example. In this example, we’ll define an action that sends an email message to a user or group of users:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
namespace App\Nova\Actions;

use App\Models\AccountData;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Fields\ActionFields;

class EmailAccountProfile extends Action
{
    use InteractsWithQueue;
    use Queueable;

    /**
     * Perform the action on the given models.
     *
     * @return mixed
     */
    public function handle(ActionFields $fields, Collection $models)
    {
        foreach ($models as $model) {
            (new AccountData($model))->send();
        }
    }

    /**
    * Get the fields available on the action.
     *
     * @return array<int, \Laravel\Nova\Fields\Field>
     */
    public function fields(NovaRequest $request): array
    {
        return [];
    }
}
```
The most important method of an action is the `handle` method. The `handle` method receives the values for any fields attached to the action, as well as a collection of selected models. The `handle` method **always** receives a `Collection` of models, even if the action is only being performed against a single model.
Within the `handle` method, you may perform whatever tasks are necessary to complete the action. You are free to update database records, send emails, call other services, etc. The sky is the limit!
#### [​](#action-titles) Action Titles
Typically, Nova utilizes the action’s class name to determine the displayable name of the action that should be shown in the action selection menu. If you would like to change the displayable name of the action, you may define a `name` property on the action class:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
/**
 * The displayable name of the action.
 *
 * @var \Stringable|string
 */
public $name = 'Send Account Profile via E-mail';
```
### [​](#destructive-actions) Destructive Actions
You may designate an action as destructive or dangerous by defining an action class that extends `Laravel\Nova\Actions\DestructiveAction`. This will change the color of the action’s confirm button to red:
When a destructive action is added to a resource that has an associated authorization policy, the policy’s `delete` method must return `true` in order for the action to run.
### [​](#action-callbacks) Action Callbacks
The `Action::then` method should not be utilized if your action is queued. To achieve similar functionality when using queued actions, you should leverage Nova’s [action batching callbacks](#job-batching).
When running an action against multiple resources, you may wish to execute some code after the action has completed executing against all of the resources. For example, you may wish to generate a report detailing all of the changes for the selected resources. To accomplish this, you may invoke the `then` method when [registering your action](./registering-actions).
The `then` methods accepts a closure which will be invoked when the action has finished executing against all of the selected resources. The closure will receive a flattened Laravel [collection](https://laravel.com/docs/collections) containing the values that were returned by the action.
For example, note that the following action’s `handle` method returns the `$models` it receives:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 */
public function handle(ActionFields $fields, Collection $models): Collection
{
    foreach ($models as $model) {
        (new AccountData($model))->send();
    }

    return $models;
}
```
When registering this action on a resource, we may use the `then` callback to access the returned models and interact with them after the action has finished executing:
app/Nova/~Resource.php
Copy
Ask AI
```
use App\Nova\Actions\EmailAccountProfile;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the actions available for the resource.
 *
 * @return array<int, \Laravel\Nova\Actions\Action>
 */
public function actions(NovaRequest $request): array 
{
    return [
        (new Actions\EmailAccountProfile)->then(function ($models) {
            $models->each(function ($model) {
                //
            });
        }),
    ];
}
```
## [​](#action-fields) Action Fields
Sometimes you may wish to gather additional information from the user before dispatching an action. For this reason, Nova allows you to attach most of Nova’s supported [fields](./../resources/fields) directly to an action. When the action is initiated, Nova will prompt the user to provide input for the fields:
To add a field to an action, add the field to the array of fields returned by the action’s `fields` method:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields available on the action.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array 
{
    return [
        Text::make('Subject'),
    ];
}
```
Finally, within your action’s `handle` method, you may access your fields using dynamic accessors on the provided `ActionFields` instance:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 *
 * @return mixed
 */
public function handle(ActionFields $fields, Collection $models)
{
    foreach ($models as $model) {
        (new AccountData($model))->send($fields->subject);
    }
}
```
#### [​](#action-fields-default-values) Action Fields Default Values
You may use the `default` method to set the default value for an action field:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields available on the action.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        Text::make('Subject')
            ->default(fn ($request) => 'Test: Subject'),
    ];
}
```
## [​](#action-responses) Action Responses
Typically, when an action is executed, a generic “success” messages is displayed in the Nova UI. However, you are free to customize this response using a variety of methods available via the `ActionResponse` class. To display a custom “success” message, you may invoke the `ActionResponse::message` method from your `handle` method:
app/Nova/Actions/~Action.php
Copy
Ask AI
```
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\ActionResponse;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 *
 * @return mixed
 */
public function handle(ActionFields $fields, Collection $models)
{
    return ActionResponse::message('It worked!');
}
```
To return a red, “danger” message, you may invoke the `ActionResponse::danger` method:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::danger('Something went wrong!');
```
Messages passed to `ActionResponse` are not escaped before rendering. If you are providing untrusted user data to `ActionResponse`, ensure that you escape it using the `e` function.
### [​](#redirect-responses) Redirect Responses
To redirect the user to an entirely new location after the action is executed, you may use the `ActionResponse::redirect` method:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::redirect('https://example.com');
```
To redirect the user to another location within Nova, you may use the `ActionResponse::visit` method:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::visit('/resources/posts/new', [
    'viaResource' => 'users',
    'viaResourceId' => 1,
    'viaRelationship' => 'posts'
]);
```
To redirect the user to a new location in a new browser tab, you may use the `ActionResponse::openInNewTab` method:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::openInNewTab('https://example.com');
```
### [​](#download-responses) Download Responses
To initiate a file download after the action is executed, you may use the `ActionResponse::download` method. The `download` method accepts the desired name of the file as its first argument, and the URL of the file to be downloaded as its second argument:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::download('Invoice.pdf', 'https://example.com/invoice.pdf');
```
### [​](#emitting-client-side-events) Emitting Client Side Events
To emit a client side event after the action is executed, you may use the `ActionResponse::emit` method. The `emit` method accepts an event name as its first argument and an array as its second argument:
Copy
Ask AI
```
use Laravel\Nova\Actions\ActionResponse;

// ...

return ActionResponse::emit('invoice-generated', ['model' => $model->getKey()]);
```
Your assets can listen for the `invoice-generated` event using the `Nova.$on` method:
Copy
Ask AI
```
Nova.$on('invoice-generated', ({ model }) => {
    console.log('Invoice generated for ', model)
})
```
### [​](#custom-modal-responses) Custom Modal Responses
In addition to the customization options provided before and during an action’s execution, Nova also supports the ability to present a custom modal response to the user. This allows you to provide additional context or follow-up actions to the user, customized to your use-case.
For example, let’s imagine you have defined an action named `GenerateApiToken`, which creates unique tokens for use with a REST API. Using a custom action response modal, you could show the user running the action a modal allowing them to copy the newly-generated API token to their clipboard.
Using the `nova:asset` Artisan command, you may [generate a custom asset](./../customization/assets) and register the custom modal with Nova’s Vue instance:
Copy
Ask AI
```
import ApiTokenCopier from "./components/ApiTokenCopier";

Nova.booting(app => {
  app.component("api-token-copier", ApiTokenCopier);
});
```
Next, you may use the `modal` method within your action’s `handle` method, which will instruct Nova to show the modal after running the action, passing the Vue component’s name and any additional data you specify to the component. The data will be made available to the custom modal’s Vue component as props:
app/Nova/Actions/~Action.php
Copy
Ask AI
```
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Actions\ActionResponse;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 */
public function handle(ActionFields $fields, Collection $models): ActionResponse
{
    if ($models->count() > 1) {
        return Action::danger('Please run this on only one user resource.');
    }

    $models->first()->update(['api_token' => $token = Str::random(32)]);

    return Action::modal('api-token-copier', [
        'message' => 'The API token was generated!',
        'token' => $token,
    ]);
}
```
## [​](#queued-actions) Queued Actions
Occasionally, you may have actions that take a while to finish running. For this reason, Nova makes it a cinch to [queue](https://laravel.com/docs/queues) your actions. To instruct Nova to queue an action instead of running it synchronously, mark the action with the `ShouldQueue` interface:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
namespace App\Nova\Actions;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Laravel\Nova\Actions\Action;

class EmailAccountProfile extends Action implements ShouldQueue
{
    use InteractsWithQueue;
    use Queueable;

    // ...
}
```
You may quickly create a queued Nova action by providing the `--queued` option when executing the `nova:action` Artisan command:
Copy
Ask AI
```
php artisan nova:action EmailAccountProfile --queued
```
When using queued actions, don’t forget to configure and start [queue workers](https://laravel.com/docs/queues) for your application. Otherwise, your actions won’t be processed.
At this time, Nova does not support attaching `File` fields to a queued action. If you need to attach a `File` field to an action, the action must be run synchronously.
### [​](#customizing-the-connection-and-queue) Customizing the Connection and Queue
You may customize the queue connection and queue name that the action is queued on by setting the `$connection` and `$queue` properties within the action’s constructor:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
/**
 * Create a new action instance.
 *
 * @return void
 */
public function __construct()
{
    $this->connection = 'redis';
    $this->queue = 'emails';
}
```
### [​](#job-batching) Job Batching
You may also instruct Nova to queue actions as a [batch](https://laravel.com/docs/queues#job-batching) by marking the action with the `Laravel\Nova\Contracts\BatchableAction` interface. In addition, the action should use the `Illuminate\Bus\Batchable` trait.
When an action is batchable, you should define a `withBatch` method that will be responsible for configuring the action’s [batch callbacks](https://laravel.com/docs/queues#dispatching-batches). This allows you to define code that should run after an entire batch of actions finishes executing against multiple selected resources. In fact, you can even access the model IDs for all of the resources that were selected when the batched action was executed:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
namespace App\Nova\Actions;

use App\Models\AccountData;
use Illuminate\Bus\Batch;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\PendingBatch;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Contracts\BatchableAction;
use Laravel\Nova\Fields\ActionFields;
use Throwable;

class EmailAccountProfile extends Action implements BatchableAction, ShouldQueue
{
    use Batchable;
    use InteractsWithQueue;
    use Queueable;

    /**
     * Register `then`, `catch` and `finally` event on batchable job.
     */
    public function withBatch(ActionFields $fields, PendingBatch $batch): void 
    {
        $batch->then(function (Batch $batch) {
            // All jobs completed successfully...

            $selectedModels = $batch->resourceIds;
        })->catch(function (Batch $batch, Throwable $e) {
            // First batch job failure detected...
        })->finally(function (Batch $batch) {
            // The batch has finished executing...
        });
    }
}
```
## [​](#action-log) Action Log
It is often useful to view a log of the actions that have been run against a particular resource. Additionally, when queueing actions, it’s often important to know when the queued actions have actually finished executing. Thankfully, Nova makes it a breeze to add an action log to a resource by attaching the `Laravel\Nova\Actions\Actionable` trait to the resource’s corresponding Eloquent model.
For example, we may attach the `Laravel\Nova\Actions\Actionable` trait to the `User` Eloquent model:
app/Models/User.php
Copy
Ask AI
```
namespace App\Models;

use Laravel\Nova\Actions\Actionable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    use Actionable, Notifiable;

    // ...
}
```
Once the trait has been attached to the model, Nova will automatically begin displaying an action log at the bottom of the resource’s detail page:
### [​](#disabling-the-action-log) Disabling the Action Log
If you do not want to record an action in the action log, you may disable this behavior by adding a `withoutActionEvents` property on your action class:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
/**
 * Disables action log events for this action.
 *
 * @var bool
 */
public $withoutActionEvents = true;
```
Or, using the `withoutActionEvents` method, you may disable the action log for an action when the action is attached to a resource. Disabling the action log is often particularly helpful when an action is often executed against thousands of resources at once, since it allows you to avoid thousands of slow, sequential action log database inserts:
app/Nova/~Resource.php
Copy
Ask AI
```
use App\Nova\Actions\SomeAction;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the actions available for the resource.
 *
 * @return array<int, \Laravel\Nova\Actions\Action>
 */
public function actions(NovaRequest $request): array
{
    return [
        (new SomeAction)->withoutActionEvents(),
    ];
}
```
### [​](#queued-action-statuses) Queued Action Statuses
While a queued action is running, you may update the action’s “status” for any of the models that were passed to the action via its model collection. For example, you may use the action’s `markAsFinished` method to indicate that the action has completed processing a particular model:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 */
public function handle(ActionFields $fields, Collection $models): void
{
    foreach ($models as $model) {
        (new AccountData($model))->send($fields->subject);

        $this->markAsFinished($model);
    }
}
```
Or, if you would like to indicate that an action has “failed” for a given model, you may use the `markAsFailed` method:
app/Nova/Actions/EmailAccountProfile.php
Copy
Ask AI
```
use App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 */
public function handle(ActionFields $fields, Collection $models): void
{
    foreach ($models as $model) {
        try {
            (new AccountData($model))->send($fields->subject);
        } catch (Exception $e) {
            $this->markAsFailed($model, $e);
        }
    }
}
```
## [​](#action-modal-customization) Action Modal Customization
By default, actions will ask the user for confirmation before running. You can customize the confirmation message, confirm button, and cancel button to give the user more context before running the action. This is done by calling the `confirmText`, `confirmButtonText`, and `cancelButtonText` methods when defining the action:
app/Nova/~Resource.php
Copy
Ask AI
```
use App\Nova\Actions\ActivateUser;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the actions available for the resource.
 *
 * @return array<int, \Laravel\Nova\Actions\Action>
 */
public function actions(NovaRequest $request): array
{
    return [
        Actions\ActivateUser::make()
            ->confirmText('Are you sure you want to activate this user?')
            ->confirmButtonText('Activate')
            ->cancelButtonText("Don't activate"),
    ];
}
```
Was this page helpful?
YesNo
[Registering Lenses](/docs/v5/lenses/registering-lenses)[Registering Actions](/docs/v5/actions/registering-actions)
⌘I
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)