# Forge - Sites/Redirects

*Source: https://forge.laravel.com/docs/sites/redirects*

---

Redirects - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesRedirectsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesRedirectsConfigure redirects for your sites.​Overview
Forge allows you to configure redirects that can be configured to automatically redirect visitors from one page to another. These redirect rules can be created via the “Redirects” tab of the site’s management dashboard.
​Creating Redirects
Redirects are wrappers around Nginx’s rewrite rules and can use the full redirect syntax supported by Nginx, including regular expressions. For example, you could use ^/$ to only match the root of the domain.
​Temporary vs. Permanent Redirects
Forge supports two types of redirects:

Permanent (HTTP Status Code 301)
Temporary (HTTP Status Code 302)

Although both of these redirect types are typically invisible to the user, the browser will treat them differently and it is important to know the difference.
​Temporary Redirects
When the browser encounters a temporary redirect, it will take you to the destination and forget that it was redirected from the original page. If you were to change the destination page and then visited the original page again, the browser would see the new redirect location and take you there.
​Permanent Redirects
With a permanent redirect, the browser will remember that it was redirected away from the original page. To save making another network request, the next time the browser visits the original page, it will see that it was redirected and immediately visit that page instead.
Although you can change the destination of a permanent redirect, you will need to clear the browser cache before you visit the original page again. It’s considered bad practice to change a permanent redirect, so be careful when doing so.
​Circle Permissions
You may grant a circle member authority to create and manage redirects by granting the site:manage-redirects permission.Was this page helpful?YesNoSecurity RulesSSLOn this pageOverviewCreating RedirectsTemporary vs. Permanent RedirectsTemporary RedirectsPermanent RedirectsCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge allows you to configure redirects that can be configured to automatically redirect visitors from one page to another. These redirect rules can be created via the “Redirects” tab of the site’s management dashboard.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-redirects\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Redirects\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Redirects are wrappers around Nginx’s \", _jsxs(_components.a, {\n        href: \"https://nginx.org/en/docs/http/ngx_http_rewrite_module.html#rewrite\",\n        children: [_jsx(_components.code, {\n          children: \"rewrite\"\n        }), \" rules\"]\n      }), \" and can use the full redirect syntax supported by Nginx, including regular expressions. For example, you could use \", _jsx(_components.code, {\n        children: \"^/$\"\n      }), \" to only match the root of the domain.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"temporary-vs-permanent-redirects\",\n      isAtRootLevel: \"true\",\n      children: \"Temporary vs. Permanent Redirects\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge supports two types of redirects:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Permanent (HTTP Status Code 301)\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Temporary (HTTP Status Code 302)\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Although both of these redirect types are typically invisible to the user, the browser will treat them differently and it is important to know the difference.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"temporary-redirects\",\n      isAtRootLevel: \"true\",\n      children: \"Temporary Redirects\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"When the browser encounters a temporary redirect, it will take you to the destination and forget that it was redirected from the original page. If you were to change the destination page and then visited the original page again, the browser would see the new redirect location and take you there.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"permanent-redirects\",\n      isAtRootLevel: \"true\",\n      children: \"Permanent Redirects\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"With a permanent redirect, the browser will remember that it was redirected away from the original page. To save making another network request, the next time the browser visits the original page, it will see that it was redirected and immediately visit that page instead.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Although you can change the destination of a permanent redirect, you will need to clear the browser cache before you visit the original page again. It’s considered bad practice to change a permanent redirect, so be careful when doing so.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"circle-permissions\",\n      isAtRootLevel: \"true\",\n      children: \"Circle Permissions\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may grant a circle member authority to create and manage redirects by granting the \", _jsx(_components.code, {\n        children: \"site:manage-redirects\"\n      }), \" permission.\"]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"$