Source: https://laravel.com/cloud/docs/intro.md

# Welcome to Laravel Cloud

The official infrastructure and deployment platform for Laravel, with support for Symfony, Next.js, Nuxt, Go, Python, Rails, Rust, and more.

Laravel Cloud is a fully managed infrastructure platform for deploying and scaling ambitious web applications, with built-in solutions for web and worker compute, relational databases, caches, managed queues, file and object storage, and more.

Laravel Cloud is built for the Laravel framework and a curated selection of additional popular frameworks. We take extra care to support each framework's particular conventions, from how it is built and started to how its environment is configured. When you create an application, Laravel Cloud detects its framework and configures the matching runtime for you:

| Framework | Runtime |
| - | - |
| laravelLaravel | PHP |
| symfonySymfony | PHP |
| phpPHP (Other PHP backend applications) | PHP |
| nextjsNext.js | Node.js, Bun, or Deno |
| nuxtNuxt | Node.js, Bun, or Deno |
| tanstackTanStack Start | Node.js, Bun, or Deno |
| expressExpress | Node.js, Bun, or Deno |
| honoHono | Node.js, Bun, or Deno |
| nestjsNestJS | Node.js, Bun, or Deno |
| nodejsNode.js (Other backend Node.js applications) | Node.js, Bun, or Deno |
| goGo | Go |
| djangoDjango | Python |
| flaskFlask | Python |
| fastapiFastAPI | Python |
| pythonPython (Other Python applications) | Python |
| railsRuby on Rails | Ruby |
| rubyRuby (Other Ruby applications) | Ruby |
| axumaxum | Rust |
| actixActix Web | Rust |
| rocketRocket | Rust |
| warpwarp | Rust |
| rustRust (Other Rust applications) | Rust |

See [Runtimes](https://laravel.com/cloud/docs/runtimes) for the supported versions of each runtime.

## Unmatched developer experience

Laravel Cloud is the only fully managed platform-as-a-service (PaaS) obsessively optimized for shipping and scaling your applications.

* **No application or server configuration necessary.** Most applications built on supported frameworks can be [deployed to Laravel Cloud](https://laravel.com/cloud/docs/deployments) without any additional changes to your application's architecture. You also don't need any server management experience to deploy to Laravel Cloud.

* **Fully managed databases and caches.** You can provision and manage [Laravel MySQL](https://laravel.com/cloud/docs/resources/databases/laravel-mysql) and [Laravel Serverless Postgres](https://laravel.com/cloud/docs/resources/databases/postgres) databases directly from the Laravel Cloud dashboard. You can also provision [Laravel Valkey](https://laravel.com/cloud/docs/resources/caches/valkey) caches in seconds.

* **Managed queues.** Laravel and Symfony applications can use [fully managed queues](https://laravel.com/cloud/docs/queues#managed-queues) with dedicated workers. The workers scale automatically with the jobs waiting to be processed, down to zero when idle, and a built-in dashboard lets you retry failed jobs.

* **Workers.** All supported frameworks and runtimes can use [dedicated worker clusters](https://laravel.com/cloud/docs/workers#worker-clusters) to run custom worker tasks, including queue workers and other long-running background processes.

* **Zero downtime deployments and scaling.** Laravel Cloud automatically rolls out [changes to your application](https://laravel.com/cloud/docs/deployments) without downtime. You can also [scale your application's infrastructure](https://laravel.com/cloud/docs/compute#autoscaling) at any time without interrupting your users.

* **Scale to zero.** Laravel Cloud can [put your environment to sleep](https://laravel.com/cloud/docs/compute#scale-to-zero) when it is idle so you are not charged for compute, then wake it in under 500 milliseconds when a request arrives. Managed queues run on dedicated workers and continue to process jobs while your environment sleeps. For Laravel applications, scheduled tasks also continue to run while the environment sleeps.

* **Preview environments.** Automatically provision a [fully isolated environment for every pull request](https://laravel.com/cloud/docs/preview-environments), then tear it down when the pull request is merged or closed, so your team can review changes in a production-like environment before they ship.

* **Automatic SSL and load balancing.** Every application running on Laravel Cloud automatically receives [SSL certificates](https://laravel.com/cloud/docs/domains), and Cloud renews them for you. Cloud also [distributes incoming traffic across your available application replicas](https://laravel.com/cloud/docs/network#cloud-compute-network).

* **Cloud Edge Network.** Laravel Cloud partners with Cloudflare to offer a [globally distributed caching and security network at the edge](https://laravel.com/cloud/docs/network#cloud-edge-network). This edge network provides DDoS protection and edge asset caching to all applications running on Laravel Cloud.

* **Monitoring and logs.** Basic [infrastructure metrics](https://laravel.com/cloud/docs/compute#compute-metrics), such as CPU and memory usage, are available in the Laravel Cloud dashboard. You can also [view and search your application's logs](https://laravel.com/cloud/docs/logs).

## Next steps

We can't wait to see what you ship on Laravel Cloud. When you're ready to dive in, check out our [quickstart documentation](https://laravel.com/cloud/docs/quickstart).

## Prerequisites

Laravel applications require Laravel 9.x or greater, and Symfony applications require Symfony 7.4 LTS or 8.x. Your application must also use a supported runtime version. See [Runtimes](https://laravel.com/cloud/docs/runtimes) for the supported PHP, Node.js, Bun, Deno, Go, Python, and Ruby versions.
