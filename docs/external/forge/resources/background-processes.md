# Forge - Resources/Background-Processes

*Source: https://forge.laravel.com/docs/resources/background-processes*

---

[Laravel Forge home page](https://forge.laravel.com)
Search...
⌘KAsk AI
- [Get started](https://forge.laravel.com)
- [Get started](https://forge.laravel.com)
Search...
Navigation
Resources
Background Processes
[Documentation](/docs/introduction)[Knowledge Base](/docs/knowledge-base/servers)[API Reference](/docs/api-reference/introduction)
- [Blog](https://blog.laravel.com)
- [Status](https://status.on-forge.com)
##### Get Started
- [Introduction](/docs/introduction)
- [Laravel Forge CLI](/docs/cli)
- [Laravel Forge SDK](/docs/sdk)
##### Basics
- [Organizations](/docs/organizations)
- [Teams](/docs/teams)
- [Server Providers](/docs/server-providers)
- [Storage Providers](/docs/storage-providers)
- [Source Control](/docs/source-control)
- [SSH Keys](/docs/ssh)
- [Recipes](/docs/recipes)
- [API](/docs/api)
##### Servers
- [Managing Servers](/docs/servers/the-basics)
- [Server Types](/docs/servers/types)
- [Laravel VPS](/docs/servers/laravel-vps)
- [PHP](/docs/servers/php)
- [Load Balancing](/docs/servers/load-balancing)
- [Nginx Templates](/docs/servers/nginx-templates)
- [Security](/docs/servers/security)
- [Monitoring](/docs/servers/monitoring)
- [Real-Time Metrics](/docs/servers/real-time-metrics)
##### Sites
- [Managing Sites](/docs/sites/the-basics)
- [Domains](/docs/sites/domains)
- [Deployments](/docs/sites/deployments)
- [Environment Variables](/docs/sites/environment-variables)
- [Commands](/docs/sites/commands)
- [Queues](/docs/sites/queues)
- [Network](/docs/sites/network)
- [Isolation](/docs/sites/user-isolation)
- [Laravel](/docs/sites/laravel)
- [Logs](/docs/sites/logs)
##### Resources
- [Databases](/docs/resources/databases)
- [Database Backups](/docs/resources/database-backups)
- [Caches](/docs/resources/caches)
- [Background Processes](/docs/resources/background-processes)
- [Scheduler](/docs/resources/scheduler)
- [Network](/docs/resources/network)
- [Packages](/docs/resources/packages)
##### Integrations
- [Envoyer](/docs/integrations/envoyer)
- [Sentry](/docs/integrations/sentry)
- [Aikido](/docs/integrations/aikido)
- [OpenClaw](/docs/integrations/openclaw)
##### Other
- [Support](/docs/support)
- [Changelog](/docs/changelog)
- [Abuse](/docs/abuse)
On this page
- [Introduction](#introduction)
- [Configuring background processes](#configuring-background-processes)
- [Creating Laravel queue workers](#creating-laravel-queue-workers)
- [Manually restarting background processes](#manually-restarting-background-processes)
- [Log files](#log-files)
Resources
# Background Processes
Copy page
Learn how to configure and manage background processes on your Laravel Forge server.
Copy page
## [​](#introduction) Introduction
Laravel Forge uses [Supervisor](http://supervisord.org) to manage background processes, ensuring your long-running scripts stay active. This is particularly useful for maintaining daemons like [ReactPHP](http://reactphp.org/) applications. When a process stops unexpectedly, Supervisor automatically restarts it to maintain continuous operation.
## [​](#configuring-background-processes) Configuring background processes
Background processes can be configured on both a server and site level.
To create a background process, navigate to the “Processes” tab on the server or site. Then, click the “Add background process” button. After providing the required fields, click the “Create background process” button.
When creating a new background process, you’ll need to configure the following settings:
- **Name:** Provide a descriptive name for the background process to help identify it.
- **Command:** Specify the command that the background process should execute. For example: `php artisan reverb:start`.
- **Working Directory:** Set the working directory for your command. This field is optional and can be left empty.
- **User:** Choose the operating system user to run the command. The `forge` user is used by default.
- **Processes:** Define how many instances of the process should run simultaneously.
- **Start Seconds:** Set the minimum runtime (in seconds) required to consider the process startup successful.
- **Stop Seconds:** Specify how long Supervisor waits for a graceful shutdown before forcing termination.
- **Stop Signal:** Choose the signal used to terminate the program during shutdown.
### [​](#creating-laravel-queue-workers) Creating Laravel queue workers
For sites using Laravel and Statamic, creating a new background process will display two tabs: **Queue worker** or **Custom**.
The Queue worker tab is designed to make configuring Laravel queue workers easier. Instead of manually writing the `php artisan queue:work` command, you can use the form to configure the following options:
- **PHP Version:** The PHP version to use for the queue worker.
- **Queue Connection:** The name of the queue connection (e.g., `redis`, `database`, `sqs`) in your `config/queue.php` file.
- **Number of Processes:** How many instances of the queue worker should run simultaneously.
- **Queue:** Which queue(s) the worker should process.
- **Backoff:** The number of seconds to wait before retrying a failed job.
- **Sleep:** The number of seconds the worker should sleep when no jobs are available.
- **Rest:** The number of seconds to rest between jobs.
- **Timeout:** The maximum number of seconds a job is allowed to run.
- **Tries:** The maximum number of times a job may be attempted.
- **Memory:** The memory limit (in megabytes) for the queue worker.
- **Environment:** The application environment.
- **Force:** Force the worker to run even in maintenance mode.
Laravel Forge will generate a preview of the queue worker command based on your selections, showing you the exact command that will be configured as a background process. This preview updates in real-time as you adjust the settings, allowing you to verify the configuration before creating the background process.
### [​](#manually-restarting-background-processes) Manually restarting background processes
You can manually restart any background process using the command `sudo -S supervisorctl restart daemon-{id}:*`, where `{id}` represents the background process’s unique identifier. For instance, to restart a background process with ID `65654`, you would run `sudo -S supervisorctl restart daemon-65654:*`.
This command can also be integrated into your deployment scripts to restart background processes automatically during deployments.
## [​](#log-files) Log files
Laravel Forge automatically configures each background process to maintain its own log file within the `/home/forge/.forge/` directory. Log files follow the naming convention `daemon-*.log`.
When using Laravel Forge’s user isolation features, daemon log files are located in the `.forge` directory within `/home/{username}`, where `{username}` corresponds to the user assigned to run the process.
Was this page helpful?
YesNo
[Caches](/docs/resources/caches)[Scheduler](/docs/resources/scheduler)
⌘I
Assistant
Responses are generated using AI and may contain mistakes.