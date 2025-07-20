# Forge - Servers/Packages

*Source: https://forge.laravel.com/docs/servers/packages*

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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersPackagesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersPackagesManage Composer credentials on your server.​Overview
Forge allows you to manage the “http-basic” portion of the selected server user’s auth.json Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not in Forge itself.
​Global Composer Credentials
The Composer credentials that you can manage on the server level will apply to all sites that are served by the same Ubuntu user account. For example, if you have two sites installed under the forge user, both these sites will benefit from the globally stored credentials. If you need fine-grained control, please see the Packages documentation for sites.
​User Selection
If you have sites configured with user isolation, you will first need to select the appropriate server user. The auth.json file is global within each individual server user account.
​Managing Credentials
Forge makes it easy to manage Composer credentials across all sites on your server. You can add, remove, and update credentials directly from the Forge UI.
​Add Credentials
Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:

Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users
Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses
Password - this is generally the password associated with the username, however in some case, this may also be a license key

Click “Save” in order to store these credentials in the user’s global Composer configuration directory (~/.config/composer/auth.json).
​Remove Credentials
In order to remove Composer credentials, you can click on the red X button.
After removing credentials, you must click “Save” in order to update the credentials configuration on the server.
​Update Credentials
Any credentials that are shown on the screen can be updated with any new adequate value.
After updating the credential, you must click “Save” in order to update the credentials configuration on the server.
​Circle Permissions
The ability to manage a server’s Composer packages is determined by the server:manage-packages permission. This permission will also allow the circle member to manage a site’s Composer packages too.Was this page helpful?YesNoPHPRecipesOn this pageOverviewGlobal Composer CredentialsUser SelectionManaging CredentialsAdd CredentialsRemove CredentialsUpdate CredentialsCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge allows you to manage the “http-basic” portion of the selected server user’s \", _jsx(_components.code, {\n        children: \"auth.json\"\n      }), \" Composer configuration file. The provided credentials are only stored on the server being managed by Forge - not in Forge itself.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"global-composer-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Global Composer Credentials\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The Composer credentials that you can manage on the server level will apply to all sites that are served by the same Ubuntu user account. For example, if you have two sites installed under the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user, both these sites will benefit from the globally stored credentials. If you need fine-grained control, please see the \", _jsx(_components.a, {\n        href: \"/sites/packages\",\n        children: \"Packages\"\n      }), \" documentation for sites.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"user-selection\",\n      isAtRootLevel: \"true\",\n      children: \"User Selection\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If you have sites configured with user isolation, you will first need to select the appropriate server user. The \", _jsx(_components.code, {\n        children: \"auth.json\"\n      }), \" file is global within each individual server user account.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"managing-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Credentials\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge makes it easy to manage Composer credentials across all sites on your server. You can add, remove, and update credentials directly from the Forge UI.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"add-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Add Credentials\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Additional credentials can be added by clicking the “Add Credentials” button. You need to provide:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Repository URL - this is how Composer matches the credentials to the package for which the provider wants to authenticate users\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Username - this is often an email address, but can also be any kind of unique identifier that the provider of the package uses\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Password - this is generally the password associated with the username, however in some case, this may also be a license key\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Click “Save” in order to store these credentials in the user’s global Composer configuration directory (\", _jsx(_components.code, {\n        children: \"~/.config/composer/auth.json\"\n      }), \").\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"remove-credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Remove Credentials\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"In order to remove Composer credentials, you can click on the red \", _jsx(_components.strong, {\n        childre