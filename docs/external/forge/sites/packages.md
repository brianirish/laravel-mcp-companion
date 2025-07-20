# Forge - Sites/Packages

*Source: https://forge.laravel.com/docs/sites/packages*

---

Packages - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesPackagesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesPackagesManage Composer credentials on your site.​Overview
Forge allows you to manage the “http-basic” portion of the selected site’s user’s auth.json Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not within Forge itself.
​Site Composer Credentials
The Composer Credentials that you can manage on the site level only apply to this site . For example, if you have two sites installed under the forge user, and you need both sites to use different credentials for the same Composer package, you should use the site’s packages. If you want to store one set of credentials that applies to all sites with a user’s home directory, please see Packages for more details.
​Adding Credentials Before Installing a Repository
Forge does not allow you to install credentials before you have installed a repository; instead, it will redirect you back to the “App” tab. This is because Forge recreates the site’s base directory if the initial installation does not finish successfully. So, if you need to provide local Composer credentials, you first need to install a repository without the “Install Composer Dependencies” checked so that you can update the credentials after the repository is installed.
​Managing Credentials
Forge makes it easy to manage Composer credentials for a site. You can add, remove, and update credentials directly from the Forge UI.
​Add Credentials
Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:

Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users
Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses
Password - this is generally the password associated with the username, however in some case, this may also be a license key

Click “Save” in order to store these credentials in the user’s global Composer configuration directory (~/.config/composer/auth.json).
​Remove Credentials
In order to remove Composer credentials, you can simply click on the red button displayed on the same line as the Repository URL.
After removing credentials, please do not forget to click “Save” in order to store your new credentials configuration on the server.
​Update Credentials
Any credentials that are shown on the screen can be updated with any new adequate value.
After updating the value, please do not forget to click the “Save” button in order your new credentials configuration on the server.
​Circle Permissions
The ability to manage a site’s Composer packages is determined by the server:manage-packages permission. This permission will also allow the circle member to manage a server’s Composer packages too.Was this page helpful?YesNoCommandsQueuesOn this pageOverviewSite Composer CredentialsAdding Credentials Before Installing a RepositoryManaging CredentialsAdd CredentialsRemove CredentialsUpdate CredentialsCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge allows you to manage the “http-basic” portion of the selected site’s user’s \", _jsx(_components.code, {\n        children: \"auth.json\"\n      }), \" Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not within Forge itself.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"site-composer-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Site Composer Credentials\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The Composer Credentials that you can manage on the site level only apply to this site . For example, if you have two sites installed under the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user, and you need both sites to use different credentials for the same Composer package, you should use the site’s packages. If you want to store one set of credentials that applies to all sites with a user’s home directory, please see \", _jsx(_components.a, {\n        href: \"/servers/packages\",\n        children: \"Packages\"\n      }), \" for more details.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"adding-credentials-before-installing-a-repository\",\n      isAtRootLevel: \"true\",\n      children: \"Adding Credentials Before Installing a Repository\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge does not allow you to install credentials before you have installed a repository; instead, it will redirect you back to the “App” tab. This is because Forge recreates the site’s base directory if the initial installation does not finish successfully. So, if you need to provide local Composer credentials, you first need to install a repository without the “Install Composer Dependencies” checked so that you can update the credentials after the repository is installed.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"managing-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Credentials\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge makes it easy to manage Composer credentials for a site. You can add, remove, and update credentials directly from the Forge UI.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"add-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Add Credentials\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses\"\n      }), \"