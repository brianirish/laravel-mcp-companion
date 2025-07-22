# Forge - Sites/Deployments

*Source: https://forge.laravel.com/docs/sites/deployments*

---

Deployments - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationSitesDeploymentsDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseSitesDeploymentsManage code deployments with scripts, queues, and CI tools​Overview
A deployment is the process in which your code is downloaded from your source control provider on to your server, ready for the world to access. Forge tracks the latest 10 deployments so that you can see what was deployed, when it was deployed, how long it took to be deployed, and also view the output of your deploy script.
​Environments
Some applications, such as those created with the Laravel framework, may require a .env file to configure settings such as databases and caches. You can create and edit your Environment file within the Forge site’s management dashboard.
If your project contains a .env.example file, Forge will automatically copy this and replace some of the settings to match your server’s database settings. An empty .env.example could result in an empty environment file on the first deploy.
​Environment Circle Permission
You may grant a circle member authority to view and edit a site’s environment file (or WordPress configuration) using the site:manage-environment permission. Without this permission, Forge will not display the contents of the environment file to circle members.
​Encrypted Environment Files
Forge provides support for Laravel’s encrypted environment files without requiring you to include your encryption key within your deployment script.
To leverage this feature, add your encryption key to the “Environment Encryption Key” section of your site’s management dashboard. Once added, Forge will inject the value into the LARAVEL_ENV_ENCRYPTION_KEY environment variable during deployment, allowing you to add the env:decrypt Artisan command to your deployment script without explicitly setting the --key option:
CopyAsk AIphp artisan env:decrypt --force

​Quick Deploy
Forge’s “Quick Deploy” feature allows you to easily deploy your projects when you push to your source control provider. When you push to your configured quick deploy branch, Forge will pull your latest code from source control and run your application’s configured deployment script.
You can enable Forge’s quick deploy feature by clicking the “Enable Quick Deploy” button within the Apps tab of your site’s management dashboard.
For sites using a custom source control provider you will need to manually set up a Deployment Trigger to have your code deployed when you push to your source provider. Click the “Manage Quick Deploy” button within the Apps tab of your site’s management dashboard for instructions.
​Deploy Script
The commands that are executed on your server when your project is deployed are determined by your site’s deployment script. Of course, this deployment script can be edited directly within the Forge UI. By default, your site’s deployment script will:

Navigate into the site’s directory
Execute the git pull command
Installs your application’s Composer dependencies
Execute the php artisan migrate command (if your application contains an artisan file)

You can make your .env variables available to your deploy script by checking the “Make .env variables to deploy script” checkbox below the Deploy Script panel. When enabled, Forge will automatically inject the variables in your site’s .env file into the deploy script, allowing them to be accessed like any normal Bash variable:
CopyAsk AIecho &quot;${APP_NAME} is deploying...&quot;

Deployments may make your site unavailable for a brief moment. If you need absolutely zero downtime during deployments, check out Envoyer.
​PHP Versions
If you have installed multiple versions of PHP on your server, your deploy script may need to be updated to use the correct version of PHP.
By default, php will always point to the active version of PHP used on the CLI. If you need to use a different version of PHP, you must use phpx.x where x.x reflects on the version used (e.g. php8.4) when invoking PHP commands.
The deployment script for newly created sites uses the $FORGE_PHP environment variable. This environment variable will always contain the current PHP binary configured for the site, so no additional changes are needed to your deployment script when using this variable and switching your site’s PHP version.
​Restarting Daemons During Deployment
When deploying applications that use daemons (such as Next.js applications), you may need to restart the daemon to ensure it picks up your code changes. You can do this by adding the restart command to your deployment script:
CopyAsk AI# Restart your daemon (replace 12345 with your daemon&#x27;s ID)...
sudo supervisorctl restart daemon-12345:*

You can find your daemon’s ID in the Forge dashboard under your server’s Daemons tab.
​Environment Variables
Forge will automatically inject the following environment variables into your deployment script at runtime:
KeyDescriptionFORGE_COMPOSERThe path to the Composer installation.FORGE_CUSTOM_DEPLOYWhether the deployment was triggered with a custom deployment trigger request.FORGE_DEPLOY_AUTHORThe author of the commit.FORGE_DEPLOY_COMMITThe Git hash of the commit being deployed.FORGE_DEPLOY_MESSAGEThe Git commit message.FORGE_DEPLOYMENT_IDThe Forge assigned ID of this deployment.FORGE_MANUAL_DEPLOYWhether the deploy was triggered by clicking “Deploy Now”.FORGE_PHP_FPMThe PHP-FPM process name that is being used by Forge.FORGE_PHPThe php binary that is being used by the Forge site or server.FORGE_QUICK_DEPLOYWhether the deploy was triggered by a source control provider webhook.FORGE_REDEPLOYWhether this is a re-deployed commit.FORGE_SERVER_IDThe ID of the Forge server that is being deployed to.FORGE_SITE_BRANCHThe name of the branch that is being deployed.FORGE_SITE_IDThe ID of the Forge site that is being deployed to.FORGE_SITE_PATHThe root of the deployment path, e.g. /home/forge/mysite.comFORGE_SITE_USERThe name of the user deploying the site.
You may use these variables as you would any other Bash variable:
CopyAsk AIif [[ $FORGE_MANUAL_DEPLOY -eq 1 ]]; then
    echo &quot;This deploy was triggered manually.&quot;
fi

For example, you may wish to prevent deployments if the commit message contains “wip”:
CopyAsk AIif [[ $FORGE_DEPLOY_MESSAGE =~ &quot;wip&quot; ]]; then
    echo &quot;WORK IN PROGRESS, DO NOT CONTINUE.&quot;
    exit 1
fi

Forge will prefix any injected variables with FORGE_. Please do not use this “namespace” when defining your own environment variables.
​Deploying From CI
So far, we have discussed deploying Forge sites from the Forge UI or by using Forge’s “Quick Deploy” feature. However, you may also deploy them from a CI platform of your choice.
To execute a Forge deployment from a CI platform, you may use Deployment Triggers or Forge CLI.
​Using Deployment Triggers
You may execute a deployment at any time by instructing your CI platform to make a GET or POST request to the “Deployment Trigger URL” displayed in your site’s details.
Although you can refresh the site token at any time, you