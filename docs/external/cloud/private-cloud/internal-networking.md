Source: https://laravel.com/cloud/docs/private-cloud/internal-networking.md

# Internal networking

Communicate between applications in the same Private Cloud over the private cluster network.

## Introduction

Internal networking lets applications running inside the same Private Cloud cluster communicate over the private cluster network instead of routing traffic through the public internet. Internal networking can reduce egress costs, lower latency, and simplify architectures where services talk to each other frequently.

## Configuring internal networking

**1. Enable internal networking**

In the environment that should receive internal traffic, enable internal networking from **Settings > Network**. Laravel Cloud generates an internal URL for your application as soon as you enable internal networking.

**2. Choose which environments can reach you**

Decide which environments can connect over the internal network. Choose **All environments** to let every environment in the cluster reach your application, or choose **Specific environments** and select one or more environments that can reach it.

> [!NOTE]
>
> You can only select environments within the same Private Cloud.

**3. Deploy to synchronize the changes**

Deploy your environment to apply the new network settings. Once the deployment finishes, the selected environments can reach your application over the internal network.

**4. Connect using the internal URL**

Retrieve your internal URL from the environment's canvas or from **Settings > Network**. Other environments can now reach your application through this internal address rather than the public internet, so traffic stays within your Cloud account.

The internal hostname follows the format `env-{uuid}.private.laravel.cloud`, for example:

```text theme={null}
env-0a116d4f-6fe4-4ce7-9c00-89b527a63eb5.private.laravel.cloud
```

When you choose **All environments**, every environment in the cluster can connect to your application over the internal network. When you choose **Specific environments**, only the environments you select can reach your application, and Cloud blocks requests from any other environment.

## Connection and routing

* When internal networking is enabled for an environment, selected environments within the same Private Cloud can reach the application over HTTP. **Laravel Cloud doesn't issue SSL certificates for internal routes.**
* **Port 80 is open by default.** If a deployment listens on port 443 (HTTPS), internal routing maps that port to port 80, without TLS.
