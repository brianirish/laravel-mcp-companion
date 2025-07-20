# Nova - Releases

*Source: https://nova.laravel.com/docs/v5/releases*

---

Release Notes - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedRelease NotesDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsGet StartedRelease NotesLaravel Nova Release NotesNova 5 continues the improvements made in Nova 4.x by introducing support for tab panels, searchable select filters, dependent field improvements, third party component improvements, and dependency modernization with support for Inertia.js 2.x.
​Modernizing Dependencies
Nova 5 removes support for Laravel 8.x and 9.x, while also requiring PHP 8.1+. This dependency upgrade allows for deeper integration with the Laravel ecosystem, including Fortify, Prompts, and Pennant.
Furthermore, Nova’s frontend code has been updated to utilize Vue 3.5, Heroicons 2.x, and Inertia.js 2.x. Please refer to the Nova upgrade guide for a detailed description of these changes and how they affect your application.
​Tab Panels
Nova 5 further improves the resource UI with the introduction of Tabs Panels  on the resource detail and form pages:
app/Nova/Event.phpCopyAsk AIuse Laravel\Nova\Fields\HasMany;
use Laravel\Nova\Fields\HasManyThrough;
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
        // ...

        Tab::group(&#x27;Details&#x27;, [
            Tab::make(&#x27;Purchases&#x27;, [ /* List of fields */ ]),
            Tab::make(&#x27;Registrations&#x27;, [ /* List of fields */ ]),
            Tab::make(&#x27;Event &amp; Venue&#x27;, [ /* List of fields */ ]),
        ]),

        Tab::group(attribute: &#x27;Relations&#x27;, fields: [
            HasMany::make(&#x27;Orders&#x27;, &#x27;orders&#x27;, Order::class),
            HasManyThrough::make(&#x27;Tickets&#x27;, &#x27;tickets&#x27;, Ticket::class),
        ]),
    ];
}

For example, the code snippet above will generate the following tabs:

To learn more about adding tab panels to your Nova resources, check out the tab documentation.
​Fields &amp; Filters Improvements
​New Dependent Computed Field via Field::computed() method
Nova 5 introduces an enhanced computed method that builds upon the previous computed fields feature. While computed fields have always been valuable for displaying additional resource information, they previously lacked a unique $attribute identifier, which limited their use as dependent fields. This limitation has been resolved in Nova 5:
CopyAsk AIuse Laravel\Nova\Fields\Boolean;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

Boolean::make(&#x27;Would you like to leave a comment?&#x27;, &#x27;comment_boolean&#x27;)
    -&gt;computed(),

Text::make(&#x27;Comment&#x27;)
    -&gt;hidden()
    -&gt;dependsOn(&#x27;comment_boolean&#x27;, function (Text $field, NovaRequest $request, FormData $formData) {
        if ($formData-&gt;boolean(&#x27;comment_boolean&#x27;) === true) {
            $field-&gt;show();
        }
    }),

More information on computed fields can be found within the computed field documentation.
​New Field::immutable() method
While readonly fields disable a field’s input and prevent form submission of its value, immutable fields offer more flexibility. By invoking the immutable method on a field, you can prevent users from modifying the field’s value while still allowing it to be submitted with the form.
You may also pass a boolean argument to the immutable method to dynamically control whether a field should be immutable:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;)-&gt;immutable(),

Further reading is available on the documentation.
​Other Field Improvements

Enums may now be used as Select::options()
Searchable select filters are now supported
JSON Repeater fields are now displayed on the resource detail page

​Separate Policy Classes for Nova Resources
In previous Nova releases, Nova resources shared authorization policies with your user-facing application. This approach to authorization can present problems if your application’s authorization logic differs from how resource authorization should be handled for Nova operations.
In Nova 5, you may now create a separate policy class that is only used for operations that are triggered via Nova:
CopyAsk AIphp artisan nova:policy


To enable the new policy you need to add the following code:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource
{
    /**
     * The policy the resource corresponds to.
     *
     * @var class-string
     */
    public static $policy = Policies\UserPolicy::class;
}

Further reading is available on the Authorization documentation.Was this page helpful?YesNoInstallationUpgrade GuideOn this pageModernizing DependenciesTab PanelsFields &amp; Filters ImprovementsNew Dependent Computed Field via Field::computed() methodNew Field::immutable() methodOther Field ImprovementsSeparate Policy Classes for Nova ResourcesLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Frame, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"Nova 5 continues the improvements made in Nova 4.x by introducing support for tab panels, searchable select filters, dependent field improvements, third party component improvements, and dependency modernization with support for Inertia.js 2.x.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"modernizing-dependencies\",\n      isAtRootLevel: \"true\",\n      children: \"Modernizing Dependencies\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Nova 5 removes support for Laravel 8.x and 9.x, while also requiring PHP 8.1+. This dependency upgrade allows for deeper integration with the Laravel ecosystem, including Fortify, Prompts, and Pennant.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Furthermore, Nova’s frontend code has been updated to utilize Vue 3.5, Heroicons 2.x, and Inertia.js 2.x. Ple