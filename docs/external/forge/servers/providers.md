# Forge - Servers/Providers

*Source: https://forge.laravel.com/docs/servers/providers*

---

Server Providers - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersServer ProvidersDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersServer ProvidersLearn about the server providers supported by Forge.​Supported Server Providers
Forge can create and manage servers on the following cloud server providers:

DigitalOcean
Vultr
Akamai / Linode Cloud
Amazon AWS

Forge supports provisioning servers in all non-Gov regions that are active in the connected AWS account.


Hetzner Cloud
Bring Your Own Server

If your preferred server provider is not supported by Forge, you may use Forge’s “Custom VPS” option to create your server. Custom VPS servers receive all of the same functionality as first-party supported server providers. Learn more
​Linking Server Providers
You can link server providers from your Server Providers dashboard. It is possible to link any number of supported provider accounts, including multiple accounts for one provider.
​Amazon AWS API Access
In order to provision servers on AWS, you need to create a new IAM role. To get started, navigate to the IAM service on your AWS dashboard. Once you are in the IAM dashboard, you may select “Roles” from the left-side navigation panel and click the “Create Role” button.
The process for creating the role is outlined in these steps:

Choose “AWS account” as the trusted entity type, and select “Another AWS account.”
Enter the “Forge AWS Account” from the Forge dashboard, then click “Next.”
In the “Permissions policies” section, select the AmazonEC2FullAccess and AmazonVPCFullAccess policies. Then, click “Next.”
In the “Name, review, and create” section, provide a name and description for the role.
Update the “Trust policy” under “Select trusted entities” by enabling the “Require external ID” checkbox and entering the “AWS External ID” shown in the Forge dashboard.
Complete the process by creating the role.
Copy the role ARN displayed in the AWS dashboard and add it to your AWS credentials in Forge.

There are a few requirements you should review to ensure Forge works correctly with your linked AWS account:

If you are using an existing VPC, the subnet must be configured to auto-assign public IP addresses.
If you are using an existing VPC, the default security group must allow Forge to SSH into the server. Here is an example:

TypeProtocolPort RangeSourceDescriptionHTTPTCP80Custom0.0.0.0/0HTTPTCP80Custom::/0SSHTCP22CustomYOUR_IP_ADDRESS/32SSH from your IPSSHTCP22Custom159.203.150.232/32SSH from ForgeSSHTCP22Custom159.203.150.216/32SSH from ForgeSSHTCP22Custom45.55.124.124/32SSH from ForgeSSHTCP22Custom165.227.248.218/32SSH from ForgeHTTPSTCP443Custom0.0.0.0/0HTTPSTCP443Custom::/0
​AWS Service Limits
AWS Service Limits can be increased through the following options:
From the AWS console
Open the Service Quotas console.
In the navigation pane, choose AWS services.
Select a service.
Select a quota.
Follow the directions to request a quota increase.
From the AWS CLI
Use the request-service-quota-increase AWS CLI command.
From a support case
If a service is not yet available in Service Quotas, use the AWS Support Center Console to create a service quota increase case.
If the service is available in Service Quotas, AWS recommends that you use the Service Quotas console instead of creating a support case.

For additional information, refer to the following AWS documentation:
Requesting a quota increase in the Service Quotas User Guide.
AWS Service Quotas reference.

​Akamai / Linode API Access
When creating a new Akamai Cloud API token for your Akamai account, Akamai will ask you to select which permissions are needed by the token. You will need to select the following permissions:

Linodes - Read/Write
IPs - Read/Write

In addition, you may wish to set the token to never expire.
​DigitalOcean OAuth Access
The easiest way to allow Forge to communicate with your DigitalOcean account is by using the “Login with DigitalOcean” button. This option can be found on the Server Providers page within your Forge account.
Clicking the “Login with DigitalOcean” button will redirect you to DigitalOcean’s Authorize Application page, where you’ll be asked to approve the required permissions requested by Forge.
Once approved, Forge will create an OAuth credential, allowing it access to the necessary permissions needed in provisioning and managing your servers on your behalf.
​DigitalOcean API Access
In addition to granting Forge access via OAuth, you can also use a Personal Access Token to enable Forge to communicate with your DigitalOcean account. When creating a new Personal Access Token for your DigitalOcean account, you will need to select which scopes will be granted on the token. You must select either:

Full Access: Grants access to all scopes based on the account’s current role permissions
Custom Scopes: Grants granular permissions on specific scopes. The following are required by Forge to successfully provision a server:

Droplet - Create / Read / Update / Delete
Reserved IP - Create / Read / Update / Delete
SSH Key - Create / Read / Update / Delete
VPC Key - Create / Read / Update / Delete



​Vultr API Access
The Vultr server provider requires you to add the Forge IP addresses to an IP address allow list so that Forge can communicate with your servers. You should ensure that you do this before provisioning a Vultr server via Forge.
​Hetzner Cloud API Access
Hetzner API tokens are specific to a Hetzner Project. If you utilize Hetzner Projects, you should ensure that Forge has an API token for each Hetzner Project.
​Bring Your Own Server
Alongside supporting several first-party server providers, Forge also supports the ability to use your own custom server. To do so, select the Custom VPS option when creating a new server. When provisioning a Custom VPS, Forge can only provision and manage an existing server — it cannot create servers on that custom provider.
In addition, you should review the following server requirements:

The server must be running a fresh installation of Ubuntu 22.04 or 24.04 x64.
The server must be accessible externally over the Internet.
The server must have root SSH access enabled.
The server requirements should meet the following criteria or more: 1 CPU Core with 1GHz, 1GB RAM, and 10GB Disk space.
The server must have curl installed.
Ensure that no firewall or security group is throttling requests to the server. Throttling SSH requests may cause provisioning to fail at the final stage.
Some server providers may modify the contents of /root/.ssh/authorized_keys. If this applies to your provider, ensure they allow Forge’s public key to access the server. You can find this key by visiting: https://forge.laravel.com/servers/&lt;serverID&gt;/settings.
If you restrict SSH access by IP address, consult the Forge IP address documentation.
If you are protecting your internal network through Network Address Translation and you are mapping public SSH ports to different internal SSH ports, you may let Forge know about this by checking the This server is behind a NAT ch