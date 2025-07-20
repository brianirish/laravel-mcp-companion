# Forge - Accounts/Cookbook

*Source: https://forge.laravel.com/docs/accounts/cookbook*

---

Troubleshooting - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationAccountsTroubleshootingDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseAccountsTroubleshootingAccount Troubleshooting​Forge Is Unable To Access Git Repository
There are several reasons Forge may not be able to access your GitHub, GitLab, or Bitbucket repository. First, you should try refreshing the source control API token that is linked to Forge via your account profile’s “Source Control” tab.
Forge attempts to access your repository using your source control provider’s API. The API credentials that will be used are the credentials tied to the account of the person who owns the Forge server. If a Forge server is shared with you via a circle, it will use the circle owner’s API credentials. You should ensure this person has full access to the repository on GitHub.
​GitHub Organization Repositories
Sometimes, if the repository is an organization repository, you will need to grant Forge access to that organization. You may do that using the following link: https://github.com/settings/connections/applications/fdb28071bd05daebc122Was this page helpful?YesNoTagsServer ProvidersOn this pageForge Is Unable To Access Git RepositoryGitHub Organization RepositoriesLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    p: \"p\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"forge-is-unable-to-access-git-repository\",\n      isAtRootLevel: \"true\",\n      children: \"Forge Is Unable To Access Git Repository\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"There are several reasons Forge may not be able to access your GitHub, GitLab, or Bitbucket repository. First, you should try refreshing the source control API token that is linked to Forge via your account profile’s “Source Control” tab.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge attempts to access your repository using your source control provider’s API. The API credentials that will be used are the credentials tied to the account of the person who \", _jsx(_components.strong, {\n        children: \"owns\"\n      }), \" the Forge server. If a Forge server is shared with you via a circle, it will use the circle \", _jsx(_components.strong, {\n        children: \"owner’s\"\n      }), \" API credentials. You should ensure this person has full access to the repository on GitHub.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"github-organization-repositories\",\n      isAtRootLevel: \"true\",\n      children: \"GitHub Organization Repositories\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Sometimes, if the repository is an organization repository, you will need to grant Forge access to that organization. You may do that using the following link: \", _jsx(_components.a, {\n        href: \"https://github.com/settings/connections/applications/fdb28071bd05daebc122\",\n        children: \"https://github.com/settings/connections/applications/fdb28071bd05daebc122\"\n      })]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"$schema":"https://mintlify.com/docs.json","theme":"mint","name":"Laravel Forge","colors":{"primary":"#18B69B","light":"#18B69B","dark":"#18B69B"},"favicon":"/favicon.png","navigation":{"tabs":[{"tab":"Documentation","groups":[{"group":"Get Started","pages":["introduction","cli","sdk"]},{"group":"Accounts","pages":["accounts/your-account","accounts/circles","accounts/source-control","accounts/ssh","accounts/api","accounts/tags","accounts/cookbook"]},{"group":"Servers","pages":["servers/providers","servers/types","servers/management","servers/provisioning-process","servers/ssh","servers/php","servers/packages","servers/recipes","servers/load-balancing","servers/nginx-templates","servers/backups","servers/monitoring","servers/cookbook"]},{"group":"Sites","pages":["sites/the-basics","sites/applications","sites/deployments","sites/commands","sites/packages","sites/queues","sites/security-rules","sites/redirects","sites/ssl","sites/user-isolation","sites/cookbook"]},{"group":"Resources","pages":["resources/daemons","resources/databases","resources/caches","resources/network","resources/scheduler","resources/integrations","resources/cookbook"]},{"group":"Integrations","pages":["integrations/envoyer","integrations/sentry","integrations/aikido"]},{"group":"Other","pages":["abuse"]}]},{"tab":"Changelog","groups":[{"group":"","pages":["changelog/changelog"]}]}],"global":{"anchors":[{"anchor":"Community","href":"https://discord.com/invite/laravel","icon":"discord"},{"anchor":"Blog","href":"https://blog.laravel.com/forge","icon":"newspaper"}]}},"logo":{"light":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","dark":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","href":"https://forge.laravel.com"},"api":{"playground":{"display":"simple"},"examples":{"languages":["php","bash","javascript","go"]}},"background":{"decoration":"windows"},"navbar":{"links":[{"label":"Support","href":"mailto:forge@laravel.com"}],"primary":{"type":"button","label":"Dashboard","href":"https://forge.laravel.com"}},"footer":{"socials":{"x":"https://x.com/laravelphp","github":"https://github.com/laravel","discord":"https://discord.com/invite/laravel","linkedin":"https://linkedin.com/company/laravel"},"links":[{"header":"Legal and Compliance","items":[{"label":"Term of Service","href":"https://forge.laravel.com/terms-of-service"},{"label":"Privacy Policy","href":"https://forge.laravel.com/privacy-policy"},{"label":"Data Processing Agreement (DPA)","href":"https://forge.laravel.com/data-processing-agreement"}]}]},"integrations":{"fathom":{"siteId":"UZINDLYX"},"posthog":{"apiKey":"phc_FMim8XOwk9B4lf2tE4wViqxdGUhFAqJ4fNlgHYvI3Xz"}},"fonts":{"heading":{"family":"Figtree"},"body":{"family":"Figtree"}},"redirects":[{"destination":"/integrations/envoyer","source":"