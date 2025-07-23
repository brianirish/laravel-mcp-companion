# Nova - Resources/Fields

*Source: https://nova.laravel.com/docs/v5/resources/fields*

---

Fields - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesFieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageDefining FieldsField Column ConventionsShowing / Hiding FieldsShowing Fields When PeekingResource Preview ModalDynamic Field MethodsDefault ValuesField Placeholder TextField HydrationSortable FieldsField TypesAudio FieldAvatar FieldBadge FieldBoolean FieldCustomizing True / False ValuesBoolean Group FieldCode FieldEditing JSONSyntax HighlightingColor FieldCountry FieldCurrency FieldDate FieldDateTime FieldEmail FieldFile FieldGravatar FieldHeading FieldHidden FieldID FieldImage FieldKeyValue FieldCustomizing KeyValue LabelsMarkdown FieldMarkdown File UploadsMultiSelect FieldNumber FieldPassword FieldPassword Confirmation FieldSelect FieldUsing Enum as OptionsSearchable Select FieldsSlug FieldSparkline FieldUsing Trend MetricsCustomizing the ChartStatus FieldStack FieldLine FieldsPassing Closures to Line FieldsTag FieldPreviewing TagsDisplaying Tags as ListsCreating New Tags InlineAdjusting the Inline Creation Modal’s SizePreloading Available TagsText FieldText Field SuggestionsFormatting Text as LinksCopying Text Field Values to the ClipboardSetting maxlength on Text FieldsTextarea FieldSetting maxlength on Textarea FieldsTimezone FieldTrix FieldTrix File UploadsUI-Avatar FieldURL FieldVapor File FieldVapor Image FieldValidating Vapor Image / File FieldsComputed FieldsCustomizationReadonly FieldsImmutable FieldsRequired FieldsNullable FieldsField Placeholder TextField Help TextField StackingFull Width FieldsField Text AlignmentField Resolution / FormattingFilterable FieldsExtending FieldsMacro ArgumentsMacro on Specific FieldsResourcesFieldsNova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.​Defining Fields
Each Nova resource contains a fields method. This method returns an array of fields, which generally extend the Laravel\Nova\Fields\Field class. Nova ships with a variety of fields out of the box, including fields for text inputs, booleans, dates, file uploads, Markdown, and more.
To add a field to a resource, you may simply add it to the resource’s fields method. Typically, fields may be created using their static make method. This method accepts several arguments; however, you usually only need to pass the “human readable” name of the field. Nova will automatically “snake case” this string to determine the underlying database column:
app/Nova/User.phpCopyAsk AIuse Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Text;
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
        ID::make()-&gt;sortable(),
        Text::make(&#x27;Name&#x27;)-&gt;sortable(),
    ];
}

​Field Column Conventions
As noted above, Nova will “snake case” the displayable name of the field to determine the underlying database column. However, if necessary, you may pass the column name as the second argument to the field’s make method:
CopyAsk AIuse Laravel\Nova\Fields\Text;

// ...

Text::make(&#x27;Name&#x27;, &#x27;name_column&#x27;),

If the field has a JSON, ArrayObject, or array cast assigned to it, you may use the -&gt; operator to specify nested properties within the field:
CopyAsk AIuse Laravel\Nova\Fields\Timezone;

// ...

Timezone::make(&#x27;User Timezone&#x27;, &#x27;settings-&gt;timezone&#x27;),

​Showing / Hiding Fields
Often, you will only want to display a field in certain situations. For example, there is typically no need to show a Password field on a resource index listing. Likewise, you may wish to only display a Created At field on the creation / update forms. Nova makes it a breeze to hide / show