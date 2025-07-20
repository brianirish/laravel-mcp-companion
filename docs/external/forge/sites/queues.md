# Forge - Sites/Queues

*Source: https://forge.laravel.com/docs/sites/queues*

---

Queues - Laravel Forge
              document.documentElement.style.setProperty('--font-family-headings-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-headings-custom', '');
              document.documentElement.style.setProperty('--font-family-body-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-body-custom', '');
            
    (function() {
      try {
        var bannerKey = "forge-laravel-bannerDismissed";
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
    --primary: 24 182 155;
    --primary-light: 24 182 155;
    --primary-dark: 24 182 155;
    --background-light: 255 255 255;
    --background-dark: 9 12 14;
    --gray-50: 243 248 247;
    --gray-100: 238 243 242;
    --gray-200: 223 228 227;
    --gray-300: 206 211 210;
    --gray-400: 159 164 163;
    --gray-500: 112 117 116;
    --gray-600: 80 85 84;
    --gray-700: 63 68 67;
    --gray-800: 38 42 42;
    --gray-900: 23 28 27;
    --gray-950: 10 15 14;
  }h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesQueuesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesQueuesManage Laravel queue workers.​Overview
Forge’s site management dashboard allows you to easily create as many Laravel queue workers as you like. Queue workers will automatically be monitored by Supervisor, and will be restarted if they crash. All workers will start automatically if the server is restarted.
​Creating A Queue Worker
You can create a new queue worker within the site’s management dashboard. The “New Worker” form is a wrapper around the Laravel queue feature. You can read more about queues in the full Laravel queue documentation.
When creating a new queue worker, you may select a version of PHP that is already installed on the server. The selected version of PHP will be used to execute the queue worker.
​Laravel Horizon
If your Laravel application is using Laravel Horizon, you should not setup queue workers as described above. Instead, you may enable Horizon on Forge using Forge’s “daemon” feature.
First, create a server daemon that executes the php artisan horizon Artisan command from your site’s root directory.
Next, add the php artisan horizon:terminate Artisan command to your site’s deployment script, as described in Horizon’s deployment documentation.
Finally, if you wish to use Horizon’s metrics graphs, you should configure the scheduled job for horizon:snapshot in your application code. In addition, you should define a Scheduler task within Forge for the php artisan schedule:run Artisan command if you have not already done so.
​Restarting Queue Workers After Deployment
When deploying your application, it is important that your existing queue workers or Horizon processes reflect the latest changes to your application. This can be achieved by gracefully restarting these services from your deployment script:
When using queue workers:
CopyAsk AI$FORGE_PHP artisan queue:restart

When using Horizon:
CopyAsk AI$FORGE_PHP artisan horizon:terminate

​Circle Permissions
You may grant a circle member authority to create and manage queue workers by granting the site:manage-queues permission.Was this page helpful?YesNoPackagesSecurity RulesOn this pageOverviewCreating A Queue WorkerLaravel HorizonRestarting Queue Workers After DeploymentCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge’s site management dashboard allows you to easily create as many Laravel queue workers as you like. Queue workers will automatically be monitored by Supervisor, and will be restarted if they crash. All workers will start automatically if the server is restarted.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-a-queue-worker\",\n      isAtRootLevel: \"true\",\n      children: \"Creating A Queue Worker\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You can create a new queue worker within the site’s management dashboard. The “New Worker” form is a wrapper around the Laravel queue feature. You can read more about queues in the \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/queues\",\n        children: \"full Laravel queue documentation\"\n      }), \".\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When creating a new queue worker, you may \", _jsx(_components.a, {\n        href: \"/servers/php\",\n        children: \"select a version of PHP\"\n      }), \" that is already installed on the server. The selected version of PHP will be used to execute the queue worker.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"laravel-horizon\",\n      isAtRootLevel: \"true\",\n      children: \"Laravel Horizon\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If your Laravel application is using \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/horizon\",\n        children: \"Laravel Horizon\"\n      }), \", you should not setup queue workers as described above. Instead, you may enable Horizon on Forge using Forge’s “daemon” feature.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"First, create a \", _jsx(_components.a, {\n        href: \"/resources/daemons#configuring-daemons\",\n        children: \"server daemon\"\n      }), \" that executes the \", _jsx(_components.code, {\n        children: \"php artisan horizon\"\n      }), \" Artisan command from your site’s root directory.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Next, add the \", _jsx(_components.code, {\n        children: \"php artisan horizon:terminate\"\n      }), \" Artisan command to your site’s deployment script, as described in \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/master/horizon#deploying-horizon\",\n        children: \"Horizon’s deployment\"\n      }), \" documentation.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Finally, if you wish to use Horizon’s \", _jsx(_components.a, {\n        href: \"https://laravel.com/docs/master/horizon#metrics\",\n        children: \"metrics graphs\"\n      }), \", you should configure the scheduled job for \", _jsx(_components.code, {\n        children: \"horizon:snapshot\"\n      }), \" in your application code. In addition, you should define a \", _jsx(_components.a, {\n        href: \"/resources/scheduler#scheduled-jobs\",\n        children: \"Scheduler task\"\n      }), \" within Forge for the \", _jsx(_components.code, {\n        children: \"php artisan schedule:run\"\n      }), \" Artisan command if you have not already done so.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"restarting-queue-workers-after-deployment\",\n      isAtRootLevel: \"true\",\n      children: \"Restarting Queue Workers After Deployment\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"When deploying your application, it is important that your existing queue workers or Horizon processes reflect the latest changes to your application. This can be achieved by gracefully restarting these services from your deployment script:\"\n    }), \"\\n\", _jsx(