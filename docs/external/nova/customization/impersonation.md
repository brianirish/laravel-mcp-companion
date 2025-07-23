# Nova - Customization/Impersonation

*Source: https://nova.laravel.com/docs/v5/customization/impersonation*

---

Impersonation - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
  --font-family-headings-custom: "Figtree";
  
  --font-family-body-custom: "Figtree";
  
}:root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperImpersonationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewEnabling ImpersonationCustomizing Impersonation AuthorizationInspecting Impersonation StateImpersonation EventsDigging DeeperImpersonationLearn how to impersonate other users in your application.​Overview
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
Was this page helpful?YesNoAuthenticationToolsAssistan