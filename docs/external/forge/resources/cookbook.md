# Forge - Resources/Cookbook

*Source: https://forge.laravel.com/docs/resources/cookbook*

---

Cookbook - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationResourcesCookbookDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseResourcesCookbookCommon issues and solutions for Laravel Forge.​Scheduled Jobs Not Running
It’s important to be aware that one single misconfigured scheduled job will break all jobs in the scheduler. You should verify that your frequency and commands are correct using a tool such as Crontab.guru.
​Deleted SSH Firewall Rule
If you have deleted the firewall rule (typically port 22) from the Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.
To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.
Forge uses ufw for the firewall, so once you’ve connected to the server you need to run the following as root:
CopyAsk AIufw allow 22
Was this page helpful?YesNoIntegrationsEnvoyerOn this pageScheduled Jobs Not RunningDeleted SSH Firewall RuleLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"scheduled-jobs-not-running\",\n      isAtRootLevel: \"true\",\n      children: \"Scheduled Jobs Not Running\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"It’s important to be aware that one single misconfigured scheduled job will break \", _jsx(_components.strong, {\n        children: \"all jobs\"\n      }), \" in the scheduler. You should verify that your frequency and commands are correct using a tool such as \", _jsx(_components.a, {\n        href: \"https://crontab.guru\",\n        children: \"Crontab.guru\"\n      }), \".\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"deleted-ssh-firewall-rule\",\n      isAtRootLevel: \"true\",\n      children: \"Deleted SSH Firewall Rule\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"If you have deleted the firewall rule (typically port 22) from the Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge uses \", _jsx(_components.code, {\n        children: \"ufw\"\n      }), \" for the firewall, so once you’ve connected to the server you need to run the following as \", _jsx(_components.code, {\n        children: \"root\"\n      }), \":\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"ufw\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" allow\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#B5CEA8\"\n              },\n              children: \" 22\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"$schema":"https://mintlify.com/docs.json","theme":"mint","name":"Laravel Forge","colors":{"primary":"#18B69B","light":"#18B69B","dark":"#18B69B"},"favicon":"/favicon.png","navigation":{"tabs":[{"tab":"Documentation","groups":[{"group":"Get Started","pages":["introduction","cli","sdk"]},{"group":"Accounts","pages":["accounts/your-account","accounts/circles","accounts/source-control","accounts/ssh","accounts/api","accounts/tags","accounts/cookbook"]},{"group":"Servers","pages":["servers/providers","servers/types","servers/management","servers/provisioning-process","servers/ssh","servers/php","servers/packages","servers/recipes","servers/load-balancing","servers/nginx-templates","servers/backups","servers/monitoring","servers/cookbook"]},{"group":"Sites","pages":["sites/the-basics","sites/applications","sites/deployments","sites/commands","sites/packages","sites/queues","sites/security-rules","sites/redirects","sites/ssl","sites/user-isolation","sites/cookbook"]},{"group":"Resources","pages":["resources/daemons","resources/databases","resources/caches","resources/network","resources/scheduler","resources/integrations","resources/cookbook"]},{"group":"Integrations","pages":["integrations/envoyer","integrations/sentry","integrations/aikido"]},{"group":"Other","pages":["abuse"]}]},{"tab":"Changelog","groups":[{"group":"","pages":["changelog/changelog"]}]}],"global":{"anchors":[{"anchor":"Community","href":"https://discord.com/invite/laravel","icon":"discord"},{"anchor":"Blog","href":"https://blog.laravel.com/forge","icon":"newspaper"}]}},"logo":{"light":"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/logo/lo