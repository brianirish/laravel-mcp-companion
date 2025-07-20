# Nova - Customization/Authentication

*Source: https://nova.laravel.com/docs/v5/customization/authentication*

---

Authentication - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperAuthenticationDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperAuthenticationLearn how to customize the Nova authentication logic.Nova utilizes Laravel Fortify and offers two-factor authentication, email address verification, and password confirmation. By default, these features are not enabled but can be enabled with just a few changes to your application’s app/Providers/NovaServiceProvider.php file.
​Using Nova as Your Application’s Default Login
Sometimes you might want to use Nova as the default authentication UI for your application. To accomplish this, you should enable Nova’s authentication and password reset routes within the routes method of your application’s App\Providers\NovaServiceProvider class:
CopyAsk AI/**
 * Register the Nova routes.
 */
protected function routes(): void
{
    Nova::routes()
        -&gt;withAuthenticationRoutes(default: true)
        -&gt;withPasswordResetRoutes()
        -&gt;register();
}

​Using Custom Authentication Routes
Alternatively, you can disable Nova’s authentication and password reset routes and instead provide Nova with your application’s own authentication route paths. This will instruct Nova where to redirect unauthenticated users:
CopyAsk AI/**
 * Register the Nova routes.
 */
protected function routes(): void
{
    Nova::routes()
        -&gt;withoutAuthenticationRoutes(
            login: &#x27;/login&#x27;, 
            logout: &#x27;/logout&#x27;,
        )
        -&gt;withoutPasswordResetRoutes(
            forgotPassword: &#x27;/forgot-password&#x27;, 
            resetPassword: &#x27;/reset-password&#x27;,
        )
        -&gt;register();
}

​Enabling Two Factor Authentication
To allow your users to authenticate with two-factor authentication, you will need to update your application’s User model and App\Providers\NovaServiceProvider service provider.
First, add the Laravel\Fortify\TwoFactorAuthenticatable trait to your application’s User model:
CopyAsk AI&lt;?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;
 
class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;

    // ...
}

Next, update the routes method in your application’s App\Providers\NovaServiceProvider class to enable two-factor authentication:
CopyAsk AIuse Laravel\Fortify\Features;
use Laravel\Nova\Nova;

// ...

/**
 * Register the configurations for Laravel Fortify.
 */
protected function fortify(): void
{
    Nova::fortify()
        -&gt;features([
            Features::updatePasswords(),
            // Features::emailVerification(),
            Features::twoFactorAuthentication([
                &#x27;confirm&#x27; =&gt; true,
                &#x27;confirmPassword&#x27; =&gt; true
            ]),
        ])
        -&gt;register();
}

Finally, run the nova:publish Artisan command to publish the required Fortify migrations. Then, run the migrate command:
CopyAsk AIphp artisan nova:publish

php artisan migrate

Once completed, Nova users will be able to access a new User Security page from the User Menu. Please refer to Fortify’s two-factor authentication documentation for more information.
​Enabling Email Verification
Nova also includes support for requiring email verification for newly registered users. To enable this feature, you should uncomment the relevant entry in the features configuration item in the fortify method of your application’s App\Provider\NovaServiceProvider class:
CopyAsk AIuse Laravel\Fortify\Features;
use Laravel\Nova\Nova;

// ...

/**
 * Register the configurations for Laravel Fortify.
 */
protected function fortify(): void
{
    Nova::fortify()
        -&gt;features([
            Features::updatePasswords(),
            Features::emailVerification(),
            // Features::twoFactorAuthentication([&#x27;confirm&#x27; =&gt; true, &#x27;confirmPassword&#x27; =&gt; true]),
        ])
        -&gt;register();
}

Next, you should ensure that your User model implements the Illuminate\Contracts\Auth\MustVerifyEmail interface:
CopyAsk AI&lt;?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}

Finally, to secure the Nova page from being used by unverified users, you can add the Laravel\Nova\Http\Middleware\EnsureEmailIsVerified middleware to the api_middleware configuration key in your application’s config/nova.php configuration file:
CopyAsk AI&#x27;api_middleware&#x27; =&gt; [
    &#x27;nova&#x27;,
    \Laravel\Nova\Http\Middleware\Authenticate::class,
    \Laravel\Nova\Http\Middleware\EnsureEmailIsVerified::class,
    \Laravel\Nova\Http\Middleware\Authorize::class,
],
Was this page helpful?YesNoNotificationsImpersonationOn this pageUsing Nova as Your Application’s Default LoginUsing Custom Authentication RoutesEnabling Two Factor AuthenticationEnabling Email VerificationLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsxs(_components.p, {\n      children: [\"Nova utilizes \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/fortify\",\n        children: \"Laravel Fortify\"\n      }), \" and offers two-factor authentication, email address verification, and password confirmation. By default, these features are not enabled but can be enabled with just a few changes to your application’s \", _jsx(_components.code, {\n        children: \"app/Providers/NovaServiceProvider.php\"\n      }), \" file.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"using-nova-as-your-application%E2%80%99s-default-login\",\n      isAtRootLevel: \"true\",\n      children: \"Using Nova as Your Application’s Default Login\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Sometimes you might want to use Nova as the default authentication UI for your application. To accomplish this, you should enable Nova’s a