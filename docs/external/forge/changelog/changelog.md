# Forge - Changelog/Changelog

*Source: https://forge.laravel.com/docs/changelog/changelog*

---

Changelog - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationChangelogDocumentationChangelogCommunityBlogChangelogChangelog​Week of May 13, 2025Changed
Removed support for Ubuntu 20.04 as it has reached end-of-life (EOL)

​Week of May 2, 2025Improvements
Increased performance around the sites API
SSH key fingerprinting algorithm
Performance of server events page
Fixes
Server packages page now loads correctly when the server has no sites
API now allows custom frequencies when creating a scheduled job

​Week of Apr 25, 2025Improvements
Provisioning process now checks for Ubuntu version
New deployment scripts now use a read-only file descriptor to prevent concurrent PHP-FPM reloads

​Week of Apr 18, 2025Improvements
Added subjects to emails sent from Forge
Better handling when archiving disconnected servers
Fixes
Trim excessive recipe output
Fix running of recipes
Daemons no longer get stuck with an incorrect status
Recipe notifications are now working again

​Week of Mar 28, 2025Improvements
Prevent deployments of sites not ready to be deployed
Slack authorization handling
Fixes
Circle invitation validation
Aikido integration correctly matches repositories
Log files can now be cleared again
Daemons can now be created with startsecs=0

​Week of Mar 17, 2025Improvements
Updated font on invoice
Fixes
No notification when server failed to delete at provider
Supplying empty username when creating a site via the API
Aikido setup when using custom GitLab
Required email field when editing backup configuration
Server disappearing from dashboard when deleting a load balanced site
pool.d file missing when changing PHP version on an isolated site
stopwaitsecs missing in deamons API (was part of docs)
Removing Laravel specific daemons sometimes removed wrong deamon
Servers not marked as connecting while refreshing status

​Week of Mar 3, 2025Fixes
Creating an isolated site via the API with invalid usernames

​Week of Feb 17, 2025Improvements
Role ARNs are required when editing AWS credentials
Fixes
Reverb and Octane daemons are created with custom ports
“Run Job Now” correctly reports the status of the job

​Week of Feb 10, 2025Improvements
Improved performance of server and site name searching
Improved server password generation
Fixes
Notification channels are now correctly removed when transferring servers
Reverb site name is now updated when a site is renamed
Blackfire is now correctly removed for PHP 8.4 when the integration is disabled
Clean up failed Reverb installations

​Week of Feb 3, 2025Improvements
Clarify Deployment Script’s reloading of PHP FPM
Increased security requirements for new passwords
Fixes
Correctly handle transferring of AWS servers when using Role ARN based credentials
Fixed deleting of Circles with pending invitations
Fixed error when transferring servers that are part of a circle

​Week of Jan 27, 2025Improvements
SSH banners are now muted when Forge connects to a server
Newly provisioned servers now write a .hushlogin file to prevent errors caused by MOTD
Improved handling of disconnected servers when running scripts
Enabled X-Frame-Options=SAMEORIGIN header for improved security
Fixes
When deleting AWS servers, the EBS block volumes are also deleted
Reload PHP-FPM when restarting Nginx
Fixed create server modal not hiding in some cases
Improved authorization retry logic when connected to Bitbucket

​Week of Jan 20, 2025Improvements
Add support for Swoole with PHP 8.4
Add Thailand (ap-southeast-1) to AWS regions list
Add Mexico (mx-central-1) to AWS regions list
New AWS credentials will use short-lived tokens via AWS Roles
Fixes
Sites can now be safely renamed back to default
Add -s flag when syncing MySQL databases to prevent errors
Fixed recipe reports

​Week of Jan 13, 2025Improvements
Server names now include a wider variety of names
SSH keys generated by Forge will now be use ed25519
Node 22.x is now installed by default (previously 18.x)
Forge now detects the process status of all daemons
Server Ubuntu versions are now shown in the information bar
Fixes
Disabled Microsoft Teams notifications
Firewall IPs may be comma separated including spaces
Worker information will now show all known information
Daemon status syncing is now more resilient
Pinned awscli to v2.22.35 to resolve issues when using DigitalOcean and Vultr S3 providers with database backups

​Week of Jan 6, 2025Improvements
Add validation message when archiving balancers from API
Switched field order when installing existing certificates
Report rate limiting errors to the frontend
Fixes
Allow installing repositories with special characters in branch names
AWS VPC is no longer always required when creating new AWS servers
“Skip this step” button now redirects correctly when onboarding
Disabled “Blogo” starter kit within Statamic integration
Let’s Encrypt certificates should timeout less frequently
Forge now reloads PHP-FPM when reloading Nginx configurations (previously calling restart could cause moments of downtime)
Was this page helpful?YesNoOn this pageWeek of May 13, 2025Week of May 2, 2025Week of Apr 25, 2025Week of Apr 18, 2025Week of Mar 28, 2025Week of Mar 17, 2025Week of Mar 3, 2025Week of Feb 17, 2025Week of Feb 10, 2025Week of Feb 3, 2025Week of Jan 27, 2025Week of Jan 20, 2025Week of Jan 13, 2025Week of Jan 6, 2025Laravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Update} = _components;\n  if (!Update) _missingMdxReference(\"Update\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsxs(Update, {\n      label: \"Week of May 13, 2025\",\n      id: \"week-of-may-13%2C-2025\",\n      children: [_jsx(_components.p, {\n        children: _jsx(_components.strong, {\n          children: \"Changed\"\n        })\n      }), _jsxs(_components.ul, {\n        children: [\"\\n\", _jsx(_components.li, {\n          children: \"Removed support for Ubuntu 20.04 as it has reached end-of-life (EOL)\"\n        }), \"\\n\"]\n      })]\n    }), \"\\n\", _jsxs(Update, {\n      label: \"Week of May 2, 2025\",\n      id: \"week-of-may-2%2C-2025\",\n      children: [_jsx(_components.p, {\n        children: _jsx(_components.strong, {\n          children: \"Improvements\"\n        })\n      }), _jsxs(_components.ul, {\n        children: [\"\\n\", _jsx(_components.li, {\n          children: \"Increased performance around the sites API\"\n        }), \"\\n\", _jsx(_components.li, {\n          children: \"SSH key fingerprinting algorithm\"\n        }), \"\\n\", _jsx(_components.li, {\n          children: \"Performance of server events page\"\n        }), \"\\n\"]\n      }), _jsx(_components.p, {\n        children: _jsx(_components.strong, {\n          children: \"Fixes\"\n        })\n      }), _jsxs(_components.ul, {\n        children: [\"\\n\", _jsx(_components.li, {\n          children: \"Server packages page now loads correctly when the server has no sites\"\n        }), \"\\n\", _jsx(_components.li, {\n          children: \"API now allows custom frequencies when c