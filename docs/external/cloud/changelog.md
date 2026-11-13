Source: https://laravel.com/cloud/docs/changelog.md

# Changelog

See the latest Laravel Cloud updates, improvements, and platform changes.

**October 27, 2026**

## Cloud Scheduler

Non-Laravel applications can now run commands on a schedule with Cloud Scheduler, whether they're written in Python, Node.js, Go, Ruby, or any other language Laravel Cloud supports. Add a command to your App cluster or a worker cluster, choose a schedule, and deploy. Cloud runs the command for you, so you don't need to install cron or run a scheduling process inside your application.

Presets cover hourly, daily, weekly, and monthly schedules. When you create a command with a preset, Cloud picks a random start time and keeps it for every run. Random start times keep commands across the platform from all starting at the top of the hour. To run a command at an exact time, select **Custom** and enter a cron expression. Cloud validates the expression and describes it in plain language as you type.

Each scheduled command runs on one instance, no matter how many replicas your cluster has. Cloud wakes clusters that scale to zero, so your commands still run on time. Each run's output, exit code, and start and finish times appear in the Logs dashboard. When a command fails, Cloud notifies you by email or Slack.

[Read the scheduled tasks documentation](https://laravel.com/cloud/docs/scheduled-tasks) to learn more.

## Domain health checks

Laravel Cloud now monitors your custom domains after they connect. If a domain stops pointing to Cloud, or its SSL certificate fails to renew, Cloud flags the domain on your environment's canvas and in your environment's **Network settings**. Cloud then notifies your team so you can fix the problem before visitors notice.

Cloud checks every connected domain once an hour to confirm that its A or CNAME record still points to Cloud. If a record goes missing or changes, Cloud marks the domain as **Disconnected**, and the alert shows the record the domain should use. If a certificate fails to renew, Cloud marks the domain with a **Certificate issue** and shows the reason, such as a CAA record that blocks issuance. Once you fix the cause, click **Retry renewal**.

Private Cloud customers with a [dedicated edge network](https://laravel.com/cloud/docs/private-cloud/edge-network) also get nameserver monitoring. Cloud checks that your domain's nameservers still point to Cloud, and alerts you if someone removes or changes them at your registrar.

Domain health checks are available on every plan. Cloud sends alerts by email and Slack under the new **Domain alerts** notification category, which you can configure in your [notification settings](https://laravel.com/cloud/docs/notifications).

[Read the domain health documentation](https://laravel.com/cloud/docs/domains#domain-health) to learn more.

**October 13, 2026**

## Resend integration


Laravel Cloud now integrates directly with Resend, so you can set up transactional email in the dashboard. Connect a Resend account to your organization once and Laravel Cloud imports the sending domains you already have.

When you add a sending domain, Cloud shows you the exact DNS records to create and tracks each record's status as Resend verifies it. You can configure sending regions and sending domains from within Laravel Cloud. When you attach email to an environment, Laravel Cloud creates a new Resend API key for that environment, or reuses an existing key, and injects the environment variables for you.

[Read the email documentation](https://laravel.com/cloud/docs/resources/email) to learn more.

**September 30, 2026**

## MySQL storage auto-upsize


Laravel MySQL databases can now automatically upsize their own storage. When a database starts running low on disk, Laravel Cloud increases its allocated storage automatically, while the database stays online and keeps serving queries.

When a database reaches 90% of its allocated storage, Laravel Cloud increases its disk size by 50%, rounded to the nearest 5GB. You can set a maximum size that automatic upsizing will not grow past. Storage can grow but cannot shrink, and Laravel Cloud upsizes each database at most once every 6 hours.

Automatic upsizing is on by default, and you can turn it off per database at any time.

[Read the Laravel MySQL documentation](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) to learn more.

**September 28, 2026**

## Log drains


Enterprise plans can now forward your application logs to an Amazon S3 bucket you own in real time. Log drains are ideal for long-term retention, compliance, or integration with your existing observability stack.

[Learn more about log drains](https://laravel.com/cloud/docs/services/log-drains/overview).

**September 25, 2026**

## Preview environment improvements


Laravel Cloud's Deployments page now shows a row for every open pull request with a preview, including its branch, its latest commit, and a link to open it. Each preview carries its own settings for password protection, automatic deletion, and environment variables.

Every preview gets fresh resources instead of pointing at production. It sleeps between reviews on scale-to-zero Flex sizes, and Laravel Cloud deletes it automatically when its pull request merges or closes. Preview environments are now included on all plans.

[Read the preview environments documentation](https://laravel.com/cloud/docs/preview-environments) to learn more.

**September 23, 2026**

## Statamic static caching

Laravel Cloud now supports Statamic's full-measure static caching. When your application requires `statamic/cms`, Cloud detects it at deploy time and configures NGINX to serve the pre-rendered HTML files in `public/static` directly. Cached pages never reach PHP. Form submissions and live previews continue to route to your application as usual.

To get started, set `STATAMIC_STATIC_CACHING_STRATEGY=full` in your environment variables and deploy. You don't need to write any custom NGINX configuration, and applications that don't use Statamic are unaffected.

The static cache lives on each instance's local filesystem, and each deployment clears it. Statamic invalidates the cache only on the instance that handled a content change, so additional replicas would keep serving stale pages. When you use full-measure static caching, run your App cluster on a single instance by setting its [autoscaling strategy](https://laravel.com/cloud/docs/compute#autoscaling) to **None**. To scale vertically, choose a larger instance size instead of adding replicas.

[Read the Statamic static caching documentation](https://statamic.dev/static-caching) to learn more.

## Self-hosted GitLab


Private Cloud customers can now deploy applications from a GitLab instance their organization runs itself. Register Laravel Cloud as an OAuth application in your GitLab instance and enter the credentials under **Settings > Integrations > Self-hosted GitLab**. Cloud then reads your repositories and receives push events just as it does for GitLab.com. Self-hosted GitLab requires GitLab v16.4 or later.

[Read the self-hosted GitLab documentation](https://laravel.com/cloud/docs/private-cloud/self-hosted-gitlab) to learn more.

**September 10, 2026**

## Request metrics


See your busiest pages, spot errors, and find slow responses directly in Laravel Cloud. The new Requests tab shows request counts, response codes, and timings by page, with filters for domain and time range.

Open the Requests tab under Monitoring to explore your application's activity. You don't need any packages or code changes.

**September 3, 2026**

## Managed database users


Laravel Cloud now lets you create and manage additional users for your database clusters, so you no longer need to share the default credentials with every service and teammate. Choose read-only or read-write access, then limit each user to the databases they need.

Cloud generates a secure password for each user and keeps their credentials available in the database cluster panel. You can update a user's access at any time or delete the user when you no longer need it. Managed database users are available for Laravel MySQL, RDS MySQL, and RDS Postgres clusters.

[Read the database users documentation](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#database-users) to learn more.

**August 27, 2026**

## Pre-deploy package checks


Laravel Cloud now detects missing or outdated packages before deployment. When you enable Laravel Octane, Inertia SSR, or Laravel Nightwatch, or attach a storage bucket, Cloud displays the required installation command next to the setting. Managed queues and scheduled tasks are covered too, including the framework versions each one requires.

The notices follow your repository rather than your last deployment. Laravel Cloud now reads your `composer.lock` on every push, so once you install the package and push, the notice clears without waiting for a deploy to confirm it.

Notices appear only for features you've enabled, and they do not prevent you from saving changes or starting a deployment.

[Read the deployments documentation](https://laravel.com/cloud/docs/deployments) to learn more.

## Scoped API tokens

You can now scope organization API tokens to specific permissions and restrict them to an application or individual environments, instead of granting full org-level access. Only organization admins can create tokens, so engineers and agents get exactly the permissions their automation needs and nothing more.

Existing tokens continue to work with no changes required. To change what a token can do, create a new one with the scope you need and revoke the old one.

[Read the scoped API documentation](https://laravel.com/cloud/docs/api/authentication#scoping-api-tokens) to learn more.

**August 6, 2026**

## Managed queues improvements


We rebuilt managed queues from the ground up. Workers now wake in under a second when jobs arrive on an idle queue, down from around fifteen seconds. Creating a queue now asks only for a name, a queue type, a memory size, and an autoscaling range. The polling interval, visibility timeout, and shutdown timeout settings are gone. Laravel Cloud delivers every job to your workers itself, so it measures pickup, visibility, and scaling instead of asking you to tune them.

The new runtime also brings two new capabilities. FIFO queues deliver jobs in the exact order you dispatched them, which makes them a good fit for order-sensitive workloads like payment processing and ledger updates. Queue compute also now comes in two classes. Flex scales to zero and is priced exactly like today's queue compute. Pro stays always on, with no cold starts, for steady throughput and jobs that run up to an hour.

Existing queues keep running unchanged. To upgrade one, update to a supported framework version (Laravel 11.55.0, 12.63.0, or 13.19.0 and newer), pick a new Flex or Pro size in the queue's settings, and deploy.

[Read the queues documentation](https://laravel.com/cloud/docs/queues) to learn more.

**July 24, 2026**

## Stage, review, ship


Save changes, review them, then deploy when you're confident. Laravel Cloud now stages every configuration change with a persistent banner that shows exactly what's waiting, wherever you are in your environment. Expand it for a full diff and ship the whole batch in one action.

Oh, and the canvas is no longer locked while resources provision. Keep working. Laravel Cloud will catch up.

**July 20, 2026**

## MySQL scale to zero


Laravel MySQL Flex databases can now scale to zero. When your database is idle, it sleeps, and you aren't billed for compute. Storage stays online the whole time, so your data is always preserved. The next connection wakes the database automatically. Every cluster sits behind a proxy layer that holds the connection while compute resumes and forwards it once the database is awake. Waking adds only a few hundred milliseconds to the first query.

Pair a Flex database that scales to zero with [application compute](https://laravel.com/cloud/docs/compute#scale-to-zero) and a [Laravel Valkey cache](https://laravel.com/cloud/docs/resources/caches/valkey#scale-to-zero) that scale to zero to minimize costs on your development environments, side projects, and even production environments that have periods of inactivity.

Scale to Zero is available on the Flex sizes in all regions. Existing databases continue to run on their current size and pricing unchanged.

[Read the Laravel MySQL documentation](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#scale-to-zero) to learn more.

**July 16, 2026**

## Secrets Manager


Laravel Cloud now includes a Secrets Manager for defining encrypted secrets at the organization level and linking them to one or more environments. Instead of copying shared values like third-party API tokens into each environment individually, you can define them once, link them where they're needed, and rotate them in a single place. Cloud injects secrets as environment variables during deployment.

Secret values are write once, read never. Your browser encrypts each value before sending it, so plaintext never reaches Cloud's servers. The dashboard never displays a saved value. Cloud decrypts secrets only when it creates a deployment, and AWS Key Management Service (KMS) protects the organization key material.

[Read the secrets documentation](https://laravel.com/cloud/docs/secrets) to learn more.

**July 8, 2026**

## First-class monorepo support


Laravel Cloud now automatically detects monorepos when you create a new application. If your repository contains multiple projects, Cloud presents the top-level directories so you can choose the one to deploy. Cloud then scopes all build and runtime operations, including commands and background processes, to that directory.

If your monorepo holds more than one application, such as a frontend and a backend, create a separate Cloud application for each one and attach the same repository. Each application deploys from its own root directory and scales independently, with its own environment variables, instances, and domains.

[Read the monorepo documentation](https://laravel.com/cloud/docs/monorepos) to learn more.

**June 29, 2026**

## Symfony support


You can now deploy Symfony applications on Laravel Cloud. Cloud reads your `composer.json`, detects `symfony/framework-bundle`, and configures the runtime automatically using `php bin/console`. You don't need to change your application's code.

Doctrine (Postgres and MySQL), Symfony Messenger with managed queues support, WebSockets through the Pusher protocol, Laravel Valkey caching, R2 object storage, and preview environments per pull request all work out of the box. When you connect a database resource, Cloud injects `DATABASE_URL` automatically. Symfony 7.4 LTS and 8.x are supported on PHP 8.2 through 8.5.

[Read the Symfony quickstart guide](https://laravel.com/cloud/docs/quickstart#symfony) to get started.

**June 29, 2026**

## Expanded outbound IP addresses


We've provisioned additional outbound IP addresses in several regions to improve networking capacity and reliability. Over the coming weeks, Laravel Cloud will begin routing outbound requests through these new addresses.

You may allowlist the IPs that Laravel Cloud uses for outbound requests, for example to permit access to a third-party API, database, or firewall. If you do, update your rules to include the new addresses before they go live to avoid disruptions. The current, complete list is always available in our documentation and through the API.

[Read the networking documentation](https://laravel.com/cloud/docs/network#ip-addresses) to learn more.

**June 22, 2026**

## Improved notifications


Email notifications are now personal to each team member, so you can choose which events you care about across your organizations, applications, and environments. You configure Slack notifications at the organization level with a default channel and per-application overrides. You can route different apps to different channels without overwhelming your team with noise.

[Read the notifications documentation](https://laravel.com/cloud/docs/notifications) to learn more.

**June 11, 2026**

## Deploy to Laravel Cloud with Stripe Projects


Laravel Cloud is now available through Stripe Projects, a tool that lets you discover, provision, and pay for developer tools directly from the Stripe CLI.

Provision, or let your agents provision, your Laravel Cloud infrastructure using a single command.

Read our [Stripe Projects docs](https://laravel.com/cloud/docs/api/stripe-projects) to get started.

**June 10, 2026**

## ElastiCache


Provision fully managed AWS ElastiCache caches, available in both Valkey and Redis OSS, directly from Laravel Cloud. ElastiCache delivers high-throughput, low-latency performance backed by AWS infrastructure, with automatic failover, multi-AZ deployments, and in-place version upgrades. ElastiCache is available with Private Cloud.

Choose from a range of node sizes and deployment options, from a single-AZ instance for development to multi-AZ clusters with automatic failover for production workloads.

[Read the ElastiCache documentation](https://laravel.com/cloud/docs/private-cloud/elasticache) to learn more.

**June 1, 2026**

## Scale to zero and new pricing


Laravel Cloud now offers a new generation of Flex compute that can scale to zero. It sleeps when your application is idle and wakes in under 500 milliseconds when a request arrives. Your scheduled tasks continue running and jobs on managed queues keep processing while the environment sleeps. Flex compute, Serverless Postgres, and Laravel Valkey can sleep and wake together so you only pay for what you use.

Alongside Scale to Zero, we've refreshed our plans:

* The new **Starter plan** is \$5/mo with \$5 in monthly usage credits and a free first month.
* Every paid plan now includes \$5 in monthly usage credits.
* **Spending limits** let you set a hard monthly cap so your bill never exceeds your budget.
* **Custom domains** are now counted per organization, with additional domains billed at \$0.25 per domain per month.

[Read the compute documentation](https://laravel.com/cloud/docs/compute#scale-to-zero) to learn more.

**May 26, 2026**

## Managed queues


Managed queues are now generally available. Laravel Cloud provisions the queue, runs workers on dedicated instances, and scales them automatically based on the work waiting to be processed. Workers scale to zero when your queue is idle, so you only pay for compute when jobs are running.

Each managed queue is independent, with its own pool of workers, instance size, and scaling configuration. Background work stays isolated from your web traffic, and you get a built-in failed jobs dashboard with retry tooling.

[Read the queues documentation](https://laravel.com/cloud/docs/queues#managed-queues) to learn more.

**May 13, 2026**

## HTTP basic authentication


Protect staging, preview, private demo, and other environments with HTTP basic authentication. When you enable it, visitors must enter the username `admin` and the environment password before traffic reaches your application.

HTTP basic authentication is available on the Growth plan or higher. It can help prevent unauthorized visitors or automated bots from waking hibernating environments.

[Read the environment documentation](https://laravel.com/cloud/docs/environments#http-basic-authentication) to learn more.

**May 7, 2026**

## Roles & permissions


Give every member of your organization the right level of access with role-based access control. Basic RBAC is available on every plan with a set of predefined team roles designed to match how most teams already work.

On the Business and Enterprise plans, Advanced RBAC unlocks custom roles, application and environment-level access, and the new Restricted role. The Restricted role is perfect for contractors, auditors, or teammates who should see only a specific slice of your organization.

[Read the roles and permissions documentation](https://laravel.com/cloud/docs/rbac) to learn more.

**April 30, 2026**

## Dedicated Edge Network enhancements


Catch the traffic costing you money or causing problems. See the top IPs and paths at your edge, turn them into firewall or cache rules in one click, and watch each rule take effect in real time.

**April 22, 2026**

## Mobile Cloud is here


The Laravel Cloud experience is now fine-tuned for any screen. Move between environments, manage resources, watch deployments, and ship releases from wherever you are. It's perfect for on-the-go deployments and AI workflows.

**March 26, 2026**

## Redesigned Usage page


We redesigned the Usage page so it's easier to understand what your organization is spending and where that spend comes from.

You can now review a cleaner summary of your current spend, bandwidth usage, credits, and billing alerts, then drill down into resource costs and application-level compute usage by environment. The new layout also makes it easier to spot the clusters, resources, and add-ons contributing to your bill during the selected billing period.

[Read the usage documentation](https://laravel.com/cloud/docs/usage) to learn more.

**March 23, 2026**

## Scheduled autoscaling


Scheduled autoscaling is now available on the Business and Enterprise plans. You can create one-time or recurring schedules that temporarily adjust your minimum and maximum replicas, as well as your CPU and memory thresholds, before predictable traffic arrives.

Schedules help you prepare for launches, promotions, business hours, and other recurring traffic patterns without manually changing your baseline scaling settings. Each schedule uses its own timezone, and Laravel Cloud automatically applies the one that matches the current time.

[Read the compute documentation](https://laravel.com/cloud/docs/compute#scheduled-autoscaling) to learn how to configure scheduled autoscaling.

**March 18, 2026**

## Sign in with GitHub


GitHub SSO is here. Sign in or create your account with GitHub, and since we already use that connection for source control, your repos come with you. Go from sign-up to first deploy faster than ever.

**March 10, 2026**

## Try Laravel Cloud for free


Start shipping on Laravel Cloud with \$5 in free usage credits, automatically applied to your account the moment you sign up. Deploy your first applications, spin up databases, caches, and more, on us.

Want a completely free trial? Our Starter plan has no subscription fee. Your \$5 in credits is all you need to get started, no questions asked.

Credits are valid for 14 days. When they run out or expire, you're billed for what you use.

[Sign up](https://laravel.com/sign-up) or [read the docs](https://laravel.com/cloud/docs/free-trial) to learn more.

## Same Git account, multiple organizations and users


Laravel Cloud now stores Git connections per user instead of per organization. You can connect the same Git account to multiple Cloud users and organizations at once.

* **One user, many orgs.** Connect once and use your Git account across every organization you belong to.
* **One Git account, many Cloud users.** Connect the same Git provider account, such as your personal GitHub, to multiple Cloud user accounts. Each Cloud account and org stays separate, but they can all use the same Git source.

To use the new model, reconnect from your organization's Git provider settings. [Learn more about source control connections](https://laravel.com/cloud/docs/source-control).

**March 2, 2026**

## Laravel Cloud API: programmable infra for teams and AI agents


You can now manage your entire Laravel Cloud infrastructure programmatically with the Laravel Cloud API. The API covers deployments, environments, databases, caches, object storage, and scaling. Use it for CI/CD integration, infrastructure-as-code workflows, and AI agents that provision resources or query status on your behalf. [Explore the API documentation](https://laravel.com/cloud/docs/api/introduction).

## New CLI: deploy and manage from your terminal


You can now run and script Laravel Cloud operations directly from the command line. The CLI provides smart defaults for quick setup and full control when you need it. [Learn more in the CLI documentation](https://laravel.com/cloud/docs/api/cli).

## MySQL 8.0 end of life: upgrade to 8.4


If your application runs on Laravel MySQL 8.0, note that our MySQL 8.0 database version will reach end of life in April 2026 and will no longer receive security updates.

To keep your database and application safe, we recommend upgrading to MySQL 8.4.

MySQL 8.4 is the current long-term support release. It continues to receive security updates and performance improvements for your workloads on Laravel Cloud.

Before you upgrade, create a backup of your database.

For complete upgrade instructions, [visit the documentation](https://laravel.com/cloud/docs/knowledge-base/upgrade-mysql-to-84). For additional context and walkthroughs, you can also watch this [Laravel Cloud Office Hours](https://www.youtube.com/live/S0DQmy8sBkY?si=JRmOqIHOSaRBAjpY) session.

To avoid thinking about this in the future, we also recommend [setting up a maintenance window](https://laravel.com/cloud/docs/resources/databases/laravel-mysql#maintenance-window) for your database. With a maintenance window, Laravel Cloud applies updates automatically at a time that works for you, so you can concentrate on shipping.

**Improvements**

* Sign in with Google SSO
* Redesigned navigation
* RDS replicas, Postgres, and MySQL now available for Private Cloud
* File explorer for bucket storage

**January 29, 2026**

## Cloud API expanded: databases, caches, buckets, and WebSockets


The Laravel Cloud API now supports additional resources, including database clusters, caches, object storage buckets (and keys), and WebSocket clusters and applications. You can now automate provisioning for more of your infrastructure, integrate Cloud into your CI/CD pipelines, and build custom tooling around your deployment workflows.

Check out the [API documentation](https://laravel.com/cloud/docs/api/introduction) to explore the available endpoints and learn how to get started.

## Valkey now generally available


Laravel Valkey is now generally available on Laravel Cloud.

With Valkey, you can provision fully managed, scalable cache instances for your Laravel applications with the same reliability and performance you expect from Cloud's managed services. Because it is fully compatible with Redis protocols and commands, existing Redis users can switch to it directly.

Because we built Laravel Valkey in-house, we could tune it to outperform standard Redis-compatible offerings:

* Our benchmarks show Laravel Valkey delivers 20-50% lower latency than similar competitor offerings.
* We've included a generous request size limit that is 5x to 20x larger than industry standards for the same price point as other providers.

Get started by creating a new Valkey cache in Laravel Cloud. [Read the docs to learn more](https://laravel.com/cloud/docs/resources/caches/valkey).

## Private Cloud now available


[Laravel Private Cloud](https://laravel.com/enterprise) offers fully isolated, enterprise-grade infrastructure operated by Laravel. Get your own dedicated Kubernetes cluster in a private AWS account with dedicated compute, private networking, static outbound IPs, and optional managed RDS databases.

Here's what you get:

* **Dedicated infrastructure.** Isolated compute and networking with predictable performance.
* **Private networking.** Connect to AWS services privately with reduced latency.
* **Dedicated outbound IPs.** Customer-specific IPs for allowlisting and compliance.
* **High availability.** Three nodes across availability zones with automatic failover.
* **Built for compliance.** SOC 2 Type II certified, designed for HIPAA and PCI-DSS.
* **Fully managed.** Laravel handles operations so you can focus on your product.

Private Cloud is ideal for regulated industries and organizations with strict security or performance requirements. It includes the Business plan, 24/7 Artisan Support, and dedicated infrastructure. Pricing is custom and typically cost-effective for \$2,000+/month workloads.

[Check out the docs](https://laravel.com/cloud/docs/private-cloud) or [contact sales](https://laravel.com/enterprise) to learn more.

**Improvements (4)**

* Start and stop environments now in the Cloud API
* Cloud API supports token expiration
* Accessibility updates
* Domain verification improvements

**Fixes (1)**

* Fixed validation error on billing alerts

**January 9, 2026**

## New: billing alerts


Stay in control of your cloud spending with billing alerts. You can now configure notifications that alert you when you cross spending thresholds, so you can manage your budget proactively and avoid unexpected costs.

Learn more in the [Billing Alerts documentation](https://laravel.com/cloud/docs/billing-alerts).

**Improvements (7)**

* Added cache details and metrics pages, with more consistent canvas actions
* Renamed "filesystems" to "buckets" across the UI and API, and added a bucket details page
* Valkey now supports configuring an eviction policy
* Improved Valkey auto-upgrade
* Improved billing alerts
* Multiple small deployment and UI polish improvements
* Require password to delete resources

**Fixes (2)**

* Fixed WebSocket application "Edit settings" button
* Fixed cache upgrade notification labeling

**December 1, 2025**

## Laravel Reverb-powered WebSocket is now generally available


We're excited to announce that [WebSockets for Laravel Cloud](https://laravel.com/cloud/docs/resources/websockets) is now generally available! WebSockets on Cloud run on Reverb, Laravel's first-party WebSocket server, and bring fast, scalable real-time communication to your applications.

To deploy Reverb on Laravel Cloud, enable it in your project settings. Cloud handles the rest, including a handy dashboard where you can keep an eye on your WebSocket connections.

With Reverb, you can build real-time features like live notifications, chat systems, and collaborative tools the Laravel way. It works with Laravel's broadcasting system and is a drop-in replacement for services like Pusher and Ably.

Check out the [Reverb documentation](https://laravel.com/cloud/docs/resources/websockets) to get started.

## Valkey now available in developer preview


Laravel Valkey is now available in developer preview on Laravel Cloud! Valkey is a high-performance, open source key-value data store and an alternative to Redis, with the same performance and feature set you rely on.

As a community-driven fork of Redis, Valkey is fully compatible with Redis commands and protocols, so it's a drop-in replacement for your existing Redis workloads. Use it for caching, session management, queues, and real-time analytics.

During the developer preview, you can try Valkey on Laravel Cloud for yourself. We're committed to supporting open source infrastructure, and Valkey is part of that commitment.

[Enable Laravel Valkey in your project settings](https://laravel.com/sign-in) and let us know what you think, or [check out the docs](https://laravel.com/cloud/docs/resources/caches/valkey) to learn more.

## Introducing the Canada region


We're pleased to announce that Laravel Cloud is now available in the Canada region (ca-central)! Located in Central Canada, this new region brings Laravel Cloud closer to our Canadian users and anyone serving customers in Canada.

With the Canada region, you can deploy your Laravel applications with reduced latency for Canadian users and meet data residency requirements.

To deploy to Canada, select the ca-central region when creating a new project or provisioning new servers. All of Laravel Cloud's features are available in this new region, including automatic scaling, zero-downtime deployments, and managed databases.

[See all the regions available in Laravel Cloud](https://laravel.com/cloud/docs/applications#regions).

## gRPC extension now available


By popular demand, Laravel Cloud now supports the gRPC PHP extension, our most requested addition. With the gRPC extension, your Laravel applications can talk directly to services like Firebase, Google Cloud APIs, and other gRPC-based backends with high performance and low latency.

To enable gRPC in your app, redeploy it. You don't need any additional configuration. Check out all [available PHP extensions on Cloud](https://laravel.com/cloud/docs/environments#php-extensions).

**Improvements (7)**

* Business plan now available with increased domain limits
* PHP 8.5 available (pdo_sqlsrv support coming soon)
* Serverless Postgres lower pricing
* Redesigned build and deploy
* Node 24 available
* 25GB Laravel Redis cache option
* Improved cache usage page

**Fixes (5)**

* Fixed domains missing on Cloudflare not being marked as failed
* Fixed cache errors on Redis by Upstash
* Fixed dropdowns not closing properly
* Fixed logs scroll bug
* Fixed MySQL storage sync

**October 31, 2025**

## Laravel Cloud API is now early access


The Laravel Cloud API is now available in early access. It gives you programmatic control over your Laravel Cloud infrastructure. Use it to automate deployments, manage environments, configure domains, and more from your own applications or scripts.

With the early access release, you can manage key aspects of your Laravel Cloud setup, including applications, environments, deployments, domains, commands, instances, and background processes. [Contact our support team for EA](https://laravel.com/cloud/docs/support).

## New region: hello, Ireland


We're excited to announce that Laravel Cloud is now available in the Europe (Ireland) region. This expansion brings improved performance and reduced latency for applications serving users across Europe and the UK.

Ireland joins our growing global infrastructure, so you have more flexibility to deploy your Laravel applications closer to your European audience. This location provides excellent connectivity throughout the region.

To deploy to Ireland, select "Europe (Ireland)" when creating a new environment or server. You can migrate existing applications to the new region. [See all regions](https://laravel.com/cloud/docs/applications#regions)

## Laravel Reverb-powered WebSocket clusters


We're excited to announce that [WebSockets for Laravel Cloud](https://laravel.com/cloud/docs/resources/websockets), powered by Laravel Reverb, is now available in developer preview.

WebSockets are our first managed WebSocket offering. You can add Reverb's real-time capabilities to your Laravel application without managing your own infrastructure.

All it takes is a few clicks in Cloud: select the desired number of concurrent connections, attach the resource to your environment, and you're off. [Learn more](https://laravel.com/cloud/docs/resources/websockets)

## Advanced rate limit rules now available for Business plan


Customers on our [Business plan](https://laravel.com/pricing) now have access to advanced rate-limiting rules within their Web Application Firewall (WAF). These rules give you more granular control over rate limiting. You can customize triggers, actions, and bot protection settings to better secure your applications.

With advanced rate limiting, you can define thresholds for request rates, set custom responses for rate-limited requests, and fine-tune bot protection mechanisms to distinguish between legitimate traffic and malicious bots. With that control, you can protect your applications from abuse and keep the experience smooth for genuine users. [Contact our support team to upgrade](https://laravel.com/cloud/docs/support)

## Set up email notifications in Laravel Cloud


You can now configure email notifications in Laravel Cloud to stay informed about important events across your organization and applications. To open your notification preferences, click **Account** under your profile and go to **Notifications**.

Email notifications are available for a wide range of events, including organization changes, team member updates, API token activity, application and environment management, resource alerts, deployment status, and payment notifications.

By default, you'll receive notifications for resource alerts, failed deployments, and failed payments. You can change which notifications you receive by toggling your preferences on or off at any time. [Manage email notification preferences](https://laravel.com/profile/notifications)

**Improvements (4)**

* Improved loading speed of source control repository selection
* Laravel Valkey cache improvements
* Updated pricing calculator
* Add cache credentials to canvas

**Fixes (3)**

* Fixed Slack channel names in notifications
* UI fix for queue configurators
* Fixed redirect on logout

**October 7, 2025**

## New region: welcome, Virginia


We're excited to announce that Laravel Cloud is now available in the US East (Virginia) region! This expansion means reduced latency and improved performance for applications deployed in the eastern United States.

Virginia joins our growing list of regions, giving you more options to deploy your Laravel applications closer to your users. This location offers excellent connectivity across the eastern seaboard.

To deploy to Virginia, select "US East (Virginia)" when creating a new environment or server. You can migrate existing applications to the new region.

[See all regions](https://laravel.com/cloud/docs/applications#regions)

## Laravel Valkey is now early access


Laravel Valkey is our new managed Redis offering. It gives you a high-performance, fully managed key-value database out of the box, in several sizes so you can choose the right fit for your application.

Laravel Valkey is available in early access. To request access, [contact our support team](https://laravel.com/cloud/docs/support).

## Coming soon to Laravel Cloud

The Laravel Cloud team has a number of features launching this fall. Keep an eye out for Reverb, the Cloud API, a new region in Ireland (eu-west-1), and an Advanced Web Application Firewall.

**Improvements (4)**

* Updated pricing for serverless Postgres
* App performance improvements
* [Laravel Cloud IPs now available in docs](https://laravel.com/cloud/docs/network#ip-addresses)
* App UI improvements: links in deployments, automation autofill

**Fixes (2)**

* Slack channel renames
* Typos in environment network settings and Bitbucket error message

**September 4, 2025**

## New pricing


We've updated Laravel Cloud's pricing plans. Starting on August 13, the Starter (formerly Sandbox), Growth (formerly Production), and Business plans offer smarter usage-based billing and richer defaults. Starter now includes custom domains, and Growth and Business include Pro-class compute. Bandwidth now scales with compute usage and is shared across environments, so billing is more transparent and better aligned with actual value.

[Learn more about the new pricing](https://blog.laravel.com/laravel-cloud-more-features-smarter-pricing)

## Smart autoscaling with queue clusters

> [!WARNING]
>
> Queue clusters are deprecated. See [Managed queues](https://laravel.com/cloud/docs/queues#managed-queues).


Laravel Cloud now supports a third cluster type (in addition to [App and Worker clusters](https://laravel.com/cloud/docs/compute)) built specifically for queue workloads. Queue clusters are available for testing in developer preview. They fully manage and autoscale Laravel queue workers. They track CPU, memory, job throughput, and backlog in real time to determine how many workers and replicas your application needs.

Autoscaling is latency-driven. When queue wait time exceeds your threshold, the cluster adds capacity automatically. Once latency improves, the cluster scales back to reduce cost. You no longer have to guess at sizing queue workers manually, and the cluster balances performance and savings for you.

[Read the docs](https://laravel.com/cloud/docs/queues)

## Laravel Cloud is now SOC2 compliant


SOC 2 Type 2 is a compliance framework created by the American Institute of Certified Public Accountants (AICPA) that evaluates how organizations secure and protect customer data. The framework consists of five Trust Services Categories (TSCs) with specific criteria for assessing an organization's controls and service commitments.

Laravel Cloud has achieved SOC 2 Type 2 attestation for Security, Confidentiality, and Availability.

More information is available at [trust.laravel.com](http://trust.laravel.com/).

## New region: welcome, Sydney!


We're thrilled to announce that Laravel Cloud is now available in the Sydney (ap-southeast-2) region, so we can better serve customers in Australia and the broader Asia-Pacific area. This new region offers lower latency and improved performance for applications serving users in this part of the world.

To deploy to Sydney, select "Asia Pacific (Sydney)" when creating a new app. Existing customers can keep using their current regions. New projects that target Australian and APAC users can use the new region.

[Learn more](https://laravel.com/cloud/docs/applications#regions)

**Improvements (4)**

* Enabled Slack notifications in private channels
* Delete MySQL scheduled snapshots
* Warnings when deleting environments with attached resources
* Adds 6-hour option to logs

**Fixes (2)**

* Slack channel pagination
* Disable database upgrade button during upgrade

**August 7, 2025**

## MySQL is production ready


You can now provision production-ready MySQL instances with compute ranging from 1 CPU/512 MB RAM up to 8 CPU/32 GB RAM, and storage tiers from 5 GB to 1 TB. Automated daily backups are included. You can configure retention up to 30 days on standard plans, and Enterprise plans offer extended retention.

[Read the docs](https://laravel.com/cloud/docs/resources/databases/laravel-mysql)

## Automated preview environments


Preview environments are now available on [Growth, Business, and Enterprise plans](https://laravel.com/pricing). For every pull request, Laravel Cloud automatically spins up a fully isolated production-like environment. You can mirror your live app using either shared or dedicated databases, configure filters to limit previews by branch or PR, and run custom deploy steps such as migrations or seeders.

You can enable auto-cleanup to delete environments when PRs close or merge, so you only pay for active environments. Preview environments help you catch bugs early and collaborate across teams.

[Read the docs](https://laravel.com/cloud/docs/preview-environments)

## Ship faster with the new starter kits


You can now deploy production-ready Laravel applications in under five minutes using the new official [Laravel Starter Kits](https://laravel.com/starter-kits) for Laravel, Livewire, React, and Vue. Select a stack, choose a region, and customize the repository name and visibility. Laravel Cloud handles repository creation, deployment configuration, and infrastructure setup.

All templates come directly from Laravel's [official GitHub](https://github.com/laravel/laravel). You don't need an existing repository, so you can launch demos, prototypes, or new apps without any setup.

Learn more about the [Laravel Starter Kits](https://youtu.be/y2FfKwcK_iU)

**Improvements (4)**

* Improved repo searching when creating new apps
* Added 6-hour period option for metrics viewing
* Improved MySQL charts
* Better validation running commands during deployments

**Fixes (3)**

* Fix 404s in app for hibernation and page reloads
* Log fixes
* Responsive layout fixes

**July 1, 2025**

## One-click Nightwatch integration


You can now [enable Laravel Nightwatch monitoring](https://laravel.com/cloud/docs/environments#nightwatch-integration) in your Cloud environment canvas with a single click. This new integration runs Nightwatch across all your App and Worker clusters and automatically injects the correct `.env` settings so you can get up and running (or edit your sampling threshold) faster.

[Start monitoring with Nightwatch](https://nightwatch.laravel.com/sign-up)

## Under Attack Mode


We've improved DDoS protection with an optional Under Attack Mode you can enable during periods of unusual traffic. Laravel Cloud already detects and mitigates DDoS attacks automatically. Under Attack Mode adds another layer of protection when you want to protect your app proactively.

When Under Attack Mode is active, Laravel Cloud restricts access to your app and shows visitors a JavaScript challenge before they can reach it. Under Attack Mode expires automatically after 24 hours so it doesn't stay on by accident. To enable it, go to your environment, click Network, and then click Web Application Firewall settings.

[Learn how to set up Under Attack Mode](https://laravel.com/cloud/docs/network#under-attack-mode)

## Improved metrics and charts


We've updated our metrics to offer a more detailed view of resource usage. We refined the CPU and memory charts to highlight trends and spikes, so you can make better decisions about scaling and optimization. For example, memory charts now display total cache storage usage instead of average cache usage. If you have one or more replicas, you now see each replica's memory usage instead of the average.

[Check your app's performance](https://laravel.com/sign-in)

## MySQL metrics land as GA nears

You can now view real-time CPU, memory, and storage metrics for your MySQL databases. Go to your environment, click Resources, and then click the Cluster card to see all metrics. These metrics give you a fuller picture of database performance. They're one of several steps we're taking as we move closer to MySQL's general availability.

[Check your MySQL database performance](https://laravel.com/sign-in)

**Improvements (5)**

* New 500gb cache type
* Added notifications to command palette
* Archive MySQL databases
* Improved Slack notifications adding MySQL and Cache alerts
* Improved speed on environments page

**Fixes (2)**

* Cache and Database dialog minor fixes
* Fix HTTP timeout validation message

**June 3, 2025**

## Visualize replica count

You can now view a replica count chart in your environment's Metrics tab that shows exactly when autoscaling occurs in your Laravel Cloud applications. The step chart shows how each of your App and Worker clusters scales from one to multiple replicas. You can also see when your application scaled to zero and stopped incurring compute usage costs, either because you stopped it manually or because it hibernated automatically. Automatic hibernation requires Hibernation to be toggled on. The chart gives you clearer performance and billing insights for each of your Cloud environments.


[View your replica metrics](https://laravel.com/to/org/applications)

## More flexible caching

You can now configure Laravel Cloud's Redis-compatible key-value stores to scale up automatically when they reach usage limits. Hard limits could lead to downtime and require manual intervention. Now caches can upsize with zero downtime as they approach monthly data transfer or usage thresholds, such as simultaneous connections, commands per second, record size, and request size. To opt in to auto-upsizing, toggle on the **Automatically Upgrade** option of your new or existing Laravel Cloud caches.


[Learn more about Laravel Cloud caches](https://laravel.com/cloud/docs/resources/caches/valkey#automatic-upsizing)

## Slack alerts

[Slack notifications](https://laravel.com/cloud/docs/notifications) now include a new **Resource Alerts** category for critical runtime issues. You'll receive real-time alerts when CPU, RAM, or disk usage nears its limit or when your compute crashes, so you can find and respond to issues fast. To be the first to know when your applications are at risk of downtime or performance degradation, set up Slack notifications in Laravel Cloud and opt in to Resource Alerts.


[Connect Slack to Laravel Cloud](https://laravel.com/to/org/settings/notifications)

**Improvements (7)**

* Show total cache storage usage instead of average cache usage
* Tooltips for identifiers in usage section
* Added source control disconnected notification
* Updated usage to include resource identifiers
* Users can now configure WWW domains as root domains
* Save and Deploy now deploys with latest commit
* Configure backup settings for Laravel Serverless Postgres

**Fixes (2)**

* Fixed average calculation on replica count chart
* Fixed network settings blank screen

**May 6, 2025**

## Slack notifications


Connect Laravel Cloud to your Slack workspace to receive notifications about your organization and application. Organization settings include notifications about resources, such as a new database or a new application, and membership requests. Application settings include notifications about deployment success, environment settings, domain verification, and more. You can send application and organization notifications to specific channels. [Connect your Slack workspace to Laravel Cloud](https://laravel.com/to/org/settings/notifications)

## Improved Usage page


The Usage page now includes an Allowances tab that shows your overall utilization of your plan's included usage. The Applications tab now also includes bandwidth usage (requests and data transfer) for each application. Together with Invoice Previews, the Usage page gives you a detailed view of usage across your applications. [View Your Usage](https://laravel.com/to/org/usage/applications)

## Pricing calculator


Our pricing calculator lets you estimate your costs on Laravel Cloud before you start deploying. Choose from our preset options, such as a personal blog or a SaaS app, or customize everything and choose the compute and resources that work best for your application. [Try the pricing calculator](https://laravel.com/pricing/calculator)

## Greater cache & response header control


You now have greater control over your cache and response headers. Laravel Cloud now fully respects all `Cache-Control` and `Expires` headers your application sets. You can choose when to purge your Edge Network cache, either manually or automatically on each new deploy. You can also bypass the cache entirely. Finally, you can override certain response headers like `X-Frame-Options`, `X-Content-Type-Options`, and `Strict-Transport-Security` directly in the Cloud environment canvas. [Learn more](https://laravel.com/cloud/docs/network#cache-control)

## Flexible backup retention window


Laravel Serverless Postgres now lets you set a backup retention window between 0 and 30 days. Previously, the window was fixed at 7 days, and you couldn't change it or opt out. Choose a backup window that works for your application, and save money on storage if your application doesn't require backups at all. [Learn more](https://laravel.com/cloud/docs/resources/databases/postgres)

**Improvements (6)**

* Hibernation is now enabled by default for all new environments on the Sandbox plan.
* Add infinite scrolling for Logs.
* Introduced full page layout for database UI.
* Added organization restricted, suspended, and terminated billing states.
* Improved Invoice Preview UI.
* Individual chart lines on Metrics pages can now be enabled or disabled.

**Fixes (2)**

* Various logs UI fixes.
* Various source control provider fixes.

**April 2, 2025**

## Replicate environments


Create copies of existing environments with all configuration intact. Replication is an important step toward shipping automatic preview environments. You can use it to spin up testing environments, create staging replicas of production, or set up identical workspaces for team members. Replication saves time and keeps your development workflow consistent. [Learn more](https://laravel.com/cloud/docs/environments#replicate)

## Stop and restart environments


Take manual control of your environment states with our new stop and restart functionality. Unlike hibernation, which happens automatically, stop and restart lets you explicitly pause environments when you don't need them and restart them when you do. It's perfect for managing costs, scheduling maintenance, or controlling resources during your development cycles. [Learn more](https://laravel.com/cloud/docs/environments#stop-and-restart)

## Invoice previews


Predict your spend with a preview of your current month's invoice to date. Previews include plan subscription, additional usage (after allowances), and discounts. [View Invoice Preview](https://laravel.com/to/org/usage/invoices)

## Inertia SSR


Laravel Cloud now supports serving [Inertia](https://inertiajs.com/) pages with [server-side rendering](https://inertiajs.com/server-side-rendering). Inertia SSR pre-renders your HTML on the server before sending it to the client, which can improve your application's SEO. [Learn more](https://laravel.com/cloud/docs/compute#inertia-ssr)

## Repository connection management

A disconnected repo no longer leaves you hanging. You can now edit which repository is connected to your application. You can now recover when a repository is deleted or access is revoked. After updating your repository, you can reconnect each environment to the appropriate branch, preserving all your settings and attached resources. [Learn more](https://laravel.com/cloud/docs/applications#reconnect-git-repository)

***

**Improvements (9)**

* Improved GitHub integration for enhanced reliability.
* Added applications usage to the usage screen.
* Improved domain verification workflow.
* Improved error messages for running commands.
* Enhanced tooltips and copy button usability.
* Allow re-running commands
* Added support for enabling "EU jurisdiction" when creating a bucket.
* Improved validation to check if Octane is installed before enabling it.
* Environments can now be "woken" from the hibernation state.

**Fixes (8)**

* Fixed an issue where "Build Logs" and "Deploy Logs" were sometimes truncated prematurely, preventing error messages from being displayed.
* Resolved an issue where deployment output was sometimes missing when a deployment failed.
* Fixed issue with the "Create Application" modal when a repository was not selected during branch refresh.
* Fixed Bitbucket link issue.
* Resolved an issue where the deployment output might incorrectly display as "complete".
* Fix the issue where changing the application's avatar also disconnects its source control.
* Prevent commands from being executed on stopped environments.
* Resolved timeout issue when creating applications with source controllers managing thousands of repositories.

**February 24, 2025**

Launched Laravel Cloud!
