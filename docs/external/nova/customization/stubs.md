# Nova - Customization/Stubs

*Source: https://nova.laravel.com/docs/v5/customization/stubs*

---

Stubs - Laravel Nova
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
}Laravel Nova home pagev5Search...⌘KAsk AISupportPlatform StatusDashboardDashboardSearch...NavigationDigging DeeperStubsDocumentationKnowledge BaseCommunityBlogGet StartedInstallationRelease NotesUpgrade GuideResourcesThe BasicsFieldsDependent FieldsDate FieldsFile FieldsRepeater FieldsField PanelsRelationshipsValidationAuthorizationSearchThe BasicsGlobal SearchScout IntegrationFiltersDefining FiltersRegistering FiltersLensesDefining LensesRegistering LensesActionsDefining ActionsRegistering ActionsMetricsDefining MetricsRegistering MetricsDigging DeeperDashboardsMenusNotificationsAuthenticationImpersonationToolsResource ToolsCardsFieldsFiltersCSS / JavaScriptAssetsLocalizationStubsDigging DeeperStubsCustomize the stubs used by Nova to generate various classes.When creating new resources, actions, filters, lens and metrics, Nova will publish files using the default stub files that exist within Nova. However, you may wish to customize these stubs for your own projects in order to apply common modifications automatically.
To publish the stubs used by Nova to generate various classes, execute the following command:
CopyAsk AIphp artisan nova:stubs

When running this Artisan command in your terminal, Nova will copy all of its stub files into ./stubs/nova, where they may then be customized.
If you do not wish to customize a particular stub, you may delete the stub and Nova will continue to use the default version of the stub that exists within Nova itself.
To learn more about stub customization, please consult the Laravel documentation.Was this page helpful?YesNoLocalizationLaravel Nova home pagexgithubdiscordlinkedinPlatformDashboardStatusLegal and ComplianceTerm of ServicePrivacy PolicyxgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(_components.p, {\n      children: \"When creating new resources, actions, filters, lens and metrics, Nova will publish files using the default stub files that exist within Nova. However, you may wish to customize these stubs for your own projects in order to apply common modifications automatically.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"To publish the stubs used by Nova to generate various classes, execute the following command:\"\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"php\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" artisan\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" nova:stubs\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When running this Artisan command in your terminal, Nova will copy all of its stub files into \", _jsx(_components.code, {\n        children: \"./stubs/nova\"\n      }), \", where they may then be customized.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"If you do not wish to customize a particular stub, you may delete the stub and Nova will continue to use the default version of the stub that exists within Nova itself.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"To learn more about stub customization, please consult the \", _jsx(_components.a, {\n          href: \"https://laravel.com/docs/artisan#stub-customization\",\n          children: \"Laravel documentation\"\n        }), \".\"]\n      })\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.components\n  };\n  return MDXLayout ? _jsx(MDXLayout, {\n    ...props,\n    children: _jsx(_createMdxContent, {\n      ...props\n    })\n  }) : _createMdxContent(props);\n}\nreturn {\n  default: MDXContent\n};\nfunction _missingMdxReference(id, component) {\n  throw new Error(\"Expected \" + (component ? \"component\" : \"object\") + \" `\" + id + \"` to be defined: you likely forgot to import, pass, or provide it.\");\n}\n","frontmatter":{},"scope":{"config":{"theme":"mint","$schema":"https://mintlify.com/docs.json","name":"Laravel Nova","colors":{"primary":"#4BA2E3","light":"#4BA2E3","dark":"#4BA2E3"},"logo":{"light":"https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/light.svg","dark":"https://mintlify.s3.us-west-1.amazonaws.com/nova-laravel/logo/dark.svg","href":"https://nova.laravel.com"},"favicon":"/favicon.png","background":{"decoration":"windows"},"navbar":{"links":[{"label":"Support","href":"mailto:nova@laravel.com"},{"label":"Platform Status","href":"https://status.laravel.com/"}],"primary":{"type":"button","label":"Dashboard","href":"https://nova.laravel.com"}},"navigation":{"global":{"anchors":[{"anchor":"Community","icon":"discord","href":"https://discord.com/invite/laravel"},{"anchor":"Blog","icon":"newspaper","href":"https://blog.laravel.com/nova"}]},"versions":[{"version":"v1","href":"https://github.com/laravel/nova-orion-docs/tree/main/1.x"},{"version":"v2","href":"https://github.com/laravel/nova-orion-docs/tree/main/2.x"},{"version":"v3","href":"https://github.com/laravel/nova-orion-docs/tree/main/3.x"},{"version":"v4","tabs":[{"tab":"Documentation","groups":[{"group":"Get Started","pages":["v4/installation","v4/releases","v4/upgrade"]},{"group":"Resources","pages":["v4/resources/the-basics","v4/resources/fields","v4/resources/date-fields","v4/resources/repeater-fields","v4/resources/relationships","v4/resources/validation","v4/resources/authorization"]},{"group":"Search","pages":["v4/search/the-basics","v4/search/global-search","v4/search/scout-integration"]},{"group":"Filters","pages":["v4/filters/defining-filters","v4/filters/registering-filters"]},{"group":"Lenses","pages":["v4/lenses/defining-lenses","v4/lenses/registering-lenses"]},{"group":"Actions","pages":["v4/actions/defining-actions","v4/actions/registering-actions"]},{"group":"Metrics","pages":["v4/metrics/defini