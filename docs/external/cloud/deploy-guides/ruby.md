Source: https://laravel.com/cloud/docs/deploy-guides/ruby.md

# Ruby and Rails deploy guide

Configure your Ruby or Ruby on Rails application for production on Laravel Cloud.

The [Ruby and Rails quickstart](https://laravel.com/cloud/docs/quickstart#ruby-and-rails) walks you through your first deployment to Laravel Cloud. Once your application is up and running, this guide will help you get it ready for production. We'll cover preparing your repository, running Puma, connecting your databases, and handling assets, uploads, and background jobs. Most of the guide focuses on Ruby on Rails, but if you are deploying another Ruby or Rack application, be sure to read [Other Ruby and Rack applications](#other-ruby-and-rack-applications) as well.

## Prepare your repository

Cloud detects a Ruby application when it finds a `Gemfile` in your application directory. You should commit both your `Gemfile` and `Gemfile.lock`, and make sure they include your production server and database adapter. For Rails applications, keep the generated `config/application.rb`, `config/environment.rb`, and `bin/rails` files in your repository, since Cloud uses them to recognize the framework.

Your application runs on Linux with ARM64 processors. If your lockfile only lists the platforms for your development machine, add Cloud's platform locally and commit the updated lockfile:

```sh theme={null}
bundle lock --add-platform aarch64-linux
```

Cloud accepts lockfiles that include the `aarch64-linux`, `aarch64-linux-gnu`, or generic `ruby` platform. If the application creation form reports a missing platform, push your updated lockfile and refresh the repository scan before continuing.

If your application lives in a [monorepo](https://laravel.com/cloud/docs/monorepos), select the directory that contains your `Gemfile`. Cloud keeps the surrounding repository available, so dependencies such as sibling path gems continue to work.

## Choose a Ruby version

Cloud supports Ruby 3.3, 3.4, and 4.0, with Ruby 4.0 as the default. The simplest way to choose your version is with a `.ruby-version` file:

```text theme={null}
3.4
```

Cloud reads your version declaration from each deployment's commit. It checks `.ruby-version` first, then the `RUBY VERSION` section of `Gemfile.lock`, the `ruby` declaration in your `Gemfile`, `.tool-versions`, and finally `mise.toml`. A minor declaration such as `3.4` follows Cloud's current patch for that release line. An exact declaration such as `3.4.7` selects that patch when Cloud supports it. A `Gemfile` version constraint selects the lowest supported release line that satisfies it.

If your repository doesn't declare a version, you may select one from your environment's **General Settings** instead. If you declare a version Cloud doesn't support, the deployment stops before building. You can find more details in the [Ruby runtime](https://laravel.com/cloud/docs/runtimes#ruby) documentation.

Keep your Ruby declarations consistent with one another. For example, if your `Gemfile` requires exactly `3.4.7`, use the same patch in `.ruby-version`. Bundler rejects a runtime that doesn't satisfy the `Gemfile`, even when another declaration takes precedence in Cloud's version detection.

## Install dependencies

Cloud installs your gems automatically before running your [build commands](https://laravel.com/cloud/docs/environments#build-commands). It uses the Bundler version recorded under `BUNDLED WITH` in your `Gemfile.lock`, or the Bundler version that ships with the runtime if that section is missing.

Cloud installs gems using Bundler's deployment and frozen modes. Update your dependencies locally and commit the lockfile rather than running `bundle update` during deployment. Be sure that every gem your application needs in production lives outside of the excluded groups, including `puma`, your database adapter, and any gems used for background jobs or building assets.

By default, Cloud skips the `development` and `test` groups. You may change which groups are installed using your [environment variables](https://laravel.com/cloud/docs/environments#environment-variables) or [linked secrets](https://laravel.com/cloud/docs/secrets):

```ini theme={null}
BUNDLE_WITHOUT=development:test
BUNDLE_WITH=production
```

If you need every ordinary group installed, set `BUNDLE_WITHOUT` to an empty value. Cloud applies these settings while installing your gems and keeps the same group configuration at runtime. Remember to redeploy after changing them.

## Run a production server

### Rails

Cloud pre-fills your Rails start command using your application's binstub, when it exists:

```sh theme={null}
bundle exec bin/rails server -b '::' -p $PORT
```

If your application doesn't have a `bin/rails` binstub, Cloud uses `bundle exec rails server` with the same bind and port options. Either way, keep `puma` in your production dependencies so Rails can start its server.

Your server must listen on the port set by the `PORT` environment variable, which is `3000` by default, and it must accept IPv6 connections. Cloud's startup probes reach your application over IPv6. If you change the start command, be sure to keep the `::` bind, since an IPv4-only or loopback-only listener will prevent the probes from reaching your application.

If you would rather start Puma directly, replace the `port` or `bind` directive in your `config/puma.rb` file with the following:

```ruby theme={null}
bind "tcp://[::]:#{ENV.fetch('PORT', '3000')}"
```

Then, set your start command to:

```sh theme={null}
bundle exec puma -C config/puma.rb
```

Puma should have a single listener for your application's port, so remove any other `port` or `bind` directives from your configuration. You should also keep Puma running in the foreground.

### Procfile commands

If your repository includes a `Procfile`, Cloud uses its `web` command as your initial start command instead of the framework default. For example:

```text theme={null}
web: bundle exec puma -C config/puma.rb
worker: bundle exec sidekiq
release: bin/rails db:prepare
```

If you use this example, remember to configure the IPv6 listener in `config/puma.rb` as described in the previous section. For Rails applications, Cloud also offers the `release` command in your deployment settings and suggests your other processes as background processes. Cloud doesn't run your entire Procfile automatically, so be sure to review these suggestions and configure the ones you need in your environment.

### Configure Puma concurrency

You should configure Puma's process and thread counts based on your instance's CPU and memory. Unlike Python applications, Cloud doesn't calculate `WEB_CONCURRENCY` for Ruby applications. You may set it yourself, or start with Puma's single-process mode and increase concurrency once you have a feel for your application's memory usage.

For example, you might add the following settings to your existing `config/puma.rb` file:

```ruby theme={null}
thread_count = Integer(ENV.fetch("RAILS_MAX_THREADS", "3"))
threads thread_count, thread_count
workers Integer(ENV.fetch("WEB_CONCURRENCY", "0"))

force_shutdown_after 20
worker_shutdown_timeout 25
```

Setting `WEB_CONCURRENCY=0` runs a single server process without clustered workers. Setting it to `1` starts a Puma master and one worker, so it uses an additional process. Avoid automatically matching the host CPU count on small instances. Keep in mind that each clustered worker has its own thread pool and its own database connection pools. Set the pool for each database large enough to accommodate every thread that uses it, including any background or asynchronous work.

## Rails environment variables

New Rails environments include a securely generated `SECRET_KEY_BASE`, which you are free to edit. You should keep this value the same across deployments so your users' existing signed cookies and sessions stay valid. If you are migrating an existing application, use its current secret.

Cloud also provides the following production defaults:

| Variable | Value |
| - | - |
| `RAILS_ENV` | `production` |
| `RACK_ENV` | `production` |
| `BUNDLE_WITHOUT` | `development:test` |
| `DISABLE_SPRING` | `1` |
| `RAILS_LOG_TO_STDOUT` | `1` |

Cloud sets your environment variables on your application's process and makes them available to your build commands, so you can read any custom settings from `ENV` just like you do locally. If you define a variable yourself, your value takes precedence over both linked secrets and the injected defaults.

### Encrypted credentials

If your application uses encrypted Rails credentials, add the matching `RAILS_MASTER_KEY` to your environment variables or [Secrets Manager](https://laravel.com/cloud/docs/secrets). Be sure to use the key for the credentials file your production configuration actually loads, such as `config/credentials.yml.enc` or `config/credentials/production.yml.enc`.

Keep in mind that `SECRET_KEY_BASE` is only used to sign your application's data. It can't decrypt your credentials, so it doesn't replace `RAILS_MASTER_KEY`. If your production configuration explicitly enables `config.require_master_key`, Cloud will check for a key before building your application.

## Databases

When you connect a [Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) or [MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) database from your environment's infrastructure canvas, Cloud provides a `DATABASE_URL` variable containing a `postgresql://` or `mysql2://` URL for Rails.

Be sure to include the `pg` gem for Postgres or the `mysql2` gem for MySQL in your production bundle. Rails reads `DATABASE_URL` automatically and merges it with your `config/database.yml` file. However, an explicit `url:` in that file takes precedence, so if your configuration still contains a URL from a previous host, remove it so Rails uses Cloud's connection instead.

You should always use a managed database in production. Since your environment's [filesystem](https://laravel.com/cloud/docs/environments#filesystem) is ephemeral, a SQLite file stored on an instance can't be shared across replicas and won't survive your next deployment.

### MySQL TLS

TLS settings depend on the database endpoint and its client library. Keep the hostname Cloud provides for your attached database. If you use a [public endpoint](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#laravel-mysql-ssl-connections), configure certificate and hostname verification in `config/database.yml`:

```yaml theme={null}
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS", 3) %>

production:
  primary:
    <<: *default
    ssl_mode: verify_identity
    sslca: <%= ENV["MYSQL_SSL_CA"] %>
```

Set `MYSQL_SSL_CA` to the path of a trusted CA bundle on the machine making the connection. Use the public hostname from **View credentials** so hostname verification can succeed. Apply the settings to any secondary connections that use that public endpoint, and keep your development and test configuration alongside these entries.

The available SSL modes depend on your `mysql2` gem and its linked MySQL or MariaDB client library. Check the [mysql2 SSL options](https://github.com/brianmario/mysql2#ssl-options) before using `verify_identity`, and use a compatible client if your current one doesn't support it.

For a private endpoint, confirm its TLS support and connection policy before changing the SSL mode. `required` encrypts the client connection without verifying the server identity and fails if the endpoint doesn't support TLS. Rails gives URL parameters precedence over matching `database.yml` options, so avoid adding `ssl_mode=required` to a URL if your application already requests stronger verification.

After deploying, check the connection from the Cloud console:

```ruby theme={null}
ActiveRecord::Base.connection.select_all("SHOW SESSION STATUS LIKE 'Ssl_cipher'").to_a
```

A nonempty `Value` confirms encryption between the client and its database endpoint. The runtime's `SSL_MODE` variable controls the HTTP proxy and doesn't configure mysql2.

### Solid Cache, Solid Queue, and Solid Cable

Rails applications may use separate production connections named `cache`, `queue`, and `cable`. Cloud detects these connections in your `config/database.yml` file, and when you attach your primary database, it creates a separate database for each one it finds. These databases live in the same database cluster as your primary connection.

For example, a Postgres application using all three Solid components might have the following configuration:

```yaml theme={null}
default: &default
  adapter: postgresql
  pool: <%= ENV.fetch("RAILS_MAX_THREADS", 3) %>

production:
  primary:
    <<: *default
    database: my_app_production
  cache:
    <<: *default
    database: my_app_production_cache
    migrations_paths: db/cache_migrate
  queue:
    <<: *default
    database: my_app_production_queue
    migrations_paths: db/queue_migrate
  cable:
    <<: *default
    database: my_app_production_cable
    migrations_paths: db/cable_migrate
```

You only need to keep the connections your application actually uses. If you are using MySQL, use the `mysql2` adapter and its gem instead. Cloud provides a connection URL for each connection, and Rails reads them automatically:

| Connection | Environment variable |
| - | - |
| `primary` | `DATABASE_URL` |
| `cache` | `CACHE_DATABASE_URL` |
| `queue` | `QUEUE_DATABASE_URL` |
| `cable` | `CABLE_DATABASE_URL` |

To have Cloud provision these databases, keep the conventional connection names and leave out any `url:` entries. It skips connections that have an explicit URL or `replica: true`, and you will need to configure connections with any other name yourself. Since Cloud reads the structure of your YAML file without evaluating its Ruby expressions, write out your production connection definitions in the file. Keep `url: <%= ENV['DATABASE_URL'] %>` out of shared YAML anchors too, since secondary connections would inherit the primary URL and use the primary database.

You may override the injected secondary URLs using your own environment variables or linked secrets, but those external connections are then yours to manage. When you replicate an environment, Cloud copies or creates the attached secondary databases based on the database replication option you choose. If you have set custom URLs, review them before deploying a replica or preview environment so it doesn't accidentally use your production data.

> [!NOTE]
>
> Changing `config/database.yml` on its own doesn't update an existing environment's database attachments, so be sure to declare your connections before Cloud scans your repository and you attach the database. Detaching a database removes the environment's secondary connections, but the databases themselves are kept.

Cloud waits for your attached databases to become available before deploying. Keep in mind that creating these connections doesn't install the Solid gems or start a queue worker for you. You will still need to configure each Solid component to use its corresponding Rails connection and include its migration or schema files. The [Rails multiple database guide](https://guides.rubyonrails.org/active_record_multiple_databases.html) walks through the application configuration.

### Prepare the databases

Database preparation belongs in your environment's [deploy commands](https://laravel.com/cloud/docs/environments#deploy-commands):

```sh theme={null}
bin/rails db:prepare
```

Cloud runs this command just before your new deployment starts receiving traffic, and it cancels the rollout if the command fails. Rails prepares each of your configured databases and applies any pending migrations.

New Rails environments start with this command commented out. When you attach a database, Cloud enables it for you automatically, as long as you haven't customized your deploy command. If you have, add the preparation step yourself.

You should avoid running migrations from your start command. The start command runs every time an instance starts, including during deployments, autoscaling, and wake-ups after scaling to zero. Since your previous deployment keeps running while the new one rolls out, you should also write your migrations so they remain compatible with both.

## Build and serve assets

When Cloud detects Propshaft or Sprockets in a Rails application that isn't configured as API-only, it pre-fills the following build command:

```sh theme={null}
SECRET_KEY_BASE_DUMMY=1 bundle exec rails assets:precompile
```

If Cloud also detects a JavaScript package manager, it adds a step to install your JavaScript dependencies. Ruby runtimes include Node.js, npm, and Yarn. Be sure to keep the dependencies your asset build needs, including any development dependencies used by your JavaScript build tools.

If you use a custom asset pipeline, review the pre-filled command and adjust it as needed. API-only Rails applications don't receive this default asset build. Cloud's Nginx server serves files from your application's `public` directory, including the compiled assets in `public/assets`.

The `SECRET_KEY_BASE_DUMMY=1` setting only applies to asset compilation. Your real `SECRET_KEY_BASE` is still used at runtime, so don't add the dummy setting as an environment variable. Also, keep in mind that initializers that access your credentials or database may still require those resources while your assets compile.

## Caches and background jobs

When you attach a [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) or [Redis](https://laravel.com/cloud/docs/resources/caches/redis) cache, Cloud provides a `REDIS_URL` variable. You should configure your cache library or Rails cache store to use this URL, and make sure it supports TLS when the URL uses the `rediss://` scheme.

To use Rails' Redis cache store, include the `redis` gem and add the following to your `config/environments/production.rb` file:

```ruby theme={null}
config.cache_store = :redis_cache_store, { url: ENV.fetch("REDIS_URL") }
```

If your application uses Solid Cache, you may keep your existing database cache configuration instead. Either way, choose the backing store your application is configured to use.

### Jobs on small instances

For a small application, running jobs inside the web process can reduce the memory used by additional Rails processes. Jobs then share CPU, memory, and database connections with web requests. Start with one job thread and measure memory and request latency under your workload before increasing concurrency.

If your installed Solid Queue version supports [async mode](https://github.com/rails/solid_queue#fork-vs-async-mode), add the following to `config/puma.rb`, replacing any existing Solid Queue plugin configuration:

```ruby theme={null}
plugin :solid_queue if ENV["SOLID_QUEUE_IN_PUMA"] == "true"
solid_queue_mode :async if ENV["SOLID_QUEUE_IN_PUMA"] == "true"
```

Set `SOLID_QUEUE_IN_PUMA=true` and `WEB_CONCURRENCY=0` in Cloud. In `config/queue.yml`, start with a single worker thread:

```yaml theme={null}
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 100
  workers:
    - queues: "*"
      threads: 1
      polling_interval: 0.1
```

Set `config.active_job.queue_adapter = :solid_queue` in `config/environments/production.rb` and configure its database connection as described in the [Solid Queue documentation](https://github.com/rails/solid_queue#installation). Async mode runs jobs in threads inside Puma. Enabling the Puma plugin alone uses Solid Queue's default fork mode, which starts additional processes. Fork mode remains Solid Queue's recommended default when you need process isolation.

For Sidekiq 7 or later, [embedding](https://github.com/sidekiq/sidekiq/wiki/Embedding) is another option. With Puma 7 or later in single-process mode, add the following to `config/puma.rb`:

```ruby theme={null}
require "sidekiq"

workers 0
embedded_sidekiq = nil

after_booted do
  embedded_sidekiq = Sidekiq.configure_embed do |config|
    config.queues = ["default", "mailers", "active_storage_analysis", "active_storage_purge"]
    config.concurrency = 1
  end

  embedded_sidekiq.run
end

after_stopped do
  embedded_sidekiq&.stop
end
```

Replace any existing `workers` setting with `workers 0`. Set `config.active_job.queue_adapter = :sidekiq` in `config/environments/production.rb` and attach a Redis-compatible cache. Embedded Sidekiq doesn't read `sidekiq.yml`, so list every queue your application uses in this configuration. Use ordinary deployments to restart this setup, and follow Sidekiq's lifecycle guidance before introducing Puma restarts or clustered workers.

Use one job backend and one startup method for it. Remove a standalone worker process if you switch its workload to embedding. Include job threads when sizing each database connection pool.

### Separate workers

For jobs that need independent resources or scaling, configure [custom background processes](https://laravel.com/cloud/docs/workers#custom-background-processes) on your App cluster or a worker cluster:

| Backend | Example command |
| - | - |
| Solid Queue | `bundle exec bin/jobs` |
| Sidekiq | `bundle exec sidekiq` |
| GoodJob | `bundle exec good_job start` |

Keep the required gems and binstubs in your production bundle. Cloud suggests Sidekiq and GoodJob commands based on your lockfile, along with processes from your Procfile. If you use Solid Queue with `bin/jobs`, add the process yourself.

A background process on the App cluster still shares that instance's resources with Puma. A worker cluster gives jobs their own compute. Each background process runs on every replica of its cluster, so account for total job concurrency and database connections when choosing process counts and replica limits. Measure the combined peak memory during web requests and jobs before choosing an instance size. Cloud console sessions and one-off [commands](https://laravel.com/cloud/docs/commands) also run inside an existing instance and use its available memory.

### Recurring tasks and scale to zero

Use [Cloud Scheduler](https://laravel.com/cloud/docs/scheduled-tasks#other-stacks) to run recurring Rails commands. Open your App cluster, then add a command and schedule under **Scheduled commands**. Save the cluster settings and deploy the environment.

For example, to execute a job named `CleanupJob` directly, add this command:

```sh theme={null}
bundle exec bin/rails runner 'CleanupJob.perform_now'
```

Set the schedule to `@hourly` to run hourly in UTC without writing a cron expression. Cloud Scheduler wakes a sleeping App cluster to run the command, so you can keep [scale to zero](https://laravel.com/cloud/docs/compute#scale-to-zero) enabled without running a separate scheduling process.

If you move a task from Solid Queue's `config/recurring.yml` into Cloud Scheduler, remove its old entry so both schedulers don't run it. Cloud Scheduler uses the commands and schedules you configure in Cloud.

A command that calls `perform_later` enqueues work for a queue worker. Keep that worker running, such as on a [worker cluster that stays awake](https://laravel.com/cloud/docs/workers#workers-and-scale-to-zero), if queued jobs must continue processing while the App cluster sleeps. The `perform_now` example completes the job within the scheduled command.

## Store files in object storage

For user uploads, you should use [object storage](https://laravel.com/cloud/docs/resources/object-storage). To get started, attach a private bucket as your environment's default disk. Cloud provides the bucket's AWS connection variables, but you will need to select and configure an Active Storage service in Rails yourself.

First, add the `aws-sdk-s3` gem to your production `Gemfile`, run `bundle install` locally, and commit the updated lockfile. Then, add the following service to your `config/storage.yml` file:

```yaml theme={null}
cloud:
  service: S3
  access_key_id: <%= ENV["AWS_ACCESS_KEY_ID"] %>
  secret_access_key: <%= ENV["AWS_SECRET_ACCESS_KEY"] %>
  region: <%= ENV.fetch("AWS_REGION", "auto") %>
  bucket: <%= ENV["AWS_BUCKET"] %>
  endpoint: <%= ENV["AWS_ENDPOINT_URL"] %>
  force_path_style: false
  request_checksum_calculation: when_required
  response_checksum_validation: when_required
```

Finally, select the service in your `config/environments/production.rb` file:

```ruby theme={null}
config.active_storage.service = :cloud
```

The checksum settings keep AWS SDK checksum handling compatible with Cloudflare R2. Use a current `aws-sdk-s3` version that supports these options. The `ENV[]` lookups allow Rails to parse the service configuration locally without Cloud credentials. Keep `config.active_storage.service = :local` in development and `:test` in tests, with their generated Disk services in `storage.yml`. Production still needs all the bucket connection values.

### Private buckets

The default S3 service generates signed URLs for a private bucket. Keep the bucket private and omit per-object ACL options. Cloudflare R2 manages visibility at the bucket level and doesn't support S3 object ACLs.

### Public buckets

Only use a public bucket for files that anyone may download. When you attach a public bucket as the environment's default disk, Cloud injects its public base URL as `AWS_URL`. Use that value to generate public file URLs. If you configure a custom domain for the bucket, you may override `AWS_URL` with that domain's HTTPS origin.

Setting `public: true` on Rails' S3 service adds a `public-read` object ACL and generates URLs using the S3 endpoint. R2's public bucket domain is separate from that API endpoint. For Rails 8.1, you can use a custom service to omit the ACL and generate public URLs from the bucket domain.

Create `lib/active_storage/service/r2_service.rb`:

```ruby theme={null}
require "active_storage/service/s3_service"
require "erb"

class ActiveStorage::Service::R2Service < ActiveStorage::Service::S3Service
  def initialize(public_url:, **options)
    super(**options, public: true)
    @public_url = public_url.delete_suffix("/")
    upload_options.delete(:acl)
  end

  private

  def public_url(key, **options)
    path = key.split("/").map { |part| ERB::Util.url_encode(part) }.join("/")
    "#{@public_url}/#{path}"
  end
end
```

Add a separate service in `config/storage.yml`, reusing the private service's connection and checksum settings with a YAML anchor:

```yaml theme={null}
cloud: &cloud
  service: S3
  access_key_id: <%= ENV["AWS_ACCESS_KEY_ID"] %>
  secret_access_key: <%= ENV["AWS_SECRET_ACCESS_KEY"] %>
  region: <%= ENV.fetch("AWS_REGION", "auto") %>
  bucket: <%= ENV["AWS_BUCKET"] %>
  endpoint: <%= ENV["AWS_ENDPOINT_URL"] %>
  force_path_style: false
  request_checksum_calculation: when_required
  response_checksum_validation: when_required

cloud_public:
  <<: *cloud
  service: R2
  public_url: <%= ENV["AWS_URL"] %>
```

Select `:cloud_public` in `config/environments/production.rb` when the attached bucket is public. Use `AWS_URL` as the public base URL without appending the bucket name. Test server-side uploads, direct uploads, and variant URLs after upgrading Rails, since the service extends Rails' [S3 adapter](https://api.rubyonrails.org/classes/ActiveStorage/Service/S3Service.html).

### Use R2 alongside other AWS services

Cloud's attached bucket credentials belong to R2. Its injected `AWS_REGION` is `auto`, and `AWS_ENDPOINT_URL` points to R2. AWS SDK clients for other services can read those same variables, so configure their region, endpoint, and credentials separately.

For example, create an SQS client in `config/initializers/sqs.rb` with a region-specific AWS endpoint and its own credentials:

```ruby theme={null}
require "aws-sdk-sqs"

Rails.application.config.x.sqs = Aws::SQS::Client.new(
  region: ENV.fetch("SQS_REGION"),
  endpoint: ENV.fetch("SQS_ENDPOINT_URL"),
  credentials: Aws::Credentials.new(
    ENV.fetch("SQS_ACCESS_KEY_ID"),
    ENV.fetch("SQS_SECRET_ACCESS_KEY")
  )
)
```

Add `aws-sdk-sqs` to your production bundle and define these values through environment variables or linked secrets. For `us-east-2`, the standard SQS endpoint is `https://sqs.us-east-2.amazonaws.com`. Apply the same separation to an SES API client using `aws-sdk-sesv2`, `Aws::SESV2::Client`, and SES-specific settings.

### Jobs, variants, and previews

Active Storage schedules analysis and purge work through Active Job. Configure a persistent production queue adapter and run a worker that consumes its queues. If you customize queue names or enqueue preprocessed variants, make sure your worker consumes those queues too.

The Ruby runtime includes libvips for image variants. See the [Ruby base image reference](https://laravel.com/cloud/docs/base-images#ruby) for included system packages and tools. Add `image_processing` to your production bundle and select the processor in `config/environments/production.rb`:

```ruby theme={null}
config.active_storage.variant_processor = :vips
```

Video previews require FFmpeg, and PDF previews require Poppler or a suitable ImageMagick installation. Cloud's Ruby runtime doesn't include those preview tools. Disable the affected previewers or perform that processing in a separate service. Test a real image upload and queued analysis job after deployment. See the [Active Storage guide](https://guides.rubyonrails.org/active_storage_overview.html) for queue configuration and preview requirements.

## WebSockets

### Cloud WebSockets

You can attach [Cloud WebSockets](https://laravel.com/cloud/docs/resources/websockets#ruby) to your Rails environment to use a managed Laravel Reverb cluster. Cloud provides `PUSHER_APP_ID`, `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_HOST`, `PUSHER_PORT`, and `PUSHER_SCHEME`. Configure the `pusher` gem with these values to publish events, and use a Pusher-compatible browser client to receive them. See the [Ruby publishing example](https://laravel.com/cloud/docs/resources/websockets/pusher#ruby) and [JavaScript client configuration](https://laravel.com/cloud/docs/resources/websockets/pusher#javascript-websocket-client).

Reverb uses the Pusher protocol. Rails' Action Cable and `turbo_stream_from` use the Action Cable protocol, so switching those subscriptions to Reverb requires changes to your application's publishing and browser subscription code. Keep the Action Cable setup described in the next section if you use Rails' built-in broadcasting.

### Action Cable and Turbo Streams

Rails can serve Action Cable WebSockets through the same Puma server as HTTP requests. Keep the default `/cable` mount, or mount `ActionCable.server` at that path in `config/routes.rb` if your application removed it. Configure the public URL and allowed browser origins in `config/environments/production.rb`:

```ruby theme={null}
app_url = ENV.fetch("APP_URL").delete_suffix("/")
config.action_cable.url = "#{app_url.sub(/\Ahttps:/, 'wss:')}/cable"
config.action_cable.allowed_request_origins = [app_url]
config.action_cable.disable_request_forgery_protection = false
```

Add every browser origin that legitimately connects, including custom domains. Keep origin checking enabled. Cloud handles the HTTPS and WebSocket connection before forwarding it to Puma.

Use a shared production subscription adapter across replicas. For Redis, include the `redis` gem and configure `config/cable.yml`:

```yaml theme={null}
production:
  adapter: redis
  url: <%= ENV["REDIS_URL"] %>
  channel_prefix: <%= ENV.fetch("LARAVEL_CLOUD_ENV_UUID", "my_app_production") %>
```

Attach a Redis-compatible cache and keep TLS enabled for `rediss://` connections. If you use Solid Cable instead, keep its `cable` database connection and migrations configured. The development `async` adapter only broadcasts within one process.

Turbo Streams uses Action Cable's connection, so you can keep your existing `turbo_stream_from` subscriptions. Test a broadcast between two browser sessions after deployment. See the [Rails Action Cable guide](https://guides.rubyonrails.org/action_cable_overview.html) for authentication and subscription setup.

## Monitoring

Cloud captures stdout and stderr in [Logs](https://laravel.com/cloud/docs/logs). Keep the stdout logger described in [Logging](#logging) enabled even when using an external monitoring service. Cloud injects `LARAVEL_CLOUD_COMMIT_SHA`, `LARAVEL_CLOUD_DEPLOY_UUID`, `LARAVEL_CLOUD_ENV_NAME`, and `LARAVEL_CLOUD_ENV_UUID` so you can identify the release and environment in reports.

### Sentry

Add `sentry-ruby` and `sentry-rails` to your production bundle, and define `SENTRY_DSN` in Cloud. Create `config/initializers/sentry.rb`:

```ruby theme={null}
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.release = ENV["LARAVEL_CLOUD_COMMIT_SHA"]
  config.environment = ENV.fetch("LARAVEL_CLOUD_ENV_NAME", Rails.env)
  config.send_default_pii = false
end

Sentry.configure_scope do |scope|
  scope.set_tags(
    cloud_deployment: ENV["LARAVEL_CLOUD_DEPLOY_UUID"],
    cloud_environment: ENV["LARAVEL_CLOUD_ENV_UUID"]
  )
end
```

Deploy and send a test error from a controlled request. Confirm that Sentry records the expected release and environment. Configure tracing and data filtering separately using the [Sentry Rails documentation](https://docs.sentry.io/platforms/ruby/guides/rails/).

### Datadog

Datadog's Ruby tracer sends traces to a Datadog Agent. Cloud doesn't provide an Agent endpoint for your application. Before enabling tracing, provide an Agent you operate that is reachable from the application, and set `DD_TRACE_AGENT_URL` to that endpoint. An API key alone doesn't configure a trace receiver.

Add the `datadog` gem to your production bundle and create `config/initializers/datadog.rb`:

```ruby theme={null}
require "datadog"

Datadog.configure do |config|
  config.service = ENV.fetch("DD_SERVICE", "my-rails-app")
  config.env = ENV.fetch("LARAVEL_CLOUD_ENV_NAME", Rails.env)
  config.version = ENV["LARAVEL_CLOUD_COMMIT_SHA"]
  config.tracing.instrument :rails
  config.tracing.log_injection = true
end
```

Configure Agent connectivity and transport security using the [Datadog Ruby tracer settings](https://docs.datadoghq.com/tracing/trace_collection/library_config/ruby/). Verify that a test request produces a trace with the expected service, environment, and version before enabling production traffic.

## Email with Resend

Attach a [Cloud email resource](https://laravel.com/cloud/docs/resources/email) to provide `RESEND_API_KEY` and sender variables. Add the `resend` gem to your production bundle and configure its Rails adapter in `config/environments/production.rb`:

```ruby theme={null}
Resend.api_key = ENV.fetch("RESEND_API_KEY")
config.action_mailer.delivery_method = :resend
```

Rails doesn't automatically select a mail adapter from Cloud's `MAIL_MAILER` variable. The Resend adapter sends through the provider's API and uses the injected `RESEND_API_KEY`.

Set the URL used for links in messages:

```ruby theme={null}
require "uri"

app_uri = URI.parse(ENV.fetch("APP_URL"))
config.action_mailer.default_url_options = {
  host: app_uri.host,
  protocol: app_uri.scheme,
  port: app_uri.port
}
config.action_mailer.raise_delivery_errors = true
```

Set your verified sender in `app/mailers/application_mailer.rb`:

```ruby theme={null}
class ApplicationMailer < ActionMailer::Base
  default from: ENV.fetch("MAIL_FROM_ADDRESS", "notifications@example.com")
  layout "mailer"
end
```

Replace the example address with a sender verified by your provider. For `deliver_later`, run a worker that consumes your application's mail queue as described in [Caches and background jobs](#caches-and-background-jobs).

Verify your sending domain and send a test message using the [Resend Rails integration](https://resend.com/docs/send-with-rails).

## Shut down gracefully

When an instance stops, whether during a deployment or while scaling down, Cloud sends a `SIGTERM` signal to your application's process. Puma handles this signal gracefully by letting active requests finish before exiting.

You should keep Puma's shutdown limits, such as the `force_shutdown_after` and `worker_shutdown_timeout` settings shown in [Configure Puma concurrency](#configure-puma-concurrency), shorter than your environment's **graceful shutdown timeout**. This leaves time for the proxy and the rest of the instance to stop cleanly. If your requests or jobs need more time to finish, increase the environment's timeout as well. Puma's [configuration documentation](https://puma.io/puma/Puma/DSL.html) describes the available shutdown and concurrency options.

## Running behind the proxy

Cloud handles TLS for you before forwarding requests to your application, so Puma only needs to speak plain HTTP. Cloud's proxy passes the original request scheme in the `X-Forwarded-Proto` header, so Rails can recognize HTTPS requests. You should keep your production HTTPS configuration, such as `config.force_ssl = true`, in place.

If you restrict hosts using `config.hosts`, be sure to allow your Cloud domain and any custom domains. You should also configure the hostnames used in URLs generated outside of a request, such as links in your mailers. Cloud provides an `APP_URL` variable, but Rails doesn't apply it to these settings automatically.

## Logging

Cloud captures everything your application writes to stdout and stderr and displays it in the [Logs](https://laravel.com/cloud/docs/logs) dashboard. Recent Rails applications already log to stdout. If you are deploying an older application that only writes to a log file, configure its logger in your `config/environments/production.rb` file:

```ruby theme={null}
config.logger = ActiveSupport::TaggedLogging.new(ActiveSupport::Logger.new($stdout))
config.log_tags = [
  :request_id,
  ->(_request) { ENV.fetch("LARAVEL_CLOUD_ENV_NAME", Rails.env) },
  ->(_request) { ENV.fetch("LARAVEL_CLOUD_COMMIT_SHA", "local") }
]
```

Keep in mind that the injected `RAILS_LOG_TO_STDOUT` variable only has an effect when your application's configuration reads it. The [Rails configuration guide](https://guides.rubyonrails.org/configuring.html) is a helpful reference when adapting an older application.

Cloud also provides `LARAVEL_CLOUD_DEPLOY_UUID` for the deployment and `LARAVEL_CLOUD_ENV_UUID` for the environment. Use these values in structured logs or error reports to distinguish deployments of the same commit. Avoid logging credentials or sensitive request data. See [Monitoring](#monitoring) for Sentry and Datadog release configuration examples.

If you are moving an existing application, follow [Migrate Rails to Cloud](https://laravel.com/cloud/docs/knowledge-base/migrating-rails-to-cloud).

## Other Ruby and Rack applications

For Ruby applications that don't use Rails, Cloud uses the `web` command from your Procfile if you have one. Otherwise, it uses the Ruby or Rack entrypoint you selected. A Ruby file such as `app.rb` runs with `bundle exec ruby app.rb`, so your program needs to start its own server, read `PORT`, and accept IPv6 connections.

For a Rack entrypoint such as `config.ru`, Cloud pre-fills the following start command:

```sh theme={null}
bundle exec rack-start.rb config.ru
```

Cloud's launcher uses Puma when it is available in your production bundle, or a compatible `rackup` executable otherwise, and it binds the server to `::` on `PORT` for you. Be sure to add Puma, or Rackup with a compatible server, to your production dependencies.

Generic Ruby applications receive `RACK_ENV=production`, `BUNDLE_WITHOUT=development:test`, and the connection variables for any attached resources. Their `DATABASE_URL` uses the `mysql://` or `postgresql://` scheme, so you may need to adapt it for the database library you use. The Rails-specific asset builds, secrets, and database preparation described in this guide don't apply to generic Ruby applications.
