# Forge - Sites/Applications

*Source: https://forge.laravel.com/docs/sites/applications*

---

Applications - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesApplicationsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesApplicationsLearn how to create and manage your applications on Laravel Forge.​Overview
Forge provides first-class support for applications running Laravel, allowing you to quickly toggle and configure:

Laravel’s Task Scheduler
Laravel’s Maintenance Mode
Laravel Horizon Daemon
Laravel Octane Daemon
Laravel Reverb Daemon
Inertia.js Server Side Rendering (SSR) Daemon


To accomplish this, Forge parses the composer.json and composer.lock files from your application and inspects for the presence and version of the packages above.
​Requirements
Forge will only show the application panel for Laravel framework installations of version 5.0 or later. In addition, the panel’s supported packages must meet the following version requirements:
DependencyMinimum Versionlaravel/framework5.0laravel/horizon1.0laravel/octane1.0laravel/pulse1.0laravel/reverb*inertiajs/inertia-laravel0.6.6
​Laravel Scheduler
You may quickly enable or disable the Laravel scheduler via the “Laravel Scheduler” toggle. Forge will create the required Scheduler for you.
Forge will automatically configure the scheduler to run every minute using the site’s configured PHP version.
​Maintenance Mode
If you have deployed a Laravel application, Forge allows you to make use of Laravel’s maintenance mode feature. Clicking the Laravel Maintenance Mode toggle within the site’s Application tab will run the php artisan down Artisan command within your application, which will make your site unavailable. When the site is in maintenance mode, you can then toggle it off to make your site available again.
​Maintenance Mode “Secret”
Laravel 8.0+ applications can make use of the “secret” option to bypass maintenance mode. Using this option with older versions of Laravel is not supported.
​Laravel Horizon
You may quickly enable or disable the Laravel Horizon daemon via the “Laravel Horizon” toggle. Forge will create the required Horizon daemon for you.
If the site’s deploy script does not contain the horizon:terminate command, Forge will automatically append it for you.
​Converting Existing Daemons
If your server is already configured with a daemon that runs Laravel Horizon, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.
​Laravel Octane
You may quickly enable or disable the Laravel Octane daemon via the “Laravel Octane” toggle. Forge will create the required Octane daemon and install Octane dependencies for you.
When enabling the Octane daemon, Forge will ask you to provide the port number you would like to use for the Octane server as well as your Octane server of choice.

If the site’s deploy script does not contain the octane:reload command, Forge will automatically append it for you.
Before enabling Laravel Octane, you must set the OCTANE_SERVER environment variable to the Octane server you choose.
​Converting Existing Daemons
If your server is already configured with a daemon that runs Laravel Octane, Forge will offer to convert the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon for you.
​Laravel Reverb
Determining the correct server type for hosting Laravel Reverb depends on your configuration requirements. You may use the table below to help inform your decision:
ConfigurationApp ServerWeb ServerReverb server alongside Laravel application⊙Dedicated Reverb server⊙Dedicated Reverb server with Pulse⊙Dedicated Reverb server with Pulse (seperate ingest and / or database)⊙
Once your preferred server has been provisioned, you should add a new site and install your Reverb-enabled Laravel application from your version control provider of choice.
Now, you may quickly enable or disable Laravel Reverb via the “Laravel Reverb” toggle within Forge’s application panel. When enabling Reverb, Forge will create the Reverb daemon, install the required dependencies, and configure the server for optimum performance.
Additionally, Forge will prompt for additional information required to setup the server per your requirements.


Public Hostname: Used to update the Nginx configuration of the site, allowing Reverb connections to be accepted by the server on the given hostname. Forge will default to a subdomain of the site’s current hostname, but you are free to customize this value. For example, if the site’s hostname is example.com, Forge will default Reverb’s hostname to ws.example.com.
Port: Used to instruct the Reverb daemon which server port it should run on. Forge will proxy requests for the given public hostname to this port.
Maximum Concurrent Connections: The number of connections your Reverb server can handle will depend on a combination of the resources available on the server and the amount of connections and messages being processed. You should enter the number of connections the server can manage before it should prevent new connections. This option will update the server’s allowed open file limit, Nginx’s allowed open file and connection limit, and install the ev event loop if required.

Forge ensures the hostname provided during Reverb’s installation process is publicly accessible by adding a new server block to your existing site’s Nginx configuration. This server block is contained within a new file and is not available to edit from the Forge UI dashboard.
If the site’s deploy script does not contain the reverb:restart command, Forge will automatically append it for you.
​SSL
If an SSL certificate exists for your site which protects Reverb’s configured hostname, Forge will automatically install it when enabling Reverb, ensuring your Reverb server is accessible via secure WebSockets (wss).
If Reverb is installed before a valid certificate is available, you may request a new certificate for Reverb’s configured hostname from your site’s “SSL” tab. Forge will automatically configure secure WebSockets for Reverb as soon as the certificate is activated. Forge will also pre-populate the “Domains” SSL form input with Reverb’s hostname when requesting a certificate.
After activating SSL on a Reverb-enabled site, you should ensure the following environment variables are properly defined before redeploying your site:
CopyAsk AIREVERB_PORT=443
REVERB_SCHEME=https

VITE_REVERB_PORT=&quot;${REVERB_PORT}&quot;
VITE_REVERB_SCHEME=&quot;${REVERB_SCHEME}&quot;

MIX_REVERB_PORT=&quot;${REVERB_PORT}&quot;
MIX_REVERB_SCHEME=&quot;${REVERB_SCHEME}&quot;

​Converting Existing Daemons
If your server is already configured with a daemon that runs Laravel Reverb, Forge will manage the daemon for you. This process links the site’s ID and the daemon’s ID together, allowing Forge to manage the daemon on your behalf.
When disabling Reverb, Forge will remove the daemon and ensure the public hostname is no longer accessible. However, any settings Forge updated when enabling Reverb, such as open file and connection