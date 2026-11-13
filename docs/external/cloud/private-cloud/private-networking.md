Source: https://laravel.com/cloud/docs/private-cloud/private-networking.md

# Private networking

Connect your Private Cloud to AWS resources in your own accounts without traversing the public internet.

## Introduction

Private networking lets your Private Cloud reach AWS resources in your own accounts without exposing traffic to the public internet.

VPC Peering, PrivateLink, and PrivateLink (Resources) are available as self-service flows in the Cloud dashboard. Laravel Cloud also supports VPC Lattice and Transit Gateway, but you need to coordinate with the Laravel Cloud team to set them up.

> [!NOTE]
>
> Private networking connects your Private Cloud to resources in your own AWS accounts. To let applications inside the same Private Cloud communicate with each other, use [internal networking](https://laravel.com/cloud/docs/private-cloud/internal-networking) instead.

## Connection types

When you create a private connection, you choose a connection type. The right choice depends on what you are connecting to and how your network is structured.

* **VPC Peering**: A direct network link between two VPCs that lets connections route internally over private IPs. Simple to set up and best for simple networks.
* **VPC Lattice**: A managed service mesh for connecting services across VPCs. Useful for strict security environments with heightened observability.
* **PrivateLink**: Expose an individual service in one VPC to another over a private endpoint. Common for connecting to vendor-managed databases or APIs privately.
* **PrivateLink (Resources)**: Reach a single resource, such as a database, that you share with Laravel Cloud through AWS Resource Access Manager (RAM).
* **Transit Gateway**: A regional hub that connects multiple VPCs or other gateways together. Best for complex, multi-VPC architectures.

## Setting up a VPC peering connection

To establish a VPC peering connection from the Cloud dashboard:

**1. Open network settings**

Click the **Private network** card on your environment's canvas and select **Request private connection**.

**2. Choose a Private Cloud**

Select the Private Cloud you want to connect.

**3. Select the connection type**

Select **VPC Peering** as the connection type.

**4. Provide connection details**

Enter the following details:

* **AWS account ID**: The 12-digit account ID of the AWS account that owns the VPC or resources you want to connect to.
* **VPC ID**: The ID of the VPC you want to peer with. You can find this in your AWS VPC dashboard.
* **CIDR range**: The IPv4 CIDR block of the target VPC. This range must not overlap with your Private Cloud's CIDR range.

**5. Submit the request**

Submit the request. Laravel Cloud provisions the peering connection and updates the connection's status as it progresses.

**6. Accept the peering request in AWS**

Once the connection reaches a state requiring your action, accept the peering request from your AWS account and update your VPC's route tables to direct traffic to the peering connection.

The connection card on the **Private connections** page shows both sides of the peering. The card lists the values you provided under `Target` and the corresponding Laravel Cloud values under `Ours`. Use the `Ours` IP information when you configure resources in your account that need to talk to your Private Cloud. Use the `Target` IPs when your Private Cloud needs to reach resources in your account.

If a connection fails or expires, click **Renew request** to restart the workflow without re-entering the details.

## Setting up a PrivateLink connection

Use PrivateLink when the service you want to reach is published as a VPC endpoint service, either by you or by a vendor such as a managed database provider. Laravel Cloud creates an interface endpoint in your Private Cloud that connects to the endpoint service, so traffic only flows one way and the two networks' CIDR ranges may overlap.

**1. Start a private connection request**

Start a request the same way as for VPC peering, and select **PrivateLink** as the connection type.

**2. Provide connection details**

Enter the following details:

* **AWS account ID** (optional): The 12-digit account ID of the AWS account that owns the endpoint service. You may leave this blank, which is common when a vendor owns the endpoint service and does not share its account ID.
* **Endpoint service name**: The name of the VPC endpoint service, such as `com.amazonaws.vpce.us-east-2.vpce-svc-0a1b2c3d4e5f6`. You can find this in AWS under **VPC** > **Endpoint services**, or in your vendor's PrivateLink instructions.
* **Ports**: The ports the endpoint service listens on, separated by commas. Laravel Cloud only reaches these ports.
* **Endpoint service region**: The AWS region where the endpoint service is located.

**3. Allow Laravel Cloud on the endpoint service**

Once the Laravel Cloud team approves your request, the connection shows a Laravel Cloud principal ARN. Add it to the endpoint service's allowed principals, then click **Mark as done**. If a vendor owns the endpoint service, send them the principal ARN to add.

**4. Accept the endpoint connection**

Laravel Cloud creates the interface endpoint and shows its endpoint ID. Accept the connection request from that endpoint under **VPC** > **Endpoint services** > **Endpoint connections**, then click **Mark as done**. If the endpoint service accepts connections automatically, you only need to click **Mark as done**.

**5. Wait for Laravel Cloud to finish the connection**

Laravel Cloud configures DNS resolution for the endpoint and verifies connectivity. The connection becomes active once verification succeeds.

## Setting up a PrivateLink (Resources) connection

Use PrivateLink (Resources) to reach a single resource, such as an RDS database, without publishing an endpoint service. You describe the resource with a VPC Lattice resource configuration and share it with Laravel Cloud through AWS RAM.

**1. Start a private connection request**

Start a request the same way as for VPC peering, and select **PrivateLink (Resources)** as the connection type.

**2. Provide connection details**

Enter the following details:

* **AWS account ID** (optional): The 12-digit account ID of the AWS account that owns the resource configuration.
* **Resource configuration ARN**: The ARN of the resource configuration you want to share. You can find this in AWS under **VPC** > **Resource configurations**.
* **Ports**: The ports the shared resource listens on, separated by commas. Laravel Cloud only reaches these ports.
* **Resource region**: The AWS region where the resource configuration is located.

**3. Share the resource configuration**

Once the Laravel Cloud team approves your request, the connection shows the Laravel Cloud AWS account ID. Share the resource configuration with that account through AWS RAM, then click **Mark as done**.

**4. Wait for Laravel Cloud to finish the connection**

Laravel Cloud accepts the resource share, creates the resource endpoint, and verifies connectivity. The connection becomes active once verification succeeds.

> [!NOTE]
>
> Steps that you need to complete in AWS must be marked as done within seven days. Otherwise, the connection fails, and you can click **Renew request** to start again.

## VPC Lattice and Transit Gateway

Laravel Cloud supports these connection types, but they aren't available as a self-service flow in the dashboard yet. To set one up, [contact the Laravel Cloud team](https://laravel.com/enterprise) with:

* The connection type you need.
* The AWS account and VPC details for the target side.
* For VPC Lattice: the resources or services you want to make available.
* For Transit Gateway: the existing Transit Gateway ID and routing details.

The Laravel Cloud team provisions the connection, and it appears in your **Private connections** list once it is live.
