Source: https://nightwatch.laravel.com/docs/guides/vapor.md

# Laravel Vapor

> Get started with Nightwatch on Vapor

Laravel Vapor is an auto-scaling serverless deployment platform for Laravel running on AWS Lambda. Due to the ephemeral nature of serverless functions on Lambda, using Nightwatch as a monitor requires a different approach than traditional server deployments.

## Overview

Since Lambda functions are stateless and short-lived, you cannot run the Nightwatch Agent directly within your Vapor application. Instead, you will need a long-running compute instance in the same network to host the Nightwatch Agent.

> [!TIP]
>
> We are building first-party support for this setup directly into Vapor. Until
> that's available, you can provision an EC2 instance to run the Nightwatch
> Agent either using Laravel Forge, or manually in the AWS console.

## Architecture

Your setup will consist of three components:

1. **EC2 Instance**: A long-running server to host the Nightwatch Agent
2. **Vapor Application**: Your serverless Laravel app configured to communicate with the EC2-hosted agent
3. **Vapor Network:** To allow private communication between your Vapor application and the Nightwatch Agent

## Forge Installation (recommended)

### Step 1: Provision a Forge worker

1. In the Forge dashboard, select **Create Server** -> **AWS**, and then configure as follows:

| Setting | Value |
| :- | :- |
| **Type** | `Worker Server` |
| **Region** | Same as your Vapor application |
| **Server Size** | `t3.micro` (the Nightwatch Agent is lightweight, and should not require a large instance) |
| **Private Network** | The Vapor network to which your Vapor application is connected |

2. Leave the other default settings, and select **Create Server**

### Step 2: Add a site on your worker

1. On your newly created worker server, select **Sites** -> **Add Site** using the default settings
2. Set the application repo and branch to mirror those used in the Vapor application
3. Ensure that **Install composer dependencies** is checked, then select **Install Repository**

> [!NOTE]
>
> Do not enable Nightwatch under the newly created Application's **Laravel**
> section, as it will interfere with the configuration needed for Vapor.

4. In your newly created site, Select **Environment** and add the following lines:

```
NIGHTWATCH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NIGHTWATCH_INGEST_URI=10.0.0.x:2407
```

Where `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` is your Nightwatch token, and `10.0.0.x` is the private IP address of your worker server (you can find this under the server's name above the Environment dialogue).

5. Select **Deploy Now**

> [!TIP]
>
> While creating a Site using your application source code is not strictly
> necessary, it offers a simple way to install the Nightwatch Agent, and helps
> ensure that the version matches that of the Nightwatch package used in your
> Vapor deployment.

### Step 3: Configure a background processes to run the Nightwatch agent

1. Noting the name of your newly created site, return to your server and select **Processes** -> **Background processes** -> **Custom**, then configure as follows:

   | Setting | Value |
   | :- | :- |
   | **Name** | `Nightwatch Agent` |
   | **Command** | `php artisan nightwatch:agent` |
   | **Directory** | `/home/forge/YOUR_SITE_NAME` (where `YOUR_SITE_NAME` is the name of the site you created in [Step 2](#step-2%3A-add-a-site-on-your-worker)) and `forge` is the site's user |

2. Leave the other default settings, and select **Create**

3. Select **Network**, and create a new firewall rule with the following settings:

* Port: `2407`
* From IP Address: `10.0.0.0/21`
* Rule Type: `Allow`

> [!NOTE]
>
> If your Vapor Network is configured with a custom IP range, you will need to
> adjust the **From IP Address** setting accordingly.

## Manual installation (coming soon)

> [!TIP]
>
> We are still working on a manual EC2 setup guide - watch this space!

## Configure your Vapor application

### Step 1: Install Nightwatch in your Laravel app

Add Nightwatch to your Laravel application:

```bash theme={null}
composer require laravel/nightwatch
```

### Step 2: Configure environment variables

In your Vapor environment configuration, add the following variables:

```env theme={null}
NIGHTWATCH_INGEST_URI=10.0.0.x:2407
```

Where `10.0.0.x` is the private IP address of your worker server

### Step 3: Verify network configuration

In your `vapor.yml` file ensure that the `network:` directive matches the Vapor network which you specified when creating your Forge worker server. This ensures that your Vapor application can communicate with the Nightwatch Agent running on that worker.

### Step 4: Synchronize Vapor deployment with EC2 instance

The Nightwatch Agent version running on your EC2 instance **must be kept in sync** with the Nightwatch package version in your Vapor application. Version mismatches will prevent the agent from ingesting data.

If you are using Forge, we recommend pinging Forge's Deployment Trigger URL for your site when deploying with Vapor. To find the Deployment Trigger URL, visit [the site you created](#forge-installation-recommended) and select the Deployments tab. There you can copy the Deployment Trigger URL.

You may then use `curl` to ping the Deployment Trigger URL during the deploy step in the `vapor.yml`:

```yml theme={null}
build:
    - 'composer install --no-dev'
    - 'php artisan event:cache'
    - 'npm ci && npm run build && rm -rf node_modules'
    # Deploy Forge Site...
    - 'curl https://forge.laravel.com/servers/{server}/sites/{site}/deploy/http?token={token}'
```

If you are not using Forge, you will need to manually keep the versions in sync between the EC2 instance and your Vapor application.

## Important considerations

### Verify network configuration

You must ensure that the `network:` directive in your `vapor.yml` file matches the network specified when creating your Forge worker server. This ensures that the Vapor application can communicate with the Nightwatch Agent running on your Forge worker.

You must also ensure that the firewall rule created in the Forge worker allows traffic from the Vapor network to the Nightwatch Agent port (default `2407`).

### Multiple Vapor applications/environments

If you wish to monitor multiple Vapor applications, you may run multiple agents on the same Forge worker by creating a separate **Site** and **Daemon** for each application, setting a unique port in the `NIGHTWATCH_INGEST_URI` environment variables in Forge/Vapor, and adding the respective firewall rules in Forge. Remember also to ensure that the `NIGHTWATCH_TOKEN` specified in each Forge Site is correct for the corresponding Vapor application/environment.
