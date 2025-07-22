# Forge - Accounts/Tags

*Source: https://forge.laravel.com/docs/accounts/tags*

---

Tags - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationAccountsTagsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseAccountsTagsLearn how to use tags to categorize servers and sites.​Overview
“Tagging” your servers and sites can make them easier to manage, especially if you have many servers / sites. Servers can be tagged via the server dashboard’s Settings tab’s Server Settings section, while sites can be tagged via the site Settings tab.
You may delete tags and their associations from Forge’s tags dashboard.
​Searching For Tagged Servers / Sites
Once servers and sites have been tagged, you may filter by those tags via Forge’s search bar located in the top navigation panel of the Forge dashboard. Alternatively, you may filter by your tags from the Forge active server list.Was this page helpful?YesNoAPITroubleshootingOn this pageOverviewSearching For Tagged Servers / SitesLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    p: \"p\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"“Tagging” your servers and sites can make them easier to manage, especially if you have many servers / sites. Servers can be tagged via the server dashboard’s \", _jsx(_components.strong, {\n        children: \"Settings\"\n      }), \" tab’s \", _jsx(_components.strong, {\n        children: \"Server Settings\"\n      }), \" section, while sites can be tagged via the site \", _jsx(_components.strong, {\n        children: \"Settings\"\n      }), \" tab.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may delete tags and their associations from Forge’s \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/tags\",\n        children: \"tags dashboard\"\n      }), \".\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"searching-for-tagged-servers-%2F-sites\",\n      isAtRootLevel: \"true\",\n      children: \"Searching For Tagged Servers / Sites\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Once servers and sites have been tagged, you may filter by those tags via Forge’s search bar located in the top navigation panel of the Forge dashboard. Alternatively, you may filter by your tags from the Forge \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/servers\",\n        children: \"active server list\"\n      }), \".\"]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"$schema":"https://mintlify.com/docs.json","theme":"mint","name":"Laravel Forge","colors":{"primary":"#18B69B","light":"#18B69B","dark":"#18B69B"},"favicon":"/favicon.png","navigation":{"tabs":[{"tab":"Documentation","groups":[{"group":"Get Started","pages":["introduction","cli","sdk"]},{"group":"Accounts","pages":["accounts/your-account","accounts/circles","accounts/source-control","accounts/ssh","accounts/api","accounts/tags","accounts/cookbook"]},{"group":"Servers","pages":["servers/providers","servers/types","servers/management","servers/provisioning-process","servers/ssh","servers/php","servers/packages","servers/recipes","servers/load-balancing","servers/nginx-templates","servers/backups","servers/monitoring","servers/cookbook"]},{"group":"Sites","pages":["sites/the-basics","sites/applications","sites/deployments","sites/commands","sites/packages","sites/queues","sites/security-rules","sites/redirects","sites/ssl","sites/user-isolation","sites/cookbook"]},{"group":"Resources","pages":["resources/daemons","resources/databases","resources/caches","resources/network","resources/scheduler","resources/integrations","resources/cookbook"]},{"group":"Integrations","pages":["integrations/envoyer","integrations/sentry","integrations/aikido"]},{"group":"Other","pages":["abuse"]}]},{"tab":"Changelog","groups":[{"group":"","pages":["changelog/changelog"]}]}],"global":{"anchors":[{"anchor":"Community","href":"https://discord.com/invite/laravel","icon":"discord"},{"anchor":"Blog","href":"https://blog.laravel.com/forge","icon":"newspaper"}]}},"logo":{"light":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","dark":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","href":"https://forge.laravel.com"},"api":{"playground":{"display":"simple"},"examples":{"languages":["php","bash","javascript","go"]}},"background":{"decoration":"windows"},"navbar":{"links":[{"label":"Support","href":"mailto:forge@laravel.com"}],"primary":{"type":"button","label":"Dashboard","href":"https://forge.laravel.com"}},"footer":{"socials":{"x":"https://x.com/laravelphp","github":"https://github.com/laravel","discord":"https://discord.com/invite/laravel","linkedin":"https://linkedin.com/company/laravel"},"links":[{"header":"Legal and Compliance","items":[{"label":"Term of Service","href":"https://forge.laravel.com/terms-of-service"},{"label":"Privacy Policy","href":"https://forge.laravel.com/privacy-policy"},{"label":"Data Processing Agreement (DPA)","href":"https://forge.laravel.com/data-processing-agreement"}]}]},"integrations":{"fathom":{"siteId":"UZINDLYX"},"posthog":{"apiKey":"phc_FMim8XOwk9B4lf2tE4wViqxdGUhFAqJ4fNlgHYvI3Xz"}},"fonts":{"heading":{"family":"Figtree"},"body":{"family":"Figtree"}},"redirects":[{"destination":"/integrations/envoyer","source":"/sites/envoyer","_id":"687ea9b6d5e92a9c2e46c2ca"},{"destination":"/introduction","source":"/introduction.html","_id":"687ea9b6d5e92a9c2e46c2cb"},{"destination":"/cli","source":"/cli.html","_id":"687ea9b6d5e92a9c2e46c2cc"},{"destination":"/sdk","source":"/sdk.html","_id":"687ea9b6d5e92a9c2e46c2cd"},{"destination":"/accounts/your-account","source":"/accounts/your-account.html","_id":"687ea9b6d5e92a9c2e46c2ce"},{"destination":"/accounts/circles","source":"/accounts/circles.html","_id":"687ea9b6d5e92a9c2e46c2cf"},{"destination":"/accoun