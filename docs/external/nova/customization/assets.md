# Nova - Customization/Assets

*Source: https://nova.laravel.com/docs/v5/customization/assets*

---

- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/nova)

##### Get Started

- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)

##### Resources

- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)

##### Search

- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)

##### Filters

- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)

##### Lenses

- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)

##### Actions

- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)

##### Metrics

- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)

##### Digging Deeper

- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)

On this page

- [Overview](#overview)
- [Defining Assets](#defining-assets)
- [Registering Assets](#registering-assets)
- [Compiling Assets](#compiling-assets)

Digging Deeper

# Assets

Learn how to extend or add additional functionality to Nova.

## [​](#overview) Overview

Assets allow you to extend or add additional functionality to Nova without the overhead of cards or resource tools. For example, you may wish to override a custom error component to match your branding or intercept Inertia interactions and provide additional data to routes.

## [​](#defining-assets) Defining Assets

Assets may be generated using the `nova:asset` Artisan command. By default, all new assets will be placed in the `nova-components` directory of your application. When generating an asset using the `nova:asset` command, the asset name you pass to the command should follow the Composer `vendor/package` format:

Copy

Ask AI

```
php artisan nova:asset acme/analytics

```

When generating an asset, Nova will prompt you to install the assets NPM dependencies, compile its dependencies, and update your application’s `composer.json` file. All custom assets are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova assets include all of the scaffolding necessary to build your asset. Each asset even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.

## [​](#registering-assets) Registering Assets

Nova assets are automatically loaded through the use of Laravel’s auto-loader, so no additional registration is required.

## [​](#compiling-assets) Compiling Assets

Your Nova asset contains a `webpack.mix.js` file, which is generated when Nova creates your custom asset. You may build your custom asset using the NPM `dev` and `prod` commands:

Copy

Ask AI

```
# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod

```

In addition, you may run the NPM `watch` command to auto-compile your assets when they are changed:

Copy

Ask AI

```
npm run watch

```

Was this page helpful?

YesNo

[CSS / JavaScript](/docs/v5/customization/frontend)[Localization](/docs/v5/customization/localization)

Assistant

Responses are generated using AI and may contain mistakes.