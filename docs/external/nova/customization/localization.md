# Nova - Customization/Localization

*Source: https://nova.laravel.com/docs/v5/customization/localization*

---

- [Community](https://discord.com/invite/laravel)
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

- [Overview](#overview)
- [Creating New Localization Files](#creating-new-localization-files)
- [User Locale Overrides](#user-locale-overrides)
- [Resources](#resources)
- [Fields](#fields)
- [Relationships](#relationships)
- [Filters](#filters)
- [Lenses](#lenses)
- [Actions](#actions)
- [Metrics](#metrics)
- [Frontend](#frontend)

Digging Deeper

# Localization

Learn how to localize your Nova application.

### [​](#overview) Overview

Nova may be fully localized using Laravel’s [localization services](https://laravel.com/docs/localization). After running the `nova:install` command during installation. Your application will contain a `lang/vendor/nova` translation directory.
Within this directory, you may customize the `en.json` file or create a new JSON translation file for your language. In addition, the `en` directory contains a few additional validation translation lines that are utilized by Nova.

#### [​](#creating-new-localization-files) Creating New Localization Files

To quickly create a new translation file for your language, you may execute the `nova:translate` Artisan command. This command will simply copy the default `en.json` translation file, allowing you to begin translating the strings into your own language:

Copy

Ask AI

```
php artisan nova:translate es
```

#### [​](#user-locale-overrides) User Locale Overrides

Laravel Nova frontend libraries, including the browser, Numbro.js, Luxon, and other libraries will utilize the locale value available via `app()->getLocale()` by default. However, if your application is only using ISO 639-1 language codes (`en`), you may wish to consider migrating your languages to IETF language tags (`en-US`, `en-GB`) for wider support across the various frontend libraries used by Nova.
To map your existing locales to IETF language tags, you may use the `Nova::userLocale` method. Typically, you should invoke this method in the `boot` method of your application’s `NovaServiceProvider`:

app/Providers/NovaServiceProvider.php

Copy

Ask AI

```
/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::userLocale(function () {
        return match (app()->getLocale()) {
            'en' => 'en-US',
            'de' => 'de-DE',
            default => null,
        };
    });
}
```

### [​](#resources) Resources

Resource names may be localized by overriding the `label` and `singularLabel` methods on the resource class:

app/Nova/~Resource.php

Copy

Ask AI

```
/**
 * Get the displayable label of the resource.
 *
 * @return string
 */
public static function label()
{
    return __('Posts');
}

/**
 * Get the displayable singular label of the resource.
 *
 * @return string
 */
public static function singularLabel()
{
    return __('Post');
}
```

To customize labels for the resource’s create and update buttons, you may override the `createButtonLabel` and `updateButtonLabel` methods on the resource:

app/Nova/~Resource.php

Copy

Ask AI

```
/**
 * Get the text for the create resource button.
 *
 * @return string|null
 */
public static function createButtonLabel()
{
    return __('Publish Post');
}

/**
 * Get the text for the update resource button.
 *
 * @return string|null
 */
public static function updateButtonLabel()
{
    return __('Save Changes');
}
```

### [​](#fields) Fields

Field names may be localized when you attach the field to your resource. The first argument to all fields is its display name, which you may customize. For example, you might localize the title of an email address field like so:

Copy

Ask AI

```
use Laravel\Nova\Fields\Text;

// ...

Text::make(__('Email Address'), 'email_address'),
```

### [​](#relationships) Relationships

Relationship field names may be customized by localizing the first argument passed to their field definition. The second and third arguments to Nova relationship fields are the relationship method name and the related Nova resource, respectively:

Copy

Ask AI

```
use App\Nova\Post;
use Laravel\Nova\Fields\HasMany;

// ...

HasMany::make(__('Posts'), 'posts', Post::class),
```

In addition, you should also override the `label` and `singularLabel` methods on the related resource:

app/Nova/~Resource.php

Copy

Ask AI

```
/**
 * Get the displayable label of the resource.
 *
 * @return string
 */
public static function label()
{
    return __('Posts');
}

/**
 * Get the displayable singular label of the resource.
 *
 * @return string
 */
public static function singularLabel()
{
    return __('Post');
}
```

### [​](#filters) Filters

Filter names may be localized by overriding the `name` method on the filter class:

app/Nova/Filters/~Filter.php

Copy

Ask AI

```
/**
 * Get the displayable name of the filter.
 *
 * @return string
 */
public function name()
{
    return __('Admin Users');
}
```

### [​](#lenses) Lenses

Lens names may be localized by overriding the `name` method on the lens class:

app/Nova/Lenses/~Lens.php

Copy

Ask AI

```
/**
 * Get the displayable name of the lens.
 *
 * @return string
 */
public function name()
{
    return __('Most Valuable Users');
}
```

### [​](#actions) Actions

Action names may be localized by overriding the `name` method on the action class:

app/Nova/Actions/~Action.php

Copy

Ask AI

```
/**
 * Get the displayable name of the action.
 *
 * @return string
 */
public function name()
{
    return __('Email Account Profile');
}
```

### [​](#metrics) Metrics

Metric names may be localized by overriding the `name` method on the metric class:

app/Nova/Metrics/~Metric.php

Copy

Ask AI

```
/**
 * Get the displayable name of the metric.
 *
 * @return string
 */
public function name()
{
    return __('Total Users');
}
```

### [​](#frontend) Frontend

To propagate your localizations to the frontend, you should call the `Nova::translations` method within your `NovaServiceProvider`:

app/Providers/NovaServiceProvider.php

Copy

Ask AI

```
/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::translations($pathToFile);
    });
}
```

You may also pass an array of key / value pairs representing each localization:

app/Providers/NovaServiceProvider.php

Copy

Ask AI

```
/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::serving(function () {
        Nova::translations([
            'Total Users' => 'Total Users'
        ]);
    });
}
```

As in Laravel, you may use the `__` helper within your custom Vue components to access these translations. To accomplish this, add the following mixins to your Inertia page component or Vue component:

Option API

Composition API

Copy

Ask AI

```
<template>
  <h2>{{ __('Total Users') }}</h2>
</template>

<script>
import { Localization } from 'laravel-nova'

export default {
  mixins: [Localization]

  // ...
}
</script>
```

Was this page helpful?

YesNo

[Assets](/docs/v5/customization/assets)[Stubs](/docs/v5/customization/stubs)

⌘I