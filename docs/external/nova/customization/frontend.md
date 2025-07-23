# Nova - Customization/Frontend

*Source: https://nova.laravel.com/docs/v5/customization/frontend*

---

CSS / JavaScript - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperCSS / JavaScriptDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageNova RequestsManual NavigationEvent BusNotificationsShortcutsGlobal VariablesLocalizationsUsing Nova MixinsVue DevToolsDigging DeeperCSS / JavaScriptLearn how to customize the CSS and JavaScript of your Nova application.When building custom Nova tools, resource tools, cards, and fields, you may use a variety of helpers that are globally available to your JavaScript components.
​Nova Requests
You may use the Nova.request() method to make XHR requests to backend routes provided by your application or custom tools, cards, and fields. The Nova.request() method is powered by Axios and offers the same API. However, the Nova.request() method configures its own instance of Axios that has pre-configured interceptors to properly handle and redirect on 401, 403, and 500 level HTTP server responses:
CopyAsk AINova.request().get(&#x27;/nova-vendor/stripe-inspector/endpoint&#x27;).then(response =&gt; {
    // ...
})

​Manual Navigation
The global Nova JavaScript object offers a visit method that may be invoked to navigate to other URLs within your Nova dashboard:
CopyAsk AI// Navigate to User&#x27;s detail page...
Nova.visit(`/resources/users/${userId}`)

// Navigate to remote URL...
Nova.visit({ url: &#x27;https://nova.laravel.com&#x27;, remote: true })

The visit method accepts an array of navigation options as its second argument. As the visit method uses Inertia’s own visit method behind the scenes, all of Inertia’s visit options are supported by Nova’s visit method:
CopyAsk AINova.visit(`/resources/users/${userId}`, {
  onFinish: () =&gt; Nova.success(`User ${userId} detail page.`)
})

​Event Bus
The global Nova JavaScript object may be used as an event bus by your custom components. The bus provides the following methods, which correspond to and have the same behavior as the event methods provided by tiny-emitter:
CopyAsk AINova.$on(event, callback)
Nova.$once(event, callback)
Nova.$off(event, callback)
Nova.$emit(event, [...args])

​Notifications
You may display toast notification to users of your custom frontend components by calling the success, error, info, or warning methods on the global Nova object:
CopyAsk AINova.success(&#x27;It worked!&#x27;)
Nova.error(&#x27;It failed!&#x27;)

​Shortcuts
Nova provides two convenience methods for managing keyboard shortcuts, powered by Mousetrap. You may use these methods within your custom components to register and unregister shortcuts:
CopyAsk AI// Add a single keyboard shortcut...
Nova.addShortcut(&#x27;ctrl+k&#x27;, event =&gt; {
    // Callback...
})

// Add multiple keyboard shortcuts...
Nova.addShortcut([&#x27;ctrl+k&#x27;, &#x27;command+k&#x27;], event =&gt; {
    // Callback...
})

// Add a sequence shortcut...
Nova.addShortcut(&#x27;* a&#x27;, event =&gt; {
    // Callback...
})

// Remove a shortcut...
Nova.disableShortcut(&#x27;ctrl+k&#x27;)

// Remove multiple shortcuts...
Nova.disableShortcut([&#x27;ctrl+k&#x27;, &#x27;command+k&#x27;])

​Global Variables
The global Nova JavaScript object’s config method allows you to get the current Nova base path and userId configuration values:
CopyAsk AIconst userId = Nova.config(&#x27;userId&#x27;);
const basePath = Nova.config(&#x27;base&#x27;);

However, you are free to add additional values to this object using the Nova::provideToScript method. You may call this method within a Nova::serving listener, which should typically be registered in the boot method of your application or custom component’s service provider:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Laravel\Nova\Nova;
use Laravel\Nova\Events\ServingNova;

// ...

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    parent::boot();

 