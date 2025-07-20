# Nova - Resources/File-Fields

*Source: https://nova.laravel.com/docs/v5/resources/file-fields*

---

File Fields - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationResourcesFile FieldsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsResourcesFile FieldsLearn how to work with file fields in Nova.Nova offers several types of file fields: File, Image, Avatar, VaporFile, and VaporImage. The File field is the most basic form of file upload field, and is the base class for both the Image and Avatar fields. In the following documentation, we will explore each of these fields and discuss their similarities and differences.
​Overview
To illustrate the behavior of Nova file upload fields, let’s assume our application’s users can upload “profile photos” to their account. So, our users database table will have a profile_photo column. This column will contain the path to the profile photo on disk, or, when using a cloud storage provider such as Amazon S3, the profile photo’s path within its “bucket”.
​Defining the Field
Next, let’s attach the file field to our User resource. In this example, we will create the field and instruct it to store the underlying file on the public disk. This disk name should correspond to a disk name in your application’s filesystems configuration file:
CopyAsk AIuse Laravel\Nova\Fields\File;

// ...

File::make(&#x27;Profile Photo&#x27;)
    -&gt;disk(&#x27;public&#x27;),

​Disabling File Downloads
By default, the File field allows the user to download the corresponding file. To disable this, you may call the disableDownload method on the field definition:
CopyAsk AIuse Laravel\Nova\Fields\File;

// ...

File::make(&#x27;Profile Photo&#x27;)
    -&gt;disableDownload(),

​How Files Are Stored
When a file is uploaded using this field, Nova will use Laravel’s Flysystem integration to store the file on the disk of your choosing and the file will be assigned a randomly generated filename. Once the file is stored, Nova will store the relative path to the file in the file field’s underlying database column.
To illustrate the default behavior of the File field, let’s take a look at an equivalent Laravel route that would store the file in the same way:
routes/web.phpCopyAsk AIuse Illuminate\Http\Request;

// ...

Route::post(&#x27;/photo&#x27;, function (Request $request) {
    $path = $request-&gt;profile_photo-&gt;store(&#x27;/&#x27;, &#x27;public&#x27;);

    $request-&gt;user()-&gt;update([
        &#x27;profile_photo&#x27; =&gt; $path,
    ]);
});

Of course, once the file has been stored, you may retrieve it within your application using the Laravel Storage facade:
CopyAsk AIuse Illuminate\Support\Facades\Storage;

// ...

Storage::get($user-&gt;profile_photo);
Storage::url($user-&gt;profile_photo);

The documentation above only demonstrates the default behavior of the File field. To learn more about how to customize its behavior, check out the customization documentation.
​The Local Disk
If you are using the public disk in conjunction with the local driver, you should run the php artisan storage:link Artisan command to create a symbolic link from public/storage to storage/app/public. To learn more about file storage in Laravel, check out the Laravel file storage documentation.
​Images
The Image field behaves exactly like the File field; however, instead of only displaying the path to the file within the Nova dashboard, an Image field will show a thumbnail preview of the underlying file. All of the configuration and customization options of the Image field mirror that of the File field:
CopyAsk AIuse Laravel\Nova\Fields\Image;

// ...

Image::make(&#x27;Profile Photo&#x27;)
    -&gt;disk(&#x27;public&#x27;),

To set the width of the Image field when being displayed, you can use the maxWidth method:
CopyAsk AIuse Laravel\Nova\Fields\Image;

// ...

Image::make(&#x27;Profile Photo&#x27;)
    -&gt;maxWidth(100),

Alternatively, you can set separate widths for the index and detail views using the indexWidth and detailWidth methods:
CopyAsk AIuse Laravel\Nova\Fields\Image;

// ...

Image::make(&#x27;Profile Photo&#x27;)
    -&gt;indexWidth(60)
    -&gt;detailWidth(150),

You may also use the maxWidth, indexWidth, and detailWidth methods on the Avatar and Gravatar fields.
​Avatars
The Avatar field behaves exactly like the File field; however, instead of only displaying the path to the file within the Nova dashboard, an Avatar field will show a thumbnail preview of the underlying file. All of the configuration and customization options of the Avatar field mirror that of the File field:
CopyAsk AIuse Laravel\Nova\Fields\Avatar;

// ...

Avatar::make(&#x27;Poster&#x27;)
    -&gt;disk(&#x27;public&#x27;),

In addition to displaying a thumbnail preview of the underlying file, an Avatar field will also be automatically displayed in Nova search results. An Avatar field is not limited to “user” resources - you may attach Avatar fields to any resource within your Nova application:

​Storing Metadata
In addition to storing the path to the file within the storage system, you may also instruct Nova to store the original client filename and its size (in bytes). You may accomplish this using the storeOriginalName and storeSize methods. Each of these methods accept the name of the column you would like to store the file information:
CopyAsk AIuse Illuminate\Http\Request;
use Laravel\Nova\Fields\File;
use Laravel\Nova\Fields\Text;

// ... 

/**
 * Get the fields displayed by the resource.
 *
 * @return array&lt;int, \Laravel\Nova\Fields\Field&gt;
 */
public function fields(NovaRequest $request): array 
{
    return [
        // ...

        File::make(&#x27;Attachment&#x27;)
                -&gt;disk(&#x27;s3&#x27;)
                -&gt;storeOriginalName(&#x27;attachment_name&#x27;)
                -&gt;storeSize(&#x27;attachment_size&#x27;),

        Text::make(&#x27;Attachment Name&#x27;)-&gt;exceptOnForms(),

        Text::make(&#x27;Attachment Size&#x27;)
                -&gt;exceptOnForms()
                -&gt;displayUsing(function ($value) {
                    return number_format($value / 1024, 2).&#x27;kb&#x27;;
                }),
    ];
}

One benefit of storing the original client filename is the ability to create file download responses using the original filename that was used to upload the file. For example, you may do something like the following in one of your application’s routes:
routes/web.phpCopyAsk AIuse Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

// ... 

Route::get(&#x27;/download&#x27;, function (Request $request) {
    $user = $request-&gt;user();

    return Storage::download(
        $user-&gt;attachment, $user-&gt;attachment_name
    );
});

When using the storeOriginalName method, the file field’s “Download” link within the Nova dashboard will automatically download the file using its original name.
​Pruning &amp; Deletion
File fields are deletable by default, but you can override this behavior by using the deletable method:
CopyAsk AIuse Laravel\Nova\Fields\File;

// ..