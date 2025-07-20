# Nova - Customization/Filters

*Source: https://nova.laravel.com/docs/v5/customization/filters*

---

Filters - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperFiltersDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperFiltersLearn how to build custom filters for your Nova resources.​Overview
Nova ships with several filter types; however, sometimes you may need a filter type that isn’t provided out of the box. For this reason, Nova allows you to build custom filters.
​Defining Filters
Custom filters may be generated using the nova:custom-filter Artisan command. By default, all new filters will be placed in the nova-components directory of your application. When generating a filter using the nova:custom-filter command, the filter name you pass to the command should follow the Composer vendor/package format. So, if we were building an age-range filter, we might run the following command:
CopyAsk AIphp artisan nova:custom-filter acme/age-range

When generating a filter, Nova will prompt you to install the filter’s NPM dependencies, compile its assets, and update your application’s composer.json file. All custom filters are registered with your application as a Composer “path” repository.
Nova filters include all of the scaffolding necessary to build your filter. Each filter even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Filters
Nova filters may be registered in your resource’s filters method. This method returns an array of filters available to the resource. To register your filter, add your filter to the array of filters returned by this method:
ConstructMakeCopyAsk AIuse Acme\AgeRange\AgeRange;
use Laravel\Nova\Http\Requests\NovaRequest;

// ...

/**
 * Get the filters available for the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Filters\Filter&gt;
 */
public function filters(NovaRequest $request): array
{
    return [
        new AgeRange,
    ];
}

​Building Filters
Each filter generated by Nova includes its own service provider and “filter” class. Using the age-range filter as an example, the filter class will be located at src/AgeRange.php.
The filter’s service provider is also located within the src directory of the filter, and is registered in your filter’s composer.json file so that it will be auto-loaded by the Laravel framework.
​The Filter Vue Component
When Nova generates your filter, it creates a resources/js/components/Filter.vue Vue component. This component contains the template and logic for your filter when it is displayed in the filter dropdown menu. By default, the component displays a simple select filter component, along with the needed code for updating the filter’s state.
​Managing Filter State
Custom Nova filters use Vuex to manage their state. By default, your filter’s Vue component stub contains the basic logic necessary to update the filter’s current state. When modifying your filter’s component, you should make sure the changes are committed to the Vuex store when your filter’s “selected” value changes:
CopyAsk AIhandleChange(event) {
    this.$store.commit(&#x27;updateFilterState&#x27;, {
        filterClass: this.filterKey,
        value: event.target.value,
    })

    this.$emit(&#x27;change&#x27;)
}

​Assets
When Nova generates your filter, resources/js and resources/css directories are generated for you. These directories contain your filter’s JavaScript and CSS.
​Registering Assets
Your Nova filter’s service provider registers your filter’s compiled assets so that they will be available to the Nova front-end:
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
        Nova::mix(&#x27;age-range&#x27;, __DIR__.&#x27;/../dist/mix-manifest.json&#x27;);

        Nova::translations(__DIR__.&#x27;/../resources/lang/en/age-range.json&#x27;);
    });
}

Your components are bootstrapped and registered in the resources/js/filter.js file. You are free to modify this file or register additional components here as needed.
​Compiling Assets
Your Nova filter contains a webpack.mix.js file, which is generated when Nova creates your filter. You may build your filter using the NPM dev and prod commands:
CopyAsk AI# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod

In addition, you may run the NPM watch command to auto-compile your assets when they are changed:
CopyAsk AInpm run watch
Was this page helpful?YesNoFieldsCSS / JavaScriptOn this pageOverviewDefining FiltersRegistering FiltersBuilding FiltersThe Filter Vue ComponentManaging Filter StateAssetsRegistering AssetsCompiling AssetsLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, CodeGroup, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!CodeGroup) _missingMdxReference(\"CodeGroup\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Nova ships with several filter types; however, sometimes you may need a filter type that isn’t provided out of the box. For this reason, Nova allows you to build custom filters.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"defining-filters\",\n      isAtRootLevel: \"true\",\n      children: \"Defining Filters\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Custom filters may be generated using the \", _jsx(_components.code, {\n        children: \"nova:custom-filter\"\n      }), \" Artisan command. By default, all new filters will be placed in the \", _jsx(_components.code, {\n        children: \"nova-components\"\n      }), \" directory of your application. When generating a filter using the \", _jsx(_components.code, {\n        children: \"nova:custom-filter\"\n      }), \" command, the filter name you pass to the command should follow the Composer \", _jsx(_components.code, {\n        children: \"vendor/package\"\n      }), \" format. So, if we were 