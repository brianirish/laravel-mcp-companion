Source: https://nightwatch.laravel.com/docs/queries.md

# Queries

> Database queries executed with Eloquent, Query Builder and raw SQL

Nightwatch captures database queries executed through Laravel's query builder, Eloquent ORM, or raw SQL queries. This includes the SQL statement, execution time, connection, and context within the request or job lifecycle.

## Query List

View all queries for an application from the **Queries** panel. Each query is displayed with its SQL statement, connection, total calls, including the average and p95 execution times.

> [!TIP]
>
> P95 shows the performance experienced by your slowest 5% of queries. It
> highlights outliers, bottlenecks and inconsistent behavior that average times
> hide.

## Query Details

Click on any query in the list to view its full details page, which shows the query's performance over time. You can also see every individual execution of that query and its parent context. Clicking on an execution opens the full trace, showing the query within the context of its parent lifecycle (e.g., inside a request or job) alongside all related activities.

## Query Bindings

When viewing database queries in Nightwatch, you may notice question marks (`?`) used in place of actual values. These are called **query parameter bindings**, which represent the values that were bound to the query at runtime.

Nightwatch does **not** capture or display these bound values by design. This is a deliberate decision made to protect your application from unintentionally leaking sensitive or personally identifiable information. Security and data protection are core principles in how we designed Nightwatch.

If you need to troubleshoot a specific query and want to see the values being used, a recommended approach is to log the data manually using Laravel's `Log` facade as [contextual information](https://laravel.com/docs/12.x/logging#contextual-information). These logs will appear alongside the query in Nightwatch, giving you better context while still providing greater control over the data that is sent.

**Example:**

```sql theme={null}
select * from users where email = ?
```

In this example, the `?` represents the email address passed at runtime, which Nightwatch intentionally redacts.

## Sampling

There are no direct sampling controls for queries, they are automatically captured when their [parent execution](https://nightwatch.laravel.com/docs/events.md#execution-contexts) context is sampled.

## Filtering

There are a number of different methods to filter query events.

### Filtering All Queries

To completely disable the collection of all database queries, set the `NIGHTWATCH_IGNORE_QUERIES` environment variable to `true`:

```bash theme={null}
NIGHTWATCH_IGNORE_QUERIES=true
```

### Filtering Specific Queries

You can filter out specific queries using the `Nightwatch::rejectQueries()` method. This is useful for filtering out queries related to jobs or cache which could consume a significant portion of your quota.

```php PostgreSQL theme={null}
// AppServiceProvider.php

use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Query;

public function boot(): void
{
    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'into "jobs"');
    });

    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'from "cache"')
            || str_contains($query->sql, 'into "cache"');
    });
}
```

```php MySQL theme={null}
// AppServiceProvider.php

use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Query;

public function boot(): void
{
    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'into `jobs`');
    });

    Nightwatch::rejectQueries(function (Query $query) {
        return str_contains($query->sql, 'from `cache`')
            || str_contains($query->sql, 'into `cache`');
    });
}
```

> [!NOTE]
>
> Filtering events can help to conserve your event quota, but may also hide
> issues in your application. In the above example, if your database was
> responding slowly, your queue throughput would be reduced, but you wouldn't
> have visibility as to why.

## Redaction

You can manually redact sensitive information from query SQL statements using the `redactQueries` callback:

```php theme={null}
use Laravel\Nightwatch\Facades\Nightwatch;
use Laravel\Nightwatch\Records\Query;

Nightwatch::redactQueries(function (Query $query) {
    $query->sql = str_replace('secret', '***', $query->sql);
});
```
