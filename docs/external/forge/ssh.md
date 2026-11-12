Source: https://laravel.com/forge/docs/ssh.md

# SSH Keys

> SSH keys are used to authenticate with your server over the SSH protocol.

## Introduction

SSH is a protocol that allows you to securely access your server via a command line terminal.
SSH keys are used to authenticate with your server over the SSH protocol.
If you are new to SSH keys, we recommend checking out the [GitHub documentation of generating SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) to get started.

As part of the provisioning process, Laravel Forge will add all active organization SSH keys to the `forge` account. This will allow you to SSH into the server as the `forge` user.

After adding your SSH key to your server, you may SSH into the server without a password:

```bash theme={null}
ssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS
```

If you have provisioned a custom server that configures a different SSH port, you will need to provide the port in the command.

```bash theme={null}
ssh forge@YOUR_SERVERS_PUBLIC_IP_ADDRESS -p YOUR_SERVERS_SSH_PORT_NUMBER
```

## Managing organization SSH keys

Laravel Forge will automatically add all organization-level SSH keys to any server that is created within the organization.

### Creating organization keys

To create an organization SSH key, navigate to the organization’s dashboard and click Settings. Then, navigate to the Security page, click the Add SSH key button. After providing a key name and the **Public key** click Add key.

### Deleting organization keys

To delete an organization SSH key, navigate to the organization’s dashboard and click Settings. Then, navigate to the Security tab and click the dropdown next to the key you want to delete. Click Delete and confirm that you want to delete the key.

> [!WARNING]
>
> Laravel Forge will not automatically remove organization SSH keys from servers. You must do this manually.

## Managing account SSH keys

Laravel Forge makes it easy to manage SSH keys on your own account, making it easy to quickly add your own keys to servers.

### Creating account keys

To create an account SSH key, navigate to your account dashboard and click the "SSH" tab. Then, click the "Add key" button. After providing a key name and the **Public key**, click "Add key".

### Deleting account keys

To delete an account SSH key, navigate to your account dashboard and click the "SSH" tab. Then, click the dropdown next to the key you want to delete. Click "Delete" and confirm that you want to delete the key.

> [!WARNING]
>
> When deleting an account key, Laravel Forge will also attempt to remove the key from servers.

## Managing server SSH keys

### Creating server keys

To create a server SSH key, navigate to the server and click "Settings". Then, navigate to the "SSH" tab and click the "Add key" button. After providing a key name and the **Public key** click Add key. If your server has any sites configured with website isolation, you will also be able to select the user to add the key to. By default, this will be the `forge` user.

### Deleting server keys

To delete a server SSH key, navigate to the server and click "Settings". Then, navigate to the "SSH" tab and click the dropdown next to the key you want to delete. Click "Delete" and confirm that you want to delete the key.

### Adding account keys

To add your account’s SSH keys, navigate to the server and click "Settings". Then, navigate to the "SSH" tab and click the "Add key" button. Click on the "Add from account" dropdown item, then select the key you want to add to the server and click "Add".

## Server keys

### Server public key

During the provisioning process, Laravel Forge will generate its own keypair so that it may access the server. It will add the public key from this keypair to the `~/.ssh/authorized_keys` file of both the `root` and `forge` users.

### Laravel Forge public key

During the provisioning process, Laravel Forge will generate a public key for the `forge` user. This is used by Git to clone the projects to your server. The key will be added to the source control provider. This key is located at `/home/forge/.ssh/id_rsa.pub`.

> [!WARNING]
>
> When you add the server's SSH key to your source control provider, the server gains access to **all repositories** accessible by your source control account. If the server is compromised, an attacker could potentially access any repository your account can reach. For enhanced security, consider using [deploy keys](#deploy-keys) to limit access to only the specific repositories each site requires.

Alternatively, you may opt out of having this key added to your source control providers by un-checking the **Add server's SSH key to source control providers** option when creating a server. When opting-out, you will need to use site-level [deploy keys](#deploy-keys) in order to grant your server access to specific repositories on a source control provider such as GitHub, GitLab, or Bitbucket.

### Deploy keys

Sometimes you may wish to only grant the Laravel Forge user access to a specific repository. This is typically accomplished by adding an SSH key to that repository's "Deploy Keys" on the repository's GitHub, GitLab, or Bitbucket dashboard.

When adding a new site to the server, you may choose to generate a Deploy Key for that application. Once the key has been generated, you can add it to the repository of your choice via your source control provider's dashboard - allowing the server to clone that specific repository. You may also add, retrieve, or remove a deploy key for an existing site through the API - see [managing a site deploy key via the API](https://forge.laravel.com/docs/sites/repository-access.md#managing-a-site-deploy-key-via-the-api).

> [!TIP]
>
> Deploy keys provide better security isolation than server-level SSH keys. Each deploy key only grants access to a single repository, so if a server is compromised, the attacker can only access the repositories explicitly configured with deploy keys on that server—not your entire source control account.

> [!TIP]
>
> Deploy keys can be used on servers that have their SSH key attached to your source control provider accounts, allowing you to grant the server access to clone a repository that the source control account connected to your Laravel Forge account does not have collaborator access to.
