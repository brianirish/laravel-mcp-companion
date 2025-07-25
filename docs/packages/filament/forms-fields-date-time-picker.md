# Filament - Forms/Fields/Date Time Picker

Source: https://filamentphp.com/docs/3.x/forms/fields/date-time-picker

#Overview
---------

The date-time picker provides an interactive interface for selecting a date and/or a time.

```php
use Filament\Forms\Components\DatePicker;
use Filament\Forms\Components\DateTimePicker;
use Filament\Forms\Components\TimePicker;

DateTimePicker::make('published_at')
DatePicker::make('date_of_birth')
TimePicker::make('alarm_at')

```
![Date time pickers](/docs/3.x/images/light/forms/fields/date-time-picker/simple.jpg) ![Date time pickers](/docs/3.x/images/dark/forms/fields/date-time-picker/simple.jpg)

#Customizing the storage format
-------------------------------

You may customize the format of the field when it is saved in your database, using the `format()` method. This accepts a string date format, using PHP date formatting tokens:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->format('d/m/Y')

```
#Disabling the seconds input
----------------------------

When using the time picker, you may disable the seconds input using the `seconds(false)` method:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->seconds(false)

```
![Date time picker without seconds](/docs/3.x/images/light/forms/fields/date-time-picker/without-seconds.jpg) ![Date time picker without seconds](/docs/3.x/images/dark/forms/fields/date-time-picker/without-seconds.jpg)

#Timezones
----------

If you’d like users to be able to manage dates in their own timezone, you can use the `timezone()` method:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->timezone('America/New_York')

```
While dates will still be stored using the app’s configured timezone, the date will now load in the new timezone, and it will be converted back when the form is saved.

#Enabling the JavaScript date picker
------------------------------------

By default, Filament uses the native HTML5 date picker. You may enable a more customizable JavaScript date picker using the `native(false)` method:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->native(false)

```
![JavaScript-based date time picker](/docs/3.x/images/light/forms/fields/date-time-picker/javascript.jpg) ![JavaScript-based date time picker](/docs/3.x/images/dark/forms/fields/date-time-picker/javascript.jpg)

Please be aware that while being accessible, the JavaScript date picker does not support full keyboard input in the same way that the native date picker does. If you require full keyboard input, you should use the native date picker.

### #Customizing the display format

You may customize the display format of the field, separately from the format used when it is saved in your database. For this, use the `displayFormat()` method, which also accepts a string date format, using PHP date formatting tokens:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->native(false)
    ->displayFormat('d/m/Y')

```
![Date time picker with custom display format](/docs/3.x/images/light/forms/fields/date-time-picker/display-format.jpg) ![Date time picker with custom display format](/docs/3.x/images/dark/forms/fields/date-time-picker/display-format.jpg)

You may also configure the locale that is used when rendering the display, if you want to use different locale from your app config. For this, you can use the `locale()` method:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->native(false)
    ->displayFormat('d F Y')
    ->locale('fr')

```
### #Configuring the time input intervals

You may customize the input interval for increasing/decreasing the hours/minutes /seconds using the `hoursStep()` , `minutesStep()` or `secondsStep()` methods:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->native(false)
    ->hoursStep(2)
    ->minutesStep(15)
    ->secondsStep(10)

```
### #Configuring the first day of the week

In some countries, the first day of the week is not Monday. To customize the first day of the week in the date picker, use the `firstDayOfWeek()` method on the component. 0 to 7 are accepted values, with Monday as 1 and Sunday as 7 or 0:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->native(false)
    ->firstDayOfWeek(7)

```
![Date time picker where the week starts on Sunday](/docs/3.x/images/light/forms/fields/date-time-picker/week-starts-on-sunday.jpg) ![Date time picker where the week starts on Sunday](/docs/3.x/images/dark/forms/fields/date-time-picker/week-starts-on-sunday.jpg)

There are additionally convenient helper methods to set the first day of the week more semantically:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('published_at')
    ->native(false)
    ->weekStartsOnMonday()

DateTimePicker::make('published_at')
    ->native(false)
    ->weekStartsOnSunday()

