# Nova - Metrics/Defining-Metrics

*Source: https://nova.laravel.com/docs/v5/metrics/defining-metrics*

---

Defining Metrics - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationMetricsDefining MetricsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsMetricsDefining MetricsLearn how to define metrics in Nova.Nova metrics allow you to quickly gain insight on key business indicators for your application. For example, you may define a metric to display the total number of users added to your application per day, or the amount of weekly sales for a given product.
Nova offers several types of built-in metrics: value, trend, partition, and progress. We’ll examine each type of metric and demonstrate their usage below.
​Value Metrics
Value metrics display a single value and, if desired, its change compared to a previous time interval. For example, a value metric might display the total number of users created in the last thirty days compared with the previous thirty days:

Value metrics may be generated using the nova:value Artisan command. By default, all new metrics will be placed in the app/Nova/Metrics directory:
CopyAsk AIphp artisan nova:value NewUsers

Once your value metric class has been generated, you’re ready to customize it. Each value metric class contains a calculate method. This method should return a Laravel\Nova\Metrics\ValueResult instance. Don’t worry, Nova ships with a variety of helpers for quickly generating metric results.
In this example, we are using the count helper, which will automatically perform a count query against the specified Eloquent model for the selected range, as well as automatically retrieve the count for the “previous” range:
app/Nova/Metrics/NewUsers.phpCopyAsk AInamespace App\Nova\Metrics;

use App\Models\User;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\Value;
use Laravel\Nova\Metrics\ValueResult;
use Laravel\Nova\Nova;

class NewUsers extends Value
{
    /**
     * Calculate the value of the metric.
     */
    public function calculate(NovaRequest $request): ValueResult
    {
        return $this-&gt;count($request, User::class);
    }

    /**
     * Get the ranges available for the metric.
     */
    public function ranges(): array
    {
        return [
            30 =&gt; Nova::__(&#x27;30 Days&#x27;),
            60 =&gt; Nova::__(&#x27;60 Days&#x27;),
            365 =&gt; Nova::__(&#x27;365 Days&#x27;),
            &#x27;TODAY&#x27; =&gt; Nova::__(&#x27;Today&#x27;),
            &#x27;MTD&#x27; =&gt; Nova::__(&#x27;Month To Date&#x27;),
            &#x27;QTD&#x27; =&gt; Nova::__(&#x27;Quarter To Date&#x27;),
            &#x27;YTD&#x27; =&gt; Nova::__(&#x27;Year To Date&#x27;),
        ];
    }
}

​Value Query Types
Value metrics don’t only ship with a count helper. You may also use a variety of other aggregate functions when building your metric. Let’s explore each of them now.
​Average
The average method may be used to calculate the average of a given column compared to the previous time interval / range:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Post;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return $this-&gt;average($request, Post::class, &#x27;word_count&#x27;);
}

​Sum
The sum method may be used to calculate the sum of a given column compared to the previous time interval / range:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Order;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return $this-&gt;sum($request, Order::class, &#x27;price&#x27;);
}

​Max
The max method may be used to calculate the maximum value of a given column compared to the previous time interval / range:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Order;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return $this-&gt;max($request, Order::class, &#x27;total&#x27;);
}

​Min
The min method may be used to calculate the minimum value of a given column compared to the previous time interval / range:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Order;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return $this-&gt;min($request, Order::class, &#x27;total&#x27;);
}

​Value Ranges
Every value metric class contains a ranges method. This method determines the ranges that will be available in the value metric’s range selection menu. The array’s keys determine the number of days that should be included in the query, while the values determine the “human readable” text that will be placed in the range selection menu. Of course, you are not required to define any ranges at all:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse Laravel\Nova\Nova;

/**
 * Get the ranges available for the metric.
 */
public function ranges(): array
{
    return [
        30 =&gt; Nova::__(&#x27;30 Days&#x27;),
        60 =&gt; Nova::__(&#x27;60 Days&#x27;),
        365 =&gt; Nova::__(&#x27;365 Days&#x27;),
        &#x27;TODAY&#x27; =&gt; Nova::__(&#x27;Today&#x27;),
        &#x27;YESTERDAY&#x27; =&gt; Nova::__(&#x27;Yesterday&#x27;),
        &#x27;MTD&#x27; =&gt; Nova::__(&#x27;Month To Date&#x27;),
        &#x27;QTD&#x27; =&gt; Nova::__(&#x27;Quarter To Date&#x27;),
        &#x27;YTD&#x27; =&gt; Nova::__(&#x27;Year To Date&#x27;),
        &#x27;ALL&#x27; =&gt; Nova::__(&#x27;All Time&#x27;),
    ];
}

You may customize these ranges to suit your needs; however, if you are using the built-in “Today”, “Yesterday”, “Month To Date”, “Quarter To Date”, “Year To Date”, or “All Time” ranges, you should not change their keys.
​Zero Result Values
By default, Nova will handle results of 0 as a result containing no data. This may not always be correct, which is why you can use the allowZeroResult method to indicate that 0 is a valid value result:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return $this-&gt;result(0)
        -&gt;allowZeroResult();
}

​Formatting the Value
You can add a prefix and / or suffix to the Value metric’s result by invoking the prefix and suffix methods when returning the ValueResult instance:
app/Nova/Metrics/~Metric.phpCopyAsk AIuse App\Models\Order;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Metrics\ValueResult;

// ...

/**
 * Calculate the value of the metric.
 */
public function calculate(NovaRequest $request): ValueResult
{
    return