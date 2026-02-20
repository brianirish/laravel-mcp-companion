# Vapor - Resources/Queues

*Source: https://docs.vapor.build/resources/queues*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)
[Laravel Vapor home page](https://vapor.laravel.com)
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)
Search...
Navigation
Resources
Queues
[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)
- [Blog](https://blog.laravel.com)
##### Get Started
- [Introduction](/introduction)
##### Projects
- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)
##### Resources
- [Migrate to Cloud](/resources/migrate-to-cloud)
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
On this page
- [Introduction](#introduction)
- [Custom Queue Names](#custom-queue-names)
- [Queue Names Should Be Unique](#queue-names-should-be-unique)
- [Disabling The Queue](#disabling-the-queue)
- [FIFO Queues](#fifo-queues)
- [Queue Concurrency](#queue-concurrency)
- [Individual Queue Concurrency](#individual-queue-concurrency)
- [Queue Visibility Timeout](#queue-visibility-timeout)
- [Queue Memory](#queue-memory)
- [Queue Database Connections](#queue-database-connections)
- [Monitoring Jobs](#monitoring-jobs)
- [Failed Jobs](#failed-jobs)
- [Queues and Maintenance Mode](#queues-and-maintenance-mode)
- [Laravel Horizon on Vapor](#laravel-horizon-on-vapor)
- [Alternative Solutions](#alternative-solutions)
Resources
# Queues
Using queues with Laravel Vapor.
## [​](#introduction) Introduction
Laravel’s queues are one of the framework’s most powerful features. With Vapor, you can continue writing and dispatching queued jobs exactly as you would in a traditional server-hosted Laravel application. The only difference is that Vapor will automatically scale your queue processing throughput on-demand within seconds:
Copy
Ask AI
```
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast);
```
When using Vapor, your application will use the AWS SQS service, which is already a first-party queue driver within Laravel. Vapor will automatically configure your deployed application to use this queue driver by injecting the proper Laravel environment variables. You do not need to perform any additional configuration.
Currently, serverless applications on AWS may only process a single request (web or queue) for a maximum of 15 minutes. If your queued jobs take longer than 15 minutes, you will need to either chunk your job’s work into smaller pieces or consider another deployment solution for your application. In addition, a queued job may not have a “delay” greater than 15 minutes.
## [​](#custom-queue-names) Custom Queue Names
By default, Vapor will create an SQS queue that has the same name as your project and inject the proper environment variables to make this queue the default queue. If you would like to specify your own custom queue names that Vapor should create instead, you may define a `queues` option in your environment’s `vapor.yml` configuration. The first queue in the list of queues will be considered your “default” queue and will automatically be set as the `SQS_QUEUE` environment variable:
vapor.yml vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails
            - invoices
```
### [​](#queue-names-should-be-unique) Queue Names Should Be Unique
When using custom queue names, it is important to ensure the names are unique between projects and environments. For instance, you can add suffix values such as `-staging` and `-production` to the queue names specified in your application’s `vapor.yml` file:
vapor.yml
Copy
Ask AI
```
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
Copy
Ask AI
```
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
### [​](#disabling-the-queue) Disabling The Queue
If your application does not use queues, you may set the environment’s `queues` option to `false`:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues: false
        build:
            - 'composer install --no-dev'
```
## [​](#fifo-queues) FIFO Queues
AWS SQS FIFO (First-In-First-Out) queues guarantee that messages are processed exactly once and in the exact order they are sent. To use FIFO queues with Vapor, you must first create the FIFO queue directly in the AWS Console. FIFO queue names must end with the `.fifo` suffix, such as `notifications-production.fifo`.
Once you have created the FIFO queue in AWS, you may add it to your environment’s `vapor.yml` configuration file:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - notifications-production.fifo
```
## [​](#queue-concurrency) Queue Concurrency
By default, Vapor will allow your queue to process jobs at max concurrency, which is typically 1,000 concurrent jobs executing at the same time. If you would like to reduce the maximum queue concurrency, you may define the `queue-concurrency` option in the environment’s `vapor.yml` configuration:
vapor.yml
Copy
Ask AI
```
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
### [​](#individual-queue-concurrency) Individual Queue Concurrency
In addition to setting the overall queue concurrency, you may also set the maximum concurrency of each queue. Doing so can be helpful if you wish to prevent certain queues from consuming all available resources:
vapor.yml
Copy
Ask AI
```
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
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queues:
            - emails: 10
            - invoices
```
It is not possible to set the maximum concurrency of an individual queue higher than the value of the overall currency set by either the `queue-concurrency` option or the general AWS account concurrency limit. In addition, the concurrency value must be an integer between 2 and 1,000.
## [​](#queue-visibility-timeout) Queue Visibility Timeout
By default, if your queued job is not deleted or released within one minute of beginning to process, SQS will retry the job. To configure this “visibility timeout”, you may define the `queue-timeout` option in the environment’s `vapor.yml` configuration. For example, we may set this timeout to five minutes:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-timeout: 300
        build:
            - 'composer install --no-dev'
```
## [​](#queue-memory) Queue Memory
You may use the `queue-memory` option in your environment’s `vapor.yml` configuration to define the memory that should be available to your queue worker Lambda function:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-memory: 1024
        build:
            - 'composer install --no-dev'
```
## [​](#queue-database-connections) Queue Database Connections
By default, database connections do not persist between queued jobs, ensuring that the database does not get overwhelmed with active connections. However, if your database can handle a large number of connections and you want to reduce the overhead involved in creating a database connection on each job, you may define the `queue-database-session-persist` option in your environment’s `vapor.yml` configuration file to instruct Vapor to reuse the same database connection across jobs:
vapor.yml
Copy
Ask AI
```
id: 2
name: vapor-laravel-app
environments:
    production:
        queue-database-session-persist: true
        build:
            - 'composer install --no-dev'
```
## [​](#monitoring-jobs) Monitoring Jobs
You may monitor your queued jobs directly from the Vapor dashboard by navigating to the “Queues” tab of any environment. Here, you can see how your queues perform and also details regarding the number of jobs processed, in flight, and failed jobs over time. You may refine the results by selecting a specific queue and period.
If you have had job failures during the selected period, you may examine them further by clicking on the “View Failed Jobs” link. Doing so will present you with a list of failed jobs along with a snapshot of the failure. You may filter the results further by selecting the specific queue and period or providing a search term. Clicking on an entry presents the full payload and stack trace. From here, you may also retry or delete the job.
In order to view details of failed jobs in the Vapor dashboard, your application must be running Vapor Core >= v2.29.0.
## [​](#failed-jobs) Failed Jobs
Vapor automatically keeps track of failed job attempts using your environment’s configured cache driver. This allows Vapor to ensure the correct number of failed attempts is accessible by your application, even if a queued job does not complete due to exceeding the maximum execution time enforced by Lambda (15 minutes) or fails due to an unhandled exception causing the entire container processing your job to fail.
Applications processing a large volume of queued jobs may notice an increase in AWS charges when using the DynamoDB cache driver. In these situations, we recommend utilizing a Redis cache.
## [​](#queues-and-maintenance-mode) Queues and Maintenance Mode
Queue processing is automatically paused when an environment is in [maintenance mode](/projects/environments#queue-processing-during-maintenance-mode). Jobs will remain in the queue and resume processing once maintenance mode is disabled. Unlike traditional Laravel deployments, Vapor does not support forcing queue processing during maintenance mode using the `--force` flag.
## [​](#laravel-horizon-on-vapor) Laravel Horizon on Vapor
Laravel Vapor does not currently support [Laravel Horizon](https://laravel.com/docs/horizon) due to the serverless architecture of AWS Lambda. The long-running processes required by Horizon are incompatible with Vapor’s execution environment.
### [​](#alternative-solutions) Alternative Solutions
For applications that require Laravel Horizon’s powerful queue monitoring and management capabilities, we recommend exploring these alternative Laravel hosting platforms which support Horizon:
- **[Laravel Cloud](https://cloud.laravel.com/docs/queues#custom-background-processes)** - Our fully-managed Laravel application platform.
- **[Laravel Forge](https://forge.laravel.com/docs/sites/queues#laravel-horizon)** - Our VPS server management platform.
Was this page helpful?
YesNo
[Migrate to Cloud](/resources/migrate-to-cloud)[Storage](/resources/storage)
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.