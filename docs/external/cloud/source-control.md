Source: https://laravel.com/cloud/docs/source-control.md

# Source control

Connect and manage source control providers for your Laravel Cloud applications.

## Introduction

Laravel Cloud deploys your application by connecting to a Git provider. Cloud supports GitHub, GitLab, and Bitbucket. Private Cloud customers can also deploy from a [self-hosted GitLab instance](https://laravel.com/cloud/docs/private-cloud/self-hosted-gitlab).

### Connecting a source control provider

To connect a source control provider, go to **Account settings > Source control**.


Select a provider and go through the OAuth flow to authorize the connection.

For GitHub, you may need to install the Laravel Cloud App on the GitHub account or organization that owns your repositories. The app installation controls which repositories Cloud can access. GitLab and Bitbucket do not require this step.

### Connecting the same Git to multiple Cloud accounts

You can connect the same Git account to more than one Laravel Cloud user.

Each connection is separate. Disconnecting Git from one Cloud account does not disconnect it from the others. To fully remove a Git account connection from Laravel Cloud, disconnect every Cloud user that uses that Git account.

### Disconnecting a source control provider

You can disconnect a provider from **Account settings > Source control**. Click **...** next to the provider and then **Disconnect**.

> [!WARNING]
>
> **Disconnecting a provider affects all applications that rely on that connection, across all organizations under the same Cloud user.** Those applications keep running, but they can't deploy until you or another user with access to the repository reconnects it.

### Refreshing tokens

If your provider token expires or you need to re-authorize access, go to **Account settings > Source control**, click **...** next to the provider, and then **Reauthorize**.

## Troubleshooting

### I can't find my repository


There are two likely reasons we can't find your repository.

#### 1. Your GitHub user doesn't have access to the repository

Laravel Cloud follows GitHub's permissions and displays only the repositories your GitHub user has access to.

To check whether your GitHub user has access to the repository:

1. Go to github.com.
2. Sign in using **the same user you've authenticated on Laravel Cloud**.
3. Search your list of repositories.

If the repository isn't in that list, it won't be available in Laravel Cloud either. You may need to request access from the owner of the repository.

#### 2. The Laravel Cloud app doesn't have the permissions to access the repository

You must grant the Laravel Cloud GitHub app access to the repositories you wish to import.

To check the Laravel Cloud app's permissions:

1. Go to the [Laravel Cloud app installation settings](https://github.com/apps/laravel-cloud-app/installations/select_target) on GitHub.
2. Select your GitHub account.
3. Select **All repositories**, or select your individual repositories.
4. Click **Save**.


If you are using GitLab or Bitbucket, make sure you have access to that repository on the provider's side. Laravel Cloud follows the provider's permissions.

### Missing GitHub installation

If you encounter the "Missing GitHub installation for 'your name', please re-install" error, GitHub failed to send us the confirmation webhook when you installed the Laravel Cloud GitHub application on your GitHub account.


To fix the error:

1. Go to the [Laravel Cloud app installation settings](https://github.com/apps/laravel-cloud-app/installations/select_target) on GitHub.
2. Select your GitHub account.
3. In the **Danger zone** section, click **Uninstall**.
4. Back on Laravel Cloud, go to **Overview > + New application**.
5. Go through the authorization process again.
