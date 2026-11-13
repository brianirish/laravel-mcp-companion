Source: https://laravel.com/cloud/docs/knowledge-base/migrating-rails-to-cloud.md

# Migrate Rails to Cloud

Move a Rails application from Heroku, AWS, or a Kamal deployment to Laravel Cloud.

Move your Rails application to Laravel Cloud by deploying a staging environment, copying its persistent data, and testing the application before changing production traffic. Use the [Ruby and Rails deploy guide](https://laravel.com/cloud/docs/deploy-guides/ruby) for runtime, database, and worker configuration.

## Prepare a staging deployment

1. Commit `Gemfile.lock`, a supported Ruby version declaration, and the `aarch64-linux` lockfile platform.
2. Create a Cloud application from your repository and select its deployment branch.
3. Attach a managed database and any cache or object storage the application needs.
4. Copy application secrets through environment variables or [Secrets Manager](https://laravel.com/cloud/docs/secrets), including the existing `SECRET_KEY_BASE` and the matching `RAILS_MASTER_KEY`.
5. Configure the web command, deploy command, and background processes, then deploy to a staging environment.

Keep the existing production application serving traffic while you test. Use staging credentials for email, payments, and other integrations that could affect real users.

## Move from Heroku

Replace Heroku resources and process settings with their Cloud equivalents:

| Heroku configuration | Cloud configuration |
| - | - |
| Ruby buildpack and stack | Detected Ruby runtime and committed version declaration |
| Config vars | Environment variables or linked secrets |
| `web` Procfile entry | Initial start command, with an IPv6 listener on `PORT` |
| `release` Procfile entry | Suggested deploy command, reviewed in deployment settings |
| Worker dynos | Custom background processes or worker clusters |
| Heroku Postgres | Attached managed Postgres or your existing external database |
| Redis add-on | Attached Redis-compatible cache or an external connection |
| Scheduler add-on | [Cloud Scheduler](https://laravel.com/cloud/docs/scheduled-tasks#other-stacks) with scheduled Rails commands |

Cloud reads Procfile suggestions but doesn't start every entry automatically. Review each command, especially worker and release commands, before deploying. Remove buildpack-specific scripts and replace any packages they installed with dependencies available in Cloud's runtime.

Create a database backup using [Heroku Postgres backups](https://devcenter.heroku.com/articles/heroku-postgres-backups). Restore a copy into your target Postgres database using the connection details in **View credentials**. For managed Postgres, include `sslmode=require` in the connection URL. Use compatible `pg_dump` and `pg_restore` versions, and review extensions, ownership, and permissions before restoring.

You can keep an existing S3 bucket or email provider during the move. Configure its credentials explicitly. If you replace S3 with Cloud object storage, follow the [object storage migration guide](https://laravel.com/cloud/docs/knowledge-base/migrating-object-storage) and preserve Active Storage object keys.

## Move from AWS

Inventory each AWS dependency before moving the application. Cloud can host the Rails web process and workers while you retain services such as SQS or SES through their public service endpoints.

| Existing AWS resource | Migration action |
| - | - |
| EC2, ECS, or Elastic Beanstalk | Move web and worker commands to Cloud and review runtime dependencies |
| RDS | Restore into a managed database, or configure an external connection |
| ElastiCache | Attach a Cloud cache, or configure a reachable external cache |
| S3 | Retain the bucket, or copy objects to Cloud storage while preserving keys |
| SQS and SES | Keep service-specific credentials, endpoints, and regions |
| Instance profiles and task roles | Replace implicit role credentials with credentials available to your Cloud application |

A private RDS or ElastiCache address inside your AWS VPC isn't automatically reachable from Cloud. Plan connectivity before relying on an external resource, or migrate it to an attached Cloud resource. Restrict any public endpoint and use verified TLS where the service supports it.

Cloud's attached R2 bucket injects AWS-named variables. Keep [R2 and AWS clients separate](https://laravel.com/cloud/docs/deploy-guides/ruby#use-r2-alongside-other-aws-services) so SQS, SES, or an existing S3 bucket doesn't inherit R2's region or endpoint. Review credentials that previously came from an EC2 instance profile or ECS task role.

Export a consistent database snapshot using the source database's tools. For MySQL imports, follow [Importing MySQL data](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#importing-mysql-data). For Postgres, restore a dump into a staging database first and check extensions, row counts, constraints, and generated ID sequences before cutover.

### Differences from Kamal

Cloud builds your application from the repository and runs it on a managed Ruby runtime. Your Kamal `config/deploy.yml`, Dockerfile, accessory definitions, and host volumes don't configure that runtime.

Move Kamal secrets into Cloud environment variables or linked secrets. Translate the web and worker roles into Cloud commands and clusters. Replace host-mounted uploads and SQLite files with object storage and managed databases. Review any custom OS packages from your Dockerfile against the Cloud Ruby runtime, including tools used for media processing.

Cloud handles the public HTTPS endpoint and deployment routing. Keep Rails' HTTPS and [proxy configuration](https://laravel.com/cloud/docs/deploy-guides/ruby#running-behind-the-proxy), and test WebSockets and graceful shutdown before switching traffic. Use Cloud deploy commands for database preparation, and remove Kamal hooks that assume SSH access or a persistent host filesystem.

## Move SQLite data to a managed database

Cloud instances have ephemeral filesystems, so a production SQLite database can't remain on the instance. Plan a separate migration for the primary database and any SQLite databases used by Solid Queue, Solid Cache, or Solid Cable.

1. Back up each SQLite file and rehearse the migration using a copy.
2. Add `pg` or `mysql2` to the production bundle and update `config/database.yml` for the managed adapter.
3. Review migrations for SQLite-specific SQL and types. Run your test suite against the target database engine.
4. Create the schema and import data using one migration method from the [SQLite migration guide](https://laravel.com/cloud/docs/knowledge-base/sqlite#migrating-from-sqlite-to-postgresql-or-mysql).
5. Verify row counts, foreign keys, unique constraints, and generated IDs before deploying the application against the target.

Choose whether Rails migrations create the target schema or your import tool creates it. Avoid loading a second schema over imported tables. If you create the schema outside Rails, reconcile `schema_migrations` with the migrations represented by that schema before running `db:prepare`. Otherwise, Rails may attempt to create existing tables.

Check boolean values, timestamps, JSON fields, and database-specific queries against the target adapter. Reset Postgres sequences after preserving numeric primary keys during import. Keep the original SQLite files as a recovery copy until you have verified the new database and its backups.

For Rails' Solid components, configure the conventional `cache`, `queue`, and `cable` connections before attaching the primary database. Cloud can then create their [secondary databases](https://laravel.com/cloud/docs/deploy-guides/ruby#solid-cache-solid-queue-and-solid-cable). Decide which cached data can be discarded and drain pending jobs before moving the queue database.

## Keep or replace Delayed Job

You can continue using [Delayed Job](https://github.com/collectiveidea/delayed_job) on Cloud. Keep `delayed_job_active_record`, the `daemons` gem, and the existing jobs table in your production setup, and configure Active Job in `config/environments/production.rb`:

```ruby theme={null}
config.active_job.queue_adapter = :delayed_job
```

If your application has the generated `bin/delayed_job` executable, add a custom background process that runs in the foreground:

```sh theme={null}
bundle exec bin/delayed_job run
```

If the executable is missing, run `bin/rails generate delayed_job` locally and commit the generated executable. If the jobs table is also missing, use `bin/rails generate delayed_job:active_record` to generate its migration, review it, and apply it through your deploy command. Avoid generating a duplicate migration if the `delayed_jobs` table already exists. Keep the worker's [cluster awake](https://laravel.com/cloud/docs/workers#workers-and-scale-to-zero) when jobs must run without HTTP traffic.

To replace Delayed Job with Solid Queue or Sidekiq, install and configure the new backend in staging first. Active Job abstracts the enqueue API, but it doesn't translate stored Delayed Job records into another backend's queue.

Stop new enqueues to Delayed Job during cutover and let its workers drain pending jobs. Inventory scheduled and failed jobs, then explicitly re-enqueue the jobs you need through application code after changing the adapter. Direct calls such as `object.delay` also need to move to job classes or another supported API. Keep jobs safe to retry so a cutover retry doesn't duplicate a payment or email.

## Switch production traffic

1. Rehearse the database and object-storage imports, and record how long the final copy takes.
2. Pause writes on the source application and stop producers of new jobs. Drain or record pending and scheduled jobs before stopping its workers.
3. Take the final database backup and copy the remaining data and uploaded objects.
4. Deploy Cloud against the final database, then test sign-in, a write, an upload, a background job, and email delivery.
5. Add and verify your [custom domain](https://laravel.com/cloud/docs/domains), update DNS, and check HTTPS and WebSocket connections through the production hostname.

Keep the old deployment available until you finish verification, but prevent it from writing to a stale database or processing the same jobs. If you need to return traffic to the old host after Cloud has accepted writes, reconcile that data first. Changing DNS alone doesn't copy those writes back.
