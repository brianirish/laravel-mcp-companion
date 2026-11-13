Source: https://laravel.com/cloud/docs/knowledge-base/migrate-from-queue-clusters.md

# Migrate from queue clusters

Learn how to move your queue workers off a deprecated queue cluster to a managed queue or a worker cluster before queue clusters are retired.

[Queue clusters](https://laravel.com/cloud/docs/workers#queue-clusters-deprecated) are deprecated and are being retired on September 30, 2026. Their replacements are:

* **[Managed queues](https://laravel.com/cloud/docs/queues#managed-queues) (recommended)**, where Laravel Cloud provisions all the infrastructure needed to run a queue (compute, driver, and monitoring) and runs and scales the workers for you
* [Worker clusters](https://laravel.com/cloud/docs/workers#worker-clusters), where you manage `queue:work` yourself on compute that is separate from your web traffic

This guide walks through moving a queue cluster's workload to either option.

> [!WARNING]
>
> Existing queue clusters continue processing jobs until **September 30, 2026**. After that date they stop processing jobs, and anything still dispatched to the queues they served will wait unprocessed until a replacement worker picks it up. How long those jobs survive depends on your queue driver: Redis and database queues keep them indefinitely, while an SQS connection drops them after its message retention period (14 days at most). Migrate production queue clusters well before then.
>
> The first generation of managed queues also retires on September 30, 2026. Those run on SQS, so jobs are retained for a maximum of 14 days before being lost. If you also have a managed queue that needs upgrading, see [Upgrading from earlier managed queues](https://laravel.com/cloud/docs/queues#upgrading-from-earlier-managed-queues).

A queue cluster runs `php artisan queue:work` against your application's own queue driver (`redis`, `database`, your own SQS, or whatever your configured connection points at) and scales its worker count on job latency and queue pressure. Neither replacement is a one-to-one copy of that.

* A managed queue swaps your queue driver for one that Laravel Cloud provisions, then scales workers on the work waiting to be processed, including down to zero.
* A worker cluster keeps your driver and your `queue:work` command exactly as they are, but scales on CPU and memory rather than on queue depth.

Both paths start by creating and deploying the replacement, then verifying that jobs can flow through it. For a managed queue, switch dispatching to the `cloud` connection and let the old connection drain before deleting the queue cluster. A worker cluster keeps the existing connection, so both clusters process its backlog until you delete the queue cluster.

Deleting the queue cluster is the one step you cannot undo. Before you do it, confirm all of the following:

* The replacement has processed a test job on every queue name the cluster served.
* `queue:monitor` reports zero jobs on the old connection, including delayed jobs.
* Failed jobs have been retried or deleted. A retried failed job is re-dispatched onto the connection recorded on it, so a retry after the cutover can land on the old connection with no worker left to run it.
* You have a copy of the queue cluster's settings, since they are discarded with it.

## Before you start

Open the queue cluster on your environment's infrastructure canvas and write down its settings: the connection, the queue name or names it processes (a single queue cluster may serve a comma-separated list such as `emails,notifications`), and the worker options (backoff, sleep, rest, timeout, tries, max-jobs, max-time, and force). You will recreate these on the replacement, and they disappear with the queue cluster when it is deleted.

If you are not sure which queue names your application dispatches to, check the `queue` value of your connection in `config/queue.php`, then search your code for explicit queue names:

```sh theme={null}
grep -rn "onQueue(" app/
```

Here is how each queue cluster setting maps onto the replacements:

| Queue cluster setting | Managed queue | Worker cluster |
| - | - | - |
| Connection (`redis`, `database`, `SQS`, ...) | Replaced by the `cloud` connection Laravel Cloud injects | Copied one-to-one |
| Queue names (`emails,notifications`) | One managed queue per name | Copied one-to-one into one background process |
| backoff, sleep, rest, timeout, tries, force | No worker flags to set. Laravel Cloud manages pickup and visibility. Per-job `$tries` and `$backoff` on the job class still apply | Copied one-to-one into the worker form |
| max-jobs, max-time | Not needed | Custom worker with the full `queue:work` command |
| Worker count, scaled on job latency and queue pressure | Autoscaling range, scaled on the work waiting | Processes times replicas, scaled on CPU and memory |
| Failed jobs | Queues dashboard and API | Your application's failed job driver, as today. Not visible in Laravel Cloud |

Then check the one thing that decides your path: whether your jobs depend on behavior specific to your current driver. Redis-specific queue features, per-job delays longer than 15 minutes, and strict ordering are the usual reasons to keep the driver. Queue clusters and worker clusters are available on the same plans, so plan is not a factor.

| Path | Use when | What changes |
| - | - | - |
| [Managed queue](#move-to-a-managed-queue) | You want Laravel Cloud to run and scale the workers, and your jobs do not depend on driver-specific behavior | Jobs move to the `cloud` connection. Workers scale on the work waiting, and to zero when idle. Failed jobs appear on the Queues dashboard. |
| [Worker cluster](#move-to-a-worker-cluster) | You must keep your own driver (Redis or Valkey, database, your own SQS) or rely on driver-specific queue behavior | Nothing changes in your application. Workers run on a separate cluster that scales on CPU and memory. |

Managed queues are the right destination for most applications, and the one we recommend. Choose a worker cluster when your application must keep its current driver.

## Move to a managed queue

**1. Check the requirements**

Managed queues require Laravel 11.55.0, 12.63.0, 13.19.0, or newer, with `aws/aws-sdk-php` in your `composer.json`. Laravel Cloud reads your `composer.lock` at deploy time, so update the framework, commit the lock file, and deploy before you create the queue. A deployment that creates a managed queue without the SDK fails with a clear error. Symfony applications are supported via [`laravel/laravel-cloud-symfony`](https://github.com/laravel/laravel-cloud-symfony). See [Requirements](https://laravel.com/cloud/docs/queues#requirements).

**2. Create one managed queue per queue name**

Click **Add compute** on the canvas toolbar, then **Managed queue**. Each managed queue handles exactly one Laravel queue name, so a queue cluster processing `emails,notifications` becomes two managed queues, one named `emails` and one named `notifications`. Name each queue exactly as your application dispatches to it. The first managed queue you create becomes the environment's default and receives any job dispatched without a queue name. See [Setting a default queue](https://laravel.com/cloud/docs/queues#setting-a-default-queue).

For [memory](https://laravel.com/cloud/docs/queues#memory-allocation), start close to the queue cluster's compute size (256 MiB covers typical email, webhook, and record-update jobs) and adjust after watching the Memory chart on the Queues dashboard. For the [worker autoscaling range](https://laravel.com/cloud/docs/queues#worker-autoscaling), set the maximum by how much parallelism your database and third-party APIs can absorb, not by the queue cluster's worker count. The two scale differently, so that number does not carry over. Queue and worker allowances vary by plan. See [Managed queues](https://laravel.com/cloud/docs/queues#managed-queues) for the current limits.

**3. Decide what happens to QUEUE\_CONNECTION**

Deploying a managed queue sets `QUEUE_CONNECTION=cloud` for the environment. From that deployment on, every job dispatched without an explicit connection, including the jobs your queue cluster processes today, goes to managed queues. This is usually exactly what you want. If some jobs must stay on your previous driver, set `QUEUE_CONNECTION` back to it as a custom environment variable and dispatch managed-queue jobs on the `cloud` connection explicitly:

```php theme={null}
ProcessPodcast::dispatch($podcast)->onConnection('cloud');
```

The details are in [Queue connection](https://laravel.com/cloud/docs/queues#queue-connection).

**4. Deploy and verify**

Deploy the environment. Laravel Cloud provisions each queue and starts its worker pool. Dispatch a test job to every queue name and watch it process on the **Queues** dashboard under the environment's **Monitoring** tab. Because the default connection switched with this deployment, the queue cluster stops receiving new jobs unless you pinned `QUEUE_CONNECTION` in the previous step or jobs explicitly target the old connection. When neither applies, it works through only the jobs already on the old connection.

**5. Drain and delete the queue cluster**

Leave the queue cluster running until the old connection is empty. Check from the Commands tab, substituting your own connection and queue names:

```sh theme={null}
php artisan queue:monitor redis:emails,redis:notifications
```

The reported size includes delayed and reserved jobs, so zero means genuinely done. Delayed jobs and pending retries are the ones most likely to be left behind, since they sit on the old connection until their time comes.

Then remove the queue cluster from the infrastructure canvas and deploy. Deleting it stops its workers immediately and discards its settings. Any job still on the old connection at that point is never processed.

Until you delete the queue cluster, the move is reversible. To roll back, set `QUEUE_CONNECTION` to your previous driver as a custom environment variable and deploy. New jobs return to the old connection and the queue cluster picks them up again. Jobs already sitting on a managed queue stay there until its workers finish them. Deleting the managed queue discards them. Remove the managed queue from the canvas too if you are not keeping it.

### What behaves differently

A managed queue is not the same queue your cluster was working. Expect these differences, all covered in more depth under [Limitations](https://laravel.com/cloud/docs/queues#limitations):

* Standard queues deliver each job at least once with best-effort ordering. Design jobs to tolerate a second run, or create a [FIFO queue](https://laravel.com/cloud/docs/queues#queue-types) for order-sensitive work.
* Delays are capped at 15 minutes on standard queues, and FIFO queues do not support per-job delays at all. Search your code for `->delay()` and `release()` calls beyond that window before you migrate.
* Jobs on the Flex class should finish within 90 seconds. Longer jobs belong on the [Pro class](https://laravel.com/cloud/docs/queues#compute-classes), which has no fixed limit.
* The `queue:failed`, `queue:retry`, and `queue:clear` Artisan commands are not supported. Instead, you list, retry, and delete failed jobs from the Queues dashboard or the Laravel Cloud API.

For per-job tracing that spans web requests and workers regardless of which queue backs them, [Laravel Nightwatch](https://nightwatch.laravel.com) works the same before and after the move.

## Move to a worker cluster

A worker cluster runs your `queue:work` command verbatim against your own driver, so nothing changes in your application. What you give up is the queue cluster's latency-based scaling, which this path replaces with CPU and memory scaling.

**1. Create the worker cluster**

On the infrastructure canvas, click **Add worker cluster**. Choose a compute size in the same range as the queue cluster's, since it will run the same jobs, and size it independently of the app cluster, because a worker cluster never serves HTTP traffic. See [Worker clusters](https://laravel.com/cloud/docs/workers#worker-clusters).

**2. Add a worker background process**

Click the new worker cluster, then in the **Background processes** section click **New background process**. Copy the queue cluster's connection, queue names, and worker options (backoff, sleep, rest, timeout, tries, and force) into the worker form one-to-one. The queue field accepts the same comma-separated list, so one background process replaces one queue cluster. If your queue cluster relied on max-jobs or max-time, which the worker form does not expose, use the **Custom worker** tab instead and enter the full `php artisan queue:work` command with those flags:

```sh theme={null}
php artisan queue:work redis --queue=emails,notifications --tries=3 --backoff=10 --timeout=90 --max-jobs=1000 --max-time=3600
```

See [Custom background processes](https://laravel.com/cloud/docs/workers#custom-background-processes) for how custom workers behave.

**3. Set processes and scaling**

Each background process runs between 1 and 10 processes, and that number is multiplied by the cluster's replica count. A worker with 4 processes on a cluster running 3 replicas is 12 `queue:work` processes hitting your database at once. Choose a process count that fits comfortably in one replica's memory, then pick a fixed replica count or a minimum and maximum range under [Autoscaling](https://laravel.com/cloud/docs/compute#autoscaling). The maximum replica count depends on your plan.

**4. Decide whether it sleeps**

If the App cluster scales to zero, the worker cluster can either stay awake at all times or sleep alongside the App cluster (Flex compute only, since Pro does not scale to zero). A sleeping worker cluster stops when the App cluster's sleep timeout elapses, even if a job is still running, so keep the worker cluster awake when it runs your queue workers. See [Queue workers and scale to zero](https://laravel.com/cloud/docs/queues#queue-workers-and-scale-to-zero).

**5. Deploy and verify**

Deploy the environment. Both the queue cluster and the worker cluster now consume the same queues from your driver, which is safe because only one worker or the other reserves each job. Watch the worker's output in the [Logs](https://laravel.com/cloud/docs/logs) tab under **Monitoring** and its CPU and memory on the Metrics tab, and confirm jobs complete. Laravel Cloud restarts a background process automatically if it exits, and `queue:restart` is not needed after deployments.

**6. Drain and delete the queue cluster**

Once the worker cluster is keeping up, remove the queue cluster from the canvas and deploy. Because both clusters read the same queue, no jobs are stranded. The worker cluster takes over the whole backlog. Deleting the queue cluster stops its workers immediately and discards its settings, so confirm the worker background process is saved with everything you copied in step 2 before you delete.

Until you delete the queue cluster, rolling back means removing the worker cluster from the canvas and deploying. Jobs the worker cluster was processing at that moment are released back to the queue after your driver's `retry_after` window and picked up by the queue cluster, so nothing is lost, though those jobs run twice.

> [!NOTE]
>
> Worker clusters scale on CPU and memory, never on queue depth. A backlog of cheap jobs that mostly wait on the network may never push CPU high enough to add a replica, so a queue cluster that "just kept up" can fall behind on a worker cluster with the same size. To compensate, set the minimum replica count for your peak rather than your average, or, on the Business and Enterprise plans, use [scheduled autoscaling](https://laravel.com/cloud/docs/compute#scheduled-autoscaling) to raise the minimum ahead of known bursts. If you want scaling driven by the work waiting, that is what [managed queues](#move-to-a-managed-queue) do.

## Using an AI agent

An AI coding agent can help with this migration when it has this guide, your application's repository, and an authenticated [Laravel Cloud CLI](https://laravel.com/cloud/docs/api/cli). Ask the agent to assess the application first, then approve each billable or irreversible step yourself.

```text theme={null}
Read https://laravel.com/cloud/docs/knowledge-base/migrate-from-queue-clusters and assess this
application's migration off its Laravel Cloud queue cluster. Make no changes yet.

Inspect config/queue.php, the environment's QUEUE_CONNECTION, and the queue cluster on the
environment canvas: note its connection, every queue name it processes, and its worker options.
Search the repository for Redis-specific queue features, ->delay() or release() calls
longer than 15 minutes, and jobs that run longer than 90 seconds. Recommend a managed queue or a
worker cluster, explain what changes for the application, and show the complete plan.

After I approve the plan, make any code changes on a branch and show me the diff before committing.
Stop and ask before creating a managed queue or worker cluster (both are billable), before any
deployment that changes QUEUE_CONNECTION, and before deleting the queue cluster. Do not delete
the queue cluster until I confirm the old connection is empty and the replacement is processing
jobs.
```

## Need help?

If you get stuck, or your queue cluster runs something this guide does not cover, contact support from the **Help** portal in your Laravel Cloud dashboard before you delete anything. When you reach out, include the environment, the queue cluster's name, its connection and queue names, and which path you have chosen (managed queue or worker cluster) so the team can help quickly.
