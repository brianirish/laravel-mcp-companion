# Nova - Search/The-Basics

*Source: https://nova.laravel.com/docs/v5/search/the-basics*

---

- [Laravel Nova home page](https://nova.laravel.com)v5Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#b9d7d6cfd8f9d5d8cbd8cfdcd597dad6d4)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)

Search...NavigationSearchThe Basics[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)- [Community](https://discord.com/invite/laravel)
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

Search# The Basics

Learn how to define searchable columns for your Nova resources.

## [​](#searchable-columns)Searchable Columns

To define which resource fields are searchable, you may assign an array of database columns to the `search` property or `searchableColumns` method of your resource class. This array includes the `id` column by default:

PropertyMethodCopyAsk AI```
namespace App\Nova;

class Post extends Resource 
{
    // ... 

    /**
     * The columns that should be searched.
     *
     * @var array
     */
    public static $search = [
        'id', 'title', 'content',
    ];
}

```

If you are using Nova’s Scout integration, the `$search` property has no effect on your search results and may be ignored. You should manage the searchable columns within the Algolia or Meilisearch dashboard.

## [​](#full-text-indexes)Full-Text Indexes

Typically, Nova searches your database columns using simple `LIKE` clauses. However, if you are using MySQL or Postgres, you may take advantage of any full-text indexes you have defined. To do so, you should define a `searchableColumns` method on your Nova resource class instead of defining a `$search` property.

The `searchableColumns` method should return an array of columns that are searchable. You may include an instance of `Laravel\Nova\Query\Search\SearchableText` within this array to instruct Nova to utilize your full-text indexes when querying a given column:

app/Nova/Post.phpCopyAsk AI```
use Laravel\Nova\Query\Search\SearchableText;

// ... 

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return ['id', new SearchableText('title')];
}

```

The array returned by the `searchableColumns` method can also include raw SQL expressions, which allow you to search through derived columns:

app/Nova/User.phpCopyAsk AI```
use Illuminate\Support\Facades\DB;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return ['id', DB::raw("CONCAT(first_name, ' ', last_name)")];
}

```

## [​](#searching-relationships)Searching Relationships

Laravel Nova also allows you to search against a resource’s related models. For example, imagine a `Post` model that is related to a `User` model via an `author` relatonship. You may indicate that this relationship data should be considered when searching for users by returning an instance of `Laravel\Nova\Query\Search\SearchableRelation` from your resource’s `searchableColumns` method.

If the `searchableColumns` method does not exist on your resource, you should define it. Once the `searchableColumns` method has been defined, you may remove the `$search` property from your resource:

app/Nova/Post.phpCopyAsk AI```
use Laravel\Nova\Query\Search\SearchableRelation;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return ['id', new SearchableRelation('author', 'name')];
}

```

For convenience, you may define a relationship that should be searched by adding the field to your resource’s `$search` property using “dot notation”:

app/Nova/Post.phpCopyAsk AI```
/**
 * The columns that should be searched.
 *
 * @var array
 */
public static $search = [
    'id', 'author.name'
];

```

### [​](#morphto-relationships)MorphTo Relationships

“Morph to” relationships can be made searchable by returning an instance of `Laravel\Nova\Query\Search\SearchableMorphToRelation` from your resource’s `searchableColumns` method. The `SearchableMorphToRelation` class allows you to specify which types of morphed models should be searched:

app/Nova/~Resource.phpCopyAsk AI```
use App\Nova\Post;
use Laravel\Nova\Query\Search\SearchableMorphToRelation;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return ['id', new SearchableMorphToRelation('commentable', 'title', [Post::class])];
}

```

## [​](#searching-json-data)Searching JSON Data

If the database table associated with your resource includes a column that contains a JSON string, you may instruct Nova to search within the JSON string by returning a `Laravel\Nova\Query\Search\SearchableJson` instance from your resource’s `searchableColumns` method.

If the `searchableColumns` method does not exist on your resource, you should define it. Once the `searchableColumns` method has been defined, you may remove the `$search` property from your resource:

app/Nova/UserProfile.phpCopyAsk AI```
use Laravel\Nova\Query\Search\SearchableJson;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return ['id', new SearchableJson('meta->address->postcode')];
}

```
Was this page helpful?

YesNo[Authorization](/docs/v5/resources/authorization)[Global Search](/docs/v5/search/global-search)On this page
- [Searchable Columns](#searchable-columns)
- [Full-Text Indexes](#full-text-indexes)
- [Searching Relationships](#searching-relationships)
- [MorphTo Relationships](#morphto-relationships)
- [Searching JSON Data](#searching-json-data)

[Laravel Nova home page](https://nova.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.