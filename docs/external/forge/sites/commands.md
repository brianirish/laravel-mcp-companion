# Forge - Sites/Commands

*Source: https://forge.laravel.com/docs/sites/commands*

---

Commands - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesCommandsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesCommandsLearn how to run arbitrary commands from the Commands panel.​Overview
You may execute arbitrary Bash commands from the Commands panel. Commands are executed from within the site’s root directory, e.g. /home/forge/site.com. If you need to run commands within another directory you may prefix the command with a cd operation:
CopyAsk AIcd bin &amp;&amp; ./run-command.sh

​Running Commands
Commands can be executed from the Site’s Commands panel.
Sites that were created with the General PHP / Laravel project type will automatically suggest common Laravel Artisan commands.
Commands are not executed within a tty, which means that input / passwords cannot be provided.
​Command History
The last 10 previously executed commands will be shown within the Command History table. Alongside the command that was run, Forge will also display:

The user who initiated the command. This is particularly helpful when using Forge within Circles.
The command that was executed.
The date and time of execution.
The status of the command.

From the Command History table, it’s also possible to view the output of the command and re-run the command.
​Commands vs. Recipes
While Recipes also allow you to run arbitrary Bash scripts on your servers, Commands differ in a few, but important ways:

Recipes run at a server level. In other words, they cannot dynamically change into a site’s directory unless you already know the directory ahead of time.
Recipes can run using the root user. Commands only run as the site’s user, which in most cases will be forge unless the site is “isolated”.
Recipes are better equipped for running larger Bash scripts. Commands focus on running short commands, such as php artisan config:cache.

​Circle Permissions
You may grant a circle member authority to run arbitrary commands in a site’s directory by granting the site:manage-commands permission.Was this page helpful?YesNoDeploymentsPackagesOn this pageOverviewRunning CommandsCommand HistoryCommands vs. RecipesCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may execute arbitrary Bash commands from the Commands panel. Commands are executed from within the site’s root directory, e.g. \", _jsx(_components.code, {\n        children: \"/home/forge/site.com\"\n      }), \". If you need to run commands within another directory you may prefix the command with a \", _jsx(_components.code, {\n        children: \"cd\"\n      }), \" operation:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"cd\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" bin\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#1F2328\",\n                \"--shiki-dark\": \"#f3f7f6\"\n              },\n              children: \" \u0026\u0026 \"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"./run-command.sh\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"running-commands\",\n      isAtRootLevel: \"true\",\n      children: \"Running Commands\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Commands can be executed from the Site’s \", _jsx(_components.strong, {\n        children: \"Commands\"\n      }), \" panel.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Sites that were created with the \", _jsx(_components.strong, {\n        children: \"General PHP / Laravel\"\n      }), \" project type will automatically suggest common Laravel Artisan commands.\"]\n    }), \"\\n\", _jsx(Note, {\n      children: _jsx(_components.p, {\n        children: \"Commands are not executed within a tty, which means that input / passwords cannot be provided.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"command-history\",\n      isAtRootLevel: \"true\",\n      children: \"Command History\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The last 10 previously executed commands will be shown within the \", _jsx(_components.strong, {\n        children: \"Command History\"\n      }), \" table. Alongside the command that was run, Forge will also display:\"]\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsxs(_components.li, {\n        children: [\"The user who initiated the command. This is particularly helpful when using Forge within \", _jsx(_components.a, {\n          href: \"/accounts/circles\",\n          children: \"Circles\"\n        }), \".\"]\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"The command that was executed.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"The date and time of execution.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"The status of the command.\"\n      }), \"\\n\"]\n  