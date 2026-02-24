# Nova - Customization/Cards

*Source: https://nova.laravel.com/docs/v5/customization/cards*

---

[Laravel Nova home page](https://nova.laravel.com)
v5
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://nova.laravel.com)
- [Dashboard](https://nova.laravel.com)
Search...
Navigation
Digging Deeper
Cards
[Documentation](/docs/v5/installation)[Knowledge Base](/docs/kb/support)
- [Blog](https://blog.laravel.com)
##### Get Started
- [Installation](/docs/v5/installation)
- [Release Notes](/docs/v5/releases)
- [Upgrade Guide](/docs/v5/upgrade)
##### Resources
- [The Basics](/docs/v5/resources/the-basics)
- [Fields](/docs/v5/resources/fields)
- [Dependent Fields](/docs/v5/resources/dependent-fields)
- [Date Fields](/docs/v5/resources/date-fields)
- [File Fields](/docs/v5/resources/file-fields)
- [Repeater Fields](/docs/v5/resources/repeater-fields)
- [Field Panels](/docs/v5/resources/panels)
- [Relationships](/docs/v5/resources/relationships)
- [Validation](/docs/v5/resources/validation)
- [Authorization](/docs/v5/resources/authorization)
##### Search
- [The Basics](/docs/v5/search/the-basics)
- [Global Search](/docs/v5/search/global-search)
- [Scout Integration](/docs/v5/search/scout-integration)
##### Filters
- [Defining Filters](/docs/v5/filters/defining-filters)
- [Registering Filters](/docs/v5/filters/registering-filters)
##### Lenses
- [Defining Lenses](/docs/v5/lenses/defining-lenses)
- [Registering Lenses](/docs/v5/lenses/registering-lenses)
##### Actions
- [Defining Actions](/docs/v5/actions/defining-actions)
- [Registering Actions](/docs/v5/actions/registering-actions)
##### Metrics
- [Defining Metrics](/docs/v5/metrics/defining-metrics)
- [Registering Metrics](/docs/v5/metrics/registering-metrics)
##### Digging Deeper
- [Dashboards](/docs/v5/customization/dashboards)
- [Menus](/docs/v5/customization/menus)
- [Notifications](/docs/v5/customization/notifications)
- [Authentication](/docs/v5/customization/authentication)
- [Impersonation](/docs/v5/customization/impersonation)
- [Tools](/docs/v5/customization/tools)
- [Resource Tools](/docs/v5/customization/resource-tools)
- [Cards](/docs/v5/customization/cards)
- [Fields](/docs/v5/customization/fields)
- [Filters](/docs/v5/customization/filters)
- [CSS / JavaScript](/docs/v5/customization/frontend)
- [Assets](/docs/v5/customization/assets)
- [Localization](/docs/v5/customization/localization)
- [Stubs](/docs/v5/customization/stubs)
On this page
- [Overview](#overview)
- [Defining Cards](#defining-cards)
- [Registering Cards](#registering-cards)
- [Authorization](#authorization)
- [Card Options](#card-options)
- [Accessing Card Options](#accessing-card-options)
- [Building Cards](#building-cards)
- [Routing](#routing)
- [Assets](#assets)
- [Registering Assets](#registering-assets)
- [Compiling Assets](#compiling-assets)
Digging Deeper
# Cards
Learn how to build custom cards for your Nova application.
## [​](#overview) Overview
Cards are similar to resource tools, but are small, miniature tools that are typically displayed at the top of your dashboard, resource index, or resource detail pages. In fact, if you have used [Nova metrics](./../metrics/defining-metrics), you have already seen Nova cards. Custom Nova cards allow you to build your own, metric-sized tools.
## [​](#defining-cards) Defining Cards
Cards may be generated using the `nova:card` Artisan command. By default, all new cards will be placed in the `nova-components` directory of your application. When generating a card using the `nova:card` command, the card name you pass to the command should follow the Composer `vendor/package` format. So, if we were building a traffic analytics card, we might run the following command:
Copy
Ask AI
```
php artisan nova:card acme/analytics
```
When generating a card, Nova will prompt you to install the card’s NPM dependencies, compile its assets, and update your application’s `composer.json` file. All custom cards are registered with your application as a Composer [“path” repository](https://getcomposer.org/doc/05-repositories#path).
Nova cards include all of the scaffolding necessary to build your card. Each card even contains its own `composer.json` file and is ready to be shared with the world on GitHub or the source control provider of your choice.
## [​](#registering-cards) Registering Cards
Nova cards may be registered in your resource’s `cards` method. This method returns an array of cards available to the resource. To register your card, add your card to the array of cards returned by this method:
app/Nova/Post.php
Copy
Ask AI
```
namespace App\Nova;

use Acme\Analytics\Analytics;
use Laravel\Nova\Http\Requests\NovaRequest;

class Post extends Resource
{
    /**
     * Get the cards available for the resource.
     *
     * @return array<int, \Laravel\Nova\Card>
     */
    public function cards(NovaRequest $request)
    {
        return [
            new Analytics,
        ];
    }
}
```
### [​](#authorization) Authorization
If you would like to only expose a given card to certain users, you may invoke the `canSee` method when registering your card. The `canSee` method accepts a closure which should return `true` or `false`. The closure will receive the incoming HTTP request:
app/Nova/Post.php
Copy
Ask AI
```
use Acme\Analytics\Analytics;

// ...

/**
 * Get the cards available for the resource.
 *
 * @return array<int, \Laravel\Nova\Card>
 */
public function cards(NovaRequest $request)
{
    return [
        (new Analytics)->canSee(function ($request) {
            return false;
        }),
    ];
}
```
### [​](#card-options) Card Options
Often, you will need to allow the consumer’s of your card to customize run-time configuration options on the card. You may do this by exposing methods on your card class. These methods may call the card’s underlying `withMeta` method to add information to the card’s metadata, which will be available within your `Card.vue` component. The `withMeta` method accepts an array of key / value options:
nova-components/Analytics/src/Analytics.php
Copy
Ask AI
```
namespace Acme\Analytics;

use Laravel\Nova\Card;

class Analytics extends Card
{
    // ...

    /**
     * Indicates that the analytics should show current visitors.
     *
     * @return $this
     */
    public function currentVisitors()
    {
        return $this->withMeta(['currentVisitors' => true]);
    }
}
```
After registering your custom card, don’t forget to actually call any custom option methods you defined:
Copy
Ask AI
```
(new Acme\Analytics\Analytics)->currentVisitors(),
```
#### [​](#accessing-card-options) Accessing Card Options
Your card’s `Card.vue` component receives a `card` Vue `prop`. This property provides access to any card options that may be available on the card:
Copy
Ask AI
```
const currentVisitors = this.card.currentVisitors;
```
## [​](#building-cards) Building Cards
Each card generated by Nova includes its own service provider and “card” class. Using the `analytics` card as an example, the card class will be located at `src/Analytics.php`.
The card’s service provider is also located within the `src` directory of the card, and is registered in the `extra` section of your card’s `composer.json` file so that it will be auto-loaded by Laravel.
### [​](#routing) Routing
Often, you will need to define Laravel routes that are called by your card via [Nova.request](./frontend#nova-requests). When Nova generates your card, it creates a `routes/api.php` routes file. If needed, you may use this file to define any routes your card requires.
All routes within this file are automatically defined inside a route group by your card’s `CardServiceProvider`. The route group specifies that all routes within the group should receive a `/nova-vendor/card-name` prefix, where `card-name` is the “kebab-case” name of your card. So, for example, `/nova-vendor/analytics`. You are free to modify this route group definition, but take care to make sure your Nova card will co-exist with other Nova packages.
When building routes for your card, you should **always** add authorization to these routes using Laravel gates or policies.
## [​](#assets) Assets
When Nova generates your card, `resources/js` and `resources/css` directories are generated for you. These directories contain your card’s JavaScript and CSS stylesheets. The primary files of interest in these directories are: `resources/js/components/Card.vue` and `resources/css/card.css`.
The `Card.vue` file is a single-file Vue component that contains your card’s front-end. From this file, you are free to build your card however you want. Your card can make HTTP requests using Axios via [Nova.request](./frontend#nova-requests).
### [​](#registering-assets) Registering Assets
Your Nova card’s service provider registers your card’s compiled assets so that they will be available to the Nova front-end:
nova-components/Analytics/src/CardServiceProvider.php
Copy
Ask AI
```
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    $this->app->booted(function () {
        $this->routes();
    });

    Nova::serving(function (ServingNova $event) {
        Nova::mix('acme-analytic', __DIR__.'/../dist/mix-manifest.json');

        Nova::translations(__DIR__.'/../resources/lang/en/card.json');
    });
}
```
Alternatively you can also explicitly register `script` and `style` using the following code:
Copy
Ask AI
```
Nova::serving(function (ServingNova $event) {
-   Nova::mix('acme-analytic', __DIR__.'/../dist/mix-manifest.json');
+   Nova::script('acme-analytic', __DIR__.'/../dist/js/card.js');
+   Nova::style('acme-analytic', __DIR__.'/../dist/css/card.css');
    Nova::translations(__DIR__.'/../resources/lang/en/card.json');
});
```
Your component is bootstrapped and registered in the `resources/js/card.js` file. You are free to modify this file or register additional components here as needed.
### [​](#compiling-assets) Compiling Assets
Your Nova resource card contains a `webpack.mix.js` file, which is generated when Nova creates your card. You may build your card using the NPM `dev` and `prod` commands:
Copy
Ask AI
```
# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod
```
In addition, you may run the NPM `watch` command to auto-compile your assets when they are changed:
Copy
Ask AI
```
npm run watch
```
Was this page helpful?
YesNo
[Resource Tools](/docs/v5/customization/resource-tools)[Fields](/docs/v5/customization/fields)
⌘I
[Laravel Nova home page](https://nova.laravel.com)
Platform
[Dashboard](https://nova.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://nova.laravel.com/terms)[Privacy Policy](https://nova.laravel.com/privacy)
Assistant
Responses are generated using AI and may contain mistakes.