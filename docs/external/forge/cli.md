# Forge - Cli

*Source: https://forge.laravel.com/docs/cli*

---

Forge CLI - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationGet StartedForge CLIDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseGet StartedForge CLIForge CLI is a command-line tool that you may use to manage your Forge resources from the command-line.Forge CLIView the Forge CLI on GitHubForge APIView the Forge API Documentation
​Overview
Forge provides a command-line tool that you may use to manage your Forge servers, sites, and resources from the command-line.
​Installation

Requires PHP 8.0+

You may install the Forge CLI as a global Composer dependency:
CopyAsk AIcomposer global require laravel/forge-cli

​Get Started
To view a list of all available Forge CLI commands and view the current version of your installation, you may run the forge command from the command-line:
CopyAsk AIforge

​Authenticating
You will need to generate an API token to interact with the Forge CLI. Tokens are used to authenticate your account without providing personal details. API tokens can be created from Forge’s API dashboard.
After you have generated an API token, you should authenticate with your Forge account using the login command:
CopyAsk AIforge login
forge login --token=your-api-token

Alternatively, if you plan to authenticate with Forge from your CI platform, you may set a FORGE_API_TOKEN environment variable in your CI build environment.
​Current Server &amp; Switching Servers
When managing Forge servers, sites, and resources via the CLI, you will need to be aware of your currently active server. You may view your current server using the server:current command. Typically, most of the commands you execute using the Forge CLI will be executed against the active server.
CopyAsk AIforge server:current

Of course, you may switch your active server at any time. To change your active server, use the server:switch command:
CopyAsk AIforge server:switch
forge server:switch staging

To view a list of all available servers, you may use the server:list command:
CopyAsk AIforge server:list

​SSH Key Authentication
Before performing any tasks using the Forge CLI, you should ensure that you have added an SSH key for the forge user to your servers so that you can securely connect to them. You may have already done this via the Forge UI. You may test that SSH is configured correctly by running the ssh:test command:
CopyAsk AIforge ssh:test

To configure SSH key authentication, you may use the ssh:configure command. The ssh:configure command accepts a --key option which instructs the CLI which public key to add to the server. In addition, you may provide a --name option to specify the name that should be assigned to the key:
CopyAsk AIforge ssh:configure

forge ssh:configure --key=/path/to/public/key.pub --name=sallys-macbook

After you have configured SSH key authentication, you may use the ssh command to create a secure connection to your server:
CopyAsk AIforge ssh

forge ssh server-name

​Sites
To view the list of all available sites, you may use the site:list command:
CopyAsk AIforge site:list

​Initiating Deployments
One of the primary features of Laravel Forge is deployments. Deployments may be initiated via the Forge CLI using the deploy command:
CopyAsk AIforge deploy

forge deploy example.com

​Updating Environment Variables
You may update a site’s environment variables using the env:pull and env:push commands. The env:pull command may be used to pull down an environment file for a given site:
CopyAsk AIforge env:pull
forge env:pull pestphp.com
forge env:pull pestphp.com .env

Once this command has been executed the site’s environment file will be placed in your current directory. To update the site’s environment variables, simply open and edit this file. When you are done editing the variables, use the env:push command to push the variables back to your site:
CopyAsk AIforge env:push
forge env:push pestphp.com
forge env:push pestphp.com .env

If your site is utilizing Laravel’s “configuration caching” feature or has queue workers, the new variables will not be utilized until the site is deployed again.
​Viewing Application Logs
You may also view a site’s logs directly from the command-line. To do so, use the site:logs command:
CopyAsk AIforge site:logs
forge site:logs --follow              # View logs in realtime

forge site:logs example.com
forge site:logs example.com --follow  # View logs in realtime

​Reviewing Deployment Output / Logs
When a deployment fails, you may review the output / logs via the Forge UI’s deployment history screen. You may also review the output at any time on the command-line using the deploy:logs command. If the deploy:logs command is called with no additional arguments, the logs for the latest deployment will be displayed. Or, you may pass the deployment ID to the deploy:logs command to display the logs for a particular deployment:
CopyAsk AIforge deploy:logs

forge deploy:logs 12345

​Running Commands
Sometimes you may wish to run an arbitrary shell command against a site. The command command will prompt you for the command you would like to run. The command will be run relative to the site’s root directory.
CopyAsk AIforge command

forge command example.com

forge command example.com --command=&quot;php artisan inspire&quot;

​Tinker
As you may know, all Laravel applications include “Tinker” by default. To enter a Tinker environment on a remote server using the Forge CLI, run the tinker command:
CopyAsk AIforge tinker

forge tinker example.com

​Resources
Forge provisions servers with a variety of resources and additional software, such as Nginx, MySQL, etc. You may use the Forge CLI to perform common actions on those resources.
​Checking Resource Status
To check the current status of a resource, you may use the {resource}:status command:
CopyAsk AIforge daemon:status
forge database:status

forge nginx:status

forge php:status      # View PHP status (default PHP version)
forge php:status 8.4  # View PHP 8.4 status

​Viewing Resources Logs
You may also view logs directly from the command-line. To do so, use the {resource}:logs command:
CopyAsk AIforge daemon:logs
forge daemon:logs --follow  # View logs in realtime

forge database:logs

forge nginx:logs         # View error logs
forge nginx:logs access  # View access logs

forge php:logs           # View PHP logs (default PHP version)
forge php:logs 8.4       # View PHP 8.4 logs

​Restarting Resources
Resources may be restarted using the {resource}:restart command:
CopyAsk AIforge daemon:restart

forge database:restart

forge nginx:restart

forge php:restart      # Restarts PHP (default PHP version)
forge php:restart 8.4  # Restarts PHP 8.4

​Connecting To Resources Locally
You may use the {resource}:shell command to quickly access a command line shell that lets you interact with a given resource:
CopyAsk AIforge database:shell
forge database:shell my-database-name
forge database:shell my-database-name --user=my-user
Was this page helpful?YesNoIntroductionForge SDKOn this pageOverviewInstallationGet StartedAuthenticatingCurrent Server &amp; Switching ServersSS