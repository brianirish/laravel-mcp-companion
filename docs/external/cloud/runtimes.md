Source: https://laravel.com/cloud/docs/runtimes.md

# Runtimes

Laravel Cloud supports PHP, Node.js, Bun, Deno, Go, Python, Ruby, and Rust runtimes across multiple frameworks.

## Overview

Laravel Cloud supports **PHP** for Laravel and Symfony applications, **JavaScript** (Node.js, Bun, or Deno) for Next.js, Nuxt, TanStack Start, Express, and Hono applications, **Go** for Go applications, **Python** for Django, FastAPI, Flask, and other Python applications, **Ruby** for Rails and other Ruby applications, and **Rust** for axum, Actix Web, Rocket, warp, and other Rust applications. Each runtime determines which versions, extensions, and platform features are available to your application.

See the [base image reference](https://laravel.com/cloud/docs/base-images) for the system packages and bundled tools included with each runtime.

## PHP

Laravel, Symfony, and other PHP applications use the PHP runtime.

**Supported versions:** PHP 8.2, 8.3, 8.4, and 8.5. PHP 8.5 is the default for new environments.

To select your PHP version, open your environment's **General Settings** page and choose the version under the **Runtime** section. Redeploy your environment to apply the change.

> [!NOTE]
>
> PHP 8.5 is generally available, but the `pdo_sqlsrv` extension is temporarily unavailable until the upstream project adds 8.5 support. Use PHP 8.2, 8.3, or 8.4 if you need that extension today.

## Node.js, Bun, and Deno

Next.js, Nuxt, TanStack Start, Express, and Hono applications can run on the Node.js, Bun, or Deno runtime. Laravel Cloud infers which one to use by analyzing the configuration files present in your repository:

| Runtime | Detected by |
| - | - |
| bunBun | `bun.lock`, `bun.lockb`, or `bunfig.toml` |
| denoDeno | `deno.json` or `deno.lock` |
| nodejsNode.js | `package-lock.json` |

**Supported versions:**

| Runtime | Versions |
| - | - |
| nodejsNode.js | 22, 24, and 26 (26 is the default for new environments) |
| bunBun | 1.3 and 1.4 (1.4 is the default for new environments) |
| denoDeno | 2.9 |

To select your Node.js, Bun, or Deno version, open your environment's **General Settings** page and choose the version under the **Runtime** section. Redeploy your environment to apply the change.

## Go

Go applications use the Go runtime. Laravel Cloud detects a Go application from a `go.mod` file at the root of your repository. There's no separate framework detection, since Cloud builds and runs a Go application as a single compiled binary.

**Supported versions:** Go 1.25, 1.26, and 1.27. Go 1.27 is the default for new environments.

Cloud reads the `go` directive in `go.mod` at each deployment commit and uses the lowest supported version that satisfies this minimum:

```text theme={null}
go 1.25
```

> [!NOTE]
>
> Your repository controls the Go version. If no supported version satisfies the `go` directive, the deployment fails before building. When no version is declared, Cloud uses Go 1.27.

## Python

Django, FastAPI, Flask, and other Python applications use the Python runtime. Laravel Cloud detects a Python application from a `pyproject.toml`, `requirements.txt`, `Pipfile`, or `setup.py` file, and further detects Django, FastAPI, or Flask when one of those packages appears in your dependencies. Cloud also supports applications that don't use a recognized framework as generic Python applications.

**Supported versions:** Python 3.10, 3.11, 3.12, 3.13, and 3.14. Python 3.14 is the default for new environments.

Cloud reads your Python version at each deployment commit. A `.python-version` file pins the major and minor version. When that file does not declare a version, Cloud uses the lowest supported version satisfying the `requires-python` constraint in `pyproject.toml`:

```toml theme={null}
[project]
requires-python = ">=3.12"
```

> [!NOTE]
>
> A repository declaration takes precedence over the environment's version setting. If you do not declare a version, you may select one in your environment settings. New environments default to Python 3.14. An unsupported pin or a constraint that no supported version satisfies causes the deployment to fail before building.

## Ruby

The Ruby runtime supports Ruby on Rails and other Ruby applications. Laravel Cloud detects Ruby from a `Gemfile` in your application directory and recognizes Rails from its application configuration and framework files.

**Supported versions:** Ruby 3.3, 3.4, and 4.0. Ruby 4.0 is the default for new environments.

Laravel Cloud checks version declarations in this order:

1. `.ruby-version`
2. The `RUBY VERSION` section of `Gemfile.lock`
3. The `ruby` declaration in `Gemfile`
4. `.tool-versions`
5. `mise.toml`

For example, a `.ruby-version` file may contain:

```text theme={null}
3.4
```

Declarations select a major and minor release line. A `Gemfile` version constraint selects the lowest supported release line that satisfies it. Laravel Cloud reads the declaration from each deployment's commit, and an unsupported declaration stops the deployment before building.

If your repository doesn't declare a version, you may choose a Ruby version in your environment's **General Settings**. Keep your declarations consistent with Bundler's Ruby requirements. See the [Ruby and Rails deploy guide](https://laravel.com/cloud/docs/deploy-guides/ruby) for dependencies and production configuration.

## Rust

axum, Actix Web, Rocket, warp, and other Rust applications use the Rust runtime. Laravel Cloud detects a Rust application from a `Cargo.toml` file at the root of your repository, and further detects axum, Actix Web, Rocket, or warp when one of those crates appears in your dependencies. Cloud also supports applications that don't use a recognized framework as generic Rust applications.

Cloud builds your application with a recent stable Rust release, so there is no version to select. To use a specific toolchain, pin it with a `rust-toolchain.toml` file at the root of your repository:

```toml theme={null}
[toolchain]
channel = "1.90.0"
```

> [!NOTE]
>
> Your repository controls the Rust version. rustup installs a pinned toolchain during your build, which adds to your build time. See the [Rust deploy guide](https://laravel.com/cloud/docs/deploy-guides/rust) to learn how to compile, start, and configure your application.

## Feature availability

| Feature | laravelLaravel | symfonySymfony | nextjsNext.js | nuxtNuxt | tanstackTanStack Start | nodejsNode.js | goGo | pythonPython | rubyRuby | railsRails | rustRust |
| - | - | - | - | - | - | - | - | - | - | - | - |
| Scale to zero | | | | | | | | | | | |
| Preview environments | | | | | | | | | | | |
| Custom domains | | | | | | | | | | | |
| Object storage | | | | | | | | | | | |
| Worker clusters | | | | | | | | | | | |
| Managed queues | | | — | — | — | — | — | — | — | When enabled for your organization | — |
| Scheduled tasks | | | — | — | — | — | — | — | — | — | — |
| Runtime extensions | PHP extensions | PHP extensions | npm packages | npm packages | npm packages | npm packages | Go modules | pip, uv, Pipenv, or Poetry packages | Bundler gems | Bundler gems | Cargo crates |

For Rails job backends such as Solid Queue, Sidekiq, and GoodJob, use [custom background processes](https://laravel.com/cloud/docs/deploy-guides/ruby#caches-and-background-jobs). Rails managed queues require access enabled for your organization. Rails recurring tasks use your job backend's scheduler rather than Laravel Cloud's Laravel or Symfony scheduler controls.
