# Vapor - Introduction#Permissions

*Source: https://docs.vapor.build/introduction#permissions*

---

Manage your Laravel infrastructure on Vapor and fall in love with the scalability and simplicity of serverless.

[

Create your Vapor account today

Watch the free Vapor series on Laracasts

Copy

Copy

To save keystrokes when interacting with per-project installations of the Vapor CLI, you may add a shell alias to your operating system that aliases the `vapor` command to `php vendor/bin/vapor`.

Copy

Copy

Copy

Sandbox projects may not utilize API Gateway versions, load balancers, firewalls, or custom domains. To utilize these features, you will need to choose a subscription plan.

Copy

Copy

Since Vapor manages many types of resources across more than a dozen AWS services, it may be convenient to create a role with the `AdministratorAccess` policy. If desired, you may create a separate AWS account to house this role and contain all of your Vapor resources.

Copy

Copy

It’s probable this list of permissions will change as we add new features to Vapor, which may result in unexpected errors if your policy is not kept up to date.

For additional information, refer to the following AWS documentation:

- Requesting a quota increase](https://vapor.laravel.com/register) in the *Service Quotas User Guide*.

- [AWS Service Quotas reference](https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html).