# Vapor - Projects/The-Basics

*Source: https://docs.vapor.build/projects/the-basics*

---

[Migrating from Vapor to Cloud? See how Pyle did it (Webinar)](https://lrvl.co/vapor-cloud)
[Laravel Vapor home page](https://vapor.laravel.com)
Search...
⌘KAsk AI
- [email protected]
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)
Search...
Navigation
Projects
The Basics
[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)
- [Blog](https://blog.laravel.com)
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
On this page
- [Creating Projects](#creating-projects)
- [Projects & Teams](#projects-%26-teams)
- [Project Settings](#project-settings)
- [GitHub Repository](#github-repository)
- [Deleting Projects](#deleting-projects)
Projects
# The Basics
Get started with Laravel Vapor.
## [​](#creating-projects) Creating Projects
Vapor projects are created via the Vapor UI or the `vapor init` CLI command.
We recommend using the Vapor UI if you wish to start a fresh Laravel project on Vapor. This option’s fully integrated with GitHub, and once you connect your GitHub account, Vapor automatically creates a new GitHub repository (with a fresh installation of Laravel), makes the first deployment, and sets up automatic deployments on code pushes.
Or, if you need to deploy an existing project to Laravel Vapor, you may use the `vapor init` CLI command. This command should be executed within the root directory of the Laravel project you wish to deploy. The `init` command will prompt you to select the AWS account that the project should be associated with, as well as the AWS region that it should be deployed to.
Copy
Ask AI
```
vapor init
```
The `init` command will generate a `vapor.yml` file within the root of your project. This is the primary configuration file for your Vapor project and contains things like build steps, deployment hooks, linked databases / caches, and other project settings. Each time you deploy, Vapor reads this configuration file and deploys your project appropriately.
When creating a project in a region that you have not created previous projects in, Vapor will automatically begin building a “network” (AWS VPC) in that region. This network may take several minutes to finish provisioning. You can review its status in the “Networks” tab of the Vapor UI.
### [​](#projects-&-teams) Projects & Teams
Before creating a project via the Vapor CLI, ensure your current team is the team you intend to create the project for. You may view your current team using the `team:current` command. You may switch your active team using the `team:switch` command.
Copy
Ask AI
```
vapor team:switch
```
You may view your current team’s project list via the Vapor UI or the `vapor project:list` CLI command:
Copy
Ask AI
```
vapor project:list
```
## [​](#project-settings) Project Settings
### [​](#github-repository) GitHub Repository
Within Vapor’s “Project Settings” screen, you may provide the GitHub repository information for a project. Providing this information simply allows Vapor to provide links to GitHub for each deployment’s commit hash. You are not required to provide repository information for Vapor to function.
## [​](#deleting-projects) Deleting Projects
You may delete a project using the Vapor UI or the `project:delete` CLI command. The `project:delete` command should be run from the root directory of your project. This command will delete the project in Vapor as well as the AWS Lambda function and AWS API Gateway definition. Any custom resources defined for the project, such as S3 buckets, will not be deleted by Vapor in case they are being used by other projects. If you wish to delete them, you may do so manually from the AWS management console.
Was this page helpful?
YesNo
[Introduction](/introduction)[Environments](/projects/environments)
⌘I
[Laravel Vapor home page](https://vapor.laravel.com)
Platform
[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)
Legal and Compliance
[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)