# Forge - Sites/Ssl

*Source: https://forge.laravel.com/docs/sites/ssl*

---

SSL - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesSSLDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesSSLConfigure SSL certificates for your sites.​Overview
Forge supports installing custom SSL certificates and using Let’s Encrypt to generate free certificates for your websites.
​Let’s Encrypt
Let’s Encrypt provides free SSL certificates that are recognized across all major browsers.
If you need to install Let’s Encrypt for multiple domains, you may separate multiple domains using commas.
Because of the Let’s Encrypt renewal process, it is not possible to clone Let’s Encrypt certificates to other sites. You should simply issue a new Let’s Encrypt certificate for that site.
​Renewing Let’s Encrypt Certificates
Forge will automatically renew your Let’s Encrypt certificates within 21 days or less before expiration. Renewal will take place at a random day and time to avoid overwhelming the Let’s Encrypt servers.
If something goes wrong while renewing a certificate, Forge will notify the server owner via email.
You must have an active Laravel Forge subscription in order for your Let’s Encrypt certificates to automatically renew.
​Wildcard Subdomain Let’s Encrypt Certificates
To install a Let’s Encrypt certificate with support for wildcard subdomains, you will need to list both the wildcard subdomain and the root domain in your domain list: *.domain.com, domain.com. Let’s Encrypt only supports the dns-01 challenge type when issuing wildcard certificates, so you will need to provide API credentials for your DNS provider.
Forge currently supports the following Let’s Encrypt wildcard DNS providers:

Cloudflare
DNSimple
DigitalOcean
Linode
OVH
Route53

​Cloudflare API Token
If you are using Cloudflare to manage your DNS, your Cloudflare API token must have the Zone.Zone.Read and Zone.DNS.Edit permissions. In addition, the token must have permissions on all zones attached to your Cloudflare account.
​Cloudflare Universal SSL Certificates
Cloudflare provides free SSL certificates to all connected domains and all their first-level subdomains. These certificates are automatically enabled on all domains and subdomains that have Cloudflare’s proxy functionality enabled. However, if you have multiple nested subdomains (e.g. staging.api.example.com), this universal certificate will not cover those domains and may cause an ERR_SSL_VERSION_OR_CIPHER_MISMATCH error. If your application requires multiple nested subdomains, we recommend you disable Cloudflare proxying and use a traditional SSL certificate for your Forge site.
​Route53 User Policy
If you are using Route53 to manage your DNS, your IAM user must have the route53:ChangeResourceRecordSets permission on your domain’s hosted zone. In addition, the user must have the route53:GetChange and route53:ListHostedZones permissions.
​Circle Permissions
You may grant a circle member authority to create and manage SSL certificates by granting the site:manage-ssl permission.Was this page helpful?YesNoRedirectsUser IsolationOn this pageOverviewLet’s EncryptRenewing Let’s Encrypt CertificatesWildcard Subdomain Let’s Encrypt CertificatesCloudflare API TokenCloudflare Universal SSL CertificatesRoute53 User PolicyCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge supports installing custom SSL certificates and using Let’s Encrypt to generate free certificates for your websites.\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"let%E2%80%99s-encrypt\",\n      isAtRootLevel: \"true\",\n      children: \"Let’s Encrypt\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [_jsx(_components.a, {\n        href: \"https://letsencrypt.org\",\n        children: \"Let’s Encrypt\"\n      }), \" provides free SSL certificates that are recognized across all major browsers.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"If you need to install Let’s Encrypt for multiple domains, you may separate multiple domains using commas.\"\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"Because of the Let’s Encrypt renewal process, it is not possible to clone Let’s Encrypt certificates to other sites. You should simply issue a new Let’s Encrypt certificate for that site.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"renewing-let%E2%80%99s-encrypt-certificates\",\n      isAtRootLevel: \"true\",\n      children: \"Renewing Let’s Encrypt Certificates\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge will \", _jsx(_components.strong, {\n        children: \"automatically\"\n      }), \" renew your Let’s Encrypt certificates within 21 days or less before expiration. Renewal will take place at a random day and time to avoid overwhelming the Let’s Encrypt servers.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"If something goes wrong while renewing a certificate, Forge will notify the server owner via email.\"\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"You must have an active Laravel Forge subscription in order for your Let’s Encrypt certificates to automatically renew.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"wildcard-subdomain-let%E2%80%99s-encrypt-certificates\",\n      isAtRootLevel: \"true\",\n      children: \"Wildcard Subdomain Let’s Encrypt Certificates\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"To install a Let’s Encrypt certificate with support for wildcard subdomains, you will need to list both the wildcard subdomain and the root domain in your domain list: \", _jsx(_components.code, {\n        children: \"*.domain.com, domain.com\"\n      }), \". Let’s Encrypt only supports the \", _jsx(_components.code, {\n        children: \"dns-01\"\n      }), \" challenge type when issuing wildcard certificates, so you will need to provide API credentials for your DNS provider.\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge currently supports the following Let’s Encrypt wildcard DNS pr