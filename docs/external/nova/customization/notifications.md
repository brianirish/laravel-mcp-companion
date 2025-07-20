# Nova - Customization/Notifications

*Source: https://nova.laravel.com/docs/v5/customization/notifications*

---

Notifications - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperNotificationsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperNotificationsLearn how to send notifications to Nova users.​Overview
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
Was this page helpful?YesNoMenusAuthenticationOn this pageOverviewSending NotificationsOpening Remote Action URLs in New TabsNotification IconsDisabling NotificationsEnabling Unread Notifications CountLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Frame, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Nova notifications allow you to notify Nova users of events within your application, such as a report being ready to download or of an invoice that needs attention. Nova notifications are displayed within a slide-out menu that can be accessed via the “bell” icon within Nova’s top navigation menu.\"\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/images/notifications.png\",\n          alt: \"Notifications\"\n        })\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"sending-notifications\",\n      isAtRootLevel: \"true\",\n      children: \"Sending Notifications\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"To send a notification, you simply need to send a \", _jsx(_components.code, {\n        children: \"NovaNotification\"\n      }), \" instance to a user’s \", _jsx(_components.code, {\n        children: \"notify\"\n      }), \" method. Of course, before getting started, you should ensure that your user model is \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/notifications\",\n        children: \"notifiable\"\n      }), \".\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Nova notifications may be generated via the \", _jsx(_components.code, {\n        children: \"NovaNotification\"\n      }), \" class, which provides convenient methods like \", _jsx(_components.code, {\n        children: \"message\"\n      }), \", \", _jsx(_components.code, {\n        children: \"action\"\n      }), \", \", _jsx(_components.code, {\n        children: \"icon\"\n      }), \", and \", _jsx(_components.code, {\n        children: \"type\"\n      }), \". The currently supported notification types include \", _jsx(_components.code, {\n        children: \"success\"\n      }), \", \", _jsx(_components.code, {\n        children: \"error\"\n      }), \", \", _jsx(_components.code, {\n        children: \"warni