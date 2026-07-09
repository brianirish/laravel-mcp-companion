# Nova - Search/The-Basics

*Source: https://nova.laravel.com/docs/v5/search/the-basics*

---

## On this page
- [Searchable Columns](#searchable-columns)
- [Full-Text Indexes](#full-text-indexes)
- [Searching Relationships](#searching-relationships)
  - [MorphTo Relationships](#morphto-relationships)
- [Searching JSON Data](#searching-json-data)
Search
# The Basics
Learn how to define searchable columns for your Nova resources.
## [​](#searchable-columns) Searchable Columns
To define which resource fields are searchable, you may assign an array of database columns to the `search` property or `searchableColumns` method of your resource class. This array includes the `id` column by default:
Property
Method
```
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
```
namespace App\Nova;

class Post extends Resource 
{
    // ... 

    /**
     * Get the searchable columns for the resource.
     *
     * @return array
     */
    public static function searchableColumns()
    {
        return [
            'id', 'title', 'content',
        ];
    }
}
```
If you are using Nova’s Scout integration, the `$search` property has no effect on your search results and may be ignored. You should manage the searchable columns within the Algolia or Meilisearch dashboard.
## [​](#full-text-indexes) Full-Text Indexes
Typically, Nova searches your database columns using simple `LIKE` clauses. However, if you are using MySQL or Postgres, you may take advantage of any full-text indexes you have defined. To do so, you should define a `searchableColumns` method on your Nova resource class instead of defining a `$search` property.
The `searchableColumns` method should return an array of columns that are searchable. You may include an instance of `Laravel\Nova\Query\Search\SearchableText` within this array to instruct Nova to utilize your full-text indexes when querying a given column:
app/Nova/Post.php
```
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
app/Nova/User.php
```
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
## [​](#searching-relationships) Searching Relationships
Laravel Nova also allows you to search against a resource’s related models. For example, imagine a `Post` model that is related to a `User` model via an `author` relatonship. You may indicate that this relationship data should be considered when searching for users by returning an instance of `Laravel\Nova\Query\Search\SearchableRelation` from your resource’s `searchableColumns` method.
If the `searchableColumns` method does not exist on your resource, you should define it. Once the `searchableColumns` method has been defined, you may remove the `$search` property from your resource:
app/Nova/Post.php
```
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
app/Nova/Post.php
```
/**
 * The columns that should be searched.
 *
 * @var array
 */
public static $search = [
    'id', 'author.name'
];
```
### [​](#morphto-relationships) MorphTo Relationships
“Morph to” relationships can be made searchable by returning an instance of `Laravel\Nova\Query\Search\SearchableMorphToRelation` from your resource’s `searchableColumns` method. The `SearchableMorphToRelation` class allows you to specify which types of morphed models should be searched:
app/Nova/~Resource.php
```
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
## [​](#searching-json-data) Searching JSON Data
If the database table associated with your resource includes a column that contains a JSON string, you may instruct Nova to search within the JSON string by returning a `Laravel\Nova\Query\Search\SearchableJson` instance from your resource’s `searchableColumns` method.
If the `searchableColumns` method does not exist on your resource, you should define it. Once the `searchableColumns` method has been defined, you may remove the `$search` property from your resource:
app/Nova/UserProfile.php
```
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
YesNo
[Authorization](/docs/v5/resources/authorization)[Global Search](/docs/v5/search/global-search)
⌘I