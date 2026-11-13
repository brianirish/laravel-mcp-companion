Source: https://laravel.com/cloud/docs/logs.md

# Logs

Learn how to view, search, and filter Laravel Cloud application, access, and scheduled command logs.

## Introduction

Open the **Logs** tab under **Monitoring** in any environment to view and search your application's logs. You may filter your logs by type:

* **Application logs:** log entries written by your application, either manually or when the application encounters an unhandled exception.
* **Access logs:** log entries that Laravel Cloud generates automatically when your application receives a request.
* **Scheduled command logs:** the output, exit code, and start and finish times of each [Cloud Scheduler](https://laravel.com/cloud/docs/scheduled-tasks#other-stacks) run.

You may filter scheduled command logs to one command or to every scheduled command on an instance.

## Log retention

Laravel Cloud prioritizes your most recent logs. It eventually deletes older logs once they exceed your plan's retention period or storage quota allowance, whichever comes first.

Log retention periods vary by plan. See the [Plans feature table](https://laravel.com/cloud/docs/pricing#plans) for details about log and metrics retention.

## Forwarding logs

To forward an environment's logs to an external destination, configure a log drain. See [Log Drains](https://laravel.com/cloud/docs/services/log-drains/overview) for supported destinations, setup, and billing.
