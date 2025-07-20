# Forge - Servers/Management

*Source: https://forge.laravel.com/docs/servers/management*

---

Management - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationServersManagementDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseServersManagementLearn how to manage your servers in Forge.​Server Settings
The server dashboard’s Settings tab can be used to update important details of a server including its name, SSH connection details, timezone, and tags.
​IP Addresses
If your server’s IP address changes, you should inform Forge so that it can remain connected and continue to manage your server. To update the IP address of a server, navigate to the Settings tab and update the IP Address field under the Server Settings section.
When rebooting an AWS server, AWS will allocate a new IP address to the server. Therefore, you will need to update the IP address after a server reboot.
​Timezone
By default, all Forge servers are provisioned and configured to use the UTC timezone. If you need to change the timezone used by the server, you can do so by selecting one of the timezones from the list. Forge uses the timedatectl command to modify the system’s timezone.
​Archiving Servers
You may archive a server from the Forge UI by clicking the Archive button at the bottom of the server’s detail page. Archiving a server will remove Forge’s access to the server. If necessary, you may reconnect an archived server to Forge via your Forge account profile.
Archiving a server will not delete your server from the server provider and will not cause any data loss on your server.
​Archive Circle Permission
You may grant a circle member authority to archive a server from your account by granting the server:archive permission.
​Transferring Servers To Other Users
Servers may be transferred to other Forge accounts from the server’s Settings tab by providing the email address of the Forge account you wish to transfer the server to.
The Forge account that is receiving the server will receive an email asking them to confirm the request. They must also have set up the server provider that the server exists in before the transfer request can be sent. For example, if the server is a DigitalOcean server, the recipient must have DigitalOcean set up as a server provider within their own account.
You may only transfer servers to a Forge accounts with an active subscription that have not reached their server quota.
​Transfer Circle Permission
You may grant a circle member authority to transfer a server from your account by granting the server:transfer permission.
​Deleting Servers
You may delete a server from the Forge UI by clicking the Destroy Server button at the bottom of the server’s detail page. Forge requires you to confirm the name of the server before deleting it.
Deleting a server will permanently destroy the server from the connected provider, resulting in data loss.
​Deleting Custom Servers
When deleting a custom server, the server will only be removed from Forge. The server itself will continue to run.
​Delete Circle Permission
You may grant a circle member authority to delete a server from your account by granting the server:delete permission.Was this page helpful?YesNoServer TypesRoot Access / SecurityOn this pageServer SettingsIP AddressesTimezoneArchiving ServersArchive Circle PermissionTransferring Servers To Other UsersTransfer Circle PermissionDeleting ServersDeleting Custom ServersDelete Circle PermissionLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    code: \"code\",\n    p: \"p\",\n    strong: \"strong\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Note, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"server-settings\",\n      isAtRootLevel: \"true\",\n      children: \"Server Settings\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"The server dashboard’s \", _jsx(_components.strong, {\n        children: \"Settings\"\n      }), \" tab can be used to update important details of a server including its name, SSH connection details, timezone, and tags.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"ip-addresses\",\n      isAtRootLevel: \"true\",\n      children: \"IP Addresses\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If your server’s IP address changes, you should inform Forge so that it can remain connected and continue to manage your server. To update the IP address of a server, navigate to the \", _jsx(_components.strong, {\n        children: \"Settings\"\n      }), \" tab and update the \", _jsx(_components.strong, {\n        children: \"IP Address\"\n      }), \" field under the Server Settings section.\"]\n    }), \"\\n\", _jsx(Note, {\n      children: _jsx(_components.p, {\n        children: \"When rebooting an AWS server, AWS will allocate a new IP address to the server. Therefore, you will need to update the IP address after a server reboot.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"timezone\",\n      isAtRootLevel: \"true\",\n      children: \"Timezone\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"By default, all Forge servers are provisioned and configured to use the UTC timezone. If you need to change the timezone used by the server, you can do so by selecting one of the timezones from the list. Forge uses the \", _jsx(_components.code, {\n        children: \"timedatectl\"\n      }), \" command to modify the system’s timezone.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"archiving-servers\",\n      isAtRootLevel: \"true\",\n      children: \"Archiving Servers\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may archive a server from the Forge UI by clicking the \", _jsx(_components.strong, {\n        children: \"Archive\"\n      }), \" button at the bottom of the server’s detail page. Archiving a server will remove Forge’s access to the server. If necessary, you may reconnect an archived server to Forge via your Forge account profile.\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Archiving a server \", _jsx(_components.strong, {\n        children: \"will not\"\n      }), \" delete your server from the server provider and \", _jsx(_components.strong, {\n        children: \"will not\"\n      }), \" cause any data loss on your server.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"archive-circle-permission\",\n      isAtRootLevel: \"true\",\n      children: \"