# Nova - Customization/Stubs

*Source: https://nova.laravel.com/docs/v5/customization/stubs*

---

Digging Deeper
# Stubs
Customize the stubs used by Nova to generate various classes.
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://nova.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
When creating new resources, actions, filters, lens and metrics, Nova will publish files using the default stub files that exist within Nova. However, you may wish to customize these stubs for your own projects in order to apply common modifications automatically.
To publish the stubs used by Nova to generate various classes, execute the following command:
```
php artisan nova:stubs
```
When running this Artisan command in your terminal, Nova will copy all of its stub files into `./stubs/nova`, where they may then be customized.
If you do not wish to customize a particular stub, you may delete the stub and Nova will continue to use the default version of the stub that exists within Nova itself.
To learn more about stub customization, please consult the [Laravel documentation](https://laravel.com/docs/artisan#stub-customization).
Was this page helpful?
YesNo
[Localization](/docs/v5/customization/localization)
⌘I