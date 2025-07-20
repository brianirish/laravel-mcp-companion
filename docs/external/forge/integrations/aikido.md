# Forge - Integrations/Aikido

*Source: https://forge.laravel.com/docs/integrations/aikido*

---

Aikido - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationIntegrationsAikidoDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseIntegrationsAikidoAikido provides security scanning with Forge integration.​Overview
Aikido provides security scanning for repositories. Forge has partnered with Aikido to allow for a seamless integration with your Forge sites.
​Connect with Aikido
Before you can use Aikido with Forge, you must connect your Forge account to an Aikido account.
To do this, visit the Aikido panel in the Forge dashboard.
Clicking “Connect Aikido” will allow you to connect your Forge account to an Aikido account.
You can connect multiple Aikido workspaces to a single Forge account, each representing a different organization or group in your source control provider.
This can be managed from the Aikido panel within Forge.
​Viewing Aikido Findings
When viewing a site in the Forge dashboard, the top security findings will be displayed on the Aikido tab.

The Aikido integration is only supported for GitHub, GitLab, GitLab Self-Hosted, and Bitbucket.Was this page helpful?YesNoSentryAbuseOn this pageOverviewConnect with AikidoViewing Aikido FindingsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    img: \"img\",\n    p: \"p\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Frame, Heading, Note, Warning} = _components;\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [_jsx(_components.a, {\n        href: \"https://aikido.dev\",\n        children: \"Aikido\"\n      }), \" provides security scanning for repositories. Forge has partnered with Aikido to allow for a seamless integration with your Forge sites.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"connect-with-aikido\",\n      isAtRootLevel: \"true\",\n      children: \"Connect with Aikido\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Before you can use Aikido with Forge, you must connect your Forge account to an Aikido account.\\nTo do this, visit the \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/aikido\",\n        children: \"Aikido panel\"\n      }), \" in the Forge dashboard.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Clicking “Connect Aikido” will allow you to connect your Forge account to an Aikido account.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"You can connect multiple Aikido workspaces to a single Forge account, each representing a different organization or group in your source control provider.\\nThis can be managed from the \", _jsx(_components.a, {\n          href: \"https://forge.laravel.com/user-profile/aikido\",\n          children: \"Aikido panel\"\n        }), \" within Forge.\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"viewing-aikido-findings\",\n      isAtRootLevel: \"true\",\n      children: \"Viewing Aikido Findings\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"When viewing a site in the Forge dashboard, the top security findings will be displayed on the Aikido tab.\"\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/aikido-top-security-findings.png\",\n          alt: \"Screenshot showing the top security findings\"\n        })\n      })\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"The Aikido integration is only supported for GitHub, GitLab, GitLab Self-Hosted, and Bitbucket.\"\n      })\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"$schema":"https://mintlify.com/docs.json","theme":"mint","name":"Laravel Forge","colors":{"primary":"#18B69B","light":"#18B69B","dark":"#18B69B"},"favicon":"/favicon.png","navigation":{"tabs":[{"tab":"Documentation","groups":[{"group":"Get Started","pages":["introduction","cli","sdk"]},{"group":"Accounts","pages":["accounts/your-account","accounts/circles","accounts/source-control","accounts/ssh","accounts/api","accounts/tags","accounts/cookbook"]},{"group":"Servers","pages":["servers/providers","servers/types","servers/management","servers/provisioning-process","servers/ssh","servers/php","servers/packages","servers/recipes","servers/load-balancing","servers/nginx-templates","servers/backups","servers/monitoring","servers/cookbook"]},{"group":"Sites","pages":["sites/the-basics","sites/applications","sites/deployments","sites/commands","sites/packages","sites/queues","sites/security-rules","sites/redirects","sites/ssl","sites/user-isolation","sites/cookbook"]},{"group":"Resources","pages":["resources/daemons","resources/databases","resources/caches","resources/network","resources/scheduler","resources/integrations","resources/cookbook"]},{"group":"Integrations","pages":["integrations/envoyer","integrations/sentry","integrations/aikido"]},{"group":"Other","pages":["abuse"]}]},{"tab":"Changelog","groups":[{"group":"","pages":["changelog/changelog"]}]}],"global":{"anchors":[{"anchor":"Community","href":"https://discord.com/invite/laravel","icon":"discord"},{"anchor":"Blog","href":"https://blog.laravel.com/forge","icon":"newspaper"}]}},"logo":{"light":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","dark":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/logo.svg","href":"https://forge.laravel.com"},"api":{"playground":{"display":"simple"},"examples":{"languages":["php","bash","javascript","go"]}},"background":{"decoration":"windows"},"navbar":{"links":[{"label":"Support","href":"mailto:forge@laravel.com"}],"primary":{"type":"button","la