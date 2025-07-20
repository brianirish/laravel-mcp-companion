# Forge - Servers/Provisioning-Process#Automated-Security-Updates

*Source: https://forge.laravel.com/docs/servers/provisioning-process#automated-security-updates*

---

Root Access / Security - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersRoot Access / SecurityDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersRoot Access / SecurityLearn about the security measures Forge takes to protect your server.​Provisioning
During the initial provisioning of your server, Forge will connect as the root user over SSH. This is so that Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.
The provisioning process can take upwards of 15 minutes, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.
​Post-Provisioning
After initially provisioning your server, Forge continues to use root access so that it can manage your server’s software, services, and configuration. For example, root access is needed to manage:

Firewalls
Daemons
Scheduled tasks
Isolated users
PHP configuration and management
Other operating system dependencies

​Security
We take security very seriously and ensure that we do everything we can to protect customer’s data. Below is a brief overview of some of the steps we take to ensure your server’s security:

Forge issues a unique SSH key for each server that it connects to.
Password based server SSH connections are disabled during provisioning.
Each server is issued a unique root password.
All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: 22 (SSH), 80 (HTTP) and 443 (HTTPS).
Automated security updates are installed using Ubuntu’s automated security release program.

​Automated Security Updates
Security updates are automatically applied to your server on a weekly basis. Forge accomplishes this by enabling and configuring Ubuntu’s automated security update service that is built in to the operating system.
Forge does not automatically update other software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application’s code is not compatible with the upgrade. However, it is possible to install new versions and patch existing versions of PHP manually via the Forge UI.Was this page helpful?YesNoManagementSSH Keys / Git AccessOn this pageProvisioningPost-ProvisioningSecurityAutomated Security UpdatesLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"provisioning\",\n      isAtRootLevel: \"true\",\n      children: \"Provisioning\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"During the initial provisioning of your server, Forge will connect as the \", _jsx(_components.code, {\n        children: \"root\"\n      }), \" user over SSH. This is so that Forge is able to add repositories, install dependencies and configure new services, firewalls, and more.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"The provisioning process can take upwards of 15 minutes, but will depend on a variety of factors including the speed of your server, the speed of your network connection, and the number of services that need to be installed.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"post-provisioning\",\n      isAtRootLevel: \"true\",\n      children: \"Post-Provisioning\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"After initially provisioning your server, Forge continues to use root access so that it can manage your server’s software, services, and configuration. For example, root access is needed to manage:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Firewalls\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Daemons\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Scheduled tasks\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Isolated users\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"PHP configuration and management\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Other operating system dependencies\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"security\",\n      isAtRootLevel: \"true\",\n      children: \"Security\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"We take security very seriously and ensure that we do everything we can to protect customer’s data. Below is a brief overview of some of the steps we take to ensure your server’s security:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Forge issues a unique SSH key for each server that it connects to.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Password based server SSH connections are disabled during provisioning.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Each server is issued a unique root password.\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"All ports are blocked by default with UFW, a secure firewall for Ubuntu. We then explicitly open ports: 22 (SSH), 80 (HTTP) and 443 (HTTPS).\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Automated security updates are installed using Ubuntu’s automated security release program.\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"automated-security-updates\",\n      isAtRootLevel: \"true\",\n      children: \"Automated Security Updates\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Security updates are automatically applied to your server on a weekly basis. Forge accomplishes this by enabling and configuring Ubuntu’s automated security update service that is built in to the operating system.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge does not automatically update other software such as PHP or MySQL, as doing so could cause your server to suffer downtime if your application’s code is not compatible with the upgrade. However, it is possible to \", _jsx(_components.a, {\n        href: \"/servers/php#multiple-php-versions\",\n        children: \"install new versions\"\n      }), \" and \", _jsx(_components.a, {\n        href: \"/servers/php#updating-php-between-patch-releases\",\n        children: \"patch existing versions of P