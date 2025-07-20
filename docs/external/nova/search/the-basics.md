# Nova - Search/The-Basics

*Source: https://nova.laravel.com/docs/v5/search/the-basics*

---

The Basics - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchThe BasicsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsSearchThe BasicsLearn how to define searchable columns for your Nova resources.​Searchable Columns
To define which resource fields are searchable, you may assign an array of database columns to the search property or searchableColumns method of your resource class. This array includes the id column by default:
PropertyMethodCopyAsk AInamespace App\Nova;

class Post extends Resource 
{
    // ... 

    /**
     * The columns that should be searched.
     *
     * @var array
     */
    public static $search = [
        &#x27;id&#x27;, &#x27;title&#x27;, &#x27;content&#x27;,
    ];
}

If you are using Nova’s Scout integration, the $search property has no effect on your search results and may be ignored. You should manage the searchable columns within the Algolia or Meilisearch dashboard.
​Full-Text Indexes
Typically, Nova searches your database columns using simple LIKE clauses. However, if you are using MySQL or Postgres, you may take advantage of any full-text indexes you have defined. To do so, you should define a searchableColumns method on your Nova resource class instead of defining a $search property.
The searchableColumns method should return an array of columns that are searchable. You may include an instance of Laravel\Nova\Query\Search\SearchableText within this array to instruct Nova to utilize your full-text indexes when querying a given column:
app/Nova/Post.phpCopyAsk AIuse Laravel\Nova\Query\Search\SearchableText;

// ... 

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return [&#x27;id&#x27;, new SearchableText(&#x27;title&#x27;)];
}

The array returned by the searchableColumns method can also include raw SQL expressions, which allow you to search through derived columns:
app/Nova/User.phpCopyAsk AIuse Illuminate\Support\Facades\DB;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return [&#x27;id&#x27;, DB::raw(&quot;CONCAT(first_name, &#x27; &#x27;, last_name)&quot;)];
}

​Searching Relationships
Laravel Nova also allows you to search against a resource’s related models. For example, imagine a Post model that is related to a User model via an author relatonship. You may indicate that this relationship data should be considered when searching for users by returning an instance of Laravel\Nova\Query\Search\SearchableRelation from your resource’s searchableColumns method.
If the searchableColumns method does not exist on your resource, you should define it. Once the searchableColumns method has been defined, you may remove the $search property from your resource:
app/Nova/Post.phpCopyAsk AIuse Laravel\Nova\Query\Search\SearchableRelation;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return [&#x27;id&#x27;, new SearchableRelation(&#x27;author&#x27;, &#x27;name&#x27;)];
}

For convenience, you may define a relationship that should be searched by adding the field to your resource’s $search property using “dot notation”:
app/Nova/Post.phpCopyAsk AI/**
 * The columns that should be searched.
 *
 * @var array
 */
public static $search = [
    &#x27;id&#x27;, &#x27;author.name&#x27;
];

​MorphTo Relationships
“Morph to” relationships can be made searchable by returning an instance of Laravel\Nova\Query\Search\SearchableMorphToRelation from your resource’s searchableColumns method. The SearchableMorphToRelation class allows you to specify which types of morphed models should be searched:
app/Nova/~Resource.phpCopyAsk AIuse App\Nova\Post;
use Laravel\Nova\Query\Search\SearchableMorphToRelation;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return [&#x27;id&#x27;, new SearchableMorphToRelation(&#x27;commentable&#x27;, &#x27;title&#x27;, [Post::class])];
}

​Searching JSON Data
If the database table associated with your resource includes a column that contains a JSON string, you may instruct Nova to search within the JSON string by returning a Laravel\Nova\Query\Search\SearchableJson instance from your resource’s searchableColumns method.
If the searchableColumns method does not exist on your resource, you should define it. Once the searchableColumns method has been defined, you may remove the $search property from your resource:
app/Nova/UserProfile.phpCopyAsk AIuse Laravel\Nova\Query\Search\SearchableJson;

// ...

/**
 * Get the searchable columns for the resource.
 *
 * @return array
 */
public static function searchableColumns()
{
    return [&#x27;id&#x27;, new SearchableJson(&#x27;meta-&gt;address-&gt;postcode&#x27;)];
}
Was this page helpful?YesNoAuthorizationGlobal SearchOn this pageSearchable ColumnsFull-Text IndexesSearching RelationshipsMorphTo RelationshipsSearching JSON DataLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, CodeGroup, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!CodeGroup) _missingMdxReference(\"CodeGroup\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"searchable-columns\",\n      isAtRootLevel: \"true\",\n      children: \"Searchable Columns\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"To define which resource fields are searchable, you may assign an array of database columns to the \", _jsx(_components.code, {\n        children: \"search\"\n      }), \" property or \", _jsx(_components.code, {\n        children: \"searchableColumns\"\n      }), \" method of your resource class. This array includes the \", _jsx(_components.code, {\n        children: \"id\"\n      }), \" column by default:\"]\n    }), \"\\n\", _jsxs(CodeGroup, {\n      children: [_jsx(CodeBlock, {\n        filename: \"Property\",\n        numberOfLines: \"15\",\n        language: \"php\",\n        children: _jsx(_components.pre, {\n          className: \"shiki shiki-themes github-light-default dark-plus\",\n          style: {\n            backgroundColor: \"transpar