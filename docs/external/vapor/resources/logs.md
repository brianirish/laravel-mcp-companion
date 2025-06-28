# Vapor - Resources/Logs

*Source: https://docs.vapor.build/resources/logs*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#403621302f32002c21322136252c6e232f2d)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationResourcesLogs[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
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

Resources# Logs

Viewing and managing logs within Laravel Vapor.

## [​](#introduction)Introduction

As you may know, Laravel provides support for a variety of logging services. By default, when using Vapor, your application will use the AWS CloudWatch service when logging messages.

## [​](#viewing-logs)Viewing Logs

The Vapor dashboard provides the most convenient way to view and search your application’s logs. By utilizing Vapor’s powerful search and filter tools, you can easily access and analyze all of your application’s logs that are stored on AWS CloudWatch.

Vapor allows you to search for specific logs or exceptions, and apply filters based on function type, log level, and the log’s time period. Once you locate the relevant log entry, you can click it to view additional information associated with the entry, such as its context or exception details.

Alternatively, you may view logs directly in AWS CloudWatch. To do so, navigate to the AWS console’s “Lambda” dashboard. Then, locate the Lambda for your project (vapor--). Then, you may click the “View logs in CloudWatch” link within the Lambda’s “Monitoring” tab.

Remember, even if you configure a different logging service for your application logs, the AWS CloudWatch service and Vapor UI will display your infrastructure logs as well. Infrastructure logs may include logs regarding AWS Lambda timeouts, etc.

Was this page helpful?

YesNo[Caches](/resources/caches)[Sentry](/integrations/sentry)On this page
- [Introduction](#introduction)
- [Viewing Logs](#viewing-logs)

[Laravel Vapor home page](https://vapor.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.