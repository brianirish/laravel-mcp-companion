# Forge - Servers/Types

*Source: https://forge.laravel.com/docs/servers/types*

---

Server Types - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersServer TypesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersServer TypesLearn about the different types of servers you can provision with Forge.​Introduction
Forge supports provisioning several different types of servers:

Application Servers
Web Servers
Worker Servers
Load Balancers
Database Servers
Cache Servers

Below, we will discuss each of these server types in more detail.
​Server Types
For reference, here is a breakdown of what is offered by each server type:
TypeNginxPHPMySQL / Postgres / MariaDBRedis, MemcachedNode.jsMeilisearchApp Server✅✅✅✅✅Web Server✅✅✅Database Server✅Cache Server✅Worker Server✅MeiliSearch Server✅Load Balancer✅
​App Servers
Application servers are designed to include everything you need to deploy a typical Laravel / PHP application within a single server. Therefore, they are provisioned with the following software:

PHP
Nginx
MySQL / Postgres / MariaDB (if selected)
Redis
Memcached
Node.js
Supervisor

Application servers are the most typical type of server provisioned on Laravel Forge. If you’re unsure which server type you need, most likely you should provision an application server. As you need to scale your application, you may look at provisioning dedicated servers for services such as your database or caching, but starting with an App server is recommended.
​Web Servers
Web servers contain the web server software you need to deploy a typical Laravel / PHP application, but they do not contain a database or cache. Therefore, these servers are meant to be networked to other dedicated database and cache servers. Web servers are provisioned with the following software:

PHP
Nginx
Node.js
Supervisor

​Database Servers
Database servers are intended to function as dedicated MySQL / Postgres / MariaDB servers for your application. These servers are meant to be accessed by a dedicated application or web server via Forge’s network management features. Database servers are provisioned with the following software, based on your selections during the server’s creation:

MySQL, MariaDB, or PostgreSQL

​Cache Servers
Cache servers are intended to function as dedicated Redis / Memcached servers for your application. These servers are meant to be accessed by a dedicated application or web server via Forge’s network management features. Cache servers are provisioned with the following software:

Redis
Memcached

​Worker Servers
Worker servers are intended to function as dedicated PHP queue workers for your application. These servers are intended to be networked to your web servers, do not include Nginx, and are not accessible via HTTP. Worker servers are provisioned with the following software:

PHP
Supervisor

​Meilisearch Servers
Meilisearch servers install Meilisearch to provide a blazingly fast search service to your application. They are intended to be connected to another server, and communicate via a private network.
A Meilisearch server will only display and manage one Site. You cannot create or delete other sites on this server. When connecting to the Meilisearch server from a web or application server, you should connect to it via its private IP address.
​Load Balancers
Load balancers are meant to distribute incoming web traffic across your servers. To do so, load balancers use Nginx as a “reverse proxy” to evenly distribute the incoming traffic. Therefore, load balancers are only provisioned with Nginx.
Once provisioned you may configure your load balancer to meet your needs.Was this page helpful?YesNoServer ProvidersManagementOn this pageIntroductionServer TypesApp ServersWeb ServersDatabase ServersCache ServersWorker ServersMeilisearch ServersLoad BalancersLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"introduction\",\n      isAtRootLevel: \"true\",\n      children: \"Introduction\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge supports provisioning several different types of servers:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Application Servers\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Web Servers\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Worker Servers\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Load Balancers\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Database Servers\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Cache Servers\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Below, we will discuss each of these server types in more detail.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"server-types\",\n      isAtRootLevel: \"true\",\n      children: \"Server Types\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"For reference, here is a breakdown of what is offered by each server type:\"\n    }), \"\\n\", _jsxs(\"table\", {\n      children: [_jsx(\"thead\", {\n        children: _jsxs(\"tr\", {\n          children: [_jsx(\"th\", {\n            children: \"Type\"\n          }), _jsx(\"th\", {\n            children: \"Nginx\"\n          }), _jsx(\"th\", {\n            children: \"PHP\"\n          }), _jsx(\"th\", {\n            children: \"MySQL / Postgres / MariaDB\"\n          }), _jsx(\"th\", {\n            children: \"Redis, Memcached\"\n          }), _jsx(\"th\", {\n            children: \"Node.js\"\n          }), _jsx(\"th\", {\n            children: \"Meilisearch\"\n          })]\n        })\n      }), _jsxs(\"tbody\", {\n        children: [_jsxs(\"tr\", {\n          children: [_jsx(\"td\", {\n            scope: \"col\",\n            children: \"App Server\"\n          }), _jsx(\"td\", {\n            align: \"middle\",\n            children: \"✅\"\n          }), _jsx(\"td\", {\n            align: \"middle\",\n            children: \"✅\"\n          }), _jsx(\"td\", {\n            align: \"middle\",\n            children: \"✅\"\n          }), _jsx(\"td\", {\n            align: \"middle\",\n            children: \"✅\"\n          }), _jsx(\"td\", {\n            align: \"middle\",\n            children: \"✅\"\n          }), _jsx(\"td\", {\n            align: \"middle\"\n          })]\n        }), _jsxs(\"tr\", {\n          children: [_jsx(\"td\", {\n  