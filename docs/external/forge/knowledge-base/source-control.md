Source: https://laravel.com/forge/docs/knowledge-base/source-control.md

# Source Control

## Laravel Forge is unable to access Git repository

There are several reasons Laravel Forge may not be able to access your GitHub, GitLab, or Bitbucket repository. First, you should try refreshing the source control API token that is linked to Forge via your account profile's "Source Control" tab.

Laravel Forge attempts to access your repository using your source control provider's API. The API credentials that will be used are the credentials tied to the account of the person who **owns** the Forge server. If a Forge server is shared with you via a team, it will use the team **owner's** API credentials. You should ensure this person has full access to the repository on GitHub.

### GitHub organization repositories

Sometimes, if the repository is an organization repository, you will need to grant Laravel Forge access to that organization. You may do that using the following link: [https://github.com/settings/connections/applications/fdb28071bd05daebc122](https://github.com/settings/connections/applications/fdb28071bd05daebc122)
