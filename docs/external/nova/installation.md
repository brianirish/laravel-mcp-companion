# Nova - Installation

*Source: https://nova.laravel.com/docs/v5/installation*

---

Installation - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationGet StartedInstallationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsGet StartedInstallationLearn how to install Laravel Nova into your Laravel application.Purchase NovaPurchase a license for Laravel NovaLearn MoreWatch the free Nova series on Laracasts
​Requirements
Laravel Nova has a few minimum requirements you should be aware of before installing:

Composer 2
Laravel Framework 10.x, 11.x, or 12.x
Inertia.js 2.x
Laravel Mix 6.x
Node.js (Version 18.x+)
NPM 9.x

​Browser Support
Nova supports modern versions of the following browsers:

Apple Safari
Google Chrome
Microsoft Edge
Mozilla Firefox

​Installing Nova via Composer
You may install Nova as a Composer package via our private Satis repository. To get started, add the Nova repository to your application’s composer.json file:
composer.jsonCopyAsk AI&quot;repositories&quot;: [
    {
        &quot;type&quot;: &quot;composer&quot;,
        &quot;url&quot;: &quot;https://nova.laravel.com&quot;
    }
],

Or, you may use the following CLI command to add the Composer repository to your composer.json file:
CopyAsk AIcomposer config repositories.nova &#x27;{&quot;type&quot;: &quot;composer&quot;, &quot;url&quot;: &quot;https://nova.laravel.com&quot;}&#x27; --file composer.json

Next, you may add laravel/nova to your list of required packages in your composer.json file:
composer.jsonCopyAsk AI&quot;require&quot;: {
    &quot;php&quot;: &quot;^8.2&quot;,
    &quot;laravel/framework&quot;: &quot;^12.0&quot;,
    &quot;laravel/nova&quot;: &quot;^5.0&quot;
},

After your composer.json file has been updated, run the composer update command in your console terminal:
CopyAsk AIcomposer update --prefer-dist

When running composer update, you will be prompted to provide a username and password. You should use your Nova website email for the username and a license key should be used as the password. These credentials will authenticate your Composer session as having permission to download the Nova source code.
To avoid manually typing these credentials, you may create a Composer auth.json file while using your license key in place of your password:
CopyAsk AIcomposer config http-basic.nova.laravel.com [email&#160;protected] your-license-key

Finally, run the nova:install and migrate Artisan commands. The nova:install command will install Nova’s service provider and public assets within your application:
CopyAsk AIphp artisan nova:install

php artisan migrate

The default App\Nova\User Nova resource references the App\Models\User model. If you place your models in a different directory or namespace, you should adjust this value within the resource:
app/Nova/User.phpCopyAsk AInamespace App\Nova;

class User extends Resource
{
    /**
     * The model the resource corresponds to.
     *
     * @var class-string&lt;\App\Models\User&gt;
     */
    public static $model = \App\Models\User::class;
}

If your application’s users table is empty or you want to create a new user, you can run the nova:user Artisan command:
CopyAsk AIphp artisan nova:user

That’s it! Next, you may navigate to your application’s /nova path in your browser and you should be greeted with the Nova dashboard which includes links to various parts of this documentation.
​Registering a Nova License Key and Production URL
Nova requires a license key and a production URL to be used in production environments. Nova will check your license key and the current host against the values from the license details found in your Nova account.
You can generate license keys and register the production URL for your project inside the license’s page on your Nova account at https://nova.laravel.com/licenses:

You can register a wildcard subdomain for your production URL for use in multi-tenant scenarios (e.g. *.laravel.com).
You can register your license key by setting the NOVA_LICENSE_KEY variable to .env file or license_key option in your config/nova.php configuration file:
.envconfig/nova.phpCopyAsk AINOVA_LICENSE_KEY=

​Verifying Your Nova License Key Configuration
To verify everything has been configured correctly, you should run the nova:check-license command:
CopyAsk AIphp artisan nova:check-license

​Authenticating Nova in CI Environments
It’s not recommended to store your Composer auth.json file inside your project’s source control repository. However, there may be times you wish to download Nova inside a CI environment like GitHub Actions. For instance, you may wish to run tests for any custom tools you create.
To authenticate Nova in these situations, you can use Composer’s config command to set the configuration option inside your CI system’s pipeline, injecting environment variables containing your Nova username and license key:
GitHub ActionsCopyAsk AIcomposer config http-basic.nova.laravel.com &quot;${secrets.NOVA_USERNAME}&quot; &quot;${secrets.NOVA_LICENSE_KEY}&quot;

​Using Nova on Development and Staging Domains
Since Nova can be used in local and staging development environments, Nova will not check your license key when used on localhost or local TLDs like those specified in IETF RFC 2606:

.test
.example
.invalid
.localhost
.local

Nova will also not check the current license key when the subdomain is one of these commonly-used staging subdomains:

staging.
stage.
test.
testing.
dev.
development.

​Authorizing Access to Nova
Within your app/Providers/NovaServiceProvider.php file, there is a gate method. This authorization gate controls access to Nova in non-local environments. By default, any user can access the Nova dashboard when the current application environment is local. You are free to modify this gate as needed to restrict access to your Nova installation:
app/Providers/NovaServiceProvider.phpCopyAsk AIuse Illuminate\Support\Facades\Gate;

// ...

/**
 * Register the Nova gate.
 *
 * This gate determines who can access Nova in non-local environments.
 */
protected function gate(): void
{
    Gate::define(&#x27;viewNova&#x27;, function ($user) {
        return in_array($user-&gt;email, [
            &#x27;[email&#160;protected]&#x27;,
        ]);
    });
}

​Customization
​Branding
Although Nova’s interface is intended to be an isolated part of your application that is managed by Nova, you can make some small customizations to the branding logo and color used by Nova to make the interface more cohesive with the rest of your application.

​Brand Logo
To customize the logo used at the top left of the Nova interface, you may specify a configuration value for the brand.logo configuration item within your application’s config/nova.php configuration file. This configuration value should contain an absolute path to the SVG file of the logo you would like to use:
config/nova.phpCopyAsk AI&#x27;brand&#x27; =&gt; [
    &#x27;logo&#x27; =&gt; resource_path(&#x27;/img/example-logo.svg&#x27;),

    // ...
],

You may need to adjust the size and width o