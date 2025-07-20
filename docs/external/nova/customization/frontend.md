# Nova - Customization/Frontend

*Source: https://nova.laravel.com/docs/v5/customization/frontend*

---

CSS / JavaScript - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperCSS / JavaScriptDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperCSS / JavaScriptLearn how to customize the CSS and JavaScript of your Nova application.When building custom Nova tools, resource tools, cards, and fields, you may use a variety of helpers that are globally available to your JavaScript components.
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

    Nova::serving(function (ServingNova $event) {
        Nova::provideToScript([
            &#x27;mail_driver&#x27; =&gt; config(&#x27;mail.default&#x27;),
        ]);
    });
}

Once the variable has been provided to Nova via the provideToScript method, you may access it using the global Nova JavaScript object’s config method:
CopyAsk AIconst driver = Nova.config(&#x27;mail_driver&#x27;);

​Localizations
Localization strings can be passed to the frontend via your NovaServiceProvider. To learn more, please consult the full custom localization documentation.
​Using Nova Mixins
Custom Nova tools, resource tools, cards, and other custom packages that are being developed within a nova-components directory of a Laravel application can utilize laravel-nova mixins by importing nova.mix.js Mix Extension from the Nova Devtool installation that is located within your root application’s vendor directory. This extension should be placed in your package’s webpack.mix.js:
webpack.mix.jsCopyAsk AIlet mix = require(&#x27;laravel-mix&#x27;)
mix.extend(&#x27;nova&#x27;, new require(&#x27;laravel-nova-devtool&#x27;))

mix
  .setPublicPath(&#x27;dist&#x27;)
  .js(&#x27;resources/js/card.js&#x27;, &#x27;js&#x27;)
  .vue({ version: 3 })
  .css(&#x27;resources/css/card.css&#x27;, &#x27;css&#x27;)
  .nova(&#x27;acme/analytics&#x27;)

Laravel Nova’s assets are built using lockfile version 3 and require NPM 9+.
​Vue DevTools
The following feature require the laravel/nova-devtool Composer package to be installed:
CopyAsk AIcomposer require --dev &quot;laravel/nova-devtool&quot;

By default, Nova’s JavaScript is compiled for production. As such, you will not be able to access the Vue DevTools out of the box without compiling Nova’s JavaScript for development. To accomplish this, you may issue the following terminal commands from the root of your Nova project:
ApplicationPackageCopyAsk AIphp artisan nova:enable-vue-devtool
Was this page helpful?YesNoFiltersAssetsOn this pageNova RequestsManual NavigationEvent BusNotificationsShortcutsGlobal VariablesLocalizationsUsing Nova MixinsVue DevToolsLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, CodeGroup, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!CodeGroup) _missingMdxReference(\"CodeGroup\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"When building custom Nova tools, resource tools, cards, and fields, you may use a variety of helpers