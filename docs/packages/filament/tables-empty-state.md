Source: https://filamentphp.com/docs/5.x/tables/empty-state.md

# Empty state

> Filament 5.x documentation
> Source: https://filamentphp.com/docs/5.x/tables/empty-state.md

## Introduction

The table's "empty state" is rendered when there are no rows in the table.



## Setting the empty state heading

To customize the heading of the empty state, use the ` emptyStateHeading() ` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateHeading('No posts yet');
}
```



## Setting the empty state description

To customize the description of the empty state, use the ` emptyStateDescription() ` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateDescription('Once you write your first post, it will appear here.');
}
```



## Setting the empty state icon

To customize the [icon](https://filamentphp.com/docs/5.x/styling/icons.md) of the empty state, use the ` emptyStateIcon() ` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateIcon('heroicon-o-bookmark');
}
```



## Adding empty state actions

You can add [Actions](https://filamentphp.com/docs/5.x/tables/actions.md) to the empty state to prompt users to take action. Pass these to the ` emptyStateActions() ` method:

```php
use Filament\Actions\Action;
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyStateActions([
            Action::make('create')
                ->label('Create post')
                ->url(route('posts.create'))
                ->icon('heroicon-m-plus')
                ->button(),
        ]);
}
```



## Using a custom empty state view

You may use a completely custom empty state view by passing it to the ` emptyState() ` method:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->emptyState(view('tables.posts.empty-state'));
}
```
