# Forge - Accounts/Your-Account

*Source: https://forge.laravel.com/docs/accounts/your-account*

---

Your Account - Laravel Forge
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
Laravel Forge home pageSearch...⌘KAsk AISupportDashboardDashboardSearch...NavigationAccountsYour AccountDocumentationChangelogCommunityBlogGet StartedIntroductionForge CLIForge SDKAccountsYour AccountCirclesSource ControlSSH KeysAPITagsTroubleshootingServersServer ProvidersServer TypesManagementRoot Access / SecuritySSH Keys / Git AccessPHPPackagesRecipesLoad BalancingNginx TemplatesDatabase BackupsMonitoringCookbookSitesThe BasicsApplicationsDeploymentsCommandsPackagesQueuesSecurity RulesRedirectsSSLUser IsolationCookbookResourcesDaemonsDatabasesCachesNetworkSchedulerIntegrationsCookbookIntegrationsEnvoyerSentryAikidoOtherAbuseAccountsYour AccountLearn how to manage your Forge account, including updating your profile information, securing your account with Two Factor Authentication, managing authenticated sessions, deleting your account, sharing your account’s servers with other users, receiving invoices via email, accessing previous invoices, and adding business receipts.​User Account
​Updating Your Profile Information
You may update your name, email, and password from Forge’s Authentication dashboard within your user profile.
​Securing Your Account With Two Factor Authentication
You may add additional security to your user account by setting up Two Factor Authentication (2FA) via Forge’s Authentication dashboard. Once you enable 2FA, please remember to scan the 2FA barcode into your authentication app, such as Google Authenticator.
When enabling 2FA, Forge will display:

A QR code to can with your authentication app
A security code (if you can’t scan the QR code)
Several recovery codes

The recovery codes should be stored securely and can be used if you no longer have access to your 2FA device, thus it is recommended to not store your recovery codes exclusively on the device that you use for 2FA. Each recovery code can only be used once. You may re-generate the recovery codes at any time from your account’s dashboard.
If you have configured 2FA on your account and lose access to your it and your recovery codes, you will need to email [email&#160;protected] to reset it by confirming your identity.
We recommend using the Google Authenticator application on your smartphone to manage your Forge 2FA configuration.
​Managing Authenticated Sessions
To improve your account security, we allow you to view and logout any active sessions for your user account via the Authentication dashboard. This is particularly useful if you forgot to logout on a device you no longer have access to.
​Deleting Your Account
You can delete your account at any time from the Authentication dashboard.
Deleting your account will cancel your subscription and delete all of your account’s data. Your data, including billing information, will not be recoverable; however, your servers will not be deleted from your connected server providers.
​Sharing Your Account’s Servers With Other Users
If you need to allow other users to help manage the servers in your Forge account, you can create a Circle.
​Billing
​Receiving Invoices via Email
Specifying the email addresses you would like to receive new invoices can be done in Forge’s Billing Management page. You may specify several email addresses by providing a comma separated list.
​Accessing Previous Invoices
The Billing Management page list all previous invoices for you account.
​Business Receipts
If you need to add specific contact or tax information to your receipts such as your full business name, VAT / tax identification number, or address of record, you can add this extra billing information on the Billing Management page in your account. We’ll make sure this information is displayed on every receipt.Was this page helpful?YesNoForge SDKCirclesOn this pageUser AccountUpdating Your Profile InformationSecuring Your Account With Two Factor AuthenticationManaging Authenticated SessionsDeleting Your AccountSharing Your Account’s Servers With Other UsersBillingReceiving Invoices via EmailAccessing Previous InvoicesBusiness ReceiptsLaravel Forge home pagexgithubdiscordlinkedinTerm of ServicePrivacy PolicyData Processing Agreement (DPA)xgithubdiscordlinkedinAssistantResponses are generated using AI and may contain mistakes.{"props":{"pageProps":{"mdxSource":{"compiledSource":"\"use strict\";\nconst {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0];\nconst {useMDXComponents: _provideComponents} = arguments[0];\nfunction _createMdxContent(props) {\n  const _components = {\n    a: \"a\",\n    li: \"li\",\n    p: \"p\",\n    strong: \"strong\",\n    ul: \"ul\",\n    ..._provideComponents(),\n    ...props.components\n  }, {Heading, Note, Warning} = _components;\n  if (!Heading) _missingMdxReference(\"Heading\", true);\n  if (!Note) _missingMdxReference(\"Note\", true);\n  if (!Warning) _missingMdxReference(\"Warning\", true);\n  return _jsxs(_Fragment, {\n    children: [_jsx(Heading, {\n      level: \"2\",\n      id: \"user-account\",\n      isAtRootLevel: \"true\",\n      children: \"User Account\"\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"updating-your-profile-information\",\n      isAtRootLevel: \"true\",\n      children: \"Updating Your Profile Information\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may update your name, email, and password from Forge’s \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/authentication\",\n        children: \"Authentication dashboard\"\n      }), \" within your user profile.\"]\n    }), \"\\n\", _jsx(Heading, {\n      level: \"3\",\n      id: \"securing-your-account-with-two-factor-authentication\",\n      isAtRootLevel: \"true\",\n      children: \"Securing Your Account With Two Factor Authentication\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"You may add additional security to your user account by setting up Two Factor Authentication (2FA) via Forge’s \", _jsx(_components.a, {\n        href: \"https://forge.laravel.com/user-profile/authentication\",\n        children: \"Authentication dashboard\"\n      }), \". Once you enable 2FA, please remember to scan the 2FA barcode into your authentication app, such as \", _jsx(_components.a, {\n        href: \"https://support.google.com/accounts/answer/1066447\",\n        children: \"Google Authenticator\"\n      }), \".\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"When enabling 2FA, Forge will display:\"\n    }), \"\\n\", _jsxs(_components.ul, {\n      children: [\"\\n\", _jsx(_components.li, {\n        children: \"A QR code to can with your authentication app\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"A security code (if you can’t scan the QR code)\"\n      }), \"\\n\", _jsx(_components.li, {\n        children: \"Several recovery codes\"\n      }), \"\\n\"]\n    }), \"\\n\", _jsx(_components.p, {\n      children: \"The recovery codes should be stored securely and can be used if you no longer have access to your 2FA device, thus it is recommended to not store your recovery codes exclusively on the device that you use for 2FA. Each recovery code can only be used once. You may re-generate the recovery codes at any time from your account’s dashboard.\"\n    }), \"\\n\", _jsxs(_components.p, {\n      children: [\"If you have configured 2FA on your account and lose access to your it and your recovery codes, you will need to email \", _jsx(_components.a, {\n        href: \"mailto:forge@laravel.com\",\n        children: \"forge@laravel.com\"\n      }), \" to reset it by confirming your identity.\"]\