```
### #Disabling specific dates

To prevent specific dates from being selected:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('date')
    ->native(false)
    ->disabledDates(['2000-01-03', '2000-01-15', '2000-01-20'])

```
![Date time picker where dates are disabled](/docs/3.x/images/light/forms/fields/date-time-picker/disabled-dates.jpg) ![Date time picker where dates are disabled](/docs/3.x/images/dark/forms/fields/date-time-picker/disabled-dates.jpg)

### #Closing the picker when a date is selected

To close the picker when a date is selected, you can use the `closeOnDateSelection()` method:

```php
use Filament\Forms\Components\DateTimePicker;

DateTimePicker::make('date')
    ->native(false)
    ->closeOnDateSelection()

```
#Autocompleting dates with a datalist
-------------------------------------

Unless you’re using the JavaScript date picker, you may specify datalist options for a date picker using the `datalist()` method:

```php
use Filament\Forms\Components\TimePicker;

TimePicker::make('appointment_at')
    ->datalist([
        '09:00',
        '09:30',
        '10:00',
        '10:30',
        '11:00',
        '11:30',
        '12:00',
    ])

```
Datalists provide autocomplete options to users when they use the picker. However, these are purely recommendations, and the user is still able to type any value into the input. If you’re looking to strictly limit users to a set of predefined options, check out the select field.

### #Focusing a default calendar date

By default, if the field has no state, opening the calendar panel will open the calendar at the current date. This might not be convenient for situations where you want to open the calendar on a specific date instead. You can use the `defaultFocusedDate()` to set a default focused date on the calendar:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('custom_starts_at')
    ->native(false)
    ->placeholder(now()->startOfMonth())
    ->defaultFocusedDate(now()->startOfMonth())

```
#Adding affix text aside the field
----------------------------------

You may place text before and after the input using the `prefix()` and `suffix()` methods:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date')
    ->prefix('Starts')
    ->suffix('at midnight')

```
![Date time picker with affixes](/docs/3.x/images/light/forms/fields/date-time-picker/affix.jpg) ![Date time picker with affixes](/docs/3.x/images/dark/forms/fields/date-time-picker/affix.jpg)

### #Using icons as affixes

You may place an icon before and after the input using the `prefixIcon()` and `suffixIcon()` methods:

```php
use Filament\Forms\Components\TimePicker;

TimePicker::make('at')
    ->prefixIcon('heroicon-m-play')

```
![Date time picker with prefix icon](/docs/3.x/images/light/forms/fields/date-time-picker/prefix-icon.jpg) ![Date time picker with prefix icon](/docs/3.x/images/dark/forms/fields/date-time-picker/prefix-icon.jpg)

#### #Setting the affix icon’s color

Affix icons are gray by default, but you may set a different color using the `prefixIconColor()` and `suffixIconColor()` methods:

```php
use Filament\Forms\Components\TimePicker;

TimePicker::make('at')
    ->prefixIcon('heroicon-m-check-circle')
    ->prefixIconColor('success')

```
#Making the field read-only
---------------------------

Not to be confused with disabling the field, you may make the field “read-only” using the `readonly()` method:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->readonly()

```
Please note that this setting is only enforced on native date pickers. If you’re using the JavaScript date picker, you’ll need to use `disabled()`.

There are a few differences, compared to `disabled()`:

* When using `readOnly()`, the field will still be sent to the server when the form is submitted. It can be mutated with the browser console, or via JavaScript. You can use `dehydrated(false)` to prevent this.
* There are no styling changes, such as less opacity, when using `readOnly()`.
* The field is still focusable when using `readOnly()`.

#Date-time picker validation
----------------------------

As well as all rules listed on the validation page, there are additional rules that are specific to date-time pickers.

### #Max date / min date validation

You may restrict the minimum and maximum date that can be selected with the picker. The `minDate()` and `maxDate()` methods accept a `DateTime` instance (e.g. `Carbon`), or a string:

```php
use Filament\Forms\Components\DatePicker;

DatePicker::make('date_of_birth')
    ->native(false)
    ->minDate(now()->subYears(150))
    ->maxDate(now())

```
Edit on GitHub

Still need help? Join our Discord community or open a GitHub discussion