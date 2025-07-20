# Forge - Servers/Ssh

*Source: https://forge.laravel.com/docs/servers/ssh*

---

SSH Keys / Git Access - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersSSH Keys / Git AccessDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersSSH Keys / Git AccessLearn how to manage SSH keys on your Forge servers.​Account SSH Keys
When provisioning a new server Forge will automatically add any of your account’s SSH keys to the server. This means that you can SSH onto your server without using a password:
CopyAsk AIssh forge@IP_ADDRESS

​Server SSH Key / Git Project Access
When a server is provisioned, an SSH key is generated for the server. This key is stored at ~/.ssh/id_rsa and its public key counterpart is stored at ~/.ssh/id_rsa.pub. When creating a server, you will have the option to add this key to your connected source control providers. By doing so, the server will be able to clone any repository that your source control account has access to.
Alternatively, you may opt-out of having this key added to your source control providers by un-checking the Add Server’s SSH Key To Source Control Providers option when creating a server. When opting-out, you will need to use site-level Deploy Keys in order to grant your server access to specific repositories on a source control provider such as GitHub, GitLab, or Bitbucket.
​Deploy Keys
Sometimes you may wish to only grant the Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository’s “Deploy Keys” on the repository’s GitHub, GitLab, or Bitbucket dashboard.
When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider’s dashboard - allowing the server to clone that specific repository.
You are also free to use Deploy Keys even on servers that have their SSH key attached to your source control provider accounts, allowing you to grant the server access to clone a repository that the source control account connected to your Forge account does not have collaborator access to.Was this page helpful?YesNoRoot Access / SecurityPHPOn this pageAccount SSH KeysServer SSH Key / Git Project AccessDeploy KeysLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"account-ssh-keys\",\n      isAtRootLevel: \"true\",\n      children: \"Account SSH Keys\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When provisioning a new server Forge will automatically add any of your \", _jsx(_components.a, {\n        href: \"/accounts/ssh\",\n        children: \"account’s SSH keys\"\n      }), \" to the server. This means that you can SSH onto your server without using a password:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"ssh\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" forge@IP_ADDRESS\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"server-ssh-key-%2F-git-project-access\",\n      isAtRootLevel: \"true\",\n      children: \"Server SSH Key / Git Project Access\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When a server is provisioned, an SSH key is generated for the server. This key is stored at \", _jsx(_components.code, {\n        children: \"~/.ssh/id_rsa\"\n      }), \" and its public key counterpart is stored at \", _jsx(_components.code, {\n        children: \"~/.ssh/id_rsa.pub\"\n      }), \". When creating a server, you will have the option to add this key to your connected source control providers. By doing so, the server will be able to clone any repository that your source control account has access to.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Alternatively, you may opt-out of having this key added to your source control providers by un-checking the \", _jsx(_components.strong, {\n        children: \"Add Server’s SSH Key To Source Control Providers\"\n      }), \" option when creating a server. When opting-out, you will need to use site-level \", _jsx(_components.a, {\n        href: \"#deploy-keys\",\n        children: \"Deploy Keys\"\n      }), \" in order to grant your server access to specific repositories on a source control provider such as GitHub, GitLab, or Bitbucket.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"deploy-keys\",\n      isAtRootLevel: \"true\",\n      children: \"Deploy Keys\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Sometimes you may wish to only grant the Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository’s “Deploy Keys” on the repository’s GitHub, GitLab, or Bitbucket dashboard.\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider’s dashboard - allowing the server to clone that specific repository.\"\n    }), \"\\n\", _jsx(Note, {\n      children: _jsx(_components.p, {\n        children: \"You are also free to use Deploy Keys even on servers that have their SSH key attached to yo