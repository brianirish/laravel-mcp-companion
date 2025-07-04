# Database: Pagination

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)
    - [Paginating Query Builder Results](#paginating-query-builder-results)
    - [Paginating Eloquent Results](#paginating-eloquent-results)
    - [Cursor Pagination](#cursor-pagination)
    - [Manually Creating a Paginator](#manually-creating-a-paginator)
    - [Customizing Pagination URLs](#customizing-pagination-urls)
- [Displaying Pagination Results](#displaying-pagination-results)
    - [Adjusting the Pagination Link Window](#adjusting-the-pagination-link-window)
    - [Converting Results to JSON](#converting-results-to-json)
- [Customizing the Pagination View](#customizing-the-pagination-view)
    - [Using Bootstrap](#using-bootstrap)
- [Paginator and LengthAwarePaginator Instance Methods](#paginator-instance-methods)
- [Cursor Paginator Instance Methods](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## Introduction

In other frameworks, pagination can be very painful. We hope Laravel's approach to pagination will be a breath of fresh air. Laravel's paginator is integrated with the [query builder](/docs/{{version}}/queries) and [Eloquent ORM](/docs/{{version}}/eloquent) and provides convenient, easy-to-use pagination of database records with zero configuration.

By default, the HTML generated by the paginator is compatible with the [Tailwind CSS framework](https://tailwindcss.com/); however, Bootstrap pagination support is also available.

<a name="tailwind"></a>
#### Tailwind

If you are using Laravel's default Tailwind pagination views with Tailwind 4.x, your application's `resources/css/app.css` file will already be properly configured to `@source` Laravel's pagination views:

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## Basic Usage

<a name="paginating-query-builder-results"></a>
### Paginating Query Builder Results

There are several ways to paginate items. The simplest is by using the `paginate` method on the [query builder](/docs/{{version}}/queries) or an [Eloquent query](/docs/{{version}}/eloquent). The `paginate` method automatically takes care of setting the query's "limit" and "offset" based on the current page being viewed by the user. By default, the current page is detected by the value of the `page` query string argument on the HTTP request. This value is automatically detected by Laravel, and is also automatically inserted into links generated by the paginator.

In this example, the only argument passed to the `paginate` method is the number of items you would like displayed "per page". In this case, let's specify that we would like to display `15` items per page:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### Simple Pagination

The `paginate` method counts the total number of records matched by the query before retrieving the records from the database. This is done so that the paginator knows how many pages of records there are in total. However, if you do not plan to show the total number of pages in your application's UI then the record count query is unnecessary.

Therefore, if you only need to display simple "Next" and "Previous" links in your application's UI, you may use the `simplePaginate` method to perform a single, efficient query:

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Paginating Eloquent Results

You may also paginate [Eloquent](/docs/{{version}}/eloquent) queries. In this example, we will paginate the `App\Models\User` model and indicate that we plan to display 15 records per page. As you can see, the syntax is nearly identical to paginating query builder results:

```php
use App\Models\User;

$users = User::paginate(15);
```

Of course, you may call the `paginate` method after setting other constraints on the query, such as `where` clauses:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

You may also use the `simplePaginate` method when paginating Eloquent models:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

Similarly, you may use the `cursorPaginate` method to cursor paginate Eloquent models:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### Multiple Paginator Instances per Page

Sometimes you may need to render two separate paginators on a single screen that is rendered by your application. However, if both paginator instances use the `page` query string parameter to store the current page, the two paginator's will conflict. To resolve this conflict, you may pass the name of the query string parameter you wish to use to store the paginator's current page via the third argument provided to the `paginate`, `simplePaginate`, and `cursorPaginate` methods:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### Cursor Pagination

While `paginate` and `simplePaginate` create queries using the SQL "offset" clause, cursor pagination works by constructing "where" clauses that compare the values of the ordered columns contained in the query, providing the most efficient database performance available amongst all of Laravel's pagination methods. This method of pagination is particularly well-suited for large data-sets and "infinite" scrolling user interfaces.

Unlike offset based pagination, which includes a page number in the query string of the URLs generated by the paginator, cursor based pagination places a "cursor" string in the query string. The cursor is an encoded string containing the location that the next paginated query should start paginating and the direction that it should paginate:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

You may create a cursor based paginator instance via the `cursorPaginate` method offered by the query builder. This method returns an instance of `Illuminate\Pagination\CursorPaginator`:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

Once you have retrieved a cursor paginator instance, you may [display the pagination results](#displaying-pagination-results) as you typically would when using the `paginate` and `simplePaginate` methods. For more information on the instance methods offered by the cursor paginator, please consult the [cursor paginator instance method documentation](#cursor-paginator-instance-methods).

> [!WARNING]
> Your query must contain an "order by" clause in order to take advantage of cursor pagination. In addition, the columns that the query are ordered by must belong to the table you are paginating.

<a name="cursor-vs-offset-pagination"></a>
#### Cursor vs. Offset Pagination

To illustrate the differences between offset pagination and cursor pagination, let's examine some example SQL queries. Both of the following queries will both display the "second page" of results for a `users` table ordered by `id`:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

The cursor pagination query offers the following advantages over offset pagination:

- For large data-sets, cursor pagination will offer better performance if the "order by" columns are indexed. This is because the "offset" clause scans through all previously matched data.
- For data-sets with frequent writes, offset pagination may skip records or show duplicates if results have been recently added to or deleted from the page a user is currently viewing.

However, cursor pagination has the following limitations:

- Like `simplePaginate`, cursor pagination can only be used to display "Next" and "Previous" links and does not support generating links with page numbers.
- It requires that the ordering is based on at least one unique column or a combination of columns that are unique. Columns with `null` values are not supported.
- Query expressions in "order by" clauses are supported only if they are aliased and added to the "select" clause as well.
- Query expressions with parameters are not supported.

<a name="manually-creating-a-paginator"></a>
### Manually Creating a Paginator

Sometimes you may wish to create a pagination instance manually, passing it an array of items that you already have in memory. You may do so by creating either an `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator` or `Illuminate\Pagination\CursorPaginator` instance, depending on your needs.

The `Paginator` and `CursorPaginator` classes do not need to know the total number of items in the result set; however, because of this, these classes do not have methods for retrieving the index of the last page. The `LengthAwarePaginator` accepts almost the same arguments as the `Paginator`; however, it requires a count of the total number of items in the result set.

In other words, the `Paginator` corresponds to the `simplePaginate` method on the query builder, the `CursorPaginator` corresponds to the `cursorPaginate` method, and the `LengthAwarePaginator` corresponds to the `paginate` method.

> [!WARNING]
> When manually creating a paginator instance, you should manually "slice" the array of results you pass to the paginator. If you're unsure how to do this, check out the [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP function.

<a name="customizing-pagination-urls"></a>
### Customizing Pagination URLs

By default, links generated by the paginator will match the current request's URI. However, the paginator's `withPath` method allows you to customize the URI used by the paginator when generating links. For example, if you want the paginator to generate links like `http://example.com/admin/users?page=N`, you should pass `/admin/users` to the `withPath` method:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### Appending Query String Values

You may append to the query string of pagination links using the `appends` method. For example, to append `sort=votes` to each pagination link, you should make the following call to `appends`:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

You may use the `withQueryString` method if you would like to append all of the current request's query string values to the pagination links:

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### Appending Hash Fragments

If you need to append a "hash fragment" to URLs generated by the paginator, you may use the `fragment` method. For example, to append `#users` to the end of each pagination link, you should invoke the `fragment` method like so:

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## Displaying Pagination Results

When calling the `paginate` method, you will receive an instance of `Illuminate\Pagination\LengthAwarePaginator`, while calling the `simplePaginate` method returns an instance of `Illuminate\Pagination\Paginator`. And, finally, calling the `cursorPaginate` method returns an instance of `Illuminate\Pagination\CursorPaginator`.

These objects provide several methods that describe the result set. In addition to these helper methods, the paginator instances are iterators and may be looped as an array. So, once you have retrieved the results, you may display the results and render the page links using [Blade](/docs/{{version}}/blade):

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

The `links` method will render the links to the rest of the pages in the result set. Each of these links will already contain the proper `page` query string variable. Remember, the HTML generated by the `links` method is compatible with the [Tailwind CSS framework](https://tailwindcss.com).

<a name="adjusting-the-pagination-link-window"></a>
### Adjusting the Pagination Link Window

When the paginator displays pagination links, the current page number is displayed as well as links for the three pages before and after the current page. Using the `onEachSide` method, you may control how many additional links are displayed on each side of the current page within the middle, sliding window of links generated by the paginator:

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### Converting Results to JSON

The Laravel paginator classes implement the `Illuminate\Contracts\Support\Jsonable` Interface contract and expose the `toJson` method, so it's very easy to convert your pagination results to JSON. You may also convert a paginator instance to JSON by returning it from a route or controller action:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

The JSON from the paginator will include meta information such as `total`, `current_page`, `last_page`, and more. The result records are available via the `data` key in the JSON array. Here is an example of the JSON created by returning a paginator instance from a route:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## Customizing the Pagination View

By default, the views rendered to display the pagination links are compatible with the [Tailwind CSS](https://tailwindcss.com) framework. However, if you are not using Tailwind, you are free to define your own views to render these links. When calling the `links` method on a paginator instance, you may pass the view name as the first argument to the method:

```blade
{{ $paginator->links('view.name') }}

<!-- Passing additional data to the view... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

However, the easiest way to customize the pagination views is by exporting them to your `resources/views/vendor` directory using the `vendor:publish` command:

```shell
php artisan vendor:publish --tag=laravel-pagination
```

This command will place the views in your application's `resources/views/vendor/pagination` directory. The `tailwind.blade.php` file within this directory corresponds to the default pagination view. You may edit this file to modify the pagination HTML.

If you would like to designate a different file as the default pagination view, you may invoke the paginator's `defaultView` and `defaultSimpleView` methods within the `boot` method of your `App\Providers\AppServiceProvider` class:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### Using Bootstrap

Laravel includes pagination views built using [Bootstrap CSS](https://getbootstrap.com/). To use these views instead of the default Tailwind views, you may call the paginator's `useBootstrapFour` or `useBootstrapFive` methods within the `boot` method of your `App\Providers\AppServiceProvider` class:

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator Instance Methods

Each paginator instance provides additional pagination information via the following methods:

<div class="overflow-auto">

| Method                                  | Description                                                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `$paginator->count()`                   | Get the number of items for the current page.                                                                |
| `$paginator->currentPage()`             | Get the current page number.                                                                                 |
| `$paginator->firstItem()`               | Get the result number of the first item in the results.                                                      |
| `$paginator->getOptions()`              | Get the paginator options.                                                                                   |
| `$paginator->getUrlRange($start, $end)` | Create a range of pagination URLs.                                                                           |
| `$paginator->hasPages()`                | Determine if there are enough items to split into multiple pages.                                            |
| `$paginator->hasMorePages()`            | Determine if there are more items in the data store.                                                         |
| `$paginator->items()`                   | Get the items for the current page.                                                                          |
| `$paginator->lastItem()`                | Get the result number of the last item in the results.                                                       |
| `$paginator->lastPage()`                | Get the page number of the last available page. (Not available when using `simplePaginate`).                 |
| `$paginator->nextPageUrl()`             | Get the URL for the next page.                                                                               |
| `$paginator->onFirstPage()`             | Determine if the paginator is on the first page.                                                             |
| `$paginator->onLastPage()`              | Determine if the paginator is on the last page.                                                              |
| `$paginator->perPage()`                 | The number of items to be shown per page.                                                                    |
| `$paginator->previousPageUrl()`         | Get the URL for the previous page.                                                                           |
| `$paginator->total()`                   | Determine the total number of matching items in the data store. (Not available when using `simplePaginate`). |
| `$paginator->url($page)`                | Get the URL for a given page number.                                                                         |
| `$paginator->getPageName()`             | Get the query string variable used to store the page.                                                        |
| `$paginator->setPageName($name)`        | Set the query string variable used to store the page.                                                        |
| `$paginator->through($callback)`        | Transform each item using a callback.                                                                        |

</div>

<a name="cursor-paginator-instance-methods"></a>
## Cursor Paginator Instance Methods

Each cursor paginator instance provides additional pagination information via the following methods:

<div class="overflow-auto">

| Method                          | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `$paginator->count()`           | Get the number of items for the current page.                     |
| `$paginator->cursor()`          | Get the current cursor instance.                                  |
| `$paginator->getOptions()`      | Get the paginator options.                                        |
| `$paginator->hasPages()`        | Determine if there are enough items to split into multiple pages. |
| `$paginator->hasMorePages()`    | Determine if there are more items in the data store.              |
| `$paginator->getCursorName()`   | Get the query string variable used to store the cursor.           |
| `$paginator->items()`           | Get the items for the current page.                               |
| `$paginator->nextCursor()`      | Get the cursor instance for the next set of items.                |
| `$paginator->nextPageUrl()`     | Get the URL for the next page.                                    |
| `$paginator->onFirstPage()`     | Determine if the paginator is on the first page.                  |
| `$paginator->onLastPage()`      | Determine if the paginator is on the last page.                   |
| `$paginator->perPage()`         | The number of items to be shown per page.                         |
| `$paginator->previousCursor()`  | Get the cursor instance for the previous set of items.            |
| `$paginator->previousPageUrl()` | Get the URL for the previous page.                                |
| `$paginator->setCursorName()`   | Set the query string variable used to store the cursor.           |
| `$paginator->url($cursor)`      | Get the URL for a given cursor instance.                          |

</div>
