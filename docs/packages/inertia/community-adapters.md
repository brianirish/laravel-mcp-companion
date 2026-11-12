Source: https://inertiajs.com/docs/v3/installation/community-adapters.md

# Community Adapters

The [Inertia protocol](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md) is framework-agnostic, so Inertia isn't limited to Laravel. The community maintains adapters for many other frameworks, such as Rails, Django, and Phoenix.

The official [Laravel](https://laravel.com/) adapter is the [reference implementation](https://inertiajs.com/docs/v3/advanced/building-an-adapter.md#the-reference-implementation) of the protocol, so the examples in this documentation use Laravel. Each community adapter has its own documentation for installation and framework-specific APIs.

> [!NOTE]
>
> The Inertia core team does not maintain community adapters. Support for newer protocol features varies from adapter to adapter.

## Inertia Organization

The [inertiajs](https://github.com/inertiajs) GitHub organization hosts the following adapters.

> [card] [Rails](https://github.com/inertiajs/inertia-rails)
>
> The Ruby on Rails adapter.

> [card] [Django](https://github.com/inertiajs/inertia-django)
>
> The Django adapter for Python.

> [card] [Phoenix](https://github.com/inertiajs/inertia-phoenix)
>
> The Phoenix adapter for Elixir.

## Community

Community members build and maintain the following adapters.

| Language | Framework | Adapter | Inertia |
| :- | :- | :- | :- |
| C# | ASP.NET Core | [pmd-coutinho/dotnet-inertia-adapter](https://github.com/pmd-coutinho/dotnet-inertia-adapter) | v3 |
| Go | Any | [petaki/inertia-go](https://github.com/petaki/inertia-go) | v3 |
| Go | Any | [romsar/gonertia](https://github.com/romsar/gonertia) | v3 (partial) |
| Go | Echo | [kohkimakimoto/inertia-echo](https://github.com/kohkimakimoto/inertia-echo) | v3 |
| Groovy | Grails | [matrei/grails-inertia-plugin](https://github.com/matrei/grails-inertia-plugin) | v3 |
| JavaScript | Sails | [inertia-sails](https://github.com/sailscastshq/boring-stack/tree/main/packages/inertia-sails) | v3 |
| PHP | Any (PSR) | [maskulabs/inertia-psr](https://github.com/maskulabs/inertia-psr) | v3 |
| PHP | Any (PSR-15) | [sirix777/inertia-psr15](https://github.com/sirix777/inertia-psr15) | v3 |
| PHP | Core PHP | [webkul/inertia](https://github.com/webkul/inertia) | v3 (partial) |
| PHP | Mako | [inventor96/inertia-mako](https://github.com/inventor96/inertia-mako/) | v3 (partial) |
| PHP | Symfony | [nytodev/inertia-bundle](https://github.com/nytodev/inertia-bundle) | v3 |
| PHP | WordPress | [evo-mark/inertia-wordpress](https://github.com/evo-mark/inertia-wordpress) | v2 (partial) |
| PHP | Yii3 | [maskulabs/inertia-yii](https://github.com/maskulabs/inertia-yii) | v3 |
| Python | FastAPI, Starlette, Django | [usecross/cross-inertia](https://github.com/usecross/cross-inertia) | v3 |
| Python | Litestar | [litestar-org/litestar-vite](https://github.com/litestar-org/litestar-vite) | v3 (partial) |
| Rust | Any | [KaioFelps/inertia-rust](https://github.com/KaioFelps/inertia-rust) | v2 (partial) |
| Rust | Rocket, Axum | [stuarth/inertia-rs](https://github.com/stuarth/inertia-rs) | v3 (partial) |
| TypeScript | AdonisJS | [@adonisjs/inertia](https://docs.adonisjs.com/guides/frontend/inertia) | v3 |
| TypeScript | Guren | [@guren/core](https://guren.dev/docs/guides/inertia) | v3 |
| TypeScript | NestJS | [@dudousxd/nestjs-inertia](https://davidecarvalho.github.io/aviary/docs/inertia) | v3 |

A partial adapter implements the core protocol but lacks some newer features, such as once props, rescued deferred props, or shared prop keys for instant visits. An adapter for Inertia v2 does not work with the v3 client-side adapters.

## Listing Your Adapter

To list your adapter on this page, open a pull request against the [documentation repository](https://github.com/inertiajs/docs). Before you open the pull request, make sure that your adapter meets these requirements:

* It implements the [protocol](https://inertiajs.com/docs/v3/core-concepts/the-protocol.md) for a supported Inertia version.
* It documents its installation, root template, and shared data APIs.
* It states which Inertia version and protocol features it supports.
* It has an active maintainer and a release on its language's package registry.

The [building an adapter](https://inertiajs.com/docs/v3/advanced/building-an-adapter.md) guide lists the features of a complete adapter.
