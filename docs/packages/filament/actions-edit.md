Source: https://filamentphp.com/docs/5.x/actions/edit.md

# Edit action

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/actions/edit.md

## Introduction

Filament includes an action that is able to edit Eloquent records. When the trigger button is clicked, a modal will open with a form inside. The user fills the form, and that data is validated and saved into the database. You may use it like so:

```php
use Filament\Actions\EditAction;
use Filament\Forms\Components\TextInput;

EditAction::make()
    ->schema([
        TextInput::make('title')
            ->required()
            ->maxLength(255),
        // ...
    ])
```



## Customizing data before filling the form

You may wish to modify the data from a record before it is filled into the form. To do this, you may use the ` mutateRecordDataUsing() ` method to modify the ` $data ` array, and return the modified version before it is filled into the form:

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->mutateRecordDataUsing(function (array $data): array {
        $data['user_id'] = auth()->id();

        return $data;
    })
```

As well as ` $data `, the ` mutateRecordDataUsing() ` function can inject various utilities as parameters.

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


> **Warning**
>
> Filament fills the form using the record's array representation, which is sent to the browser as part of the Livewire request. If your model has a column containing binary data that is not valid UTF-8, such as a ` geometry `, ` point `, or ` blob ` column, it cannot be serialized to JSON and the modal will fail to open, often with no error in the Laravel log.
> 
> To resolve this, add the column to [the ` $hidden ` array](https://laravel.com/docs/eloquent-serialization#hiding-attributes-from-json) on your model, which excludes it from the model's array and JSON representations:
> 
> ```php
> protected $hidden = ['location'];
> ```
> 
> This applies equally to the [View](https://filamentphp.com/docs/5.x/actions/view.md) and [Replicate](https://filamentphp.com/docs/5.x/actions/replicate.md) actions.


## Customizing data before saving

Sometimes, you may wish to modify form data before it is finally saved to the database. To do this, you may use the ` mutateDataUsing() ` method, which has access to the ` $data ` as an array, and returns the modified version:

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->mutateDataUsing(function (array $data): array {
        $data['last_edited_by_id'] = auth()->id();

        return $data;
    })
```

As well as ` $data `, the ` mutateDataUsing() ` function can inject various utilities as parameters.

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


## Customizing the saving process

You can tweak how the record is updated with the ` using() ` method:

```php
use Filament\Actions\EditAction;
use Illuminate\Database\Eloquent\Model;

EditAction::make()
    ->using(function (Model $record, array $data): Model {
        $record->update($data);

        return $record;
    })
```

As well as ` $record ` and ` $data `, the ` using() ` function can inject various utilities as parameters.

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


## Redirecting after saving

You may set up a custom redirect when the form is submitted using the ` successRedirectUrl() ` method:

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->successRedirectUrl(route('posts.list'))
```

If you want to redirect using the created record, use the ` $record ` parameter:

```php
use Filament\Actions\EditAction;
use Illuminate\Database\Eloquent\Model;

EditAction::make()
    ->successRedirectUrl(fn (Model $record): string => route('posts.view', [
        'post' => $record,
    ]))
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


## Customizing the save notification

When the record is successfully updated, a notification is dispatched to the user, which indicates the success of their action.

To customize the title of this notification, use the ` successNotificationTitle() ` method:

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->successNotificationTitle('User updated')
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
use Filament\Actions\EditAction;
use Filament\Notifications\Notification;

EditAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User updated')
            ->body('The user has been saved successfully.'),
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
use Filament\Actions\EditAction;

EditAction::make()
    ->successNotification(null)
```

## Lifecycle hooks

Hooks may be used to execute code at various points within the action's lifecycle, like before a form is saved.

There are several available hooks:

```php
use Filament\Actions\EditAction;

EditAction::make()
    ->beforeFormFilled(function () {
        // Runs before the form fields are populated from the database.
    })
    ->afterFormFilled(function () {
        // Runs after the form fields are populated from the database.
    })
    ->beforeFormValidated(function () {
        // Runs before the form fields are validated when the form is saved.
    })
    ->afterFormValidated(function () {
        // Runs after the form fields are validated when the form is saved.
    })
    ->before(function () {
        // Runs before the form fields are saved to the database.
    })
    ->after(function () {
        // Runs after the form fields are saved to the database.
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


## Halting the saving process

At any time, you may call ` $action->halt() ` from inside a lifecycle hook or mutation method, which will halt the entire saving process:

```php
use App\Models\Post;
use Filament\Actions\Action;
use Filament\Actions\EditAction;
use Filament\Notifications\Notification;

EditAction::make()
    ->before(function (EditAction $action, Post $record) {
        if (! $record->team->subscribed()) {
            Notification::make()
                ->warning()
                ->title('You don\'t have an active subscription!')
                ->body('Choose a plan to continue.')
                ->persistent()
                ->actions([
                    Action::make('subscribe')
                        ->button()
                        ->url(route('subscribe'), shouldOpenInNewTab: true),
                ])
                ->send();
        
            $action->halt();
        }
    })
```

If you'd like the action modal to close too, you can completely ` cancel() ` the action instead of halting it:

```php
$action->cancel();
```
