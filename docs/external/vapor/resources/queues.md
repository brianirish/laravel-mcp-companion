# Vapor - Resources/Queues

*Source: https://docs.vapor.build/resources/queues*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#631502130c11230f02110215060f4d000c0e)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationResourcesQueues[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/vapor)
##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

Resources# Queues

Using queues with Laravel Vapor.

## [​](#introduction)Introduction

Laravel’s queues are one of the framework’s most powerful features. With Vapor, you can continue writing and dispatching queued jobs exactly as you would in a traditional server-hosted Laravel application. The only difference is that Vapor will automatically scale your queue processing throughput on-demand within seconds:

CopyAsk AI```
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast);

```

When using Vapor, your application will use the AWS SQS service, which is already a first-party queue driver within Laravel. Vapor will automatically configure your deployed application to use this queue driver by injecting the proper Laravel environment variables. You do not need to perform any additional configuration.

Currently, serverless applications on AWS may only process a single request (web or queue) for a maximum of 15 minutes. If your queued jobs take longer than 15 minutes, you will need to either chunk your job’s work into smaller pieces or consider another deployment solution for your application. In addition, a queued job may not have a “delay” greater than 15 minutes.

## [​](#custom-queue-names)Custom Queue Names

By default, Vapor will create an SQS queue that has the same name as your project and inject the proper environment variables to make this queue the default queue. If you would like to specify your own custom queue names that Vapor should create instead, you may define a `queues` option in your environment’s `vapor.yml` configuration. The first queue in the list of queues will be considered your “default” queue and will automatically be set as the `SQS_QUEUE` environment variable:

vapor.yml vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails
            - invoices

```

### [​](#queue-names-should-be-unique)Queue Names Should Be Unique

When using custom queue names, it is important to ensure the names are unique between projects and environments. For instance, you can add suffix values such as `-staging` and `-production` to the queue names specified in your application’s `vapor.yml` file:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails-production
            - invoices-production
    staging:
        queues:
            - emails-staging
            - invoices-staging

```

Because it is cumbersome to include these suffixes when dispatching jobs to specific queues in Laravel, Laravel’s `sqs` queue configuration includes a `suffix` option that references the `SQS_SUFFIX` environment variable by default. When this option and variable are defined, you may provide the queue name without its suffix when dispatching jobs and Laravel will automatically append the suffix to the queue name when interacting with SQS:

CopyAsk AI```
// Environment should include...
// SQS_SUFFIX="-production"

// Configuration...
'sqs' => [
    'driver' => 'sqs',
    // ...
    'queue' => env('SQS_QUEUE', 'invoices'),
    'suffix' => env('SQS_SUFFIX'),
    // ...
],

// Dispatching...
SendInvoice::dispatch($invoice)->onQueue('invoices');

```

### [​](#disabling-the-queue)Disabling The Queue

If your application does not use queues, you may set the environment’s `queues` option to `false`:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues: false
        build:
            - 'composer install --no-dev'

```

## [​](#queue-concurrency)Queue Concurrency

By default, Vapor will allow your queue to process jobs at max concurrency, which is typically 1,000 concurrent jobs executing at the same time. If you would like to reduce the maximum queue concurrency, you may define the `queue-concurrency` option in the environment’s `vapor.yml` configuration:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-concurrency: 50
        build:
            - 'composer install --no-dev'

```

When using multiple custom queues, the `queue-concurrency` option defines the total maximum concurrency of all queues. For example, if you were to define two custom queues and a `queue-concurrency` of 100 the total maximum concurrency will still be 100.

For the queue Lambda, Vapor defaults to the value of the `cli-concurrency` option if no value was set for `queue-concurrency`. Before you set a limit on `cli-concurrency`, make sure you provide a value for `queue-concurrency` that’s suitable specifically for your queue processing requirements.

### [​](#individual-queue-concurrency)Individual Queue Concurrency

In addition to setting the overall queue concurrency, you may also set the maximum concurrency of each queue. Doing so can be helpful if you wish to prevent certain queues from consuming all available resources:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails: 10
            - invoices: 10

```

In the example above, the concurrency of the `emails` and `invoices` queue is 10, meaning if the queue Lambda function is processing ten jobs concurrently, it will not pick up any more jobs from the queue until jobs are finished and capacity becomes available. This behavior differs from when the total invocations reach the queue function’s overall capacity, where throttling occurs instead.

You may also set the maximum concurrency on some queues but not others. In the example below, the `emails` queue is not allowed more than ten concurrent invocations, whereas it’s possible to invoke the `invoices` queue until the overall capacity is reached:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails: 10
            - invoices

```

It is not possible to set the maximum concurrency of an individual queue higher than the value of the overall currency set by either the `queue-concurrency` option or the general AWS account concurrency limit. In addition, the concurrency value must be an integer between 2 and 1,000.

## [​](#queue-visibility-timeout)Queue Visibility Timeout

By default, if your queued job is not deleted or released within one minute of beginning to process, SQS will retry the job. To configure this “visibility timeout”, you may define the `queue-timeout` option in the environment’s `vapor.yml` configuration. For example, we may set this timeout to five minutes:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-timeout: 300
        build:
            - 'composer install --no-dev'

```

## [​](#queue-memory)Queue Memory

You may use the `queue-memory` option in your environment’s `vapor.yml` configuration to define the memory that should be available to your queue worker Lambda function:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-memory: 1024
        build:
            - 'composer install --no-dev'

```

## [​](#queue-database-connections)Queue Database Connections

By default, database connections do not persist between queued jobs, ensuring that the database does not get overwhelmed with active connections. However, if your database can handle a large number of connections and you want to reduce the overhead involved in creating a database connection on each job, you may define the `queue-database-session-persist` option in your environment’s `vapor.yml` configuration file to instruct Vapor to reuse the same database connection across jobs:

vapor.ymlCopyAsk AI```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-database-session-persist: true
        build:
            - 'composer install --no-dev'

```

## [​](#monitoring-jobs)Monitoring Jobs

You may monitor your queued jobs directly from the Vapor dashboard by navigating to the “Queues” tab of any environment. Here, you can see how your queues perform and also details regarding the number of jobs processed, in flight, and failed jobs over time. You may refine the results by selecting a specific queue and period.

If you have had job failures during the selected period, you may examine them further by clicking on the “View Failed Jobs” link. Doing so will present you with a list of failed jobs along with a snapshot of the failure. You may filter the results further by selecting the specific queue and period or providing a search term. Clicking on an entry presents the full payload and stack trace. From here, you may also retry or delete the job.

In order to view details of failed jobs in the Vapor dashboard, your application must be running Vapor Core >= v2.29.0.

## [​](#failed-jobs)Failed Jobs

Vapor automatically keeps track of failed job attempts using your environment’s configured cache driver. This allows Vapor to ensure the correct number of failed attempts is accessible by your applicati

*[Content truncated for length]*