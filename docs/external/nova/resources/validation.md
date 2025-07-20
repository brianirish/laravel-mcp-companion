# Nova - Resources/Validation

*Source: https://nova.laravel.com/docs/v5/resources/validation*

---

Validation - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesValidationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesValidationNova provides a variety of ways to validate your resource fields.Unless you like to live dangerously, any Nova fields that are displayed on the Nova creation / update pages will need some validation. Thankfully, it’s a cinch to attach all of the Laravel validation rules you’re familiar with to your Nova resource fields. Let’s get started.
​Rules
​Attaching Rules
When defining a field on a resource, you may use the rules method to attach validation rules to the field:
app/Nova/~Resource.phpCopyAsk AIuse Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array
{
    return [
        Text::make(&#x27;Name&#x27;)
            -&gt;sortable()
            -&gt;rules(&#x27;required&#x27;, &#x27;max:255&#x27;),
    ];
}

Of course, if you are leveraging Laravel’s support for validation rule objects, you may attach those to resources as well:
CopyAsk AIuse App\Rules\ValidState;
use Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;State&#x27;)
    -&gt;sortable()
    -&gt;rules(&#x27;required&#x27;, new ValidState),

You may also provide rules to the rules method via an array or Closure:
CopyAsk AIuse App\Rules\ValidState;
use Laravel\Nova\Fields\Text;

// ...

// Using an array...
Text::make(&#x27;State&#x27;)-&gt;rules([&#x27;required&#x27;, new ValidState]),

// Using a Closure...
Text::make(&#x27;State&#x27;)-&gt;rules(fn ($request) =&gt; [
    &#x27;required&#x27;, 
    new ValidState(),
]);

Additionally, you may use custom closure rules to validate your resource fields:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;State&#x27;)
    -&gt;sortable()
    -&gt;rules(&#x27;required&#x27;, function($attribute, $value, $fail) {
        if (strtoupper($value) !== $value) {
            return $fail(&#x27;The &#x27;.$attribute.&#x27; field must be uppercase.&#x27;);
        }
    }),

​Creation Rules
If you would like to define rules that only apply when a resource is being created, you may use the creationRules method:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Email&#x27;)
    -&gt;sortable()
    -&gt;rules(&#x27;required&#x27;, &#x27;email&#x27;, &#x27;max:255&#x27;)
    -&gt;creationRules(&#x27;unique:users,email&#x27;),

​Update Rules
Likewise, if you would like to define rules that only apply when a resource is being updated, you may use the updateRules method. If necessary, you may use resourceId place-holder within your rule definition. This place-holder will automatically be replaced with the primary key of the resource being updated:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Email&#x27;)
    -&gt;sortable()
    -&gt;rules(&#x27;required&#x27;, &#x27;email&#x27;, &#x27;max:255&#x27;)
    -&gt;creationRules(&#x27;unique:users,email&#x27;)
    -&gt;updateRules(&#x27;unique:users,email,{{resourceId}}&#x27;),

​After Validation Hooks
Nova also provides several methods that allow you to perform tasks after a resource has been validated, providing the opportunity to perform more custom validation before the resource is persisted to the database:

afterValidation
afterCreationValidation
afterUpdateValidation

​The afterValidation Method
The afterValidation method will always be called after a resource has been validated during its creation or during an update. This method will be called before calling afterCreationValidation or afterUpdateValidation:
app/Nova/~Resource.phpCopyAsk AIuse Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-validation processing.
 *
 * @return void
 */
protected static function afterValidation( 
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator-&gt;errors()-&gt;add(&#x27;field&#x27;, &#x27;Something is wrong with this field!&#x27;);
    }
}

​The afterCreationValidation Method
The afterCreationValidation method will be called after a resource that is being created has been validated:
app/Nova/~Resource.phpCopyAsk AIuse Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-creation validation processing.
 * 
 * @return void
 */
protected static function afterCreationValidation(
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator-&gt;errors()-&gt;add(&#x27;field&#x27;, &#x27;Something is wrong with this field!&#x27;);
    }
}

​The afterUpdateValidation Method
The afterUpdateValidation method will be called after a resource that is being updated has been validated:
app/Nova/~Resource.phpCopyAsk AIuse Illuminate\Contracts\Validation\Validator as ValidatorContract;
use Laravel\Nova\Http\Requests\NovaRequest;

// ... 

/**
 * Handle any post-update validation processing.
 *
 * @return void
 */
protected static function afterUpdateValidation(
    NovaRequest $request, 
    ValidatorContract $validator
) {
    if (self::somethingElseIsInvalid()) {
        $validator-&gt;errors()-&gt;add(&#x27;field&#x27;, &#x27;Something is wrong with this field!&#x27;);
    }
}
Was this page helpful?YesNoRelationshipsAuthorizationOn this pageRulesAttaching RulesCreation RulesUpdate RulesAfter Validation HooksThe afterValidation MethodThe afterCreationValidation MethodThe afterUpdateValidation MethodLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"Unless you like to live dangerously, any Nova fields that are displayed on the Nova creation / update pages will need some validation. Thankfully, it’s a cinch to attach all of the Laravel validation rules you’re familiar with to your Nova resource fields. Let’s get started.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\