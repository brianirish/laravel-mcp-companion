# Forge - Resources/Network

*Source: https://forge.laravel.com/docs/resources/network*

---

Network - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationResourcesNetworkDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseResourcesNetworkLearn how to manage your server network and firewall.​Overview
Forge allows you to manage your server’s firewall as well as configure which servers can connect to other servers via the Network management panel within your server’s management dashboard.
If you manually create a ufw rule on your server, this will not be reflected in the Forge dashboard. Forge is only aware of rules created via the Forge dashboard.
​Server Network
Server networks make it painless to use a connected server as a separate database, cache, or queue server. For a server to be connected to an internal network, it must:

Be created by the same provider.
Be using the same server provider credentials.
Be owned by the same user.
Be within the same region.

Once you have granted access from one server to another, you may access the other server via its private IP address.
​Firewalls
You can configure and manage your firewall from within the Forge dashboard via the Network tab on the server’s management dashboard. Firewalls are used to open ports on your server to the Internet. For example, when using FTP you may need to open port 21.
For added security, you can restrict opened ports to specific IP addresses.
In the “From IP Address” field, you can provide multiple IP addresses by entering a list of comma separated IP addresses. For example: 192.168.1.1,192.168.1.2,192.168.1.3.
​Port Ranges
When creating new firewall rules, you may supply a range of ports to open (8000:8010), which will open every port from 8000 to 8010.
​Allow / Deny Rules
You may select whether to allow or deny the traffic that matches a given rule. By creating a deny rule, you will be preventing traffic from reaching the service.
To make deny rules work correctly, they are added at a higher priority than allow rules. Each new deny rule for IPv4 addresses will be added above any existing deny rules. UFW does not currently support IPv6 rules at first priority.
​Default Firewall Rules
As part of the provisioning process, Forge will automatically configure three rules:

SSH - Allow port 22 traffic from any IP Address
HTTP - Allow port 80 traffic from any IP Address
HTTPS - Allow port 443 traffic from any IP Address

You should note that although incoming traffic is allowed on port 22 for SSH connections, SSH connections that do not use an SSH key are not accepted. Therefore, it is not possible to brute force an SSH connection to your server. You should never delete the rule that allows SSH traffic to your server; otherwise, Forge will be unable to connect to or manage your server.
​Deleted SSH Firewall Rule
If you have deleted the firewall rule (typically port 22) from the Forge UI or directly on the server, Forge will be unable to connect to the server and will be unable to re-create this rule for you.
To fix this, you will need to access the server directly via your provider and manually add the SSH port again. DigitalOcean allows you to connect remotely through their dashboard.
Forge uses ufw for the firewall, so once you’ve connected to the server you need to run the following as root:
CopyAsk AIufw allow 22

​Circle Permissions
You may grant a circle member authority to manage the server’s network by granting the server:manage-network permission.Was this page helpful?YesNoCachesSchedulerOn this pageOverviewServer NetworkFirewallsPort RangesAllow / Deny RulesDefault Firewall RulesDeleted SSH Firewall RuleCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge allows you to manage your server’s firewall as well as configure which servers can connect to other servers via the \", _jsx(_components.strong, {\n        children: \"Network\"\n      }), \" management panel within your server’s management dashboard.\"]\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"If you manually create a \", _jsx(_components.code, {\n          children: \"ufw\"\n        }), \" rule on your server, this will not be reflected in the Forge dashboard. Forge is only aware of rules created via the Forge dashboard.\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"server-network\",\n      isAtRootLevel: \"true\",\n      children: \"Server Network\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Server networks make it painless to use a connected server as a separate database, cache, or queue server. For a server to be connected to an internal network, it must:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Be created by the same provider.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Be using the same server provider credentials.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Be owned by the same user.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Be within the same region.\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Once you have granted access from one server to another, you may access the other server via its private IP address.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"firewalls\",\n      isAtRootLevel: \"true\",\n      children: \"Firewalls\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You can configure and manage your firewall from within the Forge dashboard via the \", _jsx(_components.strong, {\n        children: \"Network\"\n      }), \" tab on the server’s management dashboard. Firewalls are used to open ports on your server to the Internet. For example, when using FTP you may need to open port \", _jsx(_components.code, {\n        children: \"21\"\n      }), \".\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"For added security, you can restrict opened ports to specific IP addresses.\"\n    }), \"\\n\", _jsxs(_components