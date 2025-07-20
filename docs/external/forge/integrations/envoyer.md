# Forge - Integrations/Envoyer

*Source: https://forge.laravel.com/docs/integrations/envoyer*

---

Envoyer - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationIntegrationsEnvoyerDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseIntegrationsEnvoyerZero downtime deployments with Laravel Forge and Envoyer​Overview
Forge now offers zero downtime deployments, thanks to a seamless first-party integration with Envoyer. Envoyer’s zero downtime deployments ensure you avoid even those brief milliseconds of downtime while the server updates your code.
​Creating An Envoyer API Token
To kick things off, you’ll need active subscriptions for both Laravel Forge and Envoyer. Once you’re set up, navigate to your Envoyer dashboard and create a new API token. At a minimum, Forge requires the following scopes:
CopyAsk AIdeployments:create
projects:create
servers:create

To future-proof the integration, consider providing Forge with additional access permissions. You can update your Envoyer’s API token in Forge at any point.
​Linking Your Envoyer Account To Forge
Next, it’s time to link Forge with your Envoyer API token. Navigate to your account settings in Forge and click on the Envoyer navigation item.

​Creating New Sites With Envoyer
When creating a new site in Forge, you’ll notice a new option labeled “Configure with Envoyer”. Toggle this option to reveal a dropdown menu, where you can either select an existing Envoyer project or create a brand new one.


​Envoyer Sites In Forge
To deploy your Envoyer project within Forge, simply click the “Deploy Now” button, just as you would with any other site in Forge. The “Deployment Trigger URL” is also available for use in a CI environment.
Additionally, Forge has been updated to align perfectly with Envoyer projects:

Commands are executed from the /current directory.
The Environment panel will display a read-only version of the .env file. Continue to use Envoyer to manage your environment file, especially since it may need to be synchronized across multiple servers.
The site’s Packages panel is disabled to ensure the auth.json file remains intact through subsequent deployments.


​Migrating An Existing Site To Envoyer
Before migrating your Forge site to Envoyer, ensure your site directory does not contain a directory named releases or current. This is essential in allowing Envoyer to create these directories during the project’s installation on your server.
Next, access the Envoyer dashboard and navigate to the relevant project. Within the project settings, select “Import Forge Server”, then choose the appropriate server and site before clicking “Import Server.”

After adding the server details, it’s crucial to test the connection to ensure that Envoyer can communicate with your server effectively. You can test the connection status from the server overview.

Next, click the “Manage Environment” button, unlock your environment, and sync it to the new server. This action will replace the contents of the existing .env file in the site directory on the server.

Now, you should initiate a deployment from Envoyer. Once the deployment is complete, Envoyer will download the latest version of your application into the releases directory of your site and add a symlink to /current.
Your site should still be accessible, but the old version is still being served. To address this, navigate to the “Settings” panel in Forge and prefix the web directory with /current. For example, if your site’s web directory is currently /public, update it to /current/public. Doing so will instruct Nginx to serve your application from /home/forge/example.com/current/public – the location where Envoyer has installed the latest version of your application.

You should now tidy your site directory by ensuring it only contains the .env file, along with the releases, current, and storage directories. After ensuring you have backed up anything you need, you may remove everything else, including any dotfiles and directories such as .git, .gitattributes, etc.
Now that the web directory includes /current, Forge will recognize your site as being managed by Envoyer in the “Envoyer” panel. You can now link Forge and Envoyer together by selecting the relevant project from the project list.

Finally, now that your application is being served from the /current directory, you should update your scheduler, queue workers, and any daemons to ensure they are running from the correct path.Was this page helpful?YesNoCookbookSentryOn this pageOverviewCreating An Envoyer API TokenLinking Your Envoyer Account To ForgeCreating New Sites With EnvoyerEnvoyer Sites In ForgeMigrating An Existing Site To EnvoyerLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    img: \"img\",\n    li: \"li\",\n    p: \"p\",\n    pre: \"pre\",\n    span: \"span\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {CodeBlock, Frame, Heading, Note} = _components;\n  if (!CodeBlock) _missingMdxReference(\"CodeBlock\", true);\n  if (!Frame) _missingMdxReference(\"Frame\", true);\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Forge now offers zero downtime deployments, thanks to a seamless first-party integration with \", _jsx(_components.a, {\n        href: \"https://envoyer.io\",\n        children: \"Envoyer\"\n      }), \". Envoyer’s zero downtime deployments ensure you avoid even those brief milliseconds of downtime while the server updates your code.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-an-envoyer-api-token\",\n      isAtRootLevel: \"true\",\n      children: \"Creating An Envoyer API Token\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"To kick things off, you’ll need active subscriptions for both \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/auth/register\",\n        children: \"Laravel Forge\"\n      }), \" and \", _jsx(_components.a, {\n        href: \"https://envoyer.io/auth/register\",\n        children: \"Envoyer\"\n      }), \". Once you’re set up, navigate to your Envoyer dashboard and \", _jsx(_components.a, {\n        href: \"https://envoyer.io/user/profile?name=Laravel%20Forge\u0026scopes=projects:create,deployments:create,servers:create#/api\",\n        children: \"create a new API token\"\n      }), \". At a minimum, Forge requires the following scopes:\"]\n    }), \"\\n\", _jsx(CodeBlock, {\n      numberOfLi