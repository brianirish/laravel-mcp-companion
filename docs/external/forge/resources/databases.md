# Forge - Resources/Databases

*Source: https://forge.laravel.com/docs/resources/databases*

---

Databases - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationResourcesDatabasesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseResourcesDatabasesLearn how to manage databases on your Forge server.​Overview
When provisioning a new Forge server you may choose to install an App Server or a Database Server. You can then use the Forge dashboard to manage databases, users, and permissions.
​Creating Servers With Databases
When creating a new server, you can select to install a supported database server:

MySQL (8.0)
MariaDB (10.6)
MariaDB (10.11)
PostgreSQL (12)
PostgreSQL (13)
PostgreSQL (14)
PostgreSQL (15)
PostgreSQL (16)

As part of the provisioning process, Forge will automatically install the selected database server and create a default forge database, forge user, and a secure, randomly-generated password. The database password will be shown upon creating the server alongside the root password. These passwords will also be emailed to you.
​Installing Databases Later
If you later decide to that you need to install a database on your server, you can do so through the server’s Databases management tab. Once installed, you will then be able to manage your database via Forge.
If you created a “Web Server”, you will not be able to install a database on that server at any point. Web servers are provisioned with the minimum amount of software needed to serve your PHP application only. If you need a database and web server on the same server, you should provision an “App Server”.
​Changing the Root / Forge Database Password
To reset the root and forge database user passwords, you may use the password reset functionality provided by Forge’s Databases management tab.
You should not change the root or forge database user passwords manually or outside of the Forge dashboard. Doing so will prevent Forge from being able to connect to or manage your database.
​Connecting To Databases Via A GUI Client
By default, database connections require SSH key authentication and are not able to be accessed using passwords. Therefore, when using a GUI database client to connect to your Forge database, you will need to use SSH authentication.
When selecting the SSH key to use during authentication, ensure that you select your private SSH key. For example, when using the TablePlus database client:

​Using The Database Connection URL
Some clients, such as TablePlus, allow you to connect to a database via a connection URL. Forge automatically generates this connection URL for you and you can use it to connect to your database. Note that the password is not included in this URL, so you should provide your password manually within your database client’s GUI.
​Connecting To A Database On Another Forge Server
You can utilize Forge’s server network feature to connect one server’s application to a database on another server within the same network.
If both the server hosting your application and the server hosting the external database meet the requirements for internal network connections, you may follow these steps to establish the database connection:

Allow access from your application’s web server to the database server:

Navigate to the Network settings of your application’s web server: https://forge.laravel.com/servers/&lt;serverID&gt;/networks.
Under the Server Network section of the page, enable the connection to the server of the external database.


Next, update your application’s environment configuration:

Visit your site’s environment page at https://forge.laravel.com/servers/&lt;serverID&gt;/sites/&lt;siteID&gt;/environment
Set the database host to the external server’s private IP address.
Update the database credential variables to match those of the external database.



​Managing Your Databases Within Forge
For servers running MySQL, MariaDB, and PostgreSQL, Forge offers some advanced features which allows it to manage your databases and database users easily. We’ll discuss these features below.
​Creating Databases
You can create a new database through the server’s Database tab within Forge. At a minimum, you must supply the name of your new database. The forge user will be able to access the database automatically.
​Syncing Databases
For consistency, you should use Forge to manage your databases and database users. However, if you created databases outside of the Forge dashboard, you can manually sync them into the Forge dashboard using the Sync Databases button on your Forge database management panel.
When syncing databases, some database names that are reserved by the database engine will not be synced, including:

mysql
information_schema
peformance_schema
sys
postgres
template0
template1

​Creating Database Users
You can create extra database users through the Forge dashboard’s database panel. To do so, you’ll need to provide the username, password, and select the databases that the new user can access.
​Upgrading Databases
Forge does not provide the ability to upgrade your database server software automatically. If you wish to upgrade your database server, you will need to complete this manually.
​Circle Permissions
You may grant a circle member authority to create and manage databases and database users by granting the server:create-databases and server:delete-databases permissions.Was this page helpful?YesNoDaemonsCachesOn this pageOverviewCreating Servers With DatabasesInstalling Databases LaterChanging the Root / Forge Database PasswordConnecting To Databases Via A GUI ClientUsing The Database Connection URLConnecting To A Database On Another Forge ServerManaging Your Databases Within ForgeCreating DatabasesSyncing DatabasesCreating Database UsersUpgrading DatabasesCircle PermissionsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    ol: \"ol\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Warning, ZoomImage} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  if (!ZoomImage) _missingMdxReference(\"ZoomImage\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"When provisioning a new Forge server you may choose to install an \", _jsx(_components.a, {\n        href: \"/servers/types#app-servers\",\n        children: \"App Server\"\n      }), \" or a \", _jsx(_components.a, {\n        href: \"/servers/types#database-servers\",\n        c