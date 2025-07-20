# Forge - Accounts/Circles

*Source: https://forge.laravel.com/docs/accounts/circles*

---

Circles - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationAccountsCirclesDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseAccountsCirclesForge circles allow you to collaborate with team members that may manage servers and sites on your behalf. You can create as many circles as you would like and add as many team members as needed to each circle.​Overview
Forge circles allow you to collaborate with team members that may manage servers and sites on your behalf. You can create as many circles as you would like and add as many team members as needed to each circle.
Creating and managing Circles is only available on our “business” plan.
​Creating Circles
You may create a circle via the Forge circle dashboard. To create a circle, you only need to provide a name.
​Managing Circles
Circles that you manage will be listed in the Managed Circles table.
​Editing Circles
You can edit a circle by clicking the “edit” button next to the circle’s name. Editing a circle will allow you to:

Rename the circle
Select credentials to share with circle members
Select servers to share with circle members
Invite members to the circle
Manage circle members
View or delete open circle invites

Shared credentials will allow servers to be created on your behalf. The servers will be created in your server provider’s account.
​Managing Circle Members
To invite a new member to the circle, you need to provide their email address and at least one permission. If the email address provided doesn’t match an existing Forge account, the user will be invited to create an account. The invited user may accept the invite from the same email.
​Permissions
You may limit a circle member’s access to servers and sites by selecting their permissions. Without any permissions, members will always be able to read server and site data but will be unable to make any changes.
When selecting which permissions a member has, you may hover over the “i” icon to learn more about what that permission does. You may change a member’s permissions at any time by editing the circle member.
API tokens generated by a circle member will also be restricted to the permissions they have been assigned when using the API to interact with circle servers.
​Deleting Circles
You can delete circles via the Forge circle dashboard by clicking the “delete” button next to the circle’s name. You will be asked to confirm the deletion before it is actually deleted.
When deleting a circle, members will no longer be able to access shared servers or credentials.
​Accepting a Circle invite
After being invited to a Circle, you will receive an email with a link that you may use to accept an invite.
If you would like to see any pending Circle invitations you have, you may visit the Circle dashboard and see the invitations listed under “Pending invites”.
​Leaving a Circle
You can leave a Circle that you are a member of by visiting the Circle dashboard and clicking the “leave” button next to the Circle’s name.Was this page helpful?YesNoYour AccountSource ControlOn this pageOverviewCreating CirclesManaging CirclesEditing CirclesManaging Circle MembersPermissionsDeleting CirclesAccepting a Circle inviteLeaving a CircleLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"overview\",\n      isAtRootLevel: \"true\",\n      children: \"Overview\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"Forge circles allow you to collaborate with team members that may manage servers and sites on your behalf. You can create as many circles as you would like and add as many team members as needed to each circle.\"\n    }), \"\\n\", _jsx(Warning, {\n      children: _jsx(_components.p, {\n        children: \"Creating and managing Circles is only available on our “business” plan.\"\n      })\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"creating-circles\",\n      isAtRootLevel: \"true\",\n      children: \"Creating Circles\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may create a circle via the \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/circles\",\n        children: \"Forge circle dashboard\"\n      }), \". To create a circle, you only need to provide a name.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"2\",\n      id: \"managing-circles\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Circles\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Circles that you manage will be listed in the \", _jsx(_components.strong, {\n        children: \"Managed Circles\"\n      }), \" table.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"editing-circles\",\n      isAtRootLevel: \"true\",\n      children: \"Editing Circles\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"You can edit a circle by clicking the “edit” button next to the circle’s name. Editing a circle will allow you to:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"Rename the circle\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Select credentials to share with circle members\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Select servers to share with circle members\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Invite members to the circle\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Manage circle members\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"View or delete open circle invites\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"Shared credentials will allow servers to be created on your behalf. The servers will be created in \", _jsx(_components.strong, {\n        children: \"your\"\n      }), \" server provider’s account.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"managing-circle-members\",\n      isAtRootLevel: \"true\",\n      children: \"Managing Circle Members\"\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"To invite a new member to the circle, you need to provide their email address and at least one permission. If the email address provided doesn’t match an existing Forge account, the user will be invited to crea