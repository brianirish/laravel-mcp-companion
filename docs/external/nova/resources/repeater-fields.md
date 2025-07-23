# Nova - Resources/Repeater-Fields

*Source: https://nova.laravel.com/docs/v5/resources/repeater-fields*

---

Repeater Fields - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesRepeater FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewRepeatablesGenerating RepeatablesConfirming Repeatable RemovalRepeater PresetsJSON PresetHasMany PresetUpserting Repeatables Using Unique FieldsRepeater Field CapabilitiesSupported FieldsPartially-Supported FieldsResourcesRepeater FieldsRepeater fields allow you to create and edit repeatable, structured data.​Overview
The Repeater field allows you to create and edit repeatable, structured data and store that data in a JSON column or HasMany relationship:
app/Nova/Invoice.phpCopyAsk AInamespace App\Nova;

use App\Nova\Repeaters;
use Laravel\Nova\Fields\ID;
use Laravel\Nova\Fields\Repeater;
use Laravel\Nova\Http\Requests\NovaRequest;
 
class Invoice extends Resource
{
	/**  
	 * Get the fields displayed by the resource. 
	 * 
	 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
	 */
	public function fields(NovaRequest $request): array
	{
		return [
			ID::make(),
			Repeater::make(&#x27;Line Items&#x27;)
				-&gt;repeatables([
					Repeaters\LineItem::make(),
				]),
		];
	}
}

After defining a Repeater field, your resource will have an elegant interface for adding and editing repeatable items in the field:

​Repeatables
A Repeatable object represents the repeatable data for a Repeater field. It defines the set of fields used for the repeatable item. It also optionally defines an Eloquent Model class when the Repeater is using the HasMany preset.
The Repeater field is not limited to a single type of repeatable. It also supports multiple “repeatable” types, which may contain their own unique field sets and models. These repeatables could be used to create interfaces for editing flexible content areas, similar to those offered by content management systems.
​Generating Repeatables
To generate a new Repeatable, invoke the nova:repeatable Artisan command:
CopyAsk AIphp artisan nova:repeatable LineItem

After invoking the command above, Nova generates a new file at app/Nova/Repeater/LineItem.php. This file contains a fields method in which you may list any supported Nova field. For example, below we will define a Repeatable representing a line item for an invoice:
app/Nova/Repeaters/LineItem.phpCopyAsk AInamespace App\Nova\Repeaters;

use Laravel\Nova\Http\Requests\NovaRequest;
use Laravel\Nova\Fields\Currency;
use Laravel\Nova\Fields\Number;
use Laravel\Nova\Fields\Repeater\Repeatable;
use Laravel\Nova\Fields\Textarea;

class LineItem extends Repeatable
{
	/**
	 * Get the fields displayed by the repeatable.
	 *
	 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
	 */
	public function fields(NovaRequest $request): array
	{
		return [
			Number::make(&#x27;Quantity&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;numeric&#x27;),
			Textarea::make(&#x27;Description&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;max:255&#x27;),
			Currency::make(&#x27;Price&#x27;)-&gt;rules(&#x27;required&#x27;, &#x27;numeric&#x27;),
		];
	}
}

​Confirming Repeatable Removal
You may instruct Nova to present a confirmation modal before removing a repeatable by invoking the confirmRemoval method when defining the repeatable:
CopyAsk AIuse App\Nova\Repeaters;
use Laravel\Nova\Fields\Repeater;
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
		Repeater::make(&#x27;Attachments&#x27;)-&gt;repeatables([
			Repeaters\File::make()-&gt;confirmRemoval(),
			Repeaters\Note::make(),
			Repeaters\Video::make()-&gt;confirmRemoval(),
		]),
	];
}

​Repeater Presets
The Repeater field includes two storage “presets” out-of-the-box: Json and HasMany. Each preset defines how the repeatable data