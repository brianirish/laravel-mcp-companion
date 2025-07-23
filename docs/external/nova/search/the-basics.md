# Nova - Search/The-Basics

*Source: https://nova.laravel.com/docs/v5/search/the-basics*

---

The Basics - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationSearchThe BasicsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageSearchable ColumnsFull-Text IndexesSearching RelationshipsMorphTo RelationshipsSearching JSON DataSearchThe BasicsLearn how to define searchable columns for your Nova resources.​Searchable Columns
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
app/Nova/~Reso