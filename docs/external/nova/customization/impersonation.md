# Nova - Customization/Impersonation

*Source: https://nova.laravel.com/docs/v5/customization/impersonation*

---

Impersonation - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperImpersonationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperImpersonationLearn how to impersonate other users in your application.​Overview
After deploying your application to production, you may occasionally need to “impersonate” another user of your application in order to debug problems your customers are reporting. Thankfully, Nova includes built-in functionality to handle this exact scenario.
​Enabling Impersonation
To enable user impersonation, add the Laravel\Nova\Auth\Impersonatable trait to your application’s User model:
app/Models/User.phpCopyAsk AInamespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Nova\Auth\Impersonatable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Impersonatable, Notifiable;

    // ...
}

Once the Impersonatable trait has been added to your application’s User model, an “Impersonate” action will be available via the inline action menu for the corresponding resource:

​Customizing Impersonation Authorization
By default, any user that has permission to view the Nova dashboard can impersonate any other user. However, you may customize who can impersonate other users and what users can be impersonated by defining canImpersonate and canBeImpersonated methods on your application’s Impersonatable model:
app/Models/User.phpCopyAsk AIuse Illuminate\Support\Facades\Gate;

// ...

/**
 * Determine if the user can impersonate another user.
 *
 * @return bool
 */
public function canImpersonate()
{
    return Gate::forUser($this)-&gt;check(&#x27;viewNova&#x27;);
}

/**
 * Determine if the user can be impersonated.
 *
 * @return bool
 */
public function canBeImpersonated()
{
    return true;
}

​Inspecting Impersonation State
By resolving an implementation of the Laravel\Nova\Contracts\ImpersonatesUsers interface via Laravel’s service container, you can inspect the current impersonation state of the application:
routes/web.phpCopyAsk AIuse App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Laravel\Nova\Contracts\ImpersonatesUsers;

Route::get(&#x27;/impersonation&#x27;, function (Request $request, ImpersonatesUsers $impersonator) {
    if ($impersonator-&gt;impersonating($request)) {
        $impersonator-&gt;stopImpersonating($request, Auth::guard(), User::class);
    }
});

​Impersonation Events
By default, you add additional customisation by using available events for Impersonations:

Laravel\Nova\Events\StartedImpersonating
Laravel\Nova\Events\StoppedImpersonating

For example, you may want to log impersonation events, which you can register listeners for in the boot method of your application’s AppServiceProvider or  EventServiceProvider:
app/Providers/EventServiceProvider.phpCopyAsk AIuse Illuminate\Support\Facades\Event;
use Laravel\Nova\Events\StartedImpersonating;
use Laravel\Nova\Events\StoppedImpersonating;

// ...

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Event::listen(StartedImpersonating::class, function ($event) {
        logger(&quot;User {$event-&gt;impersonator-&gt;name} started impersonating {$event-&gt;impersonated-&gt;name}&quot;);
    });

    Event::listen(StoppedImpersonating::class, function ($event) {
        logger(&quot;User {$event-&gt;impersonator-&gt;name} stopped impersonating {$event-&gt;impersonated-&gt;name}&quot;);
    });
}
Was this page helpful?YesNoAuthenticationToolsOn this pageOverviewEnabling ImpersonationCustomizing Impersonation AuthorizationInspecting Impersonation StateImpersonation EventsLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    img: \"img\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Frame, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"After deploying your application to production, you may occasionally need to “impersonate” another user of your application in order to debug problems your customers are reporting. Thankfully, Nova includes built-in functionality to handle this exact scenario.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"enabling-impersonation\",\n      isAtRootLevel: \"true\",\n      children: \"Enabling Impersonation\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"To enable user impersonation, add the \", _jsx(_components.code, {\n        children: \"Laravel\\\\Nova\\\\Auth\\\\Impersonatable\"\n      }), \" trait to your application’s \", _jsx(_components.code, {\n        children: \"User\"\n      }), \" model:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      filename: \"app/Models/User.php\",\n      highlight: \"[7,12]\",\n      numberOfLines: \"15\",\n      language: \"php\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"php\",\n        children: _jsxs(_components.code, {\n          language: \"php\",\n          numberOfLines: \"15\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \"namespace\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#4EC9B0\"\n              },\n              children: \" App\\\\Models\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"