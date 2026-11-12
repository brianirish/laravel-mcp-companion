Source: https://filamentphp.com/docs/5.x/actions/restore.md

# Restore action

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/actions/restore.md

## Introduction

Filament includes an action that is able to restore [soft-deleted](https://laravel.com/docs/eloquent#soft-deleting) Eloquent records. When the trigger button is clicked, a modal asks the user for confirmation. You may use it like so:

```php
use Filament\Actions\RestoreAction;

RestoreAction::make()
```



Or if you want to add it as a table bulk action, so that the user can choose which rows to restore, use ` Filament\Actions\RestoreBulkAction `:

```php
use Filament\Actions\RestoreBulkAction;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            RestoreBulkAction::make(),
        ]);
}
```

## Redirecting after restoring

You may set up a custom redirect when the form is submitted using the ` successRedirectUrl() ` method:

```php
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successRedirectUrl(route('posts.list'))
```

As well as ` $record `, the ` successRedirectUrl() ` function can inject various utilities as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The current action instance. |
| Arguments | ` array<string, mixed> ` | ` $arguments ` | The array of arguments passed to the action when it was triggered. |
| Data | ` array<string, mixed> ` | ` $data ` | The array of data submitted from form fields in the action's modal. It will be empty before the modal form is submitted. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Parent action | ` ?Filament\Actions\Action ` | ` $parentAction ` | The mounted parent action, or the containing parent action if one exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Actions in schemas only\] The schema object that this action belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Actions in schemas only\] The schema component that this action belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Actions in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Actions in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Actions in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema set function | ` Filament\Schemas\Components\Utilities\Set ` | ` $schemaSet ` | \[Actions in schemas only\] A function for setting values in the schema data. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Actions in schemas only\] The current value of the schema that this action belongs to, like the current repeater item. |
| Selected Eloquent records | ` Illuminate\Support\Collection\|Illuminate\Support\LazyCollection ` | ` $selectedRecords ` | \[Actions in tables only\] The selected records, filtered by individual record authorization when it is enabled. Requires ` accessSelectedRecords() `. |
| Selected Eloquent records query | ` Illuminate\Database\Eloquent\Builder ` | ` $selectedRecordsQuery ` | \[Actions in Eloquent-query-backed tables only\] The query for the selected records. Requires ` accessSelectedRecords() `. Individual record authorization has not been applied to this query. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Actions in tables only\] The table object that this action belongs to. |


## Customizing the restore notification

When the record is successfully restored, a notification is dispatched to the user, which indicates the success of their action.

To customize the title of this notification, use the ` successNotificationTitle() ` method:

```php
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successNotificationTitle('User restored')
```

As well as allowing a static value, the ` successNotificationTitle() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The current action instance. |
| Arguments | ` array<string, mixed> ` | ` $arguments ` | The array of arguments passed to the action when it was triggered. |
| Data | ` array<string, mixed> ` | ` $data ` | The array of data submitted from form fields in the action's modal. It will be empty before the modal form is submitted. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Parent action | ` ?Filament\Actions\Action ` | ` $parentAction ` | The mounted parent action, or the containing parent action if one exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Actions in schemas only\] The schema object that this action belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Actions in schemas only\] The schema component that this action belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Actions in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Actions in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Actions in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema set function | ` Filament\Schemas\Components\Utilities\Set ` | ` $schemaSet ` | \[Actions in schemas only\] A function for setting values in the schema data. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Actions in schemas only\] The current value of the schema that this action belongs to, like the current repeater item. |
| Selected Eloquent records | ` Illuminate\Support\Collection\|Illuminate\Support\LazyCollection ` | ` $selectedRecords ` | \[Actions in tables only\] The selected records, filtered by individual record authorization when it is enabled. Requires ` accessSelectedRecords() `. |
| Selected Eloquent records query | ` Illuminate\Database\Eloquent\Builder ` | ` $selectedRecordsQuery ` | \[Actions in Eloquent-query-backed tables only\] The query for the selected records. Requires ` accessSelectedRecords() `. Individual record authorization has not been applied to this query. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Actions in tables only\] The table object that this action belongs to. |


You may customize the entire notification using the ` successNotification() ` method:

```php
use Filament\Actions\RestoreAction;
use Filament\Notifications\Notification;

RestoreAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User restored')
            ->body('The user has been restored successfully.'),
    )
