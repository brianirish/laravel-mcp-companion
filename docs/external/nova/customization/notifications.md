# Nova - Customization/Notifications

*Source: https://nova.laravel.com/docs/v5/customization/notifications*

---

Notifications - Laravel Nova(function(a,b,c){try{let d=localStorage.getItem(a);if(null==d)for(let c=0;c((a,b,c,d,e,f,g,h)=>{let i=document.documentElement,j=["light","dark"];function k(b){var c;(Array.isArray(a)?a:[a]).forEach(a=>{let c="class"===a,d=c&&f?e.map(a=>f[a]||a):e;c?(i.classList.remove(...d),i.classList.add(f&&f[b]?f[b]:b)):i.setAttribute(a,b)}),c=b,h&&j.includes(c)&&(i.style.colorScheme=c)}if(d)k(d);else try{let a=localStorage.getItem(b)||c,d=g&&"system"===a?window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light":a;k(d)}catch(a){}})("class","isDarkMode","system",null,["dark","light","true","false","system"],{"true":"dark","false":"light","dark":"dark","light":"light"},true,true)(self.__next_s=self.__next_s||[]).push([0,{"children":"(function m(a,b,c,d){try{let e=document.getElementById(\"banner\"),f=e?.innerText;if(!f)return void document.documentElement.setAttribute(d,\"hidden\");let g=localStorage.getItem(a),h=g!==f&&g!==b;null!=g&&(h?(localStorage.removeItem(c),localStorage.removeItem(a)):(localStorage.setItem(c,f),localStorage.setItem(a,f))),document.documentElement.setAttribute(d,!g||h?\"visible\":\"hidden\")}catch(a){console.error(a),document.documentElement.setAttribute(d,\"hidden\")}})(\n  \"nova-laravel-bannerDismissed\",\n  undefined,\n  \"__mintlify-bannerDismissed\",\n  \"data-banner-state\",\n)","id":"_mintlify-banner-script"}]):root {
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
  }(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function(a,b,c,d){var e;let f,g=\"mint\"===d||\"linden\"===d?\"sidebar\":\"sidebar-content\",h=(e=d,f=\"navbar-transition\",\"maple\"===e&&(f+=\"-maple\"),\"willow\"===e&&(f+=\"-willow\"),f);function i(){document.documentElement.classList.add(\"lg:[--scroll-mt:9.5rem]\")}function j(a){document.getElementById(g)?.style.setProperty(\"top\",`${a}rem`)}function k(a){document.getElementById(g)?.style.setProperty(\"height\",`calc(100vh - ${a}rem)`)}function l(a,b){!a&&b||a&&!b?(i(),document.documentElement.classList.remove(\"lg:[--scroll-mt:12rem]\")):a&&b&&(document.documentElement.classList.add(\"lg:[--scroll-mt:12rem]\"),document.documentElement.classList.remove(\"lg:[--scroll-mt:9.5rem]\"))}let m=document.documentElement.getAttribute(\"data-banner-state\"),n=null!=m?\"visible\"===m:b;switch(d){case\"mint\":j(c),l(a,n);break;case\"palm\":case\"aspen\":j(c),k(c),l(a,n);break;case\"linden\":j(c),n&&i();break;case\"almond\":document.documentElement.style.setProperty(\"--scroll-mt\",\"2.5rem\"),j(c),k(c)}let o=function(){let a=document.createElement(\"style\");return a.appendChild(document.createTextNode(\"*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}\")),document.head.appendChild(a),function(){window.getComputedStyle(document.body),setTimeout(()=>{document.head.removeChild(a)},1)}}();(\"requestAnimationFrame\"in globalThis?requestAnimationFrame:setTimeout)(()=>{let a;a=!1,a=window.scrollY>50,document.getElementById(h)?.setAttribute(\"data-is-opaque\",`${!!a}`),o()})})(\n  true,\n  false,\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-scroll-top-script"}])Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperNotificationsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubs(self.__next_s=self.__next_s||[]).push([0,{"children":"document.documentElement.setAttribute('data-page-mode', 'none');","id":"_mintlify-page-mode-script"}])(self.__next_s=self.__next_s||[]).push([0,{"suppressHydrationWarning":true,"children":"(function m(a,b){if(!document.getElementById(\"footer\")?.classList.contains(\"advanced-footer\")||\"maple\"===b||\"willow\"===b||\"almond\"===b)return;let c=document.documentElement.getAttribute(\"data-page-mode\"),d=document.getElementById(\"navbar\"),e=document.getElementById(\"sidebar\"),f=document.getElementById(\"footer\"),g=document.getElementById(\"table-of-contents-content\");if(!f||\"center\"===c)return;let h=f.getBoundingClientRect().top,i=window.innerHeight-h;e&&(i>0?(e.style.top=`-${i}px`,e.style.height=`${window.innerHeight}px`):(e.style.top=`${a}rem`,e.style.height=\"auto\")),g&&d&&(i>0?g.style.top=\"custom\"===c?`${d.clientHeight-i}px`:`${40+d.clientHeight-i}px`:g.style.top=\"\")})(\n  (function l(a,b,c){let d=document.documentElement.getAttribute(\"data-banner-state\"),e=2.5*!!(null!=d?\"visible\"===d:b),f=3*!!a,g=4,h=e+g+f;switch(c){case\"mint\":case\"palm\":break;case\"aspen\":f=2.5*!!a,g=3.5,h=e+f+g;break;case\"linden\":g=4,h=e+g;break;case\"almond\":g=3.5,h=e+g}return h})(true, false, \"mint\"),\n  \"mint\",\n)","id":"_mintlify-footer-and-sidebar-scroll-script"}])h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}On this pageOverviewSending NotificationsOpening Remote Action URLs in New TabsNotification IconsDisabling NotificationsEnabling Unread Notifications CountDigging DeeperNotificationsLearn how to send notifications to Nova users.​Overview
Nova notifications allow you to notify Nova users of events within your application, such as a report being ready to download or of an invoice that needs attention. Nova notifications are displayed within a slide-out menu that can be accessed via the “bell” icon within Nova’s top navigation menu.

​Sending Notifications
To send a notification, you simply need to send a NovaNotification instance to a user’s notify method. Of course, before getting started, you should ensure that your user model is notifiable.
Nova notifications may be generated via the NovaNotification class, which provides convenient methods like message, action, icon, and type. The currently supported notification types include success, error, warning, and info:
CopyAsk AIuse Laravel\Nova\Notifications\NovaNotification;
use Laravel\Nova\URL;

// ...

$request-&gt;user()-&gt;notify(
    NovaNotification::make()
        -&gt;message(&#x27;Your report is ready to download.&#x27;)
        -&gt;action(&#x27;Download&#x27;, URL::remote(&#x27;https://example.com/report.pdf&#x27;))
        -&gt;icon(&#x27;download&#x27;)
        -&gt;type(&#x27;info&#x27;)
);

You may also send a Nova notification by including the NovaChannel in the array of channels returned by a notification’s via method:
CopyAsk AIuse Laravel\Nova\Notifications\NovaNotification;
use Laravel\Nova\Notifications\NovaChannel;
use Laravel\Nova\URL;

// ...

/**
 * Get the notification&#x27;s delivery channels
 * 
 * @param mixed $notifiable
 * @return array
 */
public function via($notifiable)
{
    return [NovaChannel::class];
}

/**
 * Get the nova representation of the notification
 * 
 * @return array
 */
public function toNova()
{
    return (new NovaNotification)
        -&gt;message(&#x27;Your report is ready to download.&#x27;)
        -&gt;action(&#x27;Download&#x27;, URL::remote(&#x27;https://example.com/report.pdf&#x27;))
        -&gt;icon(&#x27;download&#x27;)
        -&gt;type(&#x27;info&#x27;);
}

​Opening Remote Action URLs in New Tabs
When defining a notification action, the openInNewTab method may be invoked to instruct Nova to open the given URL in a new browser tab:
CopyAsk AIreturn (new NovaNotification)
    -&gt;action(
        &#x27;Download&#x27;, URL::remote(&#x27;https://example.com/report.pdf&#x27;)
    )-&gt;openInNewTab()

​Notification Icons
Nova utilizes the free Heroicons icon set by Steve Schoger. Therefore, you may simply specify the name of one of these icons when providing the icon name to the Nova notification’s icon method.
​Disabling Notifications
If you wish to completely disable notifications inside Nova, you can call the withoutNotifications method from your App/Providers/NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::withoutNotificationCenter();
}

​Enabling Unread Notifications Count
By default, Nova shows a visual indicator when there are unread notifications inside the notification center.
If you would like Nova to show the number of unread notifications, you can call the showUnreadCountInNotificationCenter method from your App/Providers/NovaServiceProvider:
app/Providers/NovaServiceProvider.phpCopyAsk AI/**
 * Boot any application services.
 */
public function boot(): void
{
    parent::boot();

    Nova::showUnreadCountInNotificationCenter();
}
Was this page helpful?YesNoMenusAuthenticationAssistantResponses are generated 