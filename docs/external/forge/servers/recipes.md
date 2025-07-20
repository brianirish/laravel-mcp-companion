# Forge - Servers/Recipes

*Source: https://forge.laravel.com/docs/servers/recipes*

---

Recipes - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersRecipesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersRecipesSave and run common Bash scripts across your servers.​Overview
Recipes allow you to save common Bash scripts and run them across any of your servers. For example, you could save a recipe to install MongoDB so you can conveniently run it on future servers. The output of the recipe will be emailed to you.
​Creating Recipes
You can create your own recipe from the Recipes dashboard. When creating a new recipe you will be asked to supply:

The name of the recipe
The operating system user that the script should be run as
The recipe script contents

​Variables
Forge provides a few variables that can be used to make your recipe more dynamic. You are free to use any of these variables within your recipe’s script:

{{server_id}} - The ID of the server that the recipe is running on
{{server_name}} - The name of the server that the recipe is running on
{{ip_address}} - The public IP address of the server
{{private_ip_address}} - The private IP address of the server
{{username}} - The server user who is running the script
{{db_password}} - The database password for the server the script is running on
{{server_type}} - The type of the server that the recipe is running on, i.e. one of the following…

&quot;app&quot;
&quot;cache&quot;
&quot;database&quot;
&quot;loadbalancer&quot;
&quot;meilisearch&quot;
&quot;web&quot;
&quot;worker&quot;



When using these variables, you should ensure that they exactly match the syntax shown above.
​Running Recipes
When running a recipe, you will be presented with options that allow you to have the output of the recipe emailed to you and allow you to configure which servers the recipe will run on.Was this page helpful?YesNoPackagesLoad BalancingOn this pageOverviewCreating RecipesVariablesRunning RecipesLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Recipes allow you to save common Bash scripts and run them across any of your servers. For example, you could save a recipe to install MongoDB so you can conveniently run it on future servers. The output of the recipe will be emailed to you.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-recipes\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Recipes\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You can create your own recipe from the \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/recipes\",\n        children: \"Recipes dashboard\"\n      }), \". When creating a new recipe you will be asked to supply:\"]\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"The name of the recipe\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"The operating system user that the script should be run as\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"The recipe script contents\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"variables\",\n      isAtRootLevel: \"true\",\n      children: \"Variables\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge provides a few variables that can be used to make your recipe more dynamic. You are free to use any of these variables within your recipe’s script:\"\n    }), \"\\n\", _jsx(\"div\", {\n      \"v-pre\": true,\n      children: _jsxs(_components.ul, {\n        children: [\"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{server_id}}\"\n          }), \" - The ID of the server that the recipe is running on\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{server_name}}\"\n          }), \" - The name of the server that the recipe is running on\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{ip_address}}\"\n          }), \" - The public IP address of the server\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{private_ip_address}}\"\n          }), \" - The private IP address of the server\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{username}}\"\n          }), \" - The server user who is running the script\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{db_password}}\"\n          }), \" - The database password for the server the script is running on\"]\n        }), \"\\n\", _jsxs(_components.li, {\n          children: [_jsx(_components.code, {\n            children: \"{{server_type}}\"\n          }), \" - The type of the server that the recipe is running on, i.e. one of the following…\", \"\\n\", _jsxs(_components.ul, {\n            children: [\"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"app\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"cache\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"database\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"loadbalancer\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"meilisearch\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"web\\\"\"\n              })\n            }), \"\\n\", _jsx(_components.li, {\n              children: _jsx(_components.code, {\n                children: \"\\\"worker\\\"\"\n              })\n            }), \"\\n\"]\n          }), \"\\n\"]\n    