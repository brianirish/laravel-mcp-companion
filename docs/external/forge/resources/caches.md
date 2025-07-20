# Forge - Resources/Caches

*Source: https://forge.laravel.com/docs/resources/caches*

---

Caches - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationResourcesCachesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseResourcesCachesLearn how to connect to Redis and Memcache on your Forge server.​Overview
When provisioning an App Server or a Cache Server, Forge will automatically install Memcache and Redis. By default, neither of these services are exposed to the public and may only be accessed from within your server.
​Connecting To Redis
Redis and Memcache are both available via 127.0.0.1 and their default ports.
CopyAsk AIMEMCACHED_HOST=127.0.0.1
MEMCACHED_PORT=11211

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

​External Connections
All Forge servers require SSH key authentication and are not able to be accessed using passwords. Therefore, when selecting the SSH key to use during authentication, ensure that you select your private SSH key. For example, when connecting to Redis using the TablePlus database client:
Was this page helpful?YesNoDatabasesNetworkOn this pageOverviewConnecting To RedisExternal ConnectionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading, ZoomImage} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!ZoomImage) _missingMdxReference(\"ZoomImage\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When provisioning an \", _jsx(_components.a, {\n        href: \"/servers/types#app-servers\",\n        children: \"App Server\"\n      }), \" or a \", _jsx(_components.a, {\n        href: \"/servers/types#cache-servers\",\n        children: \"Cache Server\"\n      }), \", Forge will automatically install \", _jsx(_components.a, {\n        href: \"https://www.memcached.org/\",\n        children: \"Memcache\"\n      }), \" and \", _jsx(_components.a, {\n        href: \"https://redis.io/\",\n        children: \"Redis\"\n      }), \". By default, neither of these services are exposed to the public and may only be accessed from within your server.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"connecting-to-redis\",\n      isAtRootLevel: \"true\",\n      children: \"Connecting To Redis\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Redis and Memcache are both available via \", _jsx(_components.code, {\n        children: \"127.0.0.1\"\n      }), \" and their default ports.\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"6\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"6\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#9CDCFE\"\n              },\n              children: \"MEMCACHED_HOST\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \"=\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \"127.0.0.1\"\n            })]\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#9CDCFE\"\n              },\n              children: \"MEMCACHED_PORT\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \"=\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \"11211\"\n            })]\n          }), \"\\n\", _jsx(_components.span, {\n            className: \"line\"\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#9CDCFE\"\n              },\n              children: \"REDIS_HOST\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \"=\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \"127.0.0.1\"\n            })]\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#9CDCFE\"\n              },\n              children: \"REDIS_PASSWORD\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#CF222E\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \"=\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \"null\"\n            })]\n          }), \"\\n\", _jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#9CDCFE\"\n              },\n              children: \"REDIS_PORT\"\n            }), _jsx(_components.span, {\n              style: {\n              