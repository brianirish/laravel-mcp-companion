# Forge - Integrations/Sentry

*Source: https://forge.laravel.com/docs/integrations/sentry*

---

Sentry - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationIntegrationsSentryDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseIntegrationsSentrySentry provides error monitoring and tracing for Laravel apps with Forge integration for creating Sentry organizations.​Overview
Sentry provides error monitoring and tracing for Laravel applications. Forge has partnered with Sentry to allow you to create new Sentry organizations without leaving Forge.
After creating your Sentry organization, you may easily add Sentry error monitoring to any of your Forge powered sites.
​Connect with Sentry
Before you can use Sentry with Forge, you must connect your Forge account to a Sentry account. To do this,
visit the Sentry panel in the Forge dashboard.

Clicking “Connect with Sentry” will create a new, Forge-linked Sentry organization with the email address shown under
“Sentry Account Email”. You will receive an email from Sentry confirming your new organization.
It is not possible to use an existing Sentry organization with the Forge integration. Forge created Sentry projects will be added
to the new organization.
​Creating Sentry Projects
Forge allows you to create new Sentry projects directly from the Forge dashboard. To create a new Sentry project,
visit the site’s Sentry dashboard.

Clicking “Create Sentry Project” will create a new project within the server owner’s connected Sentry organization.
Once the project is created, you will be provided with a DSN key that you may use to configure your Laravel application.
Forge does not automatically install Sentry into your Laravel application. You should install the
Sentry SDK for Laravel via Composer and define the SENTRY_DSN environment variable.
​Circle Permissions
The ability to manage a site’s Sentry project is determined by the site:manage-integrations permission.Was this page helpful?YesNoEnvoyerAikidoOn this pageOverviewConnect with SentryCreating Sentry ProjectsCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    p: \"p\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Frame, Heading, Note, Warning} = _components;\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [_jsx(_components.a, {\n        href: \"https://sentry.io\",\n        children: \"Sentry\"\n      }), \" provides error monitoring and tracing for Laravel applications. Forge has partnered with Sentry to allow you to create new Sentry organizations without leaving Forge.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"After creating your Sentry organization, you may easily add Sentry error monitoring to any of your Forge powered sites.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"connect-with-sentry\",\n      isAtRootLevel: \"true\",\n      children: \"Connect with Sentry\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Before you can use Sentry with Forge, you must connect your Forge account to a Sentry account. To do this,\\nvisit the \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/sentry\",\n        children: \"Sentry panel\"\n      }), \" in the Forge dashboard.\"]\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/sentry-user-profile.png\",\n          alt: \"Connect with Sentry User Profile form\"\n        })\n      })\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Clicking “Connect with Sentry” will create a new, Forge-linked Sentry organization with the email address shown under\\n“Sentry Account Email”. You will receive an email from Sentry confirming your new organization.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsx(_components.p, {\n        children: \"It is not possible to use an existing Sentry organization with the Forge integration. Forge created Sentry projects will be added\\nto the new organization.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-sentry-projects\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Sentry Projects\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge allows you to create new Sentry projects directly from the Forge dashboard. To create a new Sentry project,\\nvisit the site’s Sentry dashboard.\"\n    }), \"\\n\", _jsx(Frame, {\n      children: _jsx(_components.p, {\n        children: _jsx(_components.img, {\n          src: \"https://mintlify.s3.us-west-1.amazonaws.com/forge-laravel/images/sentry-project-form.png\",\n          alt: \"Sentry Panel\"\n        })\n      })\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Clicking “Create Sentry Project” will create a new project within the server owner’s connected Sentry organization.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Once the project is created, you will be provided with a DSN key that you may use to configure your Laravel application.\"\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsxs(_components.p, {\n        children: [\"Forge does not automatically install Sentry into your Laravel application. You should install the\\n\", _jsx(_components.a, {\n          href: \"https://github.com/getsentry/sentry-laravel\",\n          children: \"Sentry SDK for Laravel\"\n        }), \" via Composer and define the \", _jsx(_components.code, {\n          children: \"SENTRY_DSN\"\n        }), \" environment variable.\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"circle-permissions\",\n      isAtRootLevel: \"true\",\n      children: \"Circle Permissions\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The ability to manage a site’s Sentry project is determined by the \", _jsx(_components.code, {\n        children: \"site:manage-integrations\"\n      }), \" permission.\"]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(prop