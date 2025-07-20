# Forge - Servers/Load-Balancing

*Source: https://forge.laravel.com/docs/servers/load-balancing*

---

Load Balancing - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersLoad BalancingDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersLoad BalancingLearn how to use load balancers to distribute traffic across multiple servers.​Overview
Load balancers are used to distribute web traffic amongst two or more servers and are often used for websites which receive high volumes of traffic.
The key differences between a Forge application server and a load balancer are:

A database server will not be installed
PHP is not installed
Node.js is not installed

​Creating Load Balancers
When provisioning a new server, select the Load Balancer type. Once provisioning has completed, you can now create a load balanced site. The site name / domain should match the name of the corresponding site on the servers that will be receiving the traffic.
Once you have added the site to your server, Forge will ask you to select the servers you wish to balance traffic across. The list of servers will include all of the servers in the same private network as the load balancer.
​Load Balancer Methods
Forge allows you to select one of three load balancer methods:

Round Robin - The default method, where requests are distributed evenly across all servers.
Least Connections - Requests are sent to the server with the least connections.
IP Hash - The server to which a request is sent is determined by the client IP address. This means that requests from the same address are always handled by the same server unless it is unavailable.

You may switch the load balancer method at any time.
You can learn more about how Nginx load balancers work by consulting the Nginx documentation.
​Server Weights
Each server balanced by the load balancer can be configured with different weights, indicating that some servers should serve more traffic than others. For example, if you have two servers in your load balancer, one with a weight of 5 and the other with 1, then the first server would be sent five out of every six requests made to the load balancer.
​Backup Servers
Individual servers can be marked as a backup. Backup servers will receive no traffic unless all other servers managed by the load balancer are not responding.
​Pausing Traffic
You may pause traffic to a specific server being managed by the balancer. While paused, the selected server will no longer serve incoming traffic. You may unpause the server at any time.
​SSL
Typically, SSL certificates are installed on the individual application servers. However, when using load balancing, the certificate should be configured on the load balancer itself. You should consult the SSL documentation for more information on managing SSL certificates for your servers, including load balancers.
When using SSL on a load balancer, you will likely need to configure the “trusted proxies” for your application. For Laravel applications, consult the trusted proxies documentation.Was this page helpful?YesNoRecipesNginx TemplatesOn this pageOverviewCreating Load BalancersLoad Balancer MethodsServer WeightsBackup ServersPausing TrafficSSLLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    li: \"li\",\n    ol: \"ol\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Note} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Load balancers are used to distribute web traffic amongst two or more servers and are often used for websites which receive high volumes of traffic.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"The key differences between a Forge application server and a load balancer are:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"A database server will not be installed\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"PHP is not installed\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Node.js is not installed\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-load-balancers\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Load Balancers\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When provisioning a new server, select the \", _jsx(_components.strong, {\n        children: \"Load Balancer\"\n      }), \" type. Once provisioning has completed, you can now create a load balanced site. The site name / domain should match the name of the corresponding site on the servers that will be receiving the traffic.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Once you have added the site to your server, Forge will ask you to select the servers you wish to balance traffic across. The list of servers will include all of the servers in the same private network as the load balancer.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"load-balancer-methods\",\n      isAtRootLevel: \"true\",\n      children: \"Load Balancer Methods\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge allows you to select one of three load balancer methods:\"\n    }), \"\\n\", _jsxs(_components.ol, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Round Robin - The default method, where requests are distributed evenly across all servers.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Least Connections - Requests are sent to the server with the least connections.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"IP Hash - The server to which a request is sent is determined by the client IP address. This means that requests from the same address are always handled by the same server unless it is unavailable.\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"You may switch the load balancer method at any time.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"You can learn more about how Nginx load balancers work by \", _jsx(_components.a, {\n          href: \"https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/#method\",\n          children: \"consulting the Nginx documentation\"\n        }), \".\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"serve