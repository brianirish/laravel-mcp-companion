# Vapor - Resources/Networks

*Source: https://docs.vapor.build/resources/networks*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#c2b4a3b2adb082aea3b0a3b4a7aeeca1adaf)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationResourcesNetworks[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/vapor)
##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

Resources# Networks

Managing networks within Laravel Vapor.

## [​](#introduction)Introduction

Networks house your databases, caches, jumpboxes, and occasionally applications within AWS. In general, although they are displayed in the Vapor UI for you to review, you are not required to interact with networks directly when using Vapor. When you create a project in a region that does not contain any previous Vapor projects, Vapor automatically begins provisioning a network for you.

### [​](#attaching-a-network-to-an-environment)Attaching A Network To An Environment

Typically, you do not need to manually add a `network` directive to your `vapor.yml` file; however, sometimes you may want to manually specify that a Vapor environment should be placed within a given network. This may be the case when you are accessing private AWS resources, such as ElasticSearch, that are not created through Vapor. To place an environment within a network, add the `network` directive to your `vapor.yml` configuration file:

vapor.ymlCopyAsk AI```
id: 3
name: vapor-app
environments:
    production:
        network: my-network
        build:
            - 'composer install --no-dev'

```

## [​](#custom-ip-range)Custom IP Range

By default, Vapor provisions new networks with an IP address range which is more than sufficient for most projects. However, if you need more control over how your network is configured - such as when you plan to configure your Vapor environment to communicate with pre-existing resources on AWS - you may set your own custom IP range.

When creating the network within the Vapor UI, select “Configure Custom IP Range” to show the Custom IP Range interface.

You must enter an IP range in valid CIDR notation for the overall VPC, along with the public and private subnets. The total number of ranges required for private subnets varies between two and four depending on the number of availability zones for the selected region. IP ranges provided for public and private subnets must fall in the range provided for the overall VPC without overlapping each other.

## [​](#jumpboxes)Jumpboxes

Some Vapor resources, such as private databases or cache clusters, may not be accessed from the public Internet. Instead, they can only be accessed by a machine within their network. This can make it cumbersome to inspect and manipulate these resources during development. To mitigate this inconvenience, Vapor allows you to create jumpboxes. Jumpboxes are very small, SSH accessible servers that are placed within your private network.

You may create a jumpbox via the Vapor UI’s network detail screen or using the `jump` CLI command:

CopyAsk AI```
vapor jump my-jumpbox

```

Once the jumpbox has been created, Vapor will provide you with the private SSH key needed to access the jumpbox. You should connect to the jumpbox via SSH as the `ec2-user` user and the private SSH key.

For practical examples of using jumpboxes to make your serverless life easier, check out the [database](./databases#using-databases) and [cache](./caches#using-caches) documentation.

## [​](#nat-gateways)NAT Gateways

### [​](#what-are-they%3F)What Are They?

If your application interacts with a private database or a cache cluster, your network will require a NAT Gateway. It sounds complicated, but don’t worry, Vapor takes care of the heavy lifting. In summary, when a serverless application needs to interact with one of these resources, AWS requires us to place that application within that region’s network. By default, this network has no access to the outside Internet, meaning any outgoing API calls from your application will fail. Not good.

### [​](#managing-nat-gateways)Managing NAT Gateways

Anytime you deploy an application that lists a private database or cache cluster as an attached resource within its `vapor.yml` file, Vapor will automatically ensure that the network associated with that database / cache contains a NAT Gateway. If it doesn’t, Vapor will automatically begin provisioning one. Unfortunately, AWS bills for NAT Gateways by the hour, resulting in a monthly fee of about $32 / month.

To totally avoid using NAT Gateways, you can use publicly accessible RDS databases (Vapor automatically assigns a long, random password) and a [DynamoDB cache table](./caches#dynamodb-caches), which Vapor automatically creates for each of your projects. You may also manually add or remove NAT Gateways from your networks using the Vapor UI or using the `network:nat` and `network:delete-nat` CLI commands.

## [​](#load-balancers)Load Balancers

By default, Vapor routes HTTP traffic to your serverless applications using AWS API Gateway. When using this service, AWS only bills you based on the amount of requests your application receives. However, at very high scale, API Gateway can become more expensive than your Lambda functions themselves.

As an alternative to API Gateway, you may route traffic to your application using an Application Load Balancer, which provides large cost savings at scale. For example, if an application receives about 1 billion requests per month, using an Application Load Balancer will save about $3,000 on the application’s monthly Amazon bill when compared to an API Gateway REST API and about $1,000 when compared to an API Gateway HTTP API.

### [​](#creating-load-balancers)Creating Load Balancers

You may create load balancers using the Vapor UI or using the `balancer` CLI command. When using the CLI command:

CopyAsk AI```
vapor balancer my-balancer

```

### [​](#using-load-balancers)Using Load Balancers

To attach a load balancer to an environment, add a `balancer` key to the environment’s configuration in your `vapor.yml` file and deploy your application. The value of this key should be the name of the load balancer.

vapor.ymlCopyAsk AI```
id: 3
name: vapor-app
environments:
    production:
        balancer: my-balancer
        build:
            - 'composer install --no-dev'

```

By default, Vapor creates all SSL certificates in the `us-east-1` region, regardless of the region of your project. When your application is using API Gateway, AWS will automatically replicate your certificate to all regions behind the scenes.

However, when using an Application Load Balancer to route traffic to your application, you will need to create a certificate in the region that the project is actually deployed to.

### [​](#deleting-load-balancers)Deleting Load Balancers

Load balancers may be deleted via the Vapor UI or using the `balancer:delete` CLI command:

CopyAsk AI```
vapor balancer:delete my-balancer

```
Was this page helpful?

YesNo[Storage](/resources/storage)[Databases](/resources/databases)On this page
- [Introduction](#introduction)
- [Attaching A Network To An Environment](#attaching-a-network-to-an-environment)
- [Custom IP Range](#custom-ip-range)
- [Jumpboxes](#jumpboxes)
- [NAT Gateways](#nat-gateways)
- [What Are They?](#what-are-they%3F)
- [Managing NAT Gateways](#managing-nat-gateways)
- [Load Balancers](#load-balancers)
- [Creating Load Balancers](#creating-load-balancers)
- [Using Load Balancers](#using-load-balancers)
- [Deleting Load Balancers](#deleting-load-balancers)

[Laravel Vapor home page](https://vapor.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.