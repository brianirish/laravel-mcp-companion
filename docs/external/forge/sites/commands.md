Source: https://laravel.com/forge/docs/sites/commands.md

# Commands

> Learn how to run arbitrary commands from the Commands panel.

## Introduction

You may execute arbitrary Bash commands from the "Commands" panel. Commands are executed from within the site's root directory, e.g., `/home/forge/site.com`. If you need to run commands within another directory you may prefix the command with a `cd` operation:

```bash theme={null}
cd bin && ./run-command.sh
```

## Running commands

Commands can be executed from the site's "Commands" panel.

Sites that were created with the "General PHP / Laravel" project type will automatically suggest common Laravel Artisan commands.

> [!NOTE]
>
> Commands are not executed within a TTY (Teletypewriter), which means that input / passwords cannot be provided. Additionally, commands cannot exceed 5 minutes of execution time.

### Command history

* The user who initiated the command. This is particularly helpful when using Laravel Forge within [teams](https://forge.laravel.com/docs/teams.md)
* The command that was executed
* The date and time of execution
* The status of the command

## Commands vs. recipes

While [recipes](https://forge.laravel.com/docs/recipes.md) also allow you to run arbitrary Bash scripts on your servers, commands on a site differ in a few, but important ways:

* Recipes run at a server level. In other words, they cannot dynamically change into a site's directory unless you already know the directory ahead of time
* Recipes can run using the `root` user. Commands only run as the site's user, which in most cases will be `forge` unless the site is "isolated"
* Recipes are better equipped for running larger Bash scripts. Commands focus on running short commands, such as `php artisan config:cache`
* Recipes use the server's configured PHP CLI version. Commands use the PHP version configured for the site they are run on.
