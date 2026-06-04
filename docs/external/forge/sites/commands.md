# Forge - Sites/Commands

*Source: https://forge.laravel.com/docs/sites/commands*

---

## On this page
- [Introduction](#introduction)
- [Running commands](#running-commands)
  - [Command history](#command-history)
- [Commands vs. recipes](#commands-vs-recipes)
Sites
# Commands
Copy page
Learn how to run arbitrary commands from the Commands panel.
Copy page
## [​](#introduction) Introduction
You may execute arbitrary Bash commands from the “Commands” panel. Commands are executed from within the site’s root directory, e.g., `/home/forge/site.com`. If you need to run commands within another directory you may prefix the command with a `cd` operation:
```
cd bin && ./run-command.sh
```
## [​](#running-commands) Running commands
Commands can be executed from the site’s “Commands” panel.
Sites that were created with the “General PHP / Laravel” project type will automatically suggest common Laravel Artisan commands.
Commands are not executed within a TTY, which means that input / passwords cannot be provided. Additionally, commands cannot exceed 5 minutes of execution time.
### [​](#command-history) Command history
- The user who initiated the command. This is particularly helpful when using Laravel Forge within [teams](/docs/teams)
- The command that was executed
- The date and time of execution
- The status of the command
## [​](#commands-vs-recipes) Commands vs. recipes
While [recipes](/docs/recipes) also allow you to run arbitrary Bash scripts on your servers, commands on a site differ in a few, but important ways:
- Recipes run at a server level. In other words, they cannot dynamically change into a site’s directory unless you already know the directory ahead of time
- Recipes can run using the `root` user. Commands only run as the site’s user, which in most cases will be `forge` unless the site is “isolated”
- Recipes are better equipped for running larger Bash scripts. Commands focus on running short commands, such as `php artisan config:cache`
- Recipes use the server’s configured PHP CLI version. Commands use the PHP version configured for the site they are run on.
Was this page helpful?
YesNo
[Environment Variables](/docs/sites/environment-variables)[Queues](/docs/sites/queues)
⌘I