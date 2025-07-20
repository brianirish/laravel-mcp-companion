# Forge - Servers/Monitoring

*Source: https://forge.laravel.com/docs/servers/monitoring*

---

Monitoring - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersMonitoringDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersMonitoringLearn how to configure server monitoring in Forge.​Overview
Forge can be configured to monitor the following metrics on your server and email you when their state changes:

CPU Load Average
Used Disk Space
Used Memory

Server monitoring is only available on our “business” plan.
​Monitor Types
​CPU Load Average
The CPU Load Average monitor will track the server’s load average. This is based on the average system load over a one minute interval.
​Used Disk Space
The Used Disk Space monitor tracks the amount of disk space that has been used on the primary drive.
​Used Memory
The Used Memory monitor tracks how much of the RAM is in active use.
​Creating Monitors
You may configure a new monitor from the Monitoring tab within a server’s management dashboard. Below is a brief overview of how to create and configure a monitoring metric:

Select the metric to monitor.
Select whether the value of the metric should be &gt;= or &lt;= a threshold.
Enter the threshold percentage that the metric would need to meet before notifying you.
Enter how long (in minutes) the metric needs to exceed the threshold criteria for before you are notified.
Enter an email address to notify when the monitor’s state changes.
Click Install Monitor.

Once the monitor is installed, your server will begin collecting metric data and notify you once the state changes.
Forge will only accept one email address to notify. If you need to notify multiple people, you should create a distribution list such as [email&#160;protected].
​Stat Collection Frequencies
The CPU Load and Used Memory metric data will be collected every minute. The Disk Space metric will be collected hourly.
​Circle Permissions
The ability to manage server monitors is split into two permissions:

server:create-monitors
server:delete-monitors
Was this page helpful?YesNoDatabase BackupsCookbookOn this pageOverviewMonitor TypesCPU Load AverageUsed Disk SpaceUsed MemoryCreating MonitorsStat Collection FrequenciesCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    li: \"li\",\n    ol: \"ol\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Note, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge can be configured to monitor the following metrics on your server and email you when their state changes:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"CPU Load Average\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Used Disk Space\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Used Memory\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"Server monitoring is only available on our “business” plan.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"monitor-types\",\n      isAtRootLevel: \"true\",\n      children: \"Monitor Types\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"cpu-load-average\",\n      isAtRootLevel: \"true\",\n      children: \"CPU Load Average\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The \", _jsx(_components.strong, {\n        children: \"CPU Load Average\"\n      }), \" monitor will track the server’s load average. This is based on the average system load over a one minute interval.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"used-disk-space\",\n      isAtRootLevel: \"true\",\n      children: \"Used Disk Space\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The \", _jsx(_components.strong, {\n        children: \"Used Disk Space\"\n      }), \" monitor tracks the amount of disk space that has been used on the primary drive.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"used-memory\",\n      isAtRootLevel: \"true\",\n      children: \"Used Memory\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The \", _jsx(_components.strong, {\n        children: \"Used Memory\"\n      }), \" monitor tracks how much of the RAM is in active use.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-monitors\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Monitors\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may configure a new monitor from the \", _jsx(_components.strong, {\n        children: \"Monitoring\"\n      }), \" tab within a server’s management dashboard. Below is a brief overview of how to create and configure a monitoring metric:\"]\n    }), \"\\n\", _jsxs(_components.ol, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Select the metric to monitor.\"\n      }), \"\\n\", _jsxs(_components.li, {\n        children: [\"Select whether the value of the metric should be \", _jsx(_components.code, {\n          children: \"\u003e=\"\n        }), \" or \", _jsx(_components.code, {\n          children: \"\u003c=\"\n        }), \" a threshold.\"]\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Enter the threshold percentage that the metric would need to meet before notifying you.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Enter how long (in minutes) the metric needs to exceed the threshold criteria for before you are notified.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Enter an email address to notify when the monitor’s state changes.\"\n      }), \"\\n\", _jsxs(_components.li, {\n        children: [\"Click \", _jsx(_components.strong, {\n          children: \"Install Monitor\"\n        }), \".\"]\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Once the monitor is installed, your server will begin collecting metric data and notify you once the state changes.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"Forge will only accept one email address to notify. If you need to notify multiple people, you should create a distribution list such as \"