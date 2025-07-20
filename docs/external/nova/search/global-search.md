# Nova - Search/Global-Search

*Source: https://nova.laravel.com/docs/v5/search/global-search*

---

Global Search - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchGlobal SearchDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsSearchGlobal SearchLearn how to use Nova’s global search feature to search across all your resources.Nova not only allows you to search within specific resources and relationships, you may also globally search across all your resources using the global search input located within the top-navigation bar of the Nova administration panel:

You can focus the global search input by pressing / (forward slash) on your keyboard. Pressing ESC (the escape key) will also close the global search input.
​Title / Subtitle Attributes
When a resource is shown within the search results, the results will display the “title” of the resource. For example, a User resource may specify the name attribute as its title. Then, when the resource is shown within the global search results, that attribute will be displayed.
To customize the “title” attribute of a resource, you may define a title property or title method on the resource class:
PropertyMethodCopyAsk AInamespace App\Nova;

class Team extends Resource 
{
    /**
     * The single value that should be used to represent the resource when being displayed.
     *
     * @var string
     */
    public static $title = &#x27;name&#x27;;
}

You may also display resource’s “avatar” next to the title in the search result by adding an Avatar field to the resource.
​Subtitles
You may also display a smaller “subtitle” attribute within the global search results. The subtitle will be placed directly under the title attribute. In this screenshot, you can see that the Post resource’s author is displayed as a subtitle, allowing quick identification of who wrote a given post:

To define a resource’s subtitle, you should override the subtitle method of the resource:
app/Nova/Post.phpCopyAsk AI/**
 * Get the search result subtitle for the resource.
 *
 * @return string
 */
public function subtitle()
{
    return &quot;Author: {$this-&gt;user-&gt;name}&quot;;
}

If your subtitle accesses information on a related resource, you should consider adding the related resource to your resource’s eager load array.
​Customization
​Limiting Global Search Results
You can limit the number of results that are returned via global search for a given resource by overriding the globalSearchResults property on the resource:
app/Nova/Post.phpCopyAsk AI/**
 * The maximum number of results to include when searching globally.
 *
 * @var int
 */
public static $globalSearchResults = 5;

​Global Search Debounce
You can configure the debounce timing of the global search field using the Nova::globalSearchDebounce method. Normally, this method should be called from within your application’s NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void 
{
    parent::boot();
    
    Nova::globalSearchDebounce(1); // 1 second
}

​Custom Avatars / Covers
If you are building a custom field that you would like to serve as the “avatar image” / cover art for global search results, your field should implement the Laravel\Nova\Contracts\Cover interface. This interface requires you to define a resolveThumbnailUrl method, which should return the URL of your desired “cover art”:
app/Nova/Team.phpCopyAsk AInamespace App\Nova;

class Team extends Resource 
{
    /**
     * Resolve the thumbnail URL for the field.
     *
     * @return string|null
     */
    public function resolveThumbnailUrl()
    {
        return &#x27;https://www.example.com/avatar/&#x27;.md5(strtolower($this-&gt;value)).&#x27;?s=300&#x27;;
    }
}

​Disabling Global Search for a Resource
By default, all Nova resources are globally searchable; however, you may exclude a given resource from the global search by overriding the globallySearchable property on the resource:
app/Nova/Team.phpCopyAsk AI/**
 * Indicates if the resource should be globally searchable.
 *
 * @var bool
 */
public static $globallySearchable = false;

​Disabling Global Search Globally
If you wish to completely disable global search inside of Nova, you can call the withoutGlobalSearch method from your App/Providers/NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::withoutGlobalSearch();
}
Was this page helpful?YesNoThe BasicsScout IntegrationOn this pageTitle / Subtitle AttributesSubtitlesCustomizationLimiting Global Search ResultsGlobal Search DebounceCustom Avatars / CoversDisabling Global Search for a ResourceDisabling Global Search GloballyLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, CodeGroup, Frame, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!CodeGroup) _missingMdxReference(\"CodeGroup\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"Nova not only allows you to search within specific resources and relationships, you may also globally search across all your resources using the global search input located within the top-navigation bar of the Nova administration panel:\"\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/global-search.png\",\n          alt: \"Global Search\"\n        })\n      })\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"You can focus the global search input by pressing \", _jsx(_components.code, {\n          children: \"/\"\n        }), \" (forward slash) on your keyboard. Pressing \", _jsx(_components.code, {\n          children: \"ESC\"\n        }), \" (the escape key) will also close the global search input.\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"title-%2F-subtitle-attributes\",\n      isAtRootLevel: \"true\",\n      children: \"Title / Subtitle Attributes\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When a resource is shown within the search resul