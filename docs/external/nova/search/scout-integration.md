# Nova - Search/Scout-Integration

*Source: https://nova.laravel.com/docs/v5/search/scout-integration*

---

Scout Integration - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchScout IntegrationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsSearchScout IntegrationIntegrate Laravel Scout with your Nova resources.By default, Nova searches your resources using the resource’s database columns.
However, this can become inefficient and lacks support for robust fuzzy matching capabilities provided by dedicated search engines.
For this reason, Nova integrates seamlessly with Laravel Scout. When the Laravel\Scout\Searchable trait is attached to a model associated with a Nova resource, Nova will automatically begin using Scout when performing searches against that resource. There is no other configuration required.
​Customizing Scout Searches
If you would like to call methods on the Laravel\Scout\Builder instance before it executes your search query against your search engine, you may override the scoutQuery method on your resource:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Scout\Builder as ScoutBuilder;

class User extends Resource 
{
    // ... 

    /**
     * Build a Scout search query for the given resource.
     */
    public static function scoutQuery(NovaRequest $request, ScoutBuilder $query): ScoutBuilder
    {
        return $query;
    }
}

​Limiting Scout Search Results
You can customize the amount of search results returned from your Scout search engine by defining the scoutSearchResults property on the resource class that is associated with the Scout searchable model:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource 
{
    // ...

    /**
     * The number of results to display when searching the resource using Scout.
     *
     * @var int
     */
    public static $scoutSearchResults = 200;
}

​Disabling Scout Search
You may disable Scout search support for a specific resource by defining a usesScout method on the resource class. When Scout search support is disabled, simple database queries will be used to search against the given resource, even if the associated resource model includes the Scout Searchable trait:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource 
{
    /**
     * Determine if this resource uses Laravel Scout.
     *
     * @return bool
     */
    public static function usesScout()
    {
        return false;
    }
}
Was this page helpful?YesNoGlobal SearchDefining FiltersOn this pageCustomizing Scout SearchesLimiting Scout Search ResultsDisabling Scout SearchLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"By default, Nova searches your resources using the resource’s database columns.\\nHowever, this can become inefficient and lacks support for robust fuzzy matching capabilities provided by dedicated search engines.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"For this reason, Nova integrates seamlessly with \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/scout\",\n        children: \"Laravel Scout\"\n      }), \". When the \", _jsx(_components.code, {\n        children: \"Laravel\\\\Scout\\\\Searchable\"\n      }), \" trait is attached to a model associated with a Nova resource, Nova will automatically begin using Scout when performing searches against that resource. There is no other configuration required.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"customizing-scout-searches\",\n      isAtRootLevel: \"true\",\n      children: \"Customizing Scout Searches\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If you would like to call methods on the \", _jsx(_components.code, {\n        children: \"Laravel\\\\Scout\\\\Builder\"\n      }), \" instance before it executes your search query against your search engine, you may override the \", _jsx(_components.code, {\n        children: \"scoutQuery\"\n      }), \" method on your resource:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      filename: \"app/Nova/User.php\",\n      numberOfLines: \"17\",\n      language: \"php\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"php\",\n        children: _jsxs(_components.code, {\n          language: \"php\",\n          numberOfLines: \"17\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \"namespace\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#4EC9B0\"\n              },\n              children: \" App\\\\Nova\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \";\"\n            })]\n          }), \"\\n\", _jsx(_components.span, {\n            className: \"line\"\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \"use\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \" Laravel\\\\Nova\\\\Http\\\\Requests\\\\\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#4EC9B0\"\n              },\n              children: \"NovaRequest\"\n            }), _jsx(_components.span, {\n              style: {\n                