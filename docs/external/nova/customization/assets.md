# Nova - Customization/Assets

*Source: https://nova.laravel.com/docs/v5/customization/assets*

---

Assets - Laravel Nova
              document.documentElement.style.setProperty('--font-family-headings-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-headings-custom', '');
              document.documentElement.style.setProperty('--font-family-body-custom', 'Figtree');
              document.documentElement.style.setProperty('--font-weight-body-custom', '');
            
    (function() {
      try {
        var bannerKey = "nova-laravel-bannerDismissed";
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
    --primary: 75 162 227;
    --primary-light: 75 162 227;
    --primary-dark: 75 162 227;
    --background-light: 255 255 255;
    --background-dark: 10 12 15;
    --gray-50: 245 247 249;
    --gray-100: 240 242 244;
    --gray-200: 224 227 229;
    --gray-300: 208 210 212;
    --gray-400: 160 163 165;
    --gray-500: 114 116 118;
    --gray-600: 82 84 86;
    --gray-700: 64 67 69;
    --gray-800: 39 42 44;
    --gray-900: 25 27 29;
    --gray-950: 12 15 17;
  }h1, h2, h3, h4 {
    font-weight: 600 !important;
}

.codeblock-dark div:not(:last-child) {
    color: #fafafa;
}

#footer > div > div:nth-of-type(n+2) {
    display: none;
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperAssetsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperAssetsLearn how to extend or add additional functionality to Nova.​Overview
Assets allow you to extend or add additional functionality to Nova without the overhead of cards or resource tools. For example, you may wish to override a custom error component to match your branding or intercept Inertia interactions and provide additional data to routes.
​Defining Assets
Assets may be generated using the nova:asset Artisan command. By default, all new assets will be placed in the nova-components directory of your application. When generating an asset using the nova:asset command, the asset name you pass to the command should follow the Composer vendor/package format:
CopyAsk AIphp artisan nova:asset acme/analytics

When generating an asset, Nova will prompt you to install the assets NPM dependencies, compile its dependencies, and update your application’s composer.json file. All custom assets are registered with your application as a Composer “path” repository.
Nova assets include all of the scaffolding necessary to build your asset. Each asset even contains its own composer.json file and is ready to be shared with the world on GitHub or the source control provider of your choice.
​Registering Assets
Nova assets are automatically loaded through the use of Laravel’s auto-loader, so no additional registration is required.
​Compiling Assets
Your Nova asset contains a webpack.mix.js file, which is generated when Nova creates your custom asset. You may build your custom asset using the NPM dev and prod commands:
CopyAsk AI# Compile your assets for local development...
npm run dev

# Compile and minify your assets...
npm run prod

In addition, you may run the NPM watch command to auto-compile your assets when they are changed:
CopyAsk AInpm run watch
Was this page helpful?YesNoCSS / JavaScriptLocalizationOn this pageOverviewDefining AssetsRegistering AssetsCompiling AssetsLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Assets allow you to extend or add additional functionality to Nova without the overhead of cards or resource tools. For example, you may wish to override a custom error component to match your branding or intercept Inertia interactions and provide additional data to routes.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"defining-assets\",\n      isAtRootLevel: \"true\",\n      children: \"Defining Assets\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Assets may be generated using the \", _jsx(_components.code, {\n        children: \"nova:asset\"\n      }), \" Artisan command. By default, all new assets will be placed in the \", _jsx(_components.code, {\n        children: \"nova-components\"\n      }), \" directory of your application. When generating an asset using the \", _jsx(_components.code, {\n        children: \"nova:asset\"\n      }), \" command, the asset name you pass to the command should follow the Composer \", _jsx(_components.code, {\n        children: \"vendor/package\"\n      }), \" format:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"php\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" artisan\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" nova:asset\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" acme/analytics\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When generating an asset, Nova will prompt you to install the assets NPM dependencies, compile its dependencies, and update your application’s \", _jsx(_components.code, {\n        children: \"composer.json\"\n      }), \" file. All custom assets are registered with your application as a Composer \", _jsx(_components.a, {\n        href: \"https://getcomposer.org/doc/05-repositories#path\",\n        children: \"“path” repository\"\n      }), \".\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Nova assets include all of the scaffolding necessary to build your asset. Each asset even contains its own \", _jsx(_components.code, {\n        children: \"composer.json\"\n      }), \" file and is ready to be shared with the world on GitHub or the source control provider of your choice.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"registering-assets\",\n      isAtRootLevel: \"true\",\n      children: \"Registering Assets\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Nova assets are automatically loaded through the use of Laravel’s auto-loader, so no additional registration is required.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"compiling-assets\",\