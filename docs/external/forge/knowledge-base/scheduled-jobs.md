Source: https://laravel.com/forge/docs/knowledge-base/scheduled-jobs.md

# Cookbook

> Common issues and solutions for Laravel Forge.

## Scheduled jobs not running

It's important to be aware that one single misconfigured scheduled job will break **all jobs** in the scheduler. You should verify that your frequency and commands are correct using a tool such as [Crontab.guru](https://crontab.guru).
