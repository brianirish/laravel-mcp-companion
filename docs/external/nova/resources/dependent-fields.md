# Nova - Resources/Dependent-Fields

*Source: https://nova.laravel.com/docs/v5/resources/dependent-fields*

---

Dependent Fields - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesDependent FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageSupported Dependent FieldsToggling Field Visibility Using dependsOnSetting a Field’s Value Using dependsOnAccessing Request Resource IDsResourcesDependent FieldsDependent fields allow you to define fields that have unique configuration depending on the value of other fields.Dependent fields are created by invoking the dependsOn method when defining a field. The dependsOn method accepts an array of dependent field attributes and a closure that modifies the configuration of the current field instance.
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

​Accessing Request Res