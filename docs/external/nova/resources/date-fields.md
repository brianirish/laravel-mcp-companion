# Nova - Resources/Date-Fields

*Source: https://nova.laravel.com/docs/v5/resources/date-fields*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Resources
Date Fields
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
- [Blog](https://blog.laravel.com)
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
- [Options](#options)
- [Steps](#steps)
- [Minimum and Maximum Values](#minimum-and-maximum-values)
- [Timezones](#timezones)
- [Customizing the Timezone](#customizing-the-timezone)
Resources
# Date Fields
Date fields allow you to collect and display date and time information.
Nova offers two types of date fields: `Date` and `DateTime`. As you may have guessed, the `Date` field does not store time information while the `DateTime` field does:
Copy
Ask AI
```
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\DateTime;

// ...

Date::make('Birthday'),
DateTime::make('Created At'),
```
### [​](#options) Options
#### [​](#steps) Steps
By default, Nova will set a minimum “step” of 1 day for `Date` fields and 1 second for `DateTime` fields. You may modify the “step” value for both of these fields by providing an integer or `Carbon\CarbonInterval` to the field’s `step` methods:
Copy
Ask AI
```
use Carbon\CarbonInterval;
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\DateTime;

// ...

Date::make('Expired On')->step(7),
Date::make('Expired On')->step(CarbonInterval::weeks(1)),

DateTime::make('Published At')->step(60),
DateTime::make('Published At')->step(CarbonInterval::minutes(1)),
```
#### [​](#minimum-and-maximum-values) Minimum and Maximum Values
Sometimes you may wish to explicitly define minimum and maximum values for `Date` or `DateTime` fields. This can be done by passing a valid date expression, a date format supported by `strtotime`, or an instance of `Carbon\CarbonInterface` to the `min` and `max` methods of these fields:
Copy
Ask AI
```
use Carbon\Carbon;
use Laravel\Nova\Fields\Date;

// ...

Date::make('Expired On')
    ->min('tomorrow')
    ->max('next week'),

Date::make('Expired On')
    ->min(Carbon::tomorrow())
    ->max(Carbon::today()->addWeek(1)),
```
### [​](#timezones) Timezones
By default, Nova users will always see dates presented in your application’s “server-side” timezone as defined by the `timezone` configuration option in your application’s `config/app.php` configuration file.
#### [​](#customizing-the-timezone) Customizing the Timezone
Sometimes you may wish to explicitly define the Nova user’s timezone instead of using the application’s timezone configuration. For example, perhaps your application allows users to select their own timezone so that they always see consistent date timezones even when traveling around the world.
To accomplish this, you may use the `Nova::userTimezone` method. Typically you should call this method in the `boot` method of your application’s `NovaServiceProvider`:
app/Nova/NovaServiceProvider.php
Copy
Ask AI
```
use Laravel\Nova\Nova;
use Illuminate\Http\Request;

// ... 

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::userTimezone(function (Request $request) {
        return $request->user()?->timezone;
    });
}
```
Was this page helpful?
YesNo
[Dependent Fields](/docs/v5/resources/dependent-fields)[File Fields](/docs/v5/resources/file-fields)
⌘I
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)