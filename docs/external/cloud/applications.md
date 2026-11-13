Source: https://laravel.com/cloud/docs/applications.md

# Applications

Create, manage, and deploy applications on Laravel Cloud from starter kits or existing Git repositories.

## Introduction

An application is the top-level unit for deploying and managing your code on Laravel Cloud. You can create applications from official [Laravel starter kits](https://laravel.com/starter-kits) or from existing GitHub, Bitbucket, or GitLab repositories. An application can contain many environments and resources.

## Creating applications

Laravel Cloud offers two ways to create applications:

1. From a starter kit, which bootstraps a new application from an official Laravel starter kit
2. From an existing repository, which imports and deploys your existing Git repository

Both methods require you to select the region where Laravel Cloud deploys your application. An application can be deployed to only one region at a time. Laravel Cloud automatically creates a default [environment](https://laravel.com/cloud/docs/environments) for your application, whichever creation method you choose.

> [!NOTE]
>
> You cannot transfer an application to another organization after you create it. Each application stays permanently associated with the organization you create it in.

### Creating from starter kits

You can create applications from official [Laravel starter kits](https://laravel.com/starter-kits). Starter kits let you deploy a production-ready Laravel application in minutes without an existing repository.

#### Available starter kits

Laravel Cloud provides the following official starter kit templates:

* **Laravel**: a new, empty Laravel application
* **[React Starter Kit](https://laravel.com/docs/12.x/starter-kits#react)**: React, TypeScript, Inertia, and shadcn/ui
* **[Vue Starter Kit](https://laravel.com/docs/12.x/starter-kits#vue-customization)**: Vue, TypeScript, Inertia, and shadcn-vue
* **[Svelte Starter Kit](https://laravel.com/docs/12.x/starter-kits#svelte-customization)**: Svelte, TypeScript, Inertia, and shadcn-svelte
* **[Livewire Starter Kit](https://laravel.com/docs/12.x/starter-kits#livewire-customization)**: Livewire, Laravel Volt, and Flux UI

#### Creating from a starter kit

To create an application from a starter kit:

1. On the application creation page, select **Use a template**.
2. Choose your starter kit template.
3. If you have not connected your GitHub account yet, connect it. Starter kits are available only with GitHub.
4. Set your repository name and choose its visibility (private or public).
5. Assign an application name.
6. Select your deployment region.

Laravel Cloud creates a new repository in your connected GitHub account, clones the official Laravel starter kit code into it, and sets up your application for deployment.

> [!NOTE]
>
> Starter kit applications work exactly like any other Laravel application on Laravel Cloud. Once deployed, you can customize, extend, and deploy changes the same way you do for applications created from existing repositories.

### Creating from existing repository

To create an application from an existing repository, select the source control repository to deploy from, assign the application a name, and select a region. Existing repositories can contain applications built with any of Laravel Cloud's supported frameworks and runtimes.

If you have not linked a source control provider account to your organization yet, Laravel Cloud prompts you to link one when you create your application. Typically, your Laravel Cloud organization structure should mirror the organization structure of your source control provider.

> [!NOTE]
>
> After you authenticate a source control provider, every user in the organization can view the repositories you selected and create applications from them.

### Regions

Laravel Cloud currently supports the following application regions:

* US East (Virginia) / `us-east-1`
* US East (Ohio) / `us-east-2`
* Canada (Central) / `ca-central-1`
* EU Central (Frankfurt) / `eu-central-1`
* EU West (Ireland) / `eu-west-1`
* EU West (London) / `eu-west-2`
* Asia Pacific (Singapore) / `ap-southeast-1`
* Asia Pacific (Sydney) / `ap-southeast-2`
* Asia Pacific (Tokyo) / `ap-northeast-1`

For minimal latency, make sure your application and its associated resources are in the same region.

## Deleting applications

When you delete an application, Laravel Cloud deletes all environments within that application. Laravel Cloud does not delete resources such as databases, caches, and object storage buckets, since other applications within the environment may use them. To delete these resources, navigate to your organization's **Resources** tab.

## Troubleshooting

### Reconnect Git repository

An application can lose its connection to a Git repository if someone revokes Laravel Cloud's API access from within the source control provider. When the connection is lost, your application's environments can no longer deploy your latest changes. To restore your Git connection, follow these steps:

1. Navigate to your application's **Settings** page.
2. Click the **Not connected** button next to **Git repository**.


3. Click the **Source control provider** dropdown and select an existing source control provider. To connect a new one, click **Add account**.
4. Select the right repository, click **Set repository**, and then click **Save**.


Your application's Git repository is now restored, and you can resume deploying fresh code to your environments.

> [!NOTE]
>
> In most cases, Laravel Cloud restores environment branches automatically. In some cases, you may need to select and save environment branches manually from the environment **Settings** tab.
