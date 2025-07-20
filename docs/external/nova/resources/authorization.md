# Nova - Resources/Authorization

*Source: https://nova.laravel.com/docs/v5/resources/authorization*

---

Authorization - Laravel Nova
              document.documentElement.style.setProperty('--font-family-headings-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-headings-custom', '');
              document.documentElement.style.setProperty('--font-family-body-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-body-custom', '');
            
    (function() {
      try {
        var bannerKey = "nova-laravel-bannerDismissed";
        var bannerContent = undefined;
        
        if (!bannerContent) {
          document.documentElement.setAttribute('data-banner-state', 'hidden');
          return;
        }
        
        var dismissedValue = localStorage.getItem(bannerKey);
        var shouldShowBanner = !dismissedValue || dismissedValue !== bannerContent;
        
        document.documentElement.setAttribute('data-banner-state', shouldShowBanner ? 'visible' : 'hidden');
      } catch (e) {
        document.documentElement.setAttribute('data-banner-state', 'hidden');
      }
    })();
  :root{--font-inter:'Inter', 'Inter Fallback';--font-jetbrains-mono:'JetBrains Mono', 'JetBrains Mono Fallback'}((e,i,s,u,m,a,l,h)=>{let d=document.documentElement,w=["light","dark"];function p(n){(Array.isArray(e)?e:[e]).forEach(y=>{let k=y==="class",S=k&&a?m.map(f=>a[f]||f):m;k?(d.classList.remove(...S),d.classList.add(a&&a[n]?a[n]:n)):d.setAttribute(y,n)}),R(n)}function R(n){h&&w.includes(n)&&(d.style.colorScheme=n)}function c(){return window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}if(u)p(u);else try{let n=localStorage.getItem(i)||s,y=l&&n==="system"?c():n;p(y)}catch(n){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true):root {
    --primary: 75 162 227;
    --primary-light: 75 162 227;
    --primary-dark: 75 162 227;
    --background-light: 255 255 255;
    --background-dark: 10 12 15;
    --gray-50: 245 247 249;
    --gray-100: 240 242 244;
    --gray-200: 224 227 229;
    --gray-300: 208 210 212;
    --gray-400: 160 163 165;
    --gray-500: 114 116 118;
    --gray-600: 82 84 86;
    --gray-700: 64 67 69;
    --gray-800: 39 42 44;
    --gray-900: 25 27 29;
    --gray-950: 12 15 17;
  }h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesAuthorizationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesAuthorizationNova leverages Laravel policies to authorize incoming requests.When Nova is accessed only by you or your development team, you may not need additional authorization before Nova handles incoming requests. However, if you provide access to Nova to your clients or a large team of developers, you may wish to authorize certain requests. For example, perhaps only administrators may delete records. Thankfully, Nova takes a simple approach to authorization that leverages many of the Laravel features you are already familiar with.
​Policies
To limit which users may view, create, update, or delete resources, Nova leverages Laravel’s authorization policies. Policies are simple PHP classes that organize authorization logic for a particular model or resource. For example, if your application is a blog, you may have a Post model and a corresponding PostPolicy within your application.
When manipulating a resource within Nova, Nova will automatically attempt to find a corresponding policy for the model. If Nova detects a policy has been registered for the model, it will automatically check that policy’s relevant authorization methods before performing their respective actions, such as:

viewAny
view
create
update
replicate
delete
restore
forceDelete

No additional configuration is required! So, for example, to determine which users are allowed to update a Post model, you simply need to define an update method on the model’s corresponding policy class:
app/Policies/PostPolicy.phpCopyAsk AInamespace App\Policies;

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
        return $user-&gt;type == &#x27;editor&#x27;;
    }
}

​Undefined Policy Methods
If a policy exists but is missing a method for a particular action, Nova will use the following default permission for each actions:
Policy ActionDefault PermissionviewAnyAllowedviewForbiddencreateForbiddenupdateForbiddenreplicateFallback to create and updatedeleteForbiddenforceDeleteForbiddenrestoreForbiddenadd{Model}Allowedattach{Model}AllowedattachAny{Model}Alloweddetach{Model}AllowedrunActionFallback to updaterunDestructiveActionFallback to delete
So, if you have defined a policy, don’t forget to define all of its relevant authorization methods so that the authorization rules for a given resource are explicit.
​Hiding Entire Resources
If you would like to hide an entire Nova resource from a subset of your dashboard’s users, you may define a viewAny method on the model’s policy class. If no viewAny method is defined for a given policy, Nova will assume that the user can view the resource:
app/Policies/PostPolicy.phpCopyAsk AIuse App\Models\User;

// ...

/**
 * Determine whether the user can view any posts.
 *
 * @return mixed
 */
public function viewAny(User $user)
{
    return in_array(&#x27;view-posts&#x27;, $user-&gt;permissions);
}

​When Nova &amp; Application Authorization Logic Differs
If you need to authorize actions differently when a request is initiated from within Nova versus your primary application, you may utilize Nova’s whenServing method within your policy. This method allows you to only execute the given callback if the request is a Nova request. An additional callback may be provided that will be executed for non-Nova requests:
app/Policies/PostPolicy.phpCopyAsk AIuse App\Models\User;
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
        return in_array(&#x27;nova:view-posts&#x27;, $user-&gt;permissions);
    }, function (Request $request) use ($user) {
        return in_array(&#x27;view-posts&#x27;, $user-&gt;permissions);
    });
}

​Using Separate Policy Classes for Nova Resources
You may also create a policy specifically for Nova resources instead of relying on the Eloquent model’s application level policy. To get started, generate a new Nova policy via the nova:policy command:
CopyAsk AIphp artisan nova:policy PostPolicy --resource=Post

The nova:policy command above will create a new policy class as App\Nova\Policies\PostPolicy. In addition, the generated policy will authorize against App\Nova\Post instead of App\Models\Post. To register the policy with your Nova resource, you should specify the policy within the resource’s $policy property:
app/Nova/Post.phpCopyAsk AInamespace App\Nova;

class Post extends Resource
{
    /**
     * The policy the resource corresponds to.
     *
     * @var class-string
     */
    public static $policy = Policies\PostPolicy::class;
}

​Relationships
We have already learned how to authorize the typical view, create, update, and delete actions, but what about relationship interactions? For example, if you are building a podcasting application, perhaps you would like to specify that only certain Nova users may add comments to podcasts. Again, Nova makes this simple by leveraging Laravel’s policies.
When working with relationships, Nova uses a simple policy method naming convention. To illustrate this convention, lets assume your application has Podcast resources and Comment resources. If you would like to authorize which users can add comments to a podcast, you should define an addComment method on your podcast model’s policy class:
app/Policies/PodcastPolicy.phpCopyAsk AIuse App\Models\User;
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

As you can see, Nova uses a simple add{Model} policy method naming convention for authorizing relationship actions.
​Authorizing Attaching / Detaching
For many-to-many relationships, Nova uses a similar naming convention. However, instead of add{Model}, you should use an attach{Model} / detach{Model} naming convention. For example, imagine a Podcast model has a many-to-many relationship with the Tag model. If you would like to authorize which users can attach “tags” to a podcast, you may add an attachTag method to your podcast policy. In addition, you will likely want to define the inverse attachPodcast on the tag policy:
app/Policies/PodcastPolicy.phpCopyAsk AIuse App\Models\Podcast;
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
    r