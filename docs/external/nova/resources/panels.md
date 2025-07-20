# Nova - Resources/Panels

*Source: https://nova.laravel.com/docs/v5/resources/panels*

---

Field Panels - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesField PanelsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesField PanelsIf your resource contains many fields, your resource “detail” page can become crowded. For that reason, you may choose to break up groups of fields into their own “panels”:

You may accomplish this by creating a new Panel instance within the fields method of a resource. Each panel requires a name and an array of fields that belong to that panel:
app/Nova/~Resource.phpCopyAsk AIuse Laravel\Nova\Panel;
use Laravel\Nova\Fields\Date;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
    return [
        ID::make()-&gt;sortable(),

        Panel::make(&#x27;Profile&#x27;, [
            Text::make(&#x27;Full Name&#x27;),
            Date::make(&#x27;Date of Birth&#x27;),
            Text::make(&#x27;Place of Birth&#x27;),
        ]),
    ];
}

​Limiting Displayed Fields
You may limit the amount of fields shown in a panel by default using the limit method:
CopyAsk AIuse Laravel\Nova\Panel;

// ...

Panel::make(&#x27;Profile&#x27;, [
    Text::make(&#x27;Full Name&#x27;),
    Date::make(&#x27;Date of Birth&#x27;),
    Text::make(&#x27;Place of Birth&#x27;),
])-&gt;limit(1),

Panels with a defined field limit will display a Show All Fields button in order to allow the user to view all of the defined fields when needed.
​Collapsible Panels
You may allow field panels to be collapsible by invoking the collapsible method when defining the panel. This method utilizes JavaScript’s localStorage feature to remember the current state of the panel between requests:
CopyAsk AIuse Laravel\Nova\Panel;

// ...

Panel::make(&#x27;Profile&#x27;, [
    Text::make(&#x27;Full Name&#x27;),
    Date::make(&#x27;Date of Birth&#x27;),
    Text::make(&#x27;Place of Birth&#x27;),
])-&gt;collapsible(),

You may indicate that a panel should always be collapsed by default via the collapsedByDefault method:
CopyAsk AIuse Laravel\Nova\Panel;

// ...

Panel::make(&#x27;Profile&#x27;, [
    Text::make(&#x27;Full Name&#x27;),
    Date::make(&#x27;Date of Birth&#x27;),
    Text::make(&#x27;Place of Birth&#x27;),
])-&gt;collapsedByDefault(),

​Tabs
The Tab panel allows you to organize resource fields and relationships within tab panels:

To create a tab panel when defining your resource’s fields, provide the tab group title and array of tabs to the Tab::group method. Each individual tab may be constructed using Tab::make and receives a tab title and array of fields:
app/Nova/Event.phpCopyAsk AIuse Laravel\Nova\Fields\Currency;
use Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\HasManyThrough;
use Laravel\Nova\Fields\Hidden;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Tabs\Tab;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field|\Laravel\Nova\Panel&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        ID::make()-&gt;sortable(),

        // ...

        Tab::group(&#x27;Details&#x27;, [
            Tab::make(&#x27;Purchases&#x27;, [
                Currency::make(&#x27;Price&#x27;)-&gt;asMinorUnits(),
                Number::make(&#x27;Tickets Available&#x27;),
                Number::make(&#x27;Tickets Sold&#x27;),
            ]),

            Tab::make(&#x27;Registrations&#x27;, [
                // ...
            ]),

            Tab::make(&#x27;Event &amp; Venue&#x27;, [
                // ...
            ]),
        ]),

        Tab::group(&#x27;Relations&#x27;, [
            HasMany::make(&#x27;Orders&#x27;),
            HasManyThrough::make(&#x27;Tickets&#x27;),
        ]),
    ]
}

​Omitting Tab Group Titles
Tab group titles may be omitted by simply providing fields to the Tab::group method:
CopyAsk AIuse Laravel\Nova\Tabs\Tab;

// ...

Tab::group(fields: [
    HasMany::make(&#x27;Orders&#x27;),
    HasManyThrough::make(&#x27;Tickets&#x27;),
]),
Was this page helpful?YesNoRepeater FieldsRelationshipsOn this pageLimiting Displayed FieldsCollapsible PanelsTabsOmitting Tab Group TitlesLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    img: \"img\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Frame, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"If your resource contains many fields, your resource “detail” page can become crowded. For that reason, you may choose to break up groups of fields into their own “panels”:\"\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/panels.png\",\n          alt: \"Field Panel Example\"\n        })\n      })\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may accomplish this by creating a new \", _jsx(_components.code, {\n        children: \"Panel\"\n      }), \" instance within the \", _jsx(_components.code, {\n        children: \"fields\"\n      }), \" method of a resource. Each panel requires a name and an array of fields that belong to that panel:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      filename: \"app/Nova/~Resource.php\",\n      highlight: \"[1,18,19,20,21,22]\",\n      numberOfLines: \"24\",\n      language: \"php\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"php\",\n        children: _jsxs(_components.code, {\n          language: \"php\",\n          numberOfLines: \"24\",\n          children: [_jsxs(_components.span, {\n            className: \"line line-highlight\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n   