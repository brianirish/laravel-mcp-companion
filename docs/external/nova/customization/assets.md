# Nova - Customization/Assets

*Source: https://nova.laravel.com/docs/v5/customization/assets*

---

## On this page
- [Overview](#overview)
- [Defining Assets](#defining-assets)
- [Registering Assets](#registering-assets)
- [Compiling Assets](#compiling-assets)
Digging Deeper
# Assets
Learn how to extend or add additional functionality to Nova.
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://nova.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
## [​](#overview) Overview
Assets allow you to extend or add additional functionality to Nova without the overhead of cards or resource tools. For example, you may wish to override a custom error component to match your branding or intercept Inertia interactions and provide additional data to routes.
## [​](#defining-assets) Defining Assets
Assets may be generated using the `nova:asset` Artisan command. By default, all new assets will be placed in the `nova-components` directory of your application. When generating an asset using the `nova:asset` command, the asset name you pass to the command should follow the Composer `vendor/package` format:
```
php artisan nova:asset acme/analytics
```
When generating an asset, Nova will prompt you to install the assets NPM dependencies, compile its dependencies, and update your application’s `composer.json` file. All custom assets are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova assets include all of the scaffolding necessary to build your asset. Each asset even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.
## [​](#registering-assets) Registering Assets
Nova assets are automatically loaded through the use of Laravel’s auto-loader, so no additional registration is required.
## [​](#compiling-assets) Compiling Assets
Your Nova asset contains a `webpack.mix.js` file, which is generated when Nova creates your custom asset. You may build your custom asset using the NPM `dev` and `prod` commands:
```
# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod
```
In addition, you may run the NPM `watch` command to auto-compile your assets when they are changed:
```
npm run watch
```
Was this page helpful?
YesNo
[CSS / JavaScript](/docs/v5/customization/frontend)[Localization](/docs/v5/customization/localization)
⌘I