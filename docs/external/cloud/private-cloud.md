Source: https://laravel.com/cloud/docs/private-cloud.md

# Private Cloud

Your own isolated Laravel Cloud, fully managed by Laravel.

## Introduction

Laravel Private Cloud gives your organization a fully isolated environment that Laravel operates end to end. You get the control, security, and compliance of enterprise infrastructure, and your engineers don't spend their time deploying your applications or scaling on demand.

## Why Private Cloud

Private Cloud gives you dedicated infrastructure for strict security, compliance, or performance requirements.

* **Dedicated compute**: Your applications run in an isolated cluster with dedicated nodes, so compute, networking, and scaling are fully isolated. Other customers' workloads cannot affect your performance.
* **Private networking**: Connect to your existing AWS services over [private networking](https://laravel.com/cloud/docs/private-cloud/private-networking) for reduced latency and no public internet exposure.
* **Dedicated outbound IPs**: Customer-specific IP addresses for allowlisting, traceability, and compliance.
* **Built for compliance**: Private networking, isolated compute, and reduced attack surface without custom infrastructure.
* **High availability with automatic failover**: Three always-on nodes across availability zones provide automatic failover.
* **Fully managed by Laravel**: Laravel operates the platform, so your team can focus on the product.

## HIPAA compliance

Laravel Cloud supports HIPAA compliance for Private Cloud customers through a signed Business Associate Agreement (BAA) and the administrative, physical, and technical safeguards required to protect Protected Health Information (PHI).

> [!NOTE]
>
> If your application handles PHI, contact our team at [cloud@laravel.com](mailto:cloud@laravel.com) to request a BAA before deploying to Laravel Cloud.

See the [Compliance & Security](https://laravel.com/cloud/docs/compliance) page for more on Laravel Cloud's compliance posture, including SOC 2 Type 2 attestation.

## How it works

Laravel provisions your Private Cloud in a dedicated AWS account and VPC that Laravel maintains. Each Private Cloud includes:

* Private Kubernetes cluster
* Dedicated compute nodes
* [Private networking](https://laravel.com/cloud/docs/private-cloud/private-networking) through VPC Peering, PrivateLink, VPC Lattice, or Transit Gateway
* Dedicated NAT gateways with static outbound IPs
* Optional managed [RDS databases](https://laravel.com/cloud/docs/private-cloud/rds) and [ElastiCache caches](https://laravel.com/cloud/docs/private-cloud/elasticache) inside your private environment

Your applications deploy into this environment through Laravel Cloud, but everything runs inside infrastructure that belongs only to you.

To learn more about the features available to your Private Cloud, see the following pages:

* [Dedicated edge network](https://laravel.com/cloud/docs/private-cloud/edge-network): An isolated edge zone with custom rules, cache rules, and traffic visibility.
* [Private networking](https://laravel.com/cloud/docs/private-cloud/private-networking): Reach AWS resources in your own accounts without traversing the public internet.
* [Internal networking](https://laravel.com/cloud/docs/private-cloud/internal-networking): Communicate between applications in the same Private Cloud over the private cluster network.
* [IAM roles](https://laravel.com/cloud/docs/private-cloud/iam-roles): Give your environments temporary credentials for a role in your own AWS account instead of static access keys.
* [RDS](https://laravel.com/cloud/docs/private-cloud/rds): Managed AWS RDS databases for your Private Cloud applications.
* [ElastiCache](https://laravel.com/cloud/docs/private-cloud/elasticache): Managed AWS ElastiCache caches for your Private Cloud applications.
* [Data transfer](https://laravel.com/cloud/docs/private-cloud/data-transfer): How data transfer is billed and how to minimize transfer spend.

## Common use cases

Private Cloud fits organizations with specific infrastructure requirements:

* **Security and compliance**: Finance, healthcare, and regulated industries requiring isolated infrastructure.
* **Private system access**: Connect Laravel Cloud applications directly to internal APIs, services, and private databases.
* **Performance-sensitive workloads**: Predictable performance, unaffected by other customers' workloads.
* **Enterprise architecture**: Laravel Cloud as part of a broader AWS ecosystem.
* **Dedicated IP requirements**: Outbound traffic must originate from known, customer-specific IP addresses.

## Requirements

To provision your Private Cloud, you will need to provide:

* AWS account IDs
* VPC CIDR ranges, to avoid conflicts
* Any required private connectivity details

The typical lead time for provisioning is 48 hours.

## Pricing

Private Cloud pricing is a custom quote based on your organization's requirements. Private Cloud is typically cost-effective for workloads spending \$2,000 or more per month on infrastructure.

Every Private Cloud includes:

* Private networking
* Dedicated infrastructure

## Getting started

To get started with Private Cloud:

1. Schedule a Private Cloud consultation.
2. Review your architecture and security needs with our team.
3. Receive a custom quote.
4. Begin provisioning.

[Contact Sales](https://laravel.com/enterprise) to learn more.
