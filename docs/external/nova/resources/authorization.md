# Nova - Resources/Authorization

*Source: https://nova.laravel.com/docs/v5/resources/authorization*

---

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

### [​](#when-nova-%26-application-authorization-logic-differs) When Nova & Application Authorization Logic Differs

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

#### [​](#authorizing-attaching-%2F-detaching) Authorizing Attaching / Detaching

For many-to-many relationships, Nova uses a similar naming convention. However, instead of `add{Model}`, you should use an `attach{Model}` / `detach{Model}` naming convention. For example, imagine a `Podcast` model has a many-to-many relationship with the `Tag` model. If you would like to authorize which users can attach “tags” to a podcast, you may add an `attachTag` method to your podcast policy. In addition, you will li

*[Content truncated for length]*