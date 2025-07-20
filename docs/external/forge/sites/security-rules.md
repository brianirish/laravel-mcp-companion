# Forge - Sites/Security-Rules

*Source: https://forge.laravel.com/docs/sites/security-rules*

---

Security Rules - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesSecurity RulesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesSecurity RulesConfigure password protection on your sites.​Overview
Forge can configure password protection on your sites using basic access authentication. You can choose whether to protect your entire site or a specific path.
​Managing Security Rules
​Creating a Security Rule
You may create a new Security Rule from your site’s management dashboard in Forge. You must supply a security rule name, which some browsers will display in their authentication prompt, as well as at least one set of credentials. If you need to add multiple credentials, you can click the + button to add a new username and password combination.
Once you’ve configured your security rule, click the Add Security Rule button.
​Credentials
Forge creates a unique .htpasswd file for each security rule, meaning each secured path may have its own set of credentials. This also means that you will need to re-enter the same credentials when securing multiple paths. If you need to modify the credentials, you can find the .htpasswd file at /etc/nginx/forge-conf/.../server/.htpasswd-{ruleId} on your servers.
Forge does not store your security Rule passwords on our servers.
​Customization
Nginx allows you to add further access restrictions such as allowing and denying access to users by IP address. Forge does not provide the ability to configure this, but you are free to customize your own protected site configuration. Forge creates a /etc/nginx/forge-conf/.../server/protected_site-{ruleId}.conf configuration file for protected sites. You can read more about Nginx and basic access authentication in the Nginx documentation.
​Circle Permissions
You may grant a circle member authority to create and manage security rules by granting the site:manage-security permission.Was this page helpful?YesNoQueuesRedirectsOn this pageOverviewManaging Security RulesCreating a Security RuleCredentialsCustomizationCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge can configure password protection on your sites using \", _jsx(_components.a, {\n        href: \"https://en.wikipedia.org/wiki/Basic_access_authentication\",\n        children: \"basic access authentication\"\n      }), \". You can choose whether to protect your entire site or a specific path.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"managing-security-rules\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Security Rules\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"creating-a-security-rule\",\n      isAtRootLevel: \"true\",\n      children: \"Creating a Security Rule\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may create a new Security Rule from your site’s management dashboard in Forge. You must supply a security rule name, which some browsers will display in their authentication prompt, as well as at least one set of credentials. If you need to add multiple credentials, you can click the \", _jsx(_components.strong, {\n        children: \"+\"\n      }), \" button to add a new username and password combination.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Once you’ve configured your security rule, click the \", _jsx(_components.strong, {\n        children: \"Add Security Rule\"\n      }), \" button.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"credentials\",\n      isAtRootLevel: \"true\",\n      children: \"Credentials\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge creates a unique \", _jsx(_components.code, {\n        children: \".htpasswd\"\n      }), \" file for each security rule, meaning each secured path may have its own set of credentials. This also means that you will need to re-enter the same credentials when securing multiple paths. If you need to modify the credentials, you can find the \", _jsx(_components.code, {\n        children: \".htpasswd\"\n      }), \" file at \", _jsx(_components.code, {\n        children: \"/etc/nginx/forge-conf/.../server/.htpasswd-{ruleId}\"\n      }), \" on your servers.\"]\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"Forge does not store your security Rule passwords on our servers.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"customization\",\n      isAtRootLevel: \"true\",\n      children: \"Customization\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Nginx allows you to add further access restrictions such as allowing and denying access to users by IP address. Forge does not provide the ability to configure this, but you are free to customize your own protected site configuration. Forge creates a \", _jsx(_components.code, {\n        children: \"/etc/nginx/forge-conf/.../server/protected_site-{ruleId}.conf\"\n      }), \" configuration file for protected sites. You can read more about Nginx and basic access authentication \", _jsx(_components.a, {\n        href: \"https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/#\",\n        children: \"in the Nginx documentation\"\n      }), \".\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"circle-permissions\",\n      isAtRootLevel: \"true\",\n      children: \"Circle Permissions\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may grant a circle member authority to create and manage security rules by granting the \", _jsx(_components.code, {\n        children: \"site:manage-security\"\n      }), \" permission.\"]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (compon