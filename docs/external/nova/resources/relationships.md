# Nova - Resources/Relationships

*Source: https://nova.laravel.com/docs/v5/resources/relationships*

---

[Laravel Nova home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/dark.svg)](https://nova.laravel.com)

v5

Search...

⌘KAsk AI

- Support
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...

Navigation

Resources

Relationships

[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)

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

Resources

# Relationships

Nova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.

In addition to the variety of fields we’ve already discussed, Nova has full support for all of Laravel’s relationships. Once you add relationship fields to your Nova resources, you’ll start to experience the full power of the Nova dashboard, as the resource detail page will allow you to quickly view and search a resource’s related models:

![Detail page Relationship](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/detail-relationships.png)

## [​](#hasone) HasOne

The `HasOne` field corresponds to a `hasOne` Eloquent relationship. For example, let’s assume a `User` model `hasOne` `Address` model. We may add the relationship to our `User` Nova resource like so:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasOne;

// ...

HasOne::make('Address'),

```

Like other types of fields, relationship fields will automatically “camel case” the displayable name of the field to determine the underlying relationship method / attribute. However, you may explicitly specify the name of the relationship method by passing it as the second argument to the field’s `make` method:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasOne;

// ...

HasOne::make('Dirección', 'address'),

```

### [​](#hasoneofmany) HasOneOfMany

The `HasOne` relationship field can be transformed into an “has one of many” Eloquent relationship using the `ofMany` method. For example, let’s assume a `User` model `hasMany` `Post` models. We may add the “has one of many” relationship to our `User` Nova resource like so:

Copy

Ask AI

```
use App\Nova\Post;
use Laravel\Nova\Fields\HasOne;

// ...

HasOne::ofMany('Latest Post', 'latestPost', Post::class),

```

## [​](#hasmany) HasMany

The `HasMany` field corresponds to a `hasMany` Eloquent relationship. For example, let’s assume a `User` model `hasMany` `Post` models. We may add the relationship to our `User` Nova resource like so:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasMany;

// ...

HasMany::make('Posts'),

```

Once the field has been added to your resource, it will be displayed on the resource’s detail page.

When defining `HasMany` relationships, make sure to use the plural form of the relationship so Nova can infer the correct singular resource name:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasMany;

// ...

HasMany::make('Posts'),

```

## [​](#hasonethrough) HasOneThrough

The `HasOneThrough` field corresponds to a `hasOneThrough` Eloquent relationship. For example, let’s assume a `Mechanic` model has one `Car`, and each `Car` may have one `Owner`. While the `Mechanic` and the `Owner` have no direct connection, the `Mechanic` can access the `Owner` through the `Car` itself. You can display this relationship by adding it to your Nova resource:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasOneThrough;

// ...

HasOneThrough::make('Owner'),

```

## [​](#hasmanythrough) HasManyThrough

The `HasManyThrough` field corresponds to a `hasManyThrough` Eloquent relationship. For example, a `Country` model might have many `Post` models through an intermediate `User` model. In this example, you could easily gather all blog posts for a given country. To display this relationship within Nova, you may add it to your Nova resource:

Copy

Ask AI

```
use Laravel\Nova\Fields\HasManyThrough;

// ...

HasManyThrough::make('Posts'),

```

## [​](#belongsto) BelongsTo

The `BelongsTo` field corresponds to a `belongsTo` Eloquent relationship. For example, let’s assume a `Post` model `belongsTo` a `User` model. We may add the relationship to our `Post` Nova resource like so:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('User'),

```

You may customize the resource class used by the relation field by providing the second and third arguments of the `make` method, which define the name of the relationship and the underlying Nova resource class:

Copy

Ask AI

```
use App\Nova\User;
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('Author', 'author', User::class),

```

### [​](#peeking-at-belongsto-relationships) Peeking at BelongsTo Relationships

When hovering over a `BelongsTo` link when viewing the index or detail views, Nova will show a small card allowing you to “take a peek” at the linked relation:

![Relationship Peeking](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/peeking.png)

### [​](#preventing-peeking-at-belongsto-relationships) Preventing Peeking at `BelongsTo` Relationships

Relationship peeking is enabled by default; however, you can prevent the user from peeking at the relation using the `noPeeking` helper on your `BelongsTo` field:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('Author')
    ->noPeeking(),

```

You may also use the `peekable` method to determine whether the user should be allowed to peek at the relation:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

BelongsTo::make('Author')
    ->peekable(function (NovaRequest $request) {
        return $request->isResourceDetailRequest();
    }),

```

#### [​](#nullable-relationships) Nullable Relationships

If you would like your `BelongsTo` relationship to be `nullable`, you may simply chain the `nullable` method onto the field’s definition:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('User')
    ->nullable(),

```

#### [​](#title-attributes) Title Attributes

When a `BelongsTo` field is shown on a resource creation / update page, a drop-down selection menu or search menu will display the “title” of the resource. For example, a `User` resource may use the `name` attribute as its title. Then, when the resource is shown in a `BelongsTo` selection menu, that attribute will be displayed:

![Belongs To Title](https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/belongs-to-title.png)

To customize the “title” attribute of a resource, you may define a `title` property or `title` method on the resource class:

Property

Method

Copy

Ask AI

```
/**
 * The single value that should be used to represent the resource when being displayed.
 *
 * @var string
 */
public static $title = 'name';

```

#### [​](#disable-ordering-by-title) Disable Ordering by Title

By default, associatable resources will be sorted by their title when listed in a select dropdown. Using the `dontReorderAssociatables` method, you can disable this behavior so that the resources as sorted based on the ordering specified by the [relatable query](./authorization#relatable-filtering):

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('User')
    ->dontReorderAssociatables(),

```

#### [​](#filter-trashed-items) Filter Trashed Items

By default, the `BelongsTo` field will allow users to select soft-deleted models; however, this can be disabled using the `withoutTrashed` method:

Copy

Ask AI

```
use Laravel\Nova\Fields\BelongsTo;

// ...

BelongsTo::make('User')
    ->withoutTrashed(),

```

## [​](#belongstomany) BelongsToMany

The `BelongsToMany` field corresponds to a `belongsToMany` Eloquent relationship. For example, let’s assume a `User` model `belongsToMany` `Role` models:

app/Models/User.php



*[Content truncated for length]*