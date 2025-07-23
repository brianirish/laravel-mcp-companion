# Nova - Metrics/Registering-Metrics

*Source: https://nova.laravel.com/docs/v5/metrics/registering-metrics*

---

Registering Metrics - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationMetricsRegistering MetricsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewDetail MetricsDashboard MetricsAuthorizationDefault Metric RangeMetric SizesMetric Help Text / TooltipsRefreshing MetricsRefresh After ActionsRefresh After Filter ChangesMetricsRegistering MetricsLearn how to register metrics in Nova.​Overview
Once you have defined a metric, you are ready to attach it to a resource. Each resource generated by Nova contains a cards method. To attach a metric to a resource, you should simply add it to the array of metrics / cards returned by this method:
ConstructMakeCopyAsk AIuse App\Nova\Metrics\UsersPerDay;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the cards available for the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Card&gt;
 */
public function cards(NovaRequest $request): array
{
    return [
        new UsersPerDay,
    ];
}

​Detail Metrics
In addition to placing metrics on the resource index page, you may also attach a metric to the resource detail page. For example, if you are building a podcasting application, you may wish to display the total number of podcasts created by a specific user over time. To instruct a metric to be displayed on the detail page instead of the index page, invoke the onlyOnDetail method when registering your metric:
app/Nova/~Resource.phpCopyAsk AIuse Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the cards available for the request.
 *
 * @return array&lt;int, \Laravel\Nova\Card&gt;
 */
public function cards(NovaRequest $request): array
{
    return [
        Metrics\PodcastCount::make()
            -&gt;onlyOnDetail(),
    ];
}

Of course, you will need to modify your metric’s query to only gather metric data on the resource for which it is currently being displayed. To accomplish this, your metric’s calculate method may access the resourceId property on the incoming $request:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Podcast;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\TrendResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): TrendResult
{
    return $this-&gt;count(
        $request, 
        Podcast::where(&#x27;user_id&#x27;, $request-&gt;resourceId)
    );
}

​Dashboard Metrics
You are also free to add metrics to your primary Nova “dashboard”, which is the default page that Nova displays after login. By default, this page displays some helpful links to the Nova documentation via the built-in Help card. To add a metric to your dashboard, add the metric to the array of cards returned by the cards method of your Dashboard class:
app/Nova/Dashbaords/~Dashboard.phpCopyAsk AIuse App\Nova\Metrics\NewUsers;

// ...

/**
 * Get the cards that should be displayed on the Nova dashboard.
 *
 * @return array&lt;int, \Laravel\Nova\Card&gt;
 */
public function cards(): array
{
    return [
        new NewUsers,
    ];
}

​Authorization
If you would like to only expose a given metric to certain users, you may invoke the canSee method when registering your metric. The canSee method accepts a closure which should return true or false. The closure will receive the incoming HTTP request:
CopyAsk AIuse App\Models\User;
use App\Nova\Metrics\UsersPerDay;

// ...

UsersPerDay::make()
    -&gt;canSee(function ($request) {
        return $request-&gt;user()-&gt;can(&#x27;viewUsersPerDay&#x27;, User::class);
    }),

In the example above, we are using Laravel’s Authorizable trait’s can method on our User model to determine if the authorized user is authorized for the viewUsersPerDay action. However, since proxying to authorization policy methods is a common use-case for canSee, you may use the canSeeWhen method to achieve the same behavior. 