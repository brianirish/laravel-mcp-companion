Source: https://laravel.com/cloud/docs/resources/databases/laravel-mysql.md

# Laravel MySQL

Fully managed MySQL database.

## Introduction

Laravel MySQL provides a fully managed MySQL database for your application. You assign each Laravel MySQL database cluster a compute and storage size, and you can scale it at any time. Laravel Cloud can also [upsize storage automatically](#automatic-upsizing) as your data grows. Flex sizes can [scale to zero](#scale-to-zero) when idle.


## Creating MySQL databases

To create and attach a MySQL database to an environment:

1. Navigate to your environment's infrastructure canvas dashboard
2. Click **Add database**
3. Select an existing database cluster or create a new one:
   * **To create a new cluster**: Select **Laravel MySQL** as your database cluster type and configure:
     * **Cluster name**: A unique name for your database cluster
     * **Instance size**: Choose from available compute options (Flex or Pro sizes)
     * **Storage**: Configure storage from 5GB to 1,000GB
     * **Region**: Must match your compute cluster's region
4. Select an existing database within the cluster or create a new one:
   * **Database name**: The name of the database within the cluster

> [!NOTE]
>
> You can also create MySQL databases from your organization's **Resources** page, but you will need to attach them to an environment separately.


After you create a database, you can attach it to any environment in the same region. When you attach a database to an environment, redeploy the environment for the changes to take effect.

Visit the [pricing](https://laravel.com/cloud/docs/pricing#laravel-mysql) docs for information on compute and storage prices by region.

> [!NOTE]
>
> A database cluster must be in the same region as the environments that attach to its databases.

### Database clusters vs. databases

When you create a new database cluster, Laravel Cloud asks you for a name for the cluster and a name for the initial "database" it creates within the cluster. Each database cluster can hold as many databases as you need. In web development, these databases are sometimes called "schemas".

Environments attach to a database, not to a cluster. When attaching, you first choose the database cluster and then select the database within it that you want to make available through the `DB_DATABASE` environment variable.

### Editing and resizing database clusters

To edit your database clusters and adjust their compute and storage settings, navigate to **Organization > Resources > Databases** and click the **...** icon for the database cluster you would like to edit or resize. Then, click **Edit settings**.

Changing the compute size restarts your database cluster. Expect under a minute of downtime while the cluster restarts. Your data is not affected.

> [!NOTE]
>
> You can increase Laravel MySQL storage only once every 6 hours, and you cannot decrease it.

### Automatic upsizing

Laravel MySQL databases can automatically increase their storage **once they reach 90% of their allocated space**. The database stays online while Laravel Cloud applies the increase, and the additional storage is available immediately.

Each increase grows storage by 50% of the current allocation, rounded to the nearest 5GB, so larger databases receive proportionally more headroom. You can also set a maximum size for each database, and automatic upsizing will not grow a database past that limit. Laravel Cloud upsizes each database at most once every 6 hours.

Laravel Cloud sends a [notification](https://laravel.com/cloud/docs/notifications) when a database reaches 75% of its allocated storage, and another at 90%, when the upsize takes place. Each notification states the size the database will grow to and what the change adds to your monthly cost.

Automatic upsizing is enabled by default on all newly created databases.

### Monitoring database cluster metrics

To view metrics such as CPU, memory, and storage for your database cluster, navigate to **Organization > Resources > Databases**, click the database cluster card, and review the **Metrics** section. Use the time range selector to adjust the period shown. See [Database metrics](https://laravel.com/cloud/docs/metrics/databases#laravel-mysql) for what each chart means.

### Deleting database clusters

To delete a database cluster, navigate to **Organization > Resources > Databases** and click the **...** icon for the database cluster you would like to delete. Then, click **Delete** and confirm your action.

## Scale to zero

Laravel MySQL Flex sizes can scale to zero. When your database cluster is idle, it sleeps, and you are not billed for compute. The cluster's storage stays online the entire time it sleeps, so your data is always preserved. Storage is billed as usual while the cluster sleeps.

A database cluster goes to sleep when it has received no connections for its configured idle timeout. You may set the idle timeout between 1 minute and 1 hour. The next connection wakes the cluster automatically. Every Laravel MySQL database cluster sits behind a proxy layer. The proxy holds the incoming connection while compute resumes and forwards it once the cluster is awake, so your application sees a slightly slower first query instead of a connection error. Waking typically adds a few hundred milliseconds to that first query. Clusters that use more RAM take longer to wake. Scheduled backups and manual snapshots briefly wake a sleeping cluster and let it return to sleep once complete.

Scale to zero is available on the Flex sizes in all regions. New database clusters use the current generation of Flex and Pro sizes, and previous-generation sizes are no longer offered. Existing clusters continue to run on their current size and pricing unchanged. Pro sizes are always-on and do not scale to zero.

Pairing a Flex database cluster that scales to zero with [application compute](https://laravel.com/cloud/docs/compute#scale-to-zero) and a [Laravel Valkey cache](https://laravel.com/cloud/docs/resources/caches/valkey#scale-to-zero) that scale to zero helps minimize costs on development environments and side projects.

## Importing MySQL data

After enabling your [MySQL Public Endpoint](#mysql-public-endpoints), you can use any standard database tools to import your SQL data. To reduce memory usage, we recommend generating database dumps with the `--skip-extended-insert` option, especially for smaller Laravel MySQL instances.

### Recommended MySQL import tools

We recommend the following tool for database imports, particularly for larger datasets:

* [mydumper](https://github.com/mydumper/mydumper)

mydumper runs imports in parallel, so it is much faster than the traditional `mysqldump` and `mysql` commands on large databases. You can also use GUI-based tools like TablePlus for imports. However, smaller Laravel MySQL instances may run into memory limits with these tools.

## Database sizing and performance

### Choosing the right cluster size

Several factors influence the right database cluster size for your workload: connection requirements, queue workload, backup retention needs, and planned database migrations.

### Connection limits

The amount of RAM your database cluster has determines how many simultaneous connections it can support:

| Server memory | MySQL connection limit |
| - | - |
| 512 MB | 51 |
| 1 GB | 102 |
| 2 GB | 204 |
| 4 GB | 408 |
| 8 GB | 816 |
| 16 GB | 1,632 |
| 32 GB | 3,264 |

> [!NOTE]
>
> Laravel Cloud places a proxy layer in front of every database cluster. The proxy multiplexes connections for read-only queries, allowing up to 10,000 connections in some conditions. The proxy cannot multiplex writes and transactions, so those count against your MySQL connection limit. Plan your cluster size based on your expected mix of reads and writes.

### Queue workload considerations

If your application runs queue workers with a low `--sleep` interval (such as `--sleep=1` or lower), expect high CPU usage. That's acceptable for development environments, but in production, we recommend a minimum of 2 vCPUs, possibly more for high-throughput jobs.

### Backup retention planning

Backups are essential, especially for production databases. If you're working with a disposable or development database, it's fine to set the retention period to 0 days.

For anything else, we recommend at least 2 days of backup retention for basic protection and recovery.

### Database migrations and imports

Planning to transfer or import a database? You may need to temporarily scale up your database cluster's CPU and memory to handle large or fast MySQL imports.

> [!NOTE]
>
> * **CPU and memory** can scale up and down at any time, with under a minute of downtime while the cluster restarts
> * **Storage size** can only increase, never decrease, so plan for long-term needs before the import

For smoother imports, consider using optimized dump commands:

```bash theme={null}
mysqldump -u USER -h HOSTNAME -p --single-transaction --set-gtid-purged=OFF --databases my_database > backup_my_database.sql
```

## Database backups

Laravel MySQL database clusters support automated and manual backups.

### Backup configuration

To configure backups for your MySQL database cluster:

1. Navigate to **Organization > Resources > Databases**.
2. Click your Laravel MySQL database cluster.
3. In the **Backups** section, click **Settings**.
4. Enable or disable the **Backups** toggle. When enabled, configure **Backup retention** to choose how long to keep automatic daily backups.
5. Click **Update** to save your settings.

### Backup retention period

New Laravel MySQL clusters use the backup retention from the preset you choose:

| Preset | Automatic backup retention |
| - | - |
| Dev | 1 day |
| Prod | 7 days |
| Scale | 14 days |

These presets enable automatic backups. If you customize the settings, your selected retention applies instead. Check the cluster's **Backups > Settings** for its current retention and to change it or disable automatic backups.

When automatic backups are enabled, you can configure the retention period from 1 to 30 days. Automatic backups run during a daily 3-hour backup window between 3AM and 6AM EDT.

### Manual backups

To create a manual backup, click **New backup** in your database cluster's **Backups** section, provide a name and an optional description, and click **Create backup**. You can create manual backups at any time, regardless of your automatic backup settings.

### Restoring from backups

Backups restore to a new database cluster rather than overwriting the existing cluster. In your cluster's **Backups** section, find the backup you want to restore, click its **...** menu, and select **Restore**.

Enter a name for the new database cluster and click **Restore backup** to confirm.

After the restore finishes, you have two database clusters: the original and a new cluster restored from the backup you selected.

At this point, you can either detach the original database from your environment and attach the corresponding database from the restored cluster, or [connect to each database](#connecting-to-database-clusters) and selectively restore any missing information you might have. When you no longer need one of the database clusters, you may delete it.

#### How to download a backup

Laravel Cloud stores backups as internal snapshots and does not expose them as raw `mysqldump` files. To download a copy of your data:

1. Restore the desired backup into a new database cluster so your production cluster remains untouched.
2. Enable the restored cluster's public endpoint and copy the credentials (see [Connecting to database clusters](#connecting-to-database-clusters)).
3. Use your preferred tool, such as TablePlus, `mysqldump`, or [mydumper](https://github.com/mydumper/mydumper), to export or download the data to your machine.

Once you've downloaded the data, you can disable the public endpoint again and delete the temporary cluster if it is no longer needed.

### Backup pricing

Laravel Cloud bills Laravel MySQL backup storage separately from database storage, at the same rate as storage: `$0.10/GB-mo` in US regions and `$0.12/GB-mo` in other regions.

Laravel Cloud bills backups for the gigabyte-months they use. Each day, Laravel Cloud sums the size of all manual and automated snapshots, then averages those daily totals across the billing period.

## Connecting to database clusters

### From your application

When you attach a database to an environment, Laravel Cloud automatically injects database connection environment variables, including `DB_HOST`, `DB_USERNAME`, `DB_PASSWORD`, and `DB_DATABASE`. You may view these variables in your environment's General Settings.

### From your local machine

To connect to your database from your local machine using a database management client like [TablePlus](https://tableplus.com/), navigate to **Organization > Resources > Databases**, click your database cluster, and click **View credentials** at the top of the page. To view credentials for a specific database, use its **... > View credentials** menu in the **Databases** section.


The credentials dialog provides the connection details for your database. Use the **Open in database client** button in the **Deeplink** field to open your database in your local machine's default database management client, if you have one installed.

### MySQL public endpoints

Before connecting to a MySQL database cluster, you must enable its public endpoint. From your organization's **Resources** page, navigate to the **Databases** tab and click the **...** icon for the MySQL database cluster you would like to connect to. Then, click **Edit settings** and enable the **Enable public endpoint** toggle.

After you enable the public endpoint, open the MySQL database cluster page and click **View credentials**. When you are finished interacting with your database from your local machine, you may disable the public endpoint.

### Laravel MySQL SSL connections

Public endpoints present a certificate issued by a public certificate authority (Let's Encrypt), so your client can verify the server's identity using your operating system's built-in CA bundle. You do not need to download a certificate.

Traffic is encrypted between your client and Laravel Cloud's proxy layer. The proxy's connection to the underlying database runs within Laravel Cloud's private network and is not separately encrypted.

**Laravel applications**

Laravel applications that connect over SSL should add the following [environment variable](https://laravel.com/cloud/docs/environments#environment-variables), which Laravel passes to PDO as `MYSQL_ATTR_SSL_CA` (`Pdo\Mysql::ATTR_SSL_CA` on PHP 8.4 and later):

```ini theme={null}
MYSQL_ATTR_SSL_CA="/etc/ssl/certs/ca-certificates.crt"
```

**MySQL command-line client**

To verify the server's identity from the `mysql` client, connect with `VERIFY_IDENTITY` mode and point `--ssl-ca` at your system CA bundle:

```bash theme={null}
mysql --host=<host> --port=<port> --user=<username> --password \
  --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/ssl/certs/ca-certificates.crt
```

> [!NOTE]
>
> The `mysql` client refuses the `VERIFY_CA` and `VERIFY_IDENTITY` modes unless you also pass `--ssl-ca`. The bundle path in the previous example is correct for most Linux distributions. On macOS, use `/etc/ssl/cert.pem`.

## Database users

Laravel Cloud creates every database cluster with a default user and injects its credentials into your environment as the `DB_USERNAME` and `DB_PASSWORD` [environment variables](https://laravel.com/cloud/docs/environments#environment-variables). You may also create additional users with their own credentials and access level. For example, you might create a read-only user for a reporting tool or a scoped user for a background service. Laravel MySQL clusters and [RDS MySQL and RDS Postgres](https://laravel.com/cloud/docs/private-cloud/rds) clusters all support database users.

### Creating a database user

To create a new database user:

1. Navigate to **Organization > Resources > Databases** and click the database cluster.
2. In the **Database users** section, click **New user**.
3. Configure the user:
   * **Username**: A unique username for the user
   * **Permission**: Choose **Read-only** or **Read-write**
   * **Access** (optional): Restrict the user to specific databases within the cluster
4. Click **Create database user**.

You provide the username, and Laravel Cloud generates a secure password. Laravel Cloud displays the password after it creates the user. Copy the password and store it somewhere safe, because it grants access to your database.

> [!NOTE]
>
> The default user injected into your environment cannot be edited or deleted.

### Read-only vs. read-write access

* **Read-only** users may query data but cannot insert, update, or delete records or modify the schema. Read-only access suits reporting dashboards and teammates who only need to inspect data.
* **Read-write** users have full read and write access to the schemas they are scoped to.

### Rotating credentials

You may rotate the credentials of a Laravel MySQL database cluster's default user, for example after a teammate leaves your organization or if you suspect the password has leaked. Rotation causes no downtime, because your environments keep using the previous credentials until you redeploy them. Database users you create keep their credentials.

The database cluster must be running with no other operation in progress, and you need permission to update it and to deploy its environments. To rotate its credentials:

1. Navigate to **Organization > Resources > Databases**.
2. Click the **...** menu for the database cluster and select **Rotate credentials**, then confirm.
3. Once the new credentials are ready, click **Deploy** on the pending deployments notification to redeploy your connected environments. You may also click **Redeploy environments** on the database cluster card, or deploy each environment yourself.

A rotation moves through the following stages:

1. **Rotating.** Cloud creates a new default user with the same access as the previous one. If this fails, the cluster keeps its existing credentials.
2. **Awaiting deployment.** The new user becomes the cluster's default user. New deployments receive its credentials in the `DB_USERNAME` and `DB_PASSWORD` [environment variables](https://laravel.com/cloud/docs/environments#environment-variables), and **View credentials** shows them. The database cluster card lists the environments that still need redeploying.
3. **Finalizing.** Once every connected environment has deployed successfully, Cloud deletes the previous user.

> [!WARNING]
>
> Once Cloud deletes the previous user, anything else using those credentials, such as a database client on your local machine, can no longer connect. Update it with the new credentials from **View credentials**.

## Database upgrades

Laravel MySQL database clusters may periodically require an upgrade to stay secure and compatible with our latest features. To check if your cluster requires an upgrade, go to **Organization > Resources > Databases** and click the **...** menu for your database cluster. If an **Upgrade Database** option is present, an upgrade is required.

To upgrade your database cluster:

1. Click the **...** menu
2. Select **Upgrade Database**
3. Confirm the upgrade

The upgrade causes several minutes of downtime, depending on the size of your data.

### Maintenance window

For critical security fixes, Laravel Cloud may need to apply updates to your database cluster during its maintenance window.


Updates may take up to a minute, during which **your database cluster will be briefly unavailable**. We recommend placing your 30-minute maintenance window during a low-traffic period.

To set your maintenance window:

1. Click the **...** menu
2. Select **Edit settings**
3. Select **Set time** in your maintenance window dropdown
4. Select a day and a timeslot (UTC)

By default, your Laravel MySQL database cluster's maintenance window starts at 2AM in the location of your database.

## Binary logs and storage usage

Your database's storage figure covers more than your tables. MySQL writes a binary log, an ordered record of every change made to your data, and those files live on the same volume as the data itself. Laravel Cloud reports the two together as a single storage number.

Binary logs are what make replication and point-in-time recovery possible, so they are not optional. They do mean that a database can grow toward its storage limit even when the amount of data you are storing has not changed. A write-heavy workload produces binary log volume out of proportion to the rows that end up stored. A queue table churning through jobs or a repeated bulk import can leave the storage figure well above the size of your tables.

**How binary logs are cleaned up**

You do not need to manage this. Two mechanisms keep binary logs from filling your volume:

* **Scheduled rotation.** Laravel Cloud keeps binary logs for roughly 8 days, then removes them automatically.
* **Emergency cleanup.** Laravel Cloud checks disk usage every minute. If a volume passes 90% used, Laravel Cloud immediately clears all but the most recent binary log.

Because of the second mechanism, a write-heavy workload with little stored data will not run out of space from binary logs alone.

**Why your storage figure can move on its own**

Cleanup runs without prompting you, so the reported figure can fall as well as rise:

* A scheduled rotation or an emergency cleanup releases space, and usage drops.
* A busy period pushes usage back up as new logs accumulate.

A drop of this kind is normal and does not mean data was lost. It is also why a database sitting near a storage [notification](https://laravel.com/cloud/docs/notifications) threshold can cross it and fall back below more than once.

**Working out what's using your storage**

Laravel Cloud does not report binary log usage separately, so the storage figure is the total of both. To see how much of it is your data, query your table and index sizes:

```sql theme={null}
SELECT table_name,
       ROUND((data_length + index_length) / 1024 / 1024, 1) AS mb
FROM information_schema.tables
WHERE table_schema = DATABASE()
ORDER BY data_length + index_length DESC;
```

If that total sits well below your reported storage usage, the difference is largely binary logs, and it will come back down at the next rotation or cleanup.

**If binary logs are consistently taking up space**

Sustained binary log volume is a signal about write patterns rather than a fault. A few patterns commonly account for it:

* High-churn tables such as queues, sessions, caches, and logs kept in the same database as your application data.
* Batch jobs that rewrite large numbers of rows on a schedule.
* Bulk imports run repeatedly rather than once.

If the workload is what you want and you need more headroom, [automatic upsizing](#automatic-upsizing) grows the volume for you before the database runs out of space.

## Troubleshooting

### Common error messages

#### Too many connections error

```
SQLSTATE[HY000]: General error: 1040 Too many connections
```

**Solution**: Increase your database RAM, decrease the number of replicas your app has, or contact support. You may have exceeded the connection limit, or a query may have locked the database so that it needs a restart.

#### Connection timeout error

```
SQLSTATE[HY000]: General error: 9001 Max connect timeout reached while reaching hostgroup...
```

**Solutions**:

* If your database [scales to zero](#scale-to-zero), a query against a sleeping database may take slightly longer while the database wakes. The delay is expected, adds only a few hundred milliseconds, and should not trigger this error.
* If this message appears constantly, confirm you have plenty of disk space and allow 15 minutes for the database to restart after changing disk space limits.
* Check notifications to be alerted before reaching these limits.
* If this message appears occasionally, you may need to increase your database RAM, because the database likely hit an out-of-memory error and restarted during a query or connection burst.
* Contact support if issues persist.

### Performance monitoring

Monitor your database performance in the **Metrics** section of your database cluster page. Watch for:

* **High CPU usage**: May indicate inefficient queries or insufficient compute resources
* **High memory usage**: Could lead to connection issues or query failures
* **Low disk space**: Can cause database failures and connection timeouts

> [!NOTE]
>
> Enable notifications in your organization settings to receive alerts before reaching resource limits.
