# Nova - Resources/Authorization

*Source: https://nova.laravel.com/docs/v5/resources/authorization*

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
Authorization
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
- [Policies](#policies)
- [Undefined Policy Methods](#undefined-policy-methods)
- [Hiding Entire Resources](#hiding-entire-resources)
- [When Nova & Application Authorization Logic Differs](#when-nova-%26-application-authorization-logic-differs)
- [Using Separate Policy Classes for Nova Resources](#using-separate-policy-classes-for-nova-resources)
- [Relationships](#relationships)
- [Authorizing Attaching / Detaching](#authorizing-attaching-%2F-detaching)
- [Disabling Authorization](#disabling-authorization)
- [Fields](#fields)
- [Index Filtering](#index-filtering)
- [Relatable Filtering](#relatable-filtering)
- [Dynamic Relatable Methods](#dynamic-relatable-methods)
- [Relationship Types](#relationship-types)
- [Scout Filtering](#scout-filtering)
Resources
# Authorization
Nova leverages Laravel policies to authorize incoming requests.
When Nova is accessed only by you or your development team, you may not need additional authorization before Nova handles incoming requests. However, if you provide access to Nova to your clients or a large team of developers, you may wish to authorize certain requests. For example, perhaps only administrators may delete records. Thankfully, Nova takes a simple approach to authorization that leverages many of the Laravel features you are already familiar with.
## [​](#policies) Policies
To limit which users may view, create, update, or delete resources, Nova leverages Laravel’s [authorization policies](https://laravel.com/docs/authorization#creating-policies). Policies are simple PHP classes that organize authorization logic for a particular model or resource. For example, if your application is a blog, you may have a `Post` model and a corresponding `PostPolicy` within your application.
When manipulating a resource within Nova, Nova will automatically attempt to find a corresponding policy for the model. If Nova detects a policy has been registered for the model, it will automatically check that policy’s relevant authorization methods before performing their respective actions, such as:
- `viewAny`
- `view`
- `create`
- `update`
- `replicate`
- `delete`
- `restore`
- `forceDelete`
No additional configuration is required! So, for example, to determine which users are allowed to update a `Post` model, you simply need to define an `update` method on the model’s corresponding policy class:
app/Policies/PostPolicy.php
Copy
Ask AI
```
namespace App\Policies;

use App\Models\User;
use App\Models\Post;
use Illuminate\Auth\Access\HandlesAuthorization;

class PostPolicy
{
    use HandlesAuthorization;

    /**
     * Determine whether the user can update the post.
     *
     * @return mixed
     */
    public function update(User $user, Post $post)
    {
        return $user->type == 'editor';
    }
}
```
### [​](#undefined-policy-methods) Undefined Policy Methods
If a policy exists but is missing a method for a particular action, Nova will use the following default permission for each actions:
| Policy Action | Default Permission |
| --- | --- |
| `viewAny` | Allowed |
| `view` | Forbidden |
| `create` | Forbidden |
| `update` | Forbidden |
| `replicate` | Fallback to `create` and `update` |
| `delete` | Forbidden |
| `forceDelete` | Forbidden |
| `restore` | Forbidden |
| `add{Model}` | Allowed |
| `attach{Model}` | Allowed |
| `attachAny{Model}` | Allowed |
| `detach{Model}` | Allowed |
| `runAction` | Fallback to `update` |
| `runDestructiveAction` | Fallback to `delete` |
So, if you have defined a policy, don’t forget to define all of its relevant authorization methods so that the authorization rules for a given resource are explicit.
### [​](#hiding-entire-resources) Hiding Entire Resources
If you would like to hide an entire Nova resource from a subset of your dashboard’s users, you may define a `viewAny` method on the model’s policy class. If no `viewAny` method is defined for a given policy, Nova will assume that the user can view the resource:
app/Policies/PostPolicy.php
Copy
Ask AI
```
use App\Models\User;

// ...

/**
 * Determine whether the user can view any posts.
 *
 * @return mixed
 */
public function viewAny(User $user)
{
    return in_array('view-posts', $user->permissions);
}
```
### [​](#when-nova-&-application-authorization-logic-differs) When Nova & Application Authorization Logic Differs
If you need to authorize actions differently when a request is initiated from within Nova versus your primary application, you may utilize Nova’s `whenServing` method within your policy. This method allows you to only execute the given callback if the request is a Nova request. An additional callback may be provided that will be executed for non-Nova requests:
app/Policies/PostPolicy.php
Copy
Ask AI
```
use App\Models\User;
use Illuminate\Http\Request;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Nova;

// ... 

/**
 * Determine whether the user can view any posts.
 *
 * @return mixed
 */
public function viewAny(User $user)
{
    return Nova::whenServing(function (NovaRequest $request) use ($user) {
        return in_array('nova:view-posts', $user->permissions);
    }, function (Request $request) use ($user) {
        return in_array('view-posts', $user->permissions);
    });
}
```
#### [​](#using-separate-policy-classes-for-nova-resources) Using Separate Policy Classes for Nova Resources
You may also create a policy specifically for Nova resources instead of relying on the Eloquent model’s application level policy. To get started, generate a new Nova policy via the `nova:policy` command:
Copy
Ask AI
```
php artisan nova:policy PostPolicy --resource=Post
```
The `nova:policy` command above will create a new policy class as `App\Nova\Policies\PostPolicy`. In addition, the generated policy will authorize against `App\Nova\Post` instead of `App\Models\Post`. To register the policy with your Nova resource, you should specify the policy within the resource’s `$policy` property:
app/Nova/Post.php
Copy
Ask AI
```
namespace App\Nova;

class Post extends Resource
{
    /**
     * The policy the resource corresponds to.
     *
     * @var class-string
     */
    public static $policy = Policies\PostPolicy::class;
}
```
### [​](#relationships) Relationships
We have already learned how to authorize the typical view, create, update, and delete actions, but what about relationship interactions? For example, if you are building a podcasting application, perhaps you would like to specify that only certain Nova users may add comments to podcasts. Again, Nova makes this simple by leveraging Laravel’s policies.
When working with relationships, Nova uses a simple policy method naming convention. To illustrate this convention, lets assume your application has `Podcast` resources and `Comment` resources. If you would like to authorize which users can add comments to a podcast, you should define an `addComment` method on your podcast model’s policy class:
app/Policies/PodcastPolicy.php
Copy
Ask AI
```
use App\Models\User;
use App\Models\Podcast;

// ...

/**
 * Determine whether the user can add a comment to the podcast.
 *
 * @return mixed
 */
public function addComment(User $user, Podcast $podcast)
{
    return true;
}
```
As you can see, Nova uses a simple `add{Model}` policy method naming convention for authorizing relationship actions.
#### [​](#authorizing-attaching-/-detaching) Authorizing Attaching / Detaching
For many-to-many relationships, Nova uses a similar naming convention. However, instead of `add{Model}`, you should use an `attach{Model}` / `detach{Model}` naming convention. For example, imagine a `Podcast` model has a many-to-many relationship with the `Tag` model. If you would like to authorize which users can attach “tags” to a podcast, you may add an `attachTag` method to your podcast policy. In addition, you will likely want to define the inverse `attachPodcast` on the tag policy:
app/Policies/PodcastPolicy.php
Copy
Ask AI
```
use App\Models\Podcast;
use App\Models\Tag;
use App\Models\User;

// ... 

/**
 * Determine whether the user can attach a tag to a podcast.
 *
 * @return mixed
 */
public function attachTag(User $user, Podcast $podcast, Tag $tag)
{
    return true;
}

/**
 * Determine whether the user can detach a tag from a podcast.
 *
 * @return mixed
 */
public function detachTag(User $user, Podcast $podcast, Tag $tag)
{
    return true;
}
```
In the previous examples, we are determining if a user is authorized to attach one model to another. If certain types of users are **never** allowed to attach a given type of model, you may define a `attachAny{Model}` method on your policy class. This will prevent the “Attach” button from displaying in the Nova UI entirely:
app/Policies/PodcastPolicy.php
Copy
Ask AI
```
use App\Models\Podcast;
use App\Models\Tag;
use App\Models\User;

// ... 

/**
 * Determine whether the user can attach any tags to the podcast.
 * 
 * @return mixed
 */
public function attachAnyTag(User $user, Podcast $podcast)
{
    return false;
}
```
When working with many-to-many relationships, make sure you define the proper authorization policy methods on each of the related resource’s policy classes.
### [​](#disabling-authorization) Disabling Authorization
If one of your Nova resources’ models has a corresponding policy, but you want to disable Nova authorization for that resource (thus allowing all actions), you may override the `authorizable` method on the Nova resource:
app/Nova/~Resource.php
Copy
Ask AI
```
/**
 * Determine if the given resource is authorizable.
 *
 * @return bool
 */
public static function authorizable()
{
    return false;
}
```
## [​](#fields) Fields
Sometimes you may want to hide certain fields from a group of users. You may easily accomplish this by chaining the `canSee` method onto your field definition. The `canSee` method accepts a closure which should return `true` or `false`. The closure will receive the incoming HTTP request:
app/Nova/~Resource.php
Copy
Ask AI
```
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()->sortable(),

        Text::make('Name')
            ->sortable()
            ->canSee(function ($request) {
                return $request->user()->can('viewProfile', $this);
            }),
    ];
}
```
In the example above, we are using Laravel’s `Authorizable` trait’s `can` method on our `User` model to determine if the authorized user is authorized for the `viewProfile` action. However, since proxying to authorization policy methods is a common use-case for `canSee`, you may use the `canSeeWhen` method to achieve the same behavior. The `canSeeWhen` method has the same method signature as the `Illuminate\Foundation\Auth\Access\Authorizable` trait’s `can` method:
Copy
Ask AI
```
use Laravel\Nova\Fields\Text;

// ...

Text::make('Name')
        ->sortable()
        ->canSeeWhen('viewProfile', $this),
```
To learn more about Laravel’s authorization helpers and the `can` method, check out the full Laravel [authorization documentation](https://laravel.com/docs/authorization#via-the-user-model).
## [​](#index-filtering) Index Filtering
You may notice that returning `false` from a policy’s `view` method does not stop a given resource from appearing in the resource index. To filter models from the resource index query, you may override the `indexQuery` method on the resource’s class.
This method is already defined in your application’s `App\Nova\Resource` base class; therefore, you may simply copy and paste the method into a specific resource and then modify the query based on how you would like to filter the resource’s index results:
app/Nova/~Resource.php
Copy
Ask AI
```
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Build an "index" query for the given resource.
 */
public static function indexQuery(NovaRequest $request, Builder $query): Builder 
{
    return $query->where('user_id', $request->user()->id);
}
```
## [​](#relatable-filtering) Relatable Filtering
If you would like to filter the queries that are used to populate relationship model selection menus, you may override the `relatableQuery` method on your resource.
For example, if your application has a `Comment` resource that belongs to a `Podcast` resource, Nova will allow you to select the parent `Podcast` when creating a `Comment`. To limit the podcasts that are available in that selection menu, you should override the `relatableQuery` method on your `Podcast` resource:
app/Nova/~Resource.php
Copy
Ask AI
```
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Build an "relatable" query for the given resource.
 * 
 * This query determines which instances of the model may be attached to other resources.
 */
public static function relatableQuery(NovaRequest $request, Builder $query): Builder 
{
    return $query->where('user_id', $request->user()->id);
}
```
#### [​](#dynamic-relatable-methods) Dynamic Relatable Methods
You can customize the “relatable” query for individual relationships by using a dynamic, convention based method name that is suffixed with the pluralized name of the model. For example, if your application has a `Post` resource, in which posts can be tagged, but the `Tag` resource is associated with different types of models, you may define a `relatableTags` method to customize the relatable query for this relationship:
app/Nova/~Resource.php
Copy
Ask AI
```
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Build a "relatable" query for the given resource.
 *
 * This query determines which instances of the model may be attached to other resources.
 */
public static function relatableTags(NovaRequest $request, Builder $query): Builder
{
    return $query->where('type', 'posts');
}
```
If necessary, you may access the `resource` and `resourceId` for the request via the `NovaRequest` instance that is passed to your method:
app/Nova/~Resource.php
Copy
Ask AI
```
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Build a "relatable" query for the given resource.
 *
 * This query determines which instances of the model may be attached to other resources.
 */
public static function relatableTags(NovaRequest $request, Builder $query): Builder
{
    $resource = $request->route('resource'); // The resource type...
    $resourceId = $request->resourceId; // The resource ID...

    return $query->where('type', $resource);
}
```
#### [​](#relationship-types) Relationship Types
When a Nova resource depends on another resource via multiple fields, you will often assign the fields different names such as:
app/Nova/User.php
Copy
Ask AI
```
use Laravel\Nova\Fields\BelongsTo; 
use Laravel\Nova\Fields\BelongsToMany; 
use Laravel\Nova\Fields\HasMany; 
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array<int, \Laravel\Nova\Fields\Field>
 */
public function fields(NovaRequest $request): array
{
    return [
        BelongsTo::make('Current Team', 'currentTeam', Team::class),
        HasMany::make('Owned Teams', 'ownedTeams', Team::class),
        BelongsToMany::make('Teams', 'teams', Team::class),
    ];
}
```
In these situations, you should supply a third argument when defining the relationship to specify which Nova resource the relationship should utilize, since Nova may not be able to determine this via convention:
app/Nova/User.php
Copy
Ask AI
```
use Illuminate\Contracts\Database\Eloquent\Builder;
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\BelongsToMany;
use Laravel\Nova\Fields\Field;
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Build a "relatable" query for the given resource.
 *
 * This query determines which instances of the model may be attached to other resources.
 */
public static function relatableTeams(
    NovaRequest $request, 
    Builder $query, 
    Field $field
): Builder {
    if ($field instanceof BelongsToMany && $field->attribute === 'teams') {
        // ... 
    } elseif ($field instanceof BelongsTo && $field->attribute === 'currentTeam') {
        // ...
    }

    return $query;
}
```
## [​](#scout-filtering) Scout Filtering
If your application is leveraging the power of Laravel Scout for [search](./../search/scout-integration), you may also customize the `Laravel\Scout\Builder` query instance before it is sent to your search provider. To accomplish this, override the `scoutQuery` method on your resource class:
app/Nova/Post.php
Copy
Ask AI
```
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Scout\Builder as ScoutBuilder;

// ...

/**
 * Build a Scout search query for the given resource.
 */
public static function scoutQuery(
    NovaRequest $request, 
    ScoutBuilder $query
): ScoutBuilder {
    return $query->where('user_id', $request->user()->id);
}
```
Was this page helpful?
YesNo
[Validation](/docs/v5/resources/validation)[The Basics](/docs/v5/search/the-basics)
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.