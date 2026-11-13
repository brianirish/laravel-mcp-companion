Source: https://laravel.com/cloud/docs/knowledge-base/migrating-mysql-to-postgresql.md

# Migrate MySQL to PostgreSQL

Learn how to migrate from MySQL to hosted Serverless Postgres on Laravel Cloud.

If you're moving to Laravel Cloud and prefer PostgreSQL, you can migrate from MySQL to Laravel **Serverless Postgres**, which scales to zero. Your database sleeps when idle, and Laravel Cloud doesn't bill you for unused compute time.

[**Laravel MySQL** Flex sizes can also scale to zero](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#scale-to-zero), so you no longer need to switch database engines to get a database that sleeps when idle.

### Migrating your data

To move from MySQL to Postgres, you need to:

* Export your MySQL database (for example, using `mysqldump`).
* Use a tool like [**pgloader**](https://pgloader.io/) to import the data into your Serverless Postgres database.

pgloader is designed specifically to convert MySQL databases to Postgres and handles much of the transformation automatically. Depending on your schema, you may need some tweaks, but many applications migrate cleanly with minimal effort.

If you need more guidance, our database partner, **Neon**, has a helpful step-by-step guide: [Migrate from MySQL to Neon Postgres](https://neon.tech/docs/import/migrate-mysql).

### Application implementation considerations

Keep in mind that although Postgres is very similar to MySQL, it is generally stricter in certain field definitions and usage. The following table lists common considerations that may be relevant to your application.

<table>
<thead>
<tr>
<th />

<th>MySQL</th>
<th>Postgres</th>
<th>Considerations</th>
</tr>
</thead>

<tbody>
<tr>
<td>Boolean values</td>
<td>Stores as `TINYINT`</td>
<td>Stores as `BOOLEAN`</td>
<td>Boolean casting works in Laravel, but avoid direct `0` or `1` comparisons in raw queries.</td>
</tr>

<tr>
<td>Auto-increment IDs</td>
<td>Uses `AUTO_INCREMENT`</td>
<td>Uses `SERIAL`</td>
<td>Laravel handles this with `$table->id()` or `increments()`, but you may need to adjust raw SQL.</td>
</tr>

<tr>
<td>Unsigned integers</td>
<td>Supports `unsignedInteger` and `unsignedBigInteger`</td>
<td>Must use signed `bigInteger` or `foreignId()`</td>
<td>Laravel handles conversions in your migration files, but raw imports may reference `UNSIGNED BIGINT` columns. You will need to cast or redefine types on import.</td>
</tr>

<tr>
<td>UUIDs</td>
<td>Stores as strings</td>
<td>Has native UUID support</td>
<td>If you have a custom UUID definition that does not match the specification, it will fail in Postgres. Use Laravel's `Str::uuid()` helper to stay compatible.</td>
</tr>

<tr>
<td>Zero dates</td>
<td>Allows `'0000-00-00'`</td>
<td>Invalid date</td>
<td>Use `nullable()` and avoid "zero dates." Postgres throws an error on them.</td>
</tr>

<tr>
<td>JSON column</td>
<td>Supported, but is not validated.</td>
<td>Validates JSON on save.</td>
<td>Make sure the JSON you store is valid, or the Postgres save will fail.</td>
</tr>

<tr>
<td>Timestamp with timezone</td>
<td>`timestamp` does not store timezone detail</td>
<td>Supports `timestamp` with and without timezone</td>
<td>Laravel defaults to `timestamp`, so you must explicitly use `$table->timestampTz()` if you want time zone-aware behavior.</td>
</tr>

<tr>
<td>Implicit foreign key indexes</td>
<td>Foreign key columns automatically receive a corresponding index</td>
<td>Doesn't create indexes automatically</td>
<td>Explicitly add `->index()` to any `foreignId()` columns so Postgres creates their indexes.</td>
</tr>
</tbody>
</table>
