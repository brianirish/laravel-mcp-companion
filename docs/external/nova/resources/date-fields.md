# Nova - Resources/Date-Fields

*Source: https://nova.laravel.com/docs/v5/resources/date-fields*

---

Date Fields - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesDate FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesDate FieldsDate fields allow you to collect and display date and time information.Nova offers two types of date fields: Date and DateTime. As you may have guessed, the Date field does not store time information while the DateTime field does:
CopyAsk AIuse Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\DateTime;

// ...

Date::make(&#x27;Birthday&#x27;),
DateTime::make(&#x27;Created At&#x27;),

​Options
​Steps
By default, Nova will set a minimum “step” of 1 day for Date fields and 1 second for DateTime fields. You may modify the “step” value for both of these fields by providing an integer or Carbon\CarbonInterval to the field’s step methods:
CopyAsk AIuse Carbon\CarbonInterval;
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\DateTime;

// ...

Date::make(&#x27;Expired On&#x27;)-&gt;step(7),
Date::make(&#x27;Expired On&#x27;)-&gt;step(CarbonInterval::weeks(1)),

DateTime::make(&#x27;Published At&#x27;)-&gt;step(60),
DateTime::make(&#x27;Published At&#x27;)-&gt;step(CarbonInterval::minutes(1)),

​Minimum and Maximum Values
Sometimes you may wish to explicitly define minimum and maximum values for Date or DateTime fields. This can be done by passing a valid date expression, a date format supported by strtotime, or an instance of Carbon\CarbonInterface to the min and max methods of these fields:
CopyAsk AIuse Carbon\Carbon;
use Laravel\Nova\Fields\Date;

// ...

Date::make(&#x27;Expired On&#x27;)
    -&gt;min(&#x27;tomorrow&#x27;)
    -&gt;max(&#x27;next week&#x27;),

Date::make(&#x27;Expired On&#x27;)
    -&gt;min(Carbon::tomorrow())
    -&gt;max(Carbon::today()-&gt;addWeek(1)),

​Timezones
By default, Nova users will always see dates presented in your application’s “server-side” timezone as defined by the timezone configuration option in your application’s config/app.php configuration file.
​Customizing the Timezone
Sometimes you may wish to explicitly define the Nova user’s timezone instead of using the application’s timezone configuration. For example, perhaps your application allows users to select their own timezone so that they always see consistent date timezones even when traveling around the world.
To accomplish this, you may use the Nova::userTimezone method. Typically you should call this method in the boot method of your application’s NovaServiceProvider:
app/Nova/NovaServiceProvider.phpCopyAsk AIuse Laravel\Nova\Nova;
use Illuminate\Http\Request;

// ... 

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::userTimezone(function (Request $request) {
        return $request-&gt;user()?-&gt;timezone;
    });
}
Was this page helpful?YesNoDependent FieldsFile FieldsOn this pageOptionsStepsMinimum and Maximum ValuesTimezonesCustomizing the TimezoneLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsxs(_components.p, {\n      children: [\"Nova offers two types of date fields: \", _jsx(_components.code, {\n        children: \"Date\"\n      }), \" and \", _jsx(_components.code, {\n        children: \"DateTime\"\n      }), \". As you may have guessed, the \", _jsx(_components.code, {\n        children: \"Date\"\n      }), \" field does not store time information while the \", _jsx(_components.code, {\n        children: \"DateTime\"\n      }), \" field does:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"7\",\n      language: \"php\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"php\",\n        children: _jsxs(_components.code, {\n          language: \"php\",\n          numberOfLines: \"7\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \"use\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \" Laravel\\\\Nova\\\\Fields\\\\\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#4EC9B0\"\n              },\n              children: \"Date\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \";\"\n            })]\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \"use\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \" Laravel\\\\Nova\\\\Fields\\\\\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#4EC9B0\"\n              },\n              children: \"DateTime\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \";\"\n            })]\n          }), \"\\n\", _jsx(_components.span, {\n            className: \"line\"\n          }), \"\\n\", _jsx(_components.span, {\n            className: \"line\",\n            children: _jsx(_components.span, {\n              style: {\n                color: \"#6E7781\",\n                \"--shiki-dark\": \"#6A9955\"\n              },\n    