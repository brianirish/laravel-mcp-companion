Source: https://laravel.com/cloud/docs/knowledge-base/migrate-to-different-region.md

# Migrate an application to a different region

Learn how to move your Laravel Cloud application to a different region.

To move your application and its resources to a new region, create the new regional infrastructure first, then cut traffic over.

## Before you start

> [!WARNING]
>
> You cannot perform this migration in place. You will run old and new environments in parallel until cutover. Downtime is possible, especially during database cutover, so plan for it. For example, schedule a maintenance window and take backups. If you use private database connectivity, your database region must match your application region.

## Step 1: Create the new application

Create a new application in the target region using the same repository. Then recreate each environment, matching branch names and settings from the original application.

## Step 2: Migrate the database

Laravel Cloud does not provide cross-region database copy or restore. Complete the migration manually:

1. Export data from the current database with a tool such as `mysqldump`, `pg_dump`, or a Neon export.
2. Create a new database cluster and database in the target region through the normal create flow.
3. Import your data into the new database.
4. Attach the new database to the new application's environments.

Do not detach or delete the original database until you have verified cutover.

## Step 3: Migrate the cache

Laravel Cloud does not migrate cache data for you. The process depends on whether you need to keep your cache data:

1. Create a new cache in the target region.
2. Attach it to your new environments.
3. If you need to keep the data, implement dual writes in your application before you switch reads to the new cache.
4. Delete the old cache once you've cut over.

If your cache holds only ephemeral data, such as sessions or rate-limiting state, you can skip data migration and start with a fresh cache.

## Step 4: Migrate WebSockets (Reverb)

1. Create a new Reverb WebSocket cluster in the target region.
2. Attach it to the new environments.
3. Delete the old cluster after cutover.

## Step 5: Copy environment configuration

Manually copy configuration from each old environment to its corresponding new environment:

* Environment variables
* Build and deploy settings
* Vanity domains

## Step 6: Deploy and verify

Deploy each environment in the new application, then verify:

* Deployments complete successfully
* Database connections work
* Cache works
* WebSocket connections succeed
* Logs appear (logs are region-specific through OpenSearch)

## Step 7: Migrate domains

To move your domains to the new application:

1. Go to the old environment's **Network settings**.
2. Open the **...** dropdown on each domain.
3. Click the **Move** option.
4. Follow the dialog instructions and select the new environment as the target.
5. Redeploy the new application to update `APP_URL`.

You cannot move a primary domain between environments. To move it, first choose **Unset as primary** in the domain dropdown. After the move completes, set the domain as primary in the new application.

## Step 8: Clean up

Once you've confirmed everything is working in the new region:

* Delete or archive the old database cluster, cache, and WebSocket cluster
* Delete the old application
