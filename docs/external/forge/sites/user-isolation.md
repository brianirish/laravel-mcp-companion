# Forge - Sites/User-Isolation

*Source: https://forge.laravel.com/docs/sites/user-isolation*

---

User Isolation - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesUser IsolationDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesUser IsolationLearn how to isolate your sites on Laravel Forge.​Overview
By default, Forge uses the default forge user that is created as part of the server’s initial provisioning process for all deployments, daemons, scheduled jobs, PHP-FPM, and other processes.
Via Forge’s “User Isolation” feature, Forge will create a separate user for a given site. This is particularly useful when combined with a project like WordPress in order to prevent plugins from maliciously accessing content in your forge user (or other isolated user) owned directories.
The forge user is considered a “super user” and is therefore able to read all files within isolated user directories.
​Sudo Access
Like the forge user, newly created isolated users also have limited sudo access. They may reload the PHP-FPM services requiring a password:
CopyAsk AIsudo -S service php8.1-fpm reload

If you need further sudo access, you should log in as the forge user and switch to the root user using the sudo su or the sudo -i command.
​Connecting Via SFTP
You can connect to your server via SFTP as the isolated user. We recommend using an SFTP client such as Transmit or Filezilla. However, before getting started, you should first upload your SSH key to the server for the isolated user.Was this page helpful?YesNoSSLCookbookOn this pageOverviewSudo AccessConnecting Via SFTPLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"By default, Forge uses the default \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user that is created as part of the server’s initial provisioning process for all deployments, daemons, scheduled jobs, PHP-FPM, and other processes.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Via Forge’s “User Isolation” feature, Forge will create a separate user for a given site. This is particularly useful when combined with a project like WordPress in order to prevent plugins from maliciously accessing content in your \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user (or other isolated user) owned directories.\"]\n    }), \"\\n\", _jsx(Note, {\n      children: _jsxs(_components.p, {\n        children: [\"The \", _jsx(_components.code, {\n          children: \"forge\"\n        }), \" user is considered a “super user” and is therefore able to read all files within isolated user directories.\"]\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"sudo-access\",\n      isAtRootLevel: \"true\",\n      children: \"Sudo Access\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Like the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user, newly created isolated users also have limited sudo access. They may reload the PHP-FPM services requiring a password:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"sudo\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0550AE\",\n                \"--shiki-dark\": \"#9cdcfe\"\n              },\n              children: \" -S\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" service\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" php8.1-fpm\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" reload\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If you need further sudo access, you should log in as the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user and switch to the \", _jsx(_components.code, {\n        children: \"root\"\n      }), \" user using the \", _jsx(_components.code, {\n        children: \"sudo su\"\n      }), \" or the \", _jsx(_components.code, {\n        children: \"sudo -i\"\n      }), \" command.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"connecting-via-sftp\",\n      isAtRootLevel: \"true\",\n      children: \"Connecting Via SFTP\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You can connect to your server via SFTP as the isolated user. We recommend using an SFTP client such as \", _jsx(_components.a, {\n        href: \"https://panic.com/transmit/\",\n        children: \"Transmit\"\n      }), \" or \", _jsx(_components.a, {\n        href: \"https://filezilla-project.org/\",\n        children: \"Filezilla\"\n      }), \". However, before getting started, you should first \", _jsx(_components.a, {\n        href: \"/accounts/ssh\",\n        children: \"upload your SSH key to the server\"\n      }), \" for the isolated user.\"]\n    })]\n  });\n}\nfunction MDXContent(props = {}) {\n  const {wrapper: MDXLayout} = {\n    ..._provideComponents(),\n    ...props.compone