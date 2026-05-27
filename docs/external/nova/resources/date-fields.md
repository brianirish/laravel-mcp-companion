# Nova - Resources/Date-Fields

*Source: https://nova.laravel.com/docs/v5/resources/date-fields*

---

## On this page
- [Options](#options)
- [Steps](#steps)
- [Minimum and Maximum Values](#minimum-and-maximum-values)
- [Timezones](#timezones)
- [Customizing the Timezone](#customizing-the-timezone)
Resources
# Date Fields
Date fields allow you to collect and display date and time information.
> ## Documentation Index
>
> Fetch the complete documentation index at: <https://nova.laravel.com/docs/llms.txt>
>
> Use this file to discover all available pages before exploring further.
Nova offers two types of date fields: `Date` and `DateTime`. As you may have guessed, the `Date` field does not store time information while the `DateTime` field does:
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