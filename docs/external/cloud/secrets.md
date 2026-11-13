Source: https://laravel.com/cloud/docs/secrets.md

# Secrets

Manage encrypted secrets across environments.

## Introduction

Laravel Cloud's Secrets Manager lets you define encrypted secrets at the organization level and link them to one or more environments. Secrets are useful for values that several environments share, such as third-party API tokens, GitHub tokens, Cloudflare credentials, or other sensitive configuration.

Unlike custom environment variables, secrets are managed centrally. When a shared value changes, you update it once rather than copying it into each environment individually.

Laravel Cloud injects secrets into your application as environment variables during deployment.

## Creating secrets

To create a secret, navigate to your organization's dashboard and click **Settings > Secrets**. Then, click **New secret**.

Each secret has a key, value, and optional notes. Secret keys must start with a letter or underscore and may contain only letters, numbers, and underscores. For example:

```dotenv theme={null}
GITHUB_TOKEN=ghp_example
CLOUDFLARE_API_TOKEN=example-token
AWS_ACCESS_KEY_ID=example-key
```

Secret keys may contain up to 255 characters, values up to 7,500 characters, and notes up to 500 characters.

You may create multiple secrets at once by clicking **Add another**. Creating several at once is useful for a group of related credentials, such as AWS or Cloudflare credentials.

When creating a secret, you may select the environments that should use it. You can also link secrets to environments later from either the organization settings page or the environment's general settings.

> [!NOTE]
>
> Secret keys do not need to be unique. For example, you may create a separate `STRIPE_SECRET` for each of your applications, using the notes field to distinguish them. However, an environment can't link two secrets with the same key.

## Managing secrets

To edit a secret, navigate to **Settings > Secrets** and select the secret from the list. You may update its value, notes, or linked environments.

> [!NOTE]
>
> Secret values are write once, read never. When editing a secret, Laravel Cloud does not show the existing value. To rotate a secret, enter a new value and save your changes.

Deleting a secret permanently removes it from the organization and from any environments where it is linked.

## Linking secrets to environments

A secret affects an environment only after you link it. To link secrets from an environment, open the environment's general settings, scroll to the injected variables section, and click **Link secrets**.

From the link secrets dialog, you may select one or more organization secrets to attach to the environment. Environments have a hard limit of 30 linked secrets.

### Preview environments

To give [preview environments](https://laravel.com/cloud/docs/preview-environments) access to secrets, link them to the automation that creates the previews using the automation's **Linked secrets** field. Each preview environment the automation creates starts with those secrets already linked.

When you replicate an environment, Laravel Cloud copies its linked secrets to the new environment.

### Deploying changes

Laravel Cloud decrypts and injects secrets during deployment. After creating, updating, linking, unlinking, or deleting a secret, redeploy each affected environment for the change to take effect. When you link or unlink secrets, Laravel Cloud stages the change on the environment, and you can deploy it from the staged changes banner.

If you start a deployment while your environment's resources are still being created, Laravel Cloud queues it. A queued deployment uses the secret values from when you started it.

> [!WARNING]
>
> Each deployment keeps the secret values it was deployed with. If you roll back to an earlier deployment, your environment uses the secret values from that deployment, even if you have rotated a secret since. Redeploy your environment to use the current values.

### Variable precedence

Laravel Cloud merges secrets into the environment variables generated for a deployment. If a custom environment variable and a linked secret use the same key, the custom environment variable takes priority. Both custom environment variables and linked secrets take priority over Laravel Cloud's automatically injected variables.

This order lets you use shared secrets for common configuration and still override a value in a specific environment when needed.

## Security

Your browser encrypts each secret value with your organization's public key before sending it, so the plaintext value never travels over the network. Each organization has its own key pair, and Laravel Cloud protects organization key material with AWS Key Management Service (KMS).

Laravel Cloud stores the encrypted value and decrypts it only when needed: to confirm that a new value was encrypted, and when deploying an environment that uses the secret. Laravel Cloud also masks the values of linked secrets in your deployment logs.

## Permissions

Access to Secrets Manager depends on your organization role and permissions. Creating, editing, and deleting secrets are organization-level permissions. Linking secrets to an environment requires a dedicated environment-level permission.

For more information about organization access, see [Role-based access control](https://laravel.com/cloud/docs/rbac).

## Managing secrets with the CLI and API

You can manage secrets with the [Cloud CLI](https://laravel.com/cloud/docs/api/cli#secrets) using the `secret:list`, `secret:create`, `secret:update`, and `secret:delete` commands. To manage the secrets linked to an environment, use the `environment-secret:list`, `environment-secret:attach`, and `environment-secret:detach` commands. The CLI encrypts values on your machine before sending them to Laravel Cloud.

The Laravel Cloud API and MCP server also support managing secrets. Both only accept encrypted values. To encrypt a value, fetch your organization's public key, seal the value with a libsodium sealed box (`crypto_box_seal`), and send the base64-encoded result.
