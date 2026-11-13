Source: https://laravel.com/cloud/docs/resources/databases/postgres.md

# Serverless Postgres

Fully managed, autoscaling Serverless Postgres database.

&#x20;Powered by [Neon](https://neon.tech)

## Introduction

Laravel Serverless Postgres provides a fully managed, autoscaling Postgres database for your application. Serverless Postgres database clusters autoscale their compute resources and storage to match demand from your application.

Laravel Serverless Postgres supports a wide range of PostgreSQL extensions, including pgvector for AI and vector similarity search. To learn more about storing and searching vector embeddings with pgvector, see [Neon's pgvector documentation](https://neon.com/docs/extensions/pgvector).


## Creating Serverless Postgres databases

To create and attach a Serverless Postgres database to an environment:

1. Navigate to your environment's infrastructure canvas dashboard.
2. Click "Add database".
3. Select an existing database cluster or create a new one.
   * **To create a new cluster**: Select the "Laravel Serverless Postgres" type at the Postgres version you want, then configure:
     * **Cluster name**: A unique name for your database cluster
     * **Region**: Must match your compute cluster's region
     * **Configuration**: Choose a preset, or customize the [compute unit](#compute-units) range the cluster autoscales between, when it [scales to zero](#scale-to-zero), and how many days of point-in-time recovery backups to retain
4. Select an existing database within the cluster or create a new one.
   * **Database name**: The name of the database within the cluster

You do not configure storage up front. Storage autoscales with the data your application stores.

> [!NOTE]
>
> You can also create Serverless Postgres databases from your organization's **Resources** page, but you will need to attach them to an environment separately.

### Postgres versions

Laravel Serverless Postgres supports Postgres 17 and 18. New database clusters use Postgres 18 by default.

### Available regions

Laravel Serverless Postgres is available in the following regions:

* US East (N. Virginia), `us-east-1`
* US East (Ohio), `us-east-2`
* EU (Frankfurt), `eu-central-1`
* EU (London), `eu-west-2`
* Asia Pacific (Singapore), `ap-southeast-1`
* Asia Pacific (Sydney), `ap-southeast-2`

Your database cluster must be in the same region as the environments that use it.


Once you create the database, you can attach it to any environment in the same region. After you attach a database to an environment, redeploy the environment for the changes to take effect.

Visit the [pricing](https://laravel.com/cloud/docs/pricing#serverless-postgres) docs for information on compute and storage prices.

### Database clusters vs. databases

When you create a new database cluster, Laravel Cloud asks for the name of the cluster and the name of the initial "database" to create within it. Each database cluster may contain up to 500 databases. In web development, these databases are sometimes called "schemas".

If your application needs more than 500 databases, create an additional database cluster and distribute your databases across clusters.

Environments attach to a database, not to a cluster. When you attach one, you first choose the database cluster. Then you select the database within it that you want to make available through the `DB_DATABASE` environment variable.

### Editing and resizing database clusters

To edit your database clusters and adjust their compute and storage settings, navigate to **Organization > Resources > Databases** and click the **...** icon for the database cluster you would like to edit or resize. Then, click **Edit settings**.

Changing the compute unit range restarts your cluster's compute and briefly drops existing connections. Autoscaling within the configured range does not restart the compute.

### Monitoring database cluster metrics

To view your database cluster's metrics, navigate to **Organization > Resources > Databases**, click the database cluster card, and review the **Metrics** section. Use the time range selector to adjust the period shown. See [Database metrics](https://laravel.com/cloud/docs/metrics/databases#serverless-postgres) for what each chart means.

### Deleting database clusters

To delete a database cluster, navigate to **Organization > Resources > Databases** and click the **...** icon for the database cluster you would like to delete. Then, click **Delete** and confirm your action.

## Compute units

When you create a Laravel Serverless Postgres database cluster, you may configure the range of "compute units" your cluster scales between based on demand. Compute units correspond to the following vCPU and RAM configurations:

| Compute units | vCPUs | RAM |
| - | - | - |
| .25 | .25 | 1 GB |
| .5 | .5 | 2 GB |
| 1 | 1 | 4 GB |
| 2 | 2 | 8 GB |
| 4 | 4 | 16 GB |
| 8 | 8 | 32 GB |
| 10 | 10 | 40 GB |
| 16 | 16 | 64 GB |

The maximum compute units available to your cluster depend on your [plan](https://laravel.com/cloud/docs/pricing#serverless-postgres). Clusters may scale up to 1 CU on the Starter plan, 4 CU on the Growth plan, and 10 CU on the Business and Enterprise plans. If you need more compute units, [contact support](https://laravel.com/cloud/docs/support) to [request a higher limit](https://laravel.com/cloud/docs/pricing#raising-plan-limits), up to 16 CU. A cluster at 16 CU runs at a fixed size, so its minimum and maximum are both 16 CU.

## Connection pooler

Laravel Serverless Postgres offers connection pooling through [pgbouncer](https://www.pgbouncer.org/), which supports up to 10,000 concurrent connections to your cluster.

To connect to the pgbouncer endpoint of your database cluster, append `-pooler` to the first segment of the cluster's host name. For example, if your database cluster's host name is `ep-frosty-shadow-a57j6ubb.us-east-2.pg.laravel.cloud`, the corresponding pgbouncer endpoint is `ep-frosty-shadow-a57j6ubb-pooler.us-east-2.pg.laravel.cloud`.

Then, add the new host name as the `DB_HOST` environment variable in your environment's General Settings:

```ini theme={null}
DB_HOST="ep-frosty-shadow-a57j6ubb-pooler.us-east-2.pg.laravel.cloud"
```

## Scale to zero

You may configure Laravel Serverless Postgres database clusters to scale to zero automatically after they receive no queries for a given period, between 60 seconds and 7 days. You may also turn scale to zero off to keep the cluster's compute running at all times. While a Serverless Postgres cluster sleeps, you are not billed for its compute resources. Storage and point-in-time recovery history continue to be billed.

If the cluster receives a query while it is sleeping, it wakes up automatically within a few hundred milliseconds. Any open connection keeps the cluster awake, including connections held by queue workers, scheduled tasks, or monitoring tools.


## Autoscaling compute

Serverless compute can autoscale up and down based on your database cluster's utilization. Set a minimum and maximum range, and pay only for the compute resources you need.

The maximum of the range may be at most 8 CU above the minimum. For example, a range of 2 to 10 CU is allowed, but a range of .25 to 10 CU is not.


## Point-in-time recovery

Laravel Serverless Postgres keeps a continuous history of changes to your database cluster, so you can restore it to any moment within its retention period. You may set the retention period between 0 and 30 days when you create the cluster, or later using the **Settings** button in the cluster's **Backups** section. Setting the retention period to 0 days turns point-in-time recovery off.

Each preset sets a default retention period:

| Preset | Retention |
| - | - |
| Dev | 1 day |
| Prod | 7 days |
| Scale | 14 days |

The retention period applies to the whole database cluster, including every database within it. The history is billed as storage, so a longer retention period costs more. Visit the [pricing](https://laravel.com/cloud/docs/pricing#serverless-postgres) docs for point-in-time recovery storage prices.

### Restoring a database cluster

Restoring creates a new database cluster containing your data as it was at the moment you choose. Your original database cluster is not changed.

1. Navigate to **Organization > Resources > Databases** and click your database cluster.
2. In the **Backups** section, click **Restore point-in-time**.
3. Choose a restore point. The dialog shows the earliest restore point available.
4. Enter a **Backup cluster name** for the new cluster, then click **Restore backup**.

Once the restore finishes, attach a database from the new cluster to your environment and redeploy. You may delete the original cluster once you no longer need it.

## Connecting to database clusters

### From your application

When you attach a database to an environment, Laravel Cloud automatically injects database connection environment variables, including `DB_CONNECTION`, `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, and `DB_DATABASE`. You may view these variables in your environment's General Settings.

### From your local machine

To connect to your database from your local machine using a database management client like [TablePlus](https://tableplus.com/), navigate to **Organization > Resources > Databases**, click your database cluster, and click **View credentials** at the top of the page. To view credentials for a specific database, use its **... > View credentials** menu in the **Databases** section.


The credentials dialog provides the connection details for your database. Use the **Open in database client** button in the **Deeplink** field to open your database in your local machine's default database management client, if you have one installed.

### Postgres SSL connections

Neon, which powers Laravel Serverless Postgres, uses the [public ISRG Root X1 certificate](https://neon.tech/docs/connect/connect-securely#location-of-system-root-certificates) issued by Let's Encrypt. So you can create an SSL connection to your Postgres cluster using the [appropriate CA certificate](https://neon.tech/docs/connect/connect-securely#location-of-system-root-certificates:~:text=etc/security/cacerts-,macOS,-%3A) for your operating system. If you are using macOS, this certificate should already be at `/etc/ssl/cert.pem`.

## Troubleshooting

### Too many connections

```text theme={null}
SQLSTATE[08006] [7] ... FATAL:  sorry, too many clients already
```

Postgres rejects new connections once your cluster reaches its connection limit. This usually happens when many app instances, queue workers, or background processes each hold their own connections at the same time.

To resolve this error, connect through the [connection pooler](#connection-pooler), which supports up to 10,000 concurrent connections. You may also reduce the number of replicas or worker processes connecting to the database. If the error persists, [contact support](https://laravel.com/cloud/docs/support).

### High CPU usage

If queries are slow and your cluster regularly runs at the maximum of its compute unit range, first look for slow or unindexed queries, which are a common cause. If the cluster still needs more compute, [raise the maximum](#editing-and-resizing-database-clusters) of its compute unit range. Changing the range restarts the cluster's compute and briefly drops existing connections, so make the change at a quiet time. A high [**Compute** total](https://laravel.com/cloud/docs/metrics/databases#serverless-postgres) on its own does not mean your cluster needs more compute. [Laravel Nightwatch](https://nightwatch.laravel.com) can show you which queries are slowest and where in your application they run.
