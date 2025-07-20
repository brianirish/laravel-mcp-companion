# Forge - Introduction

*Source: https://forge.laravel.com/docs/introduction*

---

Introduction - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationGet StartedIntroductionDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseGet StartedIntroductionLaravel Forge is a server management and application deployment service.Create An AccountCreate your Forge account todayWatch MoreWatch the free Forge series on Laracasts
​What is Forge?
Laravel Forge is a server management and application deployment service. Forge takes the pain and hassle out of deploying servers and can be used to launch your next website. Whether your app is built with a framework such as Laravel, Symfony, Statamic, WordPress, or is a vanilla PHP application - Forge is the solution for you.
We live and breathe PHP here at Forge, but Forge is also ready to handle other tech stacks too, such as Node.js.
After connecting to your preferred server provider, Forge will be able to provision new servers for you in minutes. We offer you the ability to provision multiple server types (e.g. web servers, database servers, load balancers) with the option of having an array of services configured for you to hit the ground running, including:


Nginx web server


PHP (multiple version support)


Database (MySQL, Postgres, or MariaDB)


Logrotate


UFW Firewall


OPcache


Memcached


Redis


MeiliSearch


Automatic Security Updates


And much more!


In addition, Forge can assist you in managing scheduled jobs, queue workers, TLS/SSL certificates, and more. After your server has provisioned, you can manage and deploy your web applications using the Forge UI dashboard.
​Forge IP Addresses
In order to provision and communicate with your servers, Forge requires SSH access to them. If you have set up your servers to restrict SSH access using IP allow lists, you must allow the following Forge IP addresses:


159.203.150.232


159.203.150.216


45.55.124.124


165.227.248.218


You can also access the IP addresses via the following URL: https://forge.laravel.com/ips-v4.txt. This is particularly useful if you intend on automating your network or firewall infrastructure.
If you are restricting HTTP traffic, your server must also allow incoming and outgoing traffic from forge.laravel.com.
The Forge IP addresses may change from time to time; however, we will always email you several weeks prior to an IP address change.
​Forge Support Jumpbox
To enable the Forge Support team to provide more efficient technical assistance, you can also optionally allow our support jumpbox IP address to access your server in your firewall settings:

129.212.144.126

​Forge &amp; Envoyer Integration

Forge now offers zero downtime deployments, thanks to a seamless first-party integration with Envoyer.
​Forge API
Forge provides a powerful API that allows you to manage your servers programatically, providing access to the vast majority of Forge features. You can find the Forge API documentation here.
​Legal and Compliance
Our Terms of Service, Privacy Policy and Data Processing Agreement (DPA), provide details on the terms, conditions, and privacy practices for using Laravel Forge.Was this page helpful?YesNoForge CLIOn this pageWhat is Forge?Forge IP AddressesForge Support JumpboxForge &amp; Envoyer IntegrationForge APILegal and ComplianceLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    li: \"li\",\n    p: \"p\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Card, CardGroup, Frame, Heading, Tip} = _components;\n  if (!Card) _missingMdxReference(\"Card\", true);\n  if (!CardGroup) _missingMdxReference(\"CardGroup\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Tip) _missingMdxReference(\"Tip\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsxs(CardGroup, {\n      cols: 2,\n      children: [_jsx(Card, {\n        title: \"Create An Account\",\n        icon: \"user-plus\",\n        href: \"https://forge.laravel.com/auth/register\",\n        children: _jsx(_components.p, {\n          children: \"Create your Forge account today\"\n        })\n      }), _jsx(Card, {\n        title: \"Watch More\",\n        icon: \"circle-play\",\n        href: \"https://laracasts.com/series/learn-laravel-forge-2022-edition/\",\n        children: _jsx(_components.p, {\n          children: \"Watch the free Forge series on Laracasts\"\n        })\n      })]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"what-is-forge%3F\",\n      isAtRootLevel: \"true\",\n      children: \"What is Forge?\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Laravel Forge is a server management and application deployment service. Forge takes the pain and hassle out of deploying servers and can be used to launch your next website. Whether your app is built with a framework such as \", _jsx(_components.a, {\n        href: \"https://github.com/laravel/laravel\",\n        children: \"Laravel\"\n      }), \", \", _jsx(_components.a, {\n        href: \"https://github.com/symfony/symfony\",\n        children: \"Symfony\"\n      }), \", \", _jsx(_components.a, {\n        href: \"https://github.com/statamic/cms\",\n        children: \"Statamic\"\n      }), \", \", _jsx(_components.a, {\n        href: \"https://github.com/WordPress/WordPress\",\n        children: \"WordPress\"\n      }), \", or is a vanilla PHP application - Forge is the solution for you.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"We live and breathe PHP here at Forge, but Forge is also ready to handle other tech stacks too, such as Node.js.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"After connecting to your preferred \", _jsx(_components.a, {\n        href: \"/servers/providers\",\n        children: \"server provider\"\n      }), \", Forge will be able to provision new servers for you in minutes. We offer you the ability to provision \", _jsx(_components.a, {\n        href: \"/servers/types\",\n        children: \"multiple server types\"\n      }), \" (e.g. web servers, database servers, load balancers) with the option of having an array of services configured for you to hit the ground running, including:\"]\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsxs(_components.li, {\n        children: [\"\\n\", _jsx(_components.p, {\n          children: \"Nginx web server\"\n        }), \"\\n\"]\n      }), \"\\n\", _jsxs(_components.li, {\n        children: [\"\\n\", _jsxs(_components.p, {\n          children: [_jsx(_components.a, {\n            href: \"/servers/php\",\n            children: \"PHP\"\n          }), \" (