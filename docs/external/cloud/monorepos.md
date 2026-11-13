Source: https://laravel.com/cloud/docs/monorepos.md

# Monorepos

Deploy applications from a monorepo on Laravel Cloud.

## Introduction

Laravel Cloud includes first-class monorepo support. When you create a new application, Cloud analyzes your repository and detects whether it contains one application or several.

### How it works

If Cloud does not detect a monorepo structure, you proceed through the standard application creation flow without any additional steps.

If Cloud detects a monorepo, it lists the top-level directories in your repository so you can select the one that contains your application. Cloud uses that directory as the root for all build and runtime operations such as commands and background processes.

All directories in your repository are available during the build, so your application can reference shared packages or sibling directories. Cloud deploys only the selected application directory. Because of that, Cloud scopes all commands and processes to that directory at runtime.

### Deploying multiple applications from the same monorepo

If your monorepo contains more than one application, such as a frontend and a backend, you'll need to create a separate application in Laravel Cloud for each one. Attach the same repository to each application, then select a different root directory during setup so Cloud knows which part of the repository to deploy.

Each application you create is a fully independent Cloud resource with its own environment variables, instances, scaling settings, domains, and attached services, even though they share a single repository. Because Cloud is framework-aware, it may expose different configuration options depending on each application's runtime.

Because you deploy each application separately, you can size and scale each one independently. A frontend and a backend often have very different traffic patterns and resource needs. Keeping them as separate applications lets you size, scale, and deploy each one according to its own demands instead of treating them as a single unit.
