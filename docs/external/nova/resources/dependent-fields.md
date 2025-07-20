# Nova - Resources/Dependent-Fields

*Source: https://nova.laravel.com/docs/v5/resources/dependent-fields*

---

Dependent Fields - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesDependent FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesDependent FieldsDependent fields allow you to define fields that have unique configuration depending on the value of other fields.Dependent fields are created by invoking the dependsOn method when defining a field. The dependsOn method accepts an array of dependent field attributes and a closure that modifies the configuration of the current field instance.
Dependent fields allow advanced customization, such as toggling read-only mode, validation rules, and more based on the state of another field:
CopyAsk AIuse Laravel\Nova\Fields\FormData;
use Laravel\Nova\Fields\Select;
use Laravel\Nova\Fields\Text;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

return [
    Select::make(&#x27;Purchase Type&#x27;, &#x27;type&#x27;)
        -&gt;options([
            &#x27;personal&#x27; =&gt; &#x27;Personal&#x27;,
            &#x27;gift&#x27; =&gt; &#x27;Gift&#x27;,
        ]),

    // Recipient field configuration is customized based on purchase type...
    Text::make(&#x27;Recipient&#x27;)
        -&gt;readonly()
        -&gt;dependsOn(
            [&#x27;type&#x27;],
            function (Text $field, NovaRequest $request, FormData $formData) {
                if ($formData-&gt;type === &#x27;gift&#x27;) {
                    $field-&gt;readonly(false)-&gt;rules([&#x27;required&#x27;, &#x27;email&#x27;]);
                }
            }
        ),
];

To define dependent fields separately for creating and updating resources, you may use the dependsOnCreating and dependsOnUpdating methods.
​Supported Dependent Fields
The following field types may depend on other fields:

Audio
BelongsTo
Boolean
BooleanGroup
Color
Code
Country
Currency
Date
DateTime
File
Heading
Hidden
Image
KeyValue
Markdown
MorphTo
Number
Password
PasswordConfirmation
Select
Status
Textarea
Text
Timezone
Trix
URL
VaporAudio
VaporFile
VaporImage

The following field types may not be depended upon by other fields since they do not live-report their changes to Nova:

Audio
Code
File
Image
KeyValue
Status
Tag
Trix
VaporAudio
VaporFile
VaporImage

​Toggling Field Visibility Using dependsOn
One common use-case for dependent fields is toggling field visibility based on the value of another field. You can accomplish this using the hide and show methods:
CopyAsk AIuse Laravel\Nova\Fields\Boolean;
use Laravel\Nova\Fields\BelongsTo;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

Boolean::make(&#x27;Anonymous Comment&#x27;, &#x27;anonymous&#x27;)
    -&gt;onlyOnForms()
    -&gt;fillUsing(fn () =&gt; null)
    -&gt;default(true),

BelongsTo::make(&#x27;User&#x27;)
    -&gt;hide()
    -&gt;rules(&#x27;sometimes&#x27;)
    -&gt;dependsOn(&#x27;anonymous&#x27;, function (BelongsTo $field, NovaRequest $request, FormData $formData) {
        if ($formData-&gt;boolean(&#x27;anonymous&#x27;) === false) {
            $field-&gt;show()-&gt;rules(&#x27;required&#x27;);
        }
    }),

​Setting a Field’s Value Using dependsOn
Another common use-case for dependent fields is to set the value of a field based on the value of another field. You can accomplish this using the setValue method:
CopyAsk AIuse Laravel\Nova\Fields\DateTime;
use Laravel\Nova\Fields\FormData;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

DateTime::make(&#x27;Created At&#x27;),

DateTime::make(&#x27;Updated At&#x27;)
    -&gt;dependsOn([&#x27;created_at&#x27;], function (DateTime $field, NovaRequest $request, FormData $form) {
        $field-&gt;setValue(Carbon::parse($form-&gt;created_at)-&gt;addDays(7));
    }),

​Accessing Request Resource IDs
When interacting with dependent fields, you may retrieve the current resource and related resource IDs via the resource method:
CopyAsk AIBelongsTo::make(__(&#x27;Books&#x27;), &#x27;books&#x27;, Book::class),

Currency::make(&#x27;Price&#x27;)
    -&gt;dependsOn(&#x27;books&#x27;, function (Currency $field, NovaRequest $request, FormData $formData) {
        $bookId = (int) $formData-&gt;resource(Book::uriKey(), $formData-&gt;books);

        if ($bookId == 1) {
            $field-&gt;rules([
                &#x27;required&#x27;, &#x27;numeric&#x27;, &#x27;min:10&#x27;, &#x27;max:199&#x27;
            ])-&gt;help(&#x27;Price starts from $10-$199&#x27;);

            return;
        }

        $field-&gt;rules([
            &#x27;required&#x27;, &#x27;numeric&#x27;, &#x27;min:0&#x27;, &#x27;max:99&#x27;
        ])-&gt;help(&#x27;Price starts from $0-$99&#x27;);
    }),
Was this page helpful?YesNoFieldsDate FieldsOn this pageSupported Dependent FieldsToggling Field Visibility Using dependsOnSetting a Field’s Value Using dependsOnAccessing Request Resource IDsLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsxs(_components.p, {\n      children: [\"Dependent fields are created by invoking the \", _jsx(_components.code, {\n        children: \"dependsOn\"\n      }), \" method when defining a field. The \", _jsx(_components.code, {\n        children: \"dependsOn\"\n      }), \" method accepts an \", _jsx(_components.code, {\n        children: \"array\"\n      }), \" of dependent field attributes and a closure that modifies the configuration of the current field instance.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Dependent fields allow advanced customization, such as toggling read-only mode, validation rules, and more based on the state of another field:\"\n    }), \"\\n\", _jsx(CodeBlock, {\n      filename: \"\",\n      highlight: \"[9,18,19,20,21,22,23,24,25]\",\n      numberOfLines: \"26\",\n      language: \"php\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"php\",\n        children: _jsxs(_components.code, {\n          language: \"php\",\n          numberOfLines: \"26\",\n          childr