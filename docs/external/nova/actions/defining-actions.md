# Nova - Actions/Defining-Actions

*Source: https://nova.laravel.com/docs/v5/actions/defining-actions*

---

Defining Actions - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationActionsDefining ActionsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsActionsDefining ActionsDefining actions in NovaNova actions allow you to perform custom tasks on one or more Eloquent models. For example, you might write an action that sends an email to a user containing account data they have requested. Or, you might write an action to transfer a group of records to another user.
Once an action has been attached to a resource definition, you may initiate it from the resource’s index or detail pages:

If an action is enabled for display on the resource’s table row, you may also initiate the action from the resource’s action dropdown menu via the resource index page. These actions are referred to as “Inline Actions”:

​Overview
Nova actions may be generated using the nova:action Artisan command. By default, all actions are placed in the app/Nova/Actions directory:
CopyAsk AIphp artisan nova:action EmailAccountProfile

You may generate a destructive action by passing the --destructive option:
CopyAsk AIphp artisan nova:action DeleteUserData --destructive

To learn how to define Nova actions, let’s look at an example. In this example, we’ll define an action that sends an email message to a user or group of users:
app/Nova/Actions/EmailAccountProfile.phpCopyAsk AInamespace App\Nova\Actions;

use App\Models\AccountData;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Collection;
use Laravel\Nova\Actions\Action;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Fields\ActionFields;

class EmailAccountProfile extends Action
{
    use InteractsWithQueue;
    use Queueable;

    /**
     * Perform the action on the given models.
     *
     * @return mixed
     */
    public function handle(ActionFields $fields, Collection $models)
    {
        foreach ($models as $model) {
            (new AccountData($model))-&gt;send();
        }
    }

    /**
    * Get the fields available on the action.
     *
     * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
     */
    public function fields(NovaRequest $request): array
    {
        return [];
    }
}

The most important method of an action is the handle method. The handle method receives the values for any fields attached to the action, as well as a collection of selected models. The handle method always receives a Collection of models, even if the action is only being performed against a single model.
Within the handle method, you may perform whatever tasks are necessary to complete the action. You are free to update database records, send emails, call other services, etc. The sky is the limit!
​Action Titles
Typically, Nova utilizes the action’s class name to determine the displayable name of the action that should be shown in the action selection menu. If you would like to change the displayable name of the action, you may define a name property on the action class:
app/Nova/Actions/EmailAccountProfile.phpCopyAsk AI/**
 * The displayable name of the action.
 *
 * @var \Stringable|string
 */
public $name = &#x27;Send Account Profile via E-mail&#x27;;

​Destructive Actions
You may designate an action as destructive or dangerous by defining an action class that extends Laravel\Nova\Actions\DestructiveAction. This will change the color of the action’s confirm button to red:

When a destructive action is added to a resource that has an associated authorization policy, the policy’s delete method must return true in order for the action to run.
​Action Callbacks
The Action::then method should not be utilized if your action is queued. To achieve similar functionality when using queued actions, you should leverage Nova’s action batching callbacks.
When running an action against multiple resources, you may wish to execute some code after the action has completed executing against all of the resources. For example, you may wish to generate a report detailing all of the changes for the selected resources. To accomplish this, you may invoke the then method when registering your action.
The then methods accepts a closure which will be invoked when the action has finished executing against all of the selected resources. The closure will receive a flattened Laravel collection containing the values that were returned by the action.
For example, note that the following action’s handle method returns the $models it receives:
app/Nova/Actions/EmailAccountProfile.phpCopyAsk AIuse App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 */
public function handle(ActionFields $fields, Collection $models): Collection
{
    foreach ($models as $model) {
        (new AccountData($model))-&gt;send();
    }

    return $models;
}

When registering this action on a resource, we may use the then callback to access the returned models and interact with them after the action has finished executing:
app/Nova/~Resource.phpCopyAsk AIuse App\Nova\Actions\EmailAccountProfile;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the actions available for the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Actions\Action&gt;
 */
public function actions(NovaRequest $request): array 
{
    return [
        (new Actions\EmailAccountProfile)-&gt;then(function ($models) {
            $models-&gt;each(function ($model) {
                //
            });
        }),
    ];
}

​Action Fields
Sometimes you may wish to gather additional information from the user before dispatching an action. For this reason, Nova allows you to attach most of Nova’s supported fields directly to an action. When the action is initiated, Nova will prompt the user to provide input for the fields:

To add a field to an action, add the field to the array of fields returned by the action’s fields method:
app/Nova/Actions/EmailAccountProfile.phpCopyAsk AIuse Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields available on the action.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array 
{
    return [
        Text::make(&#x27;Subject&#x27;),
    ];
}

Finally, within your action’s handle method, you may access your fields using dynamic accessors on the provided ActionFields instance:
app/Nova/Actions/EmailAccountProfile.phpCopyAsk AIuse App\Models\AccountData;
use Illuminate\Support\Collection;
use Laravel\Nova\Fields\ActionFields;

// ...

/**
 * Perform the action on the given models.
 *
 * @return mixed
 */
public function handle(ActionFields $fields, Collection $models)
{
    foreach ($models as $model) {
        (new AccountData($model))-&gt;send($fields-&gt;subject);
    }
}

​Action Fields Default Values
You may use the default method to se