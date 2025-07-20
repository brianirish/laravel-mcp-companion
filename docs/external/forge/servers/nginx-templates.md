# Forge - Servers/Nginx-Templates

*Source: https://forge.laravel.com/docs/servers/nginx-templates*

---

Nginx Templates - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersNginx TemplatesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersNginx TemplatesLearn how to use Nginx templates to customize your site configurations.​Overview
Nginx templates allow you to customize the Nginx site configuration that Forge uses when creating your new site.
Nginx templates that are not valid will prevent Nginx from properly working and your existing sites may stop responding. You should proceed with caution when creating and deploying custom Nginx templates.
​Managing Templates
​Create Template
You may create your own Nginx templates from within a server’s management dashboard. When creating a new template, you need to provide a template name and the template’s content. Forge will provide a default template that you may alter as required.
Although the default template does not show support for TLSv1.3, Forge will automatically update a site to support it if the server is able to do so.
​Edit Templates
You may edit the name and content of your Nginx template at any time. Changes to a template will not affect existing sites that use the template.
​Delete Templates
Deleting a template will not remove any sites which were configured to use it.
​Template Variables
Forge provides several variables that can be used within your templates to dynamically alter their content for new sites:
VariableDescription{{DIRECTORY}}The site’s configured web directory, e.g. /public{{DOMAINS}}The site’s configured domains to respond to, e.g. laravel.com alias.laravel.com{{PATH}}The site’s web accessible directory, e.g. /home/forge/laravel.com/public{{PORT}}The IPv4 port the site should listen to (:80). If the site name is default, this variable will also contain default_server{{PORT_V6}}The IPV6 port to listen to ([::]:80). If the site name is default, this variable will also contain default_server{{PROXY_PASS}}The PHP socket to listen on, e.g. unix:/var/run/php/php8.0-fpm.sock{{ROOT_PATH}}The root of the configured site, e.g. /home/forge/laravel.com{{SERVER_PUBLIC_IP}}The public IP address of the server{{SERVER_PRIVATE_IP}}The private IP address of the server, if available{{SITE}}The site’s name, e.g. laravel.com. This differs from {{DOMAINS}} in that it does not include site aliases.{{SITE_ID}}The site’s ID, e.g. 12345{{USER}}The site’s user, e.g. forge
When using these variables, you should ensure that they exactly match the syntax shown above.
​Circle Permissions
The ability to manage Nginx Templates is determined by the site:manage-nginx permission. This permission is also used to restrict the ability to edit an existing site’s Nginx configuration file.Was this page helpful?YesNoLoad BalancingDatabase BackupsOn this pageOverviewManaging TemplatesCreate TemplateEdit TemplatesDelete TemplatesTemplate VariablesCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    code: \"code\",\n    p: \"p\",\n    table: \"table\",\n    tbody: \"tbody\",\n    td: \"td\",\n    th: \"th\",\n    thead: \"thead\",\n    tr: \"tr\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Note, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Nginx templates allow you to customize the Nginx site configuration that Forge uses when creating your new site.\"\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"Nginx templates that are not valid will prevent Nginx from properly working and your existing sites may stop responding. You should proceed with caution when creating and deploying custom Nginx templates.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"managing-templates\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Templates\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"create-template\",\n      isAtRootLevel: \"true\",\n      children: \"Create Template\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"You may create your own Nginx templates from within a server’s management dashboard. When creating a new template, you need to provide a template name and the template’s content. Forge will provide a default template that you may alter as required.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsx(_components.p, {\n        children: \"Although the default template does not show support for TLSv1.3, Forge will automatically update a site to support it if the server is able to do so.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"edit-templates\",\n      isAtRootLevel: \"true\",\n      children: \"Edit Templates\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"You may edit the name and content of your Nginx template at any time. Changes to a template will not affect existing sites that use the template.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"delete-templates\",\n      isAtRootLevel: \"true\",\n      children: \"Delete Templates\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Deleting a template will not remove any sites which were configured to use it.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"template-variables\",\n      isAtRootLevel: \"true\",\n      children: \"Template Variables\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge provides several variables that can be used within your templates to dynamically alter their content for new sites:\"\n    }), \"\\n\", _jsxs(_components.table, {\n      children: [_jsx(_components.thead, {\n        children: _jsxs(_components.tr, {\n          children: [_jsx(_components.th, {\n            children: \"Variable\"\n          }), _jsx(_components.th, {\n            children: \"Description\"\n          })]\n        })\n      }), _jsxs(_components.tbody, {\n        children: [_jsxs(_components.tr, {\n          children: [_jsx(_components.td, {\n            children: _jsx(_components.code, {\n              children: \"{{DIRECTORY}}\"\n            })\n          }), _jsxs(_components.td, {\n            children: [\"The site’s configured web directory, e.g. \", _jsx(_components.code, {\n              children: \"/public\"\n            })]\n          })]\n        }), _jsxs(_components