# Vapor - Resources/Databases

*Source: https://docs.vapor.build/resources/databases*

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
Databases
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
- [Creating Databases](#creating-databases)
- [The Default Database](#the-default-database)
- [Database Types](#database-types)
- [Fixed Size Databases](#fixed-size-databases)
- [Serverless Databases](#serverless-databases)
- [Quick Development Databases](#quick-development-databases)
- [Using Databases](#using-databases)
- [Connecting To Private Databases Locally](#connecting-to-private-databases-locally)
- [Jumpboxes + GUI Tool](#jumpboxes-%2B-gui-tool)
- [Shell Command](#shell-command)
- [Existing Databases](#existing-databases)
- [Database Proxies](#database-proxies)
- [Database Users](#database-users)
- [Scaling Databases](#scaling-databases)
- [Restoring Databases](#restoring-databases)
- [Upgrading Databases](#upgrading-databases)
- [Metrics](#metrics)
- [Alarms](#alarms)
- [Deleting Databases](#deleting-databases)
Resources
# Databases
Managing databases within Laravel Vapor.
## [​](#introduction) Introduction
Vapor allows you to easily create and manage RDS and Aurora Serverless databases directly from the Vapor UI or using the Vapor CLI. **Database backups are automatically performed and you may restore a database to any point in time (down to the second) within the backup retention window.**
## [​](#creating-databases) Creating Databases
You may create databases using the Vapor UI or using the `database` CLI command. When using the CLI command, the command will prompt you for more details about the database such as its desired performance class and maximum storage space.
Copy
Ask AI
```
vapor database my-application-db
```
### [​](#the-default-database) The Default Database
Vapor will automatically create a “vapor” database within each database instance that you create. You are free to create additional databases using the database management tool of your choice.
### [​](#database-types) Database Types
When creating Vapor databases, you may choose from two different types of databases: fixed size and auto-scaling serverless databases.
#### [​](#fixed-size-databases) Fixed Size Databases
Fixed sized databases are RDS MySQL 5.7 / RDS MySQL 8 / Postgres 17 databases that have a fixed amount of RAM and disk space. These databases may be scaled up or down after creation, but not without incurring downtime.
In addition, these databases may be publicly accessible (with a long, random password automatically assigned by Vapor) or private. Private databases may not typically be accessed from the public Internet. To access them from your local machine, you will need to create a Vapor jumpbox.
Vapor will place any application that uses a private database in a network with a [NAT Gateway](/resources/networks#nat-gateways). Later, if you no longer plan to use the database and are using no other private resources from your application, you may remove the NAT Gateway from your network via the network’s management screen.
#### [​](#serverless-databases) Serverless Databases
Serverless databases are auto-scaling Aurora MySQL 5.7 / MySQL 8.0 / Postgres 11 / Postgres 16 databases which do not have a fixed amount of RAM or disk space. Instead, these databases automatically scale based on the needs of your application. At their smallest scale, they are allocated 1GB of RAM.
AWS requires all serverless databases to be private, meaning Vapor will place any application that uses them in a network with a [NAT Gateway](/resources/networks#nat-gateways). If you no longer plan to use a serverless database and are using no other private resources from your application, you may remove the NAT Gateway from your network via the network’s management screen.
### [​](#quick-development-databases) Quick Development Databases
To quickly create a publicly accessible database of the smallest performance class, you may use the `--dev` flag when creating your database. These small, affordable databases are perfect for testing or staging environments:
Copy
Ask AI
```
vapor database my-test-database --dev
```
## [​](#using-databases) Using Databases
To attach a database to an environment, add a `database` key to the environment’s configuration in your `vapor.yml` file and deploy your application. The value of this key should be the name of the database. **When the environment is deployed, Vapor will automatically inject the necessary Laravel environment variables for connecting to the database, allowing your application to start using it immediately:**
vapor.yml
Copy
Ask AI
```
id: 3
name: vapor-app
environments:
    production:
        database: my-application-db
        build:
            - 'composer install --no-dev'
        deploy:
            - 'php artisan migrate --force'
```
### [​](#connecting-to-private-databases-locally) Connecting To Private Databases Locally
If you would like to connect to your private database from your local machine, you can either use a Vapor [jumpbox](/resources/networks#jumpboxes) in combination with a GUI database management tool or the `database:shell` CLI command. Jumpboxes are very small, SSH accessible servers that are placed within your private network.
#### [​](#jumpboxes-+-gui-tool) Jumpboxes + GUI Tool
Once a jumpbox has been created, you may configure your database management tool to connect to your database through the jumpbox SSH connection:
#### [​](#shell-command) Shell Command
After provisioning a jumpbox, you may use the `database:shell` command to quickly access a command line database shell that lets you interact with your database:
Copy
Ask AI
```
vapor database:shell my-application-db
```
## [​](#existing-databases) Existing Databases
If you wish to use an RDS database that was not created by Vapor, you have two options:
1. Exporting and importing the contents of your existing database into a new database created by Vapor. We recommend this approach as it allows you to use your existing data within a database and network managed by Vapor.
2. Connecting your existing database to a Vapor environment.
If your existing database is publicly accessible, make sure your Vapor project is created in the same region as the database. If the existing database is private, you will need to connect your Vapor environment to the VPC your existing database belongs to. You can find instructions on how to do this in our documentation about connecting to [Custom VPCs](/projects/environments#custom-vpcs).
After connecting your existing database, you will need to configure the appropriate environment variables:
Copy
Ask AI
```
DB_HOST=
DB_PORT=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
```
When working with an AWS RDS MySQL Fixed Size databases, an additional environment variable specifying the SSL certificate authority is required:
Copy
Ask AI
```
MYSQL_ATTR_SSL_CA=/var/task/rds-combined-ca-bundle.pem
```
If your database is hosted by [PlanetScale](https://planetscale.com/), the SSL certificate authority is as follows:
Copy
Ask AI
```
MYSQL_ATTR_SSL_CA=/opt/lib/curl/cert.pem
```
## [​](#database-proxies) Database Proxies
Even though your serverless Laravel applications running on Vapor can handle extreme amounts of web traffic, traditional relational databases such as MySQL can become overwhelmed and crash due to connection limit restrictions. To solve this, you may use an RDS proxy to efficiently manage your database connections and allow many more connections than would typically be possible.
The database proxy can be added via the Vapor UI or the `database:proxy` CLI command:
Copy
Ask AI
```
vapor database:proxy my-application-db
```
Next, you may instruct an environment to use the proxy associated with the database using the `database-proxy` configuration option within your `vapor.yml` file:
vapor.yml
Copy
Ask AI
```
id: 3
name: vapor-app
environments:
    production:
        database: my-application-db
        database-proxy: true
        build:
            - 'composer install --no-dev'
        deploy:
            - 'php artisan migrate --force'
```
You can delete the proxy at any time using the Vapor UI or the `database:delete-proxy` CLI command. Before deleting a proxy, make sure none of your applications are using the associated proxy:
Copy
Ask AI
```
vapor database:delete-proxy my-application-db
```
Before considering the usage of database proxies in Vapor, please consult Amazon’s [list of limitations](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/rds-proxy.html#rds-proxy.limitations).
## [​](#database-users) Database Users
When a database is created, Vapor creates a “vapor” master user. You may create additional database users, which will automatically be assigned a secure, random password, using the Vapor UI or the `database:user` CLI command:
Copy
Ask AI
```
vapor database:user my-application-db user-2
```
You may instruct an environment to connect to a database as a given user using the `database-user` configuration option within your `vapor.yml` file:
vapor.yml
Copy
Ask AI
```
id: 3
name: vapor-app
environments:
    production:
        database: my-application-db
        database-user: user-2
        build:
            - 'composer install --no-dev'
        deploy:
            - 'php artisan migrate --force'
```
You may use the `database:password` CLI command to rotate the password of a database. Alternatively, you may leverage users to “rotate” the password of a database without downtime by creating a new user, updating the environment to use that user, deploying the environment, and then deleting the old database user.
## [​](#scaling-databases) Scaling Databases
You may scale fixed size databases via the Vapor UI’s database detail screen or the `database:scale` CLI command. When scaling a fixed size database, the database will be unavailable, and the amount of time it takes to scale the database could vary based on the size of the database. Therefore, you should place your application in maintenance mode before beginning the scaling operation:
Copy
Ask AI
```
vapor database:scale my-application-db
```
## [​](#restoring-databases) Restoring Databases
Vapor database backups are performed automatically and you may restore databases to any point in time within the database backup retention period, which is three days by default. You can change the database backup retention period at any time via the Vapor UI’s database details screen.
Database restoration may be initiated via the Vapor UI or the `database:restore` CLI command:
Copy
Ask AI
```
vapor database:restore current-database-name new-database-name
```
When restoring a database, a new database is created with the same configuration as the previous database. Then, the previous database’s contents are restored to the new database as they existed at the exact point in time you choose. To attach the restored database to an environment, update the value of the `database` key in your `vapor.yml` file and deploy the environment.
Once you are satisfied with the database restoration, you may delete the old database.
## [​](#upgrading-databases) Upgrading Databases
You may upgrade a Vapor managed MySQL database via the Vapor UI or the `database:upgrade` CLI command. When upgrading a database, a new database is created with the same configuration and credentials as the original database:
Copy
Ask AI
```
vapor database:upgrade current-database-name new-database-name
```
Keep in mind that major version upgrades can contain database changes that are not backward-compatible with existing applications. For that reason, we recommend that you thoroughly test the new upgraded database version before attaching it to a production environment. The original database will not be affected by this operation at any point.
Upgrading a database can take several hours for large databases. Therefore, if you plan to attach the new database to a production environment, you may want to place any affected environments in maintenance mode first. Once the newly upgraded database is available, you may start using it by attaching it to an environment.
Of course, once you are satisfied with the database upgrade, you may delete the original database.
## [​](#metrics) Metrics
A variety of database performance metrics are available via the Vapor UI’s database detail screen or using the `database:metrics` CLI command:
Copy
Ask AI
```
vapor database:metrics my-application-db
vapor database:metrics my-application-db 5m
vapor database:metrics my-application-db 30m
vapor database:metrics my-application-db 1h
vapor database:metrics my-application-db 8h
vapor database:metrics my-application-db 1d
vapor database:metrics my-application-db 3d
vapor database:metrics my-application-db 7d
vapor database:metrics my-application-db 1M
```
### [​](#alarms) Alarms
You may configure alarms for all database metrics using the Vapor UI. These alarms will notify you via the notification method of your choice when an alarm’s configured threshold is broken and when an alarm recovers.
## [​](#deleting-databases) Deleting Databases
Databases may be deleted via the Vapor UI or using the `database:delete` CLI command. Once a database has been deleted, it can not be recovered, so take extra caution before deleting a database:
Copy
Ask AI
```
vapor database:delete my-application-db
```
When deleting a database via the UI, you can choose to **preserve the resource on AWS**. Enabling this option only removes the database record in Laravel Vapor; the AWS resource remains intact.
Was this page helpful?
YesNo
[Networks](/resources/networks)[Caches](/resources/caches)
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.