```

As well as allowing a static value, the ` successNotification() ` method also accepts a function to dynamically calculate it. You can inject various utilities into the function as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The current action instance. |
| Arguments | ` array<string, mixed> ` | ` $arguments ` | The array of arguments passed to the action when it was triggered. |
| Data | ` array<string, mixed> ` | ` $data ` | The array of data submitted from form fields in the action's modal. It will be empty before the modal form is submitted. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Notification | ` Filament\Notifications\Notification ` | ` $notification ` | The default notification object, which could be a useful starting point for customization. |
| Parent action | ` ?Filament\Actions\Action ` | ` $parentAction ` | The mounted parent action, or the containing parent action if one exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Actions in schemas only\] The schema object that this action belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Actions in schemas only\] The schema component that this action belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Actions in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Actions in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Actions in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema set function | ` Filament\Schemas\Components\Utilities\Set ` | ` $schemaSet ` | \[Actions in schemas only\] A function for setting values in the schema data. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Actions in schemas only\] The current value of the schema that this action belongs to, like the current repeater item. |
| Selected Eloquent records | ` Illuminate\Support\Collection\|Illuminate\Support\LazyCollection ` | ` $selectedRecords ` | \[Actions in tables only\] The selected records, filtered by individual record authorization when it is enabled. Requires ` accessSelectedRecords() `. |
| Selected Eloquent records query | ` Illuminate\Database\Eloquent\Builder ` | ` $selectedRecordsQuery ` | \[Actions in Eloquent-query-backed tables only\] The query for the selected records. Requires ` accessSelectedRecords() `. Individual record authorization has not been applied to this query. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Actions in tables only\] The table object that this action belongs to. |


To disable the notification altogether, use the ` successNotification(null) ` method:

```php
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->successNotification(null)
```

## Lifecycle hooks

You can use the ` before() ` and ` after() ` methods to execute code before and after a record is restored:

```php
use Filament\Actions\RestoreAction;

RestoreAction::make()
    ->before(function () {
        // ...
    })
    ->after(function () {
        // ...
    })
```

These hook functions can inject various utilities as parameters.

[Utility injection guide](https://filamentphp.com/docs/5.x/actions/overview.md#action-utility-injection)

| Utility | Type | Parameter | Description |
| --- | --- | --- | --- |
| Action | ` Filament\Actions\Action ` | ` $action ` | The current action instance. |
| Arguments | ` array<string, mixed> ` | ` $arguments ` | The array of arguments passed to the action when it was triggered. |
| Data | ` array<string, mixed> ` | ` $data ` | The array of data submitted from form fields in the action's modal. It will be empty before the modal form is submitted. |
| Livewire | ` Livewire\Component ` | ` $livewire ` | The Livewire component instance. |
| Eloquent model FQN | ` ?string<Illuminate\Database\Eloquent\Model> ` | ` $model ` | The Eloquent model FQN for the current action, if one is attached. |
| Mounted actions | ` array<Filament\Actions\Action> ` | ` $mountedActions ` | The array of actions that are currently mounted in the Livewire component. This is useful for accessing data from parent actions. |
| Parent action | ` ?Filament\Actions\Action ` | ` $parentAction ` | The mounted parent action, or the containing parent action if one exists. |
| Record | ` Illuminate\Database\Eloquent\Model\|array<string, mixed>\|null ` | ` $record ` | The Eloquent record or custom data array for the current action, if one is attached. |
| Schema | ` Filament\Schemas\Schema ` | ` $schema ` | \[Actions in schemas only\] The schema object that this action belongs to. |
| Schema component | ` Filament\Schemas\Components\Component ` | ` $schemaComponent ` | \[Actions in schemas only\] The schema component that this action belongs to. |
| Schema component state | ` mixed ` | ` $schemaComponentState ` | \[Actions in schemas only\] The current value of the schema component. |
| Schema get function | ` Filament\Schemas\Components\Utilities\Get ` | ` $schemaGet ` | \[Actions in schemas only\] A function for retrieving values from the schema data. Validation is not run on form fields. |
| Schema operation | ` string ` | ` $schemaOperation ` | \[Actions in schemas only\] The current operation being performed by the schema. Usually ` create `, ` edit `, or ` view `. |
| Schema set function | ` Filament\Schemas\Components\Utilities\Set ` | ` $schemaSet ` | \[Actions in schemas only\] A function for setting values in the schema data. |
| Schema state | ` mixed ` | ` $schemaState ` | \[Actions in schemas only\] The current value of the schema that this action belongs to, like the current repeater item. |
| Selected Eloquent records | ` Illuminate\Support\Collection\|Illuminate\Support\LazyCollection ` | ` $selectedRecords ` | \[Actions in tables only\] The selected records, filtered by individual record authorization when it is enabled. Requires ` accessSelectedRecords() `. |
| Selected Eloquent records query | ` Illuminate\Database\Eloquent\Builder ` | ` $selectedRecordsQuery ` | \[Actions in Eloquent-query-backed tables only\] The query for the selected records. Requires ` accessSelectedRecords() `. Individual record authorization has not been applied to this query. |
| Table | ` Filament\Tables\Table ` | ` $table ` | \[Actions in tables only\] The table object that this action belongs to. |


## Improving the performance of restore bulk actions

By default, the ` RestoreBulkAction ` will load all Eloquent records into memory, before looping over them and restoring them one by one.

If you are restoring a large number of records, you may want to use the ` chunkSelectedRecords() ` method to fetch a smaller number of records at a time. This will reduce the memory usage of your application:

```php
use Filament\Actions\RestoreBulkAction;

RestoreBulkAction::make()
    ->chunkSelectedRecords(250)
```

Filament loads Eloquent records into memory before restoring them for two reasons:

- To allow individual records in the collection to be authorized with a model policy before restoration (using ` authorizeIndividualRecords('restore') `, for example).
- To ensure that model events are run when restoring records, such as the ` restoring ` and ` restored ` events in a model observer.

If you do not require individual record policy authorization and model events, you can use the ` fetchSelectedRecords(false) ` method, which will not fetch the records into memory before restoring them, and instead will restore them in a single query:

```php
use Filament\Actions\RestoreBulkAction;

RestoreBulkAction::make()
    ->fetchSelectedRecords(false)
```
