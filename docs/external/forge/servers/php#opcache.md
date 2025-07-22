# Forge - Servers/Php#Opcache

*Source: https://forge.laravel.com/docs/servers/php#opcache*

---

PHP - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersPHPDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersPHPLearn how to manage PHP versions on your Forge server.​Overview
Forge makes it easy to install and configure multiple versions of PHP on your server. Each installed PHP version runs its own FPM process. In addition, you may update the PHP version used by specific sites at any time.
If you choose to manually install PHP versions on your server, Forge will not be aware of those PHP installations. Forge is only aware of PHP installations that are managed through the Forge dashboard.
​Multiple PHP Versions
When provisioning a server, you must decide which version of PHP you want to install by default. The php binary on your server will point to the installed version selected at the time of its creation.
Once the server has been created, Forge makes it easy to install additional versions alongside the default version. In the following documentation we will discuss how to manage these additional PHP versions.
​Installation
You can install additional versions of PHP via the PHP tab on a server’s management dashboard. Once an additional version of PHP has been installed, you may select it when creating a site or when switching a site’s PHP version.
When you install a new version of PHP onto your server, Forge will create and configure the PHP-FPM process for that version. This means that your server will be running multiple versions of PHP at once.
​Uninstalling Additional PHP Versions
You can choose to uninstall a version of PHP so long as:

There are other versions installed.
The version you wish to uninstall is not the server’s default version for new sites.
The version you wish to uninstall is not the server’s default version on the CLI.
The version you wish to uninstall is not used by any sites.

​CLI
When an additional version of PHP has been installed, you may reference it on the CLI via phpx.x, replacing the x.x with the version number (e.g. php8.4). The php binary will always point to the active CLI version (if changed from the default).
​Default PHP Installation
The “default” PHP version is the version of PHP that will be used by default when creating a new site on the server.
When selecting a new version of PHP as your server’s “default” version, the PHP versions used by existing sites will not be updated.
​Updating PHP Between Patch Releases
You can upgrade your PHP installations between patch releases of PHP at any time using the Patch Version button. Typically, these updates should not cause any breaking changes to your server, although a few seconds of downtime is possible.
​PHP Betas / Release Candidates
PHP “beta” and “release candidate” releases are often available on Forge weeks before their final release. This allows you to experiment with upcoming major PHP versions on sites that are not in production. However, some Forge features, PHP features, and PHP extensions may not work as expected during that period. In addition, once that PHP version becomes stable, you will need to fully uninstall and re-install the PHP version.
​Common PHP Configuration Settings
Changing the following settings will apply the changes to all versions of PHP installed on the server.
​Max File Upload Size
You may configure the maximum file upload size through the PHP tab of the server management dashboard. This value should be provided in megabytes. For reference, 1024MB is 1GB.
​Max Execution Time
You may configure the maximum execution time through the PHP tab of the server management dashboard. This value should be provided in seconds.
​OPcache
Optimizing the PHP OPcache for production will configure OPcache to store your compiled PHP code in memory to greatly improve performance. If you choose to optimize OPcache for production, you should verify that your deployment script reloads the PHP-FPM service at the end of each deployment.
​Circle Permissions
Circle members will require the server:manage-php permission to manage PHP installations and configurations. This permission is also required to manage integrations with Blackfire.io and Papertrail.Was this page helpful?YesNoSSH Keys / Git AccessPackagesOn this pageOverviewMultiple PHP VersionsInstallationUninstalling Additional PHP VersionsCLIDefault PHP InstallationUpdating PHP Between Patch ReleasesPHP Betas / Release CandidatesCommon PHP Configuration SettingsMax File Upload SizeMax Execution TimeOPcacheCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge makes it easy to install and configure multiple versions of PHP on your server. Each installed PHP version runs its own FPM process. In addition, you may \", _jsx(_components.a, {\n        href: \"/sites/the-basics#php-version\",\n        children: \"update the PHP version used by specific sites at any time\"\n      }), \".\"]\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"If you choose to manually install PHP versions on your server, Forge will not be aware of those PHP installations. Forge is only aware of PHP installations that are managed through the Forge dashboard.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"multiple-php-versions\",\n      isAtRootLevel: \"true\",\n      children: \"Multiple PHP Versions\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When provisioning a server, you must decide which version of PHP you want to install by default. The \", _jsx(_components.code, {\n        children: \"php\"\n      }), \" binary on your server will point to the installed version selected at the time of its creation.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Once the server has been created, Forge makes it easy to install additional versions alongside the default version. In the following documentation we will discuss how to manage these additional PHP versions.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"installation\",\n      isAtRootLevel: \"true\",\n      children: \"Installation\"\n    }), \"\\n\", _jsxs