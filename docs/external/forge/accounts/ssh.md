# Forge - Accounts/Ssh

*Source: https://forge.laravel.com/docs/accounts/ssh*

---

SSH Keys - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationAccountsSSH KeysDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseAccountsSSH KeysSSH keys are used to authenticate with your server over the SSH protocol. Learn how to add your SSH keys to your Forge account and servers.​Introduction
SSH is a protocol that allows you to access your server via a command line terminal. SSH keys are used to authenticate with your server over the SSH protocol. If you are new to SSH keys, we recommend checking out the GitHub documentation of generating SSH keys to get started.
After adding your SSH key to your server, you may SSH into the server without a password:
CopyAsk AIssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS

​Adding Your SSH Key To New Servers
Before you provision a server for the first time, you should add your SSH keys to your account. You can do this from the your accounts SSH Keys page in the Forge dashboard.
As part of the provisioning process, Forge will add all your active SSH keys to the forge account. This will allow you to SSH into the server as the forge user.
If any of your sites are using User Isolation, you will be asked to select the user you want to add the key to. You will then be able to SSH into the server as that user.
​Adding SSH Key To Existing Servers
If you already have servers provisioned and want to add a new SSH key to several servers at once, then first add your key to your account via the SSH Keys page. Once it is listed in the “Active Keys”, you may use the “Add To Servers” action and select which servers you would like the key added to.
You can also add SSH keys directly to a server without adding them to your account.
​Server Public Key
During the provisioning process, Forge will generate its own keypair so that it may access the server. It will add the public key from this keypair to the authorized_keys file of both the root and forge users.
​Forge Public Key
During the provisioning process, Forge will generate a public key for the forge user. This is used by Git to clone the projects to your server. The key will be added to the source control provider. This key is located at /home/forge/.ssh/id_rsa.pub.Was this page helpful?YesNoSource ControlAPIOn this pageIntroductionAdding Your SSH Key To New ServersAdding SSH Key To Existing ServersServer Public KeyForge Public KeyLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Heading} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"introduction\",\n      isAtRootLevel: \"true\",\n      children: \"Introduction\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"SSH is a protocol that allows you to access your server via a command line terminal. SSH keys are used to authenticate with your server over the SSH protocol. If you are new to SSH keys, we recommend checking out the \", _jsx(_components.a, {\n        href: \"https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent\",\n        children: \"GitHub documentation of generating SSH keys\"\n      }), \" to get started.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"After adding your SSH key to your server, you may SSH into the server without a password:\"\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLines: \"1\",\n      language: \"shellscript\",\n      children: _jsx(_components.pre, {\n        className: \"shiki shiki-themes github-light-default dark-plus\",\n        style: {\n          backgroundColor: \"transparent\",\n          \"--shiki-dark-bg\": \"transparent\",\n          color: \"#1f2328\",\n          \"--shiki-dark\": \"#f3f7f6\"\n        },\n        language: \"shellscript\",\n        children: _jsxs(_components.code, {\n          language: \"shellscript\",\n          numberOfLines: \"1\",\n          children: [_jsxs(_components.span, {\n            className: \"line\",\n            children: [_jsx(_components.span, {\n              style: {\n                color: \"#953800\",\n                \"--shiki-dark\": \"#DCDCAA\"\n              },\n              children: \"ssh\"\n            }), _jsx(_components.span, {\n              style: {\n                color: \"#0A3069\",\n                \"--shiki-dark\": \"#CE9178\"\n              },\n              children: \" forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS\"\n            })]\n          }), \"\\n\"]\n        })\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"adding-your-ssh-key-to-new-servers\",\n      isAtRootLevel: \"true\",\n      children: \"Adding Your SSH Key To New Servers\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Before you provision a server for the first time, you should add your SSH keys to your account. You can do this from the your accounts \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/ssh-keys\",\n        children: \"SSH Keys page\"\n      }), \" in the Forge dashboard.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"As part of the provisioning process, Forge will add all your active SSH keys to the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" account. This will allow you to SSH into the server as the \", _jsx(_components.code, {\n        children: \"forge\"\n      }), \" user.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"If any of your sites are using User Isolation, you will be asked to select the user you want to add the key to. You will then be able to SSH into the server as that user.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"adding-ssh-key-to-existing-servers\",\n      isAtRootLevel: \"true\",\n      children: \"Adding SSH Key To Existing Servers\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If you already have servers provisioned and want to add a new SSH key to several servers at once, then first add your key to your account via the \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/ssh-keys\",\n        children: \"SSH Keys page\"\n      }), \". Once it is listed in the “Active Keys”, you may use the “Add To Servers” action and select which servers you would like the key added to.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You can also \", _jsx(_co