Source: https://herd.laravel.com/docs/windows/guides/coding-agents.md

# Coding Agents

# Working with coding agents

Coding agents write code fast – but they can only be as good as the environment they work in. To build a real Laravel application, an agent needs to run PHP, migrate a database, send an email, read the logs, look at the result in a browser and fix what's broken.

Herd gives your agent all of that on your PC. Every application has a real `.test` domain, services like MySQL and Redis are one command away, and the Herd CLI lets agents read mails, dumps and logs without asking you to copy and paste anything. Herd and a coding agent are a perfect match for working on applications locally.

It doesn't matter which agent you prefer. Herd works with Claude Code, Codex, Cursor, and any other agent that can run commands in your terminal – or you use Herd Studio and start building right in your browser.

## Choose your harness

> [card] [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md)
>
> Chat with an agent right next to a live preview of your site, review its changes and run terminals in your browser.

> [card] [Your own agent](#give-your-agent-access-to-herd)
>
> Use Claude Code, Codex, Cursor or any other agent in your terminal or IDE, and give it access to Herd via the CLI and MCP.

### Herd Studio

[Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md) is the harness that ships with Herd. Enable it in the AI tab of the settings, [connect your AI provider](https://herd.laravel.com/docs/windows/herd-studio/ai-providers.md) and open any `.test` site to start a conversation with an agent. Herd Studio uses the bundled opencode to talk to your provider, so it works with Anthropic, OpenAI, Google, GitHub Copilot, OpenRouter and many more.


No AI subscription yet? Herd Studio comes with [free models via opencode](https://herd.laravel.com/docs/windows/herd-studio/ai-providers.md#free-models), so you can try coding agents with Herd without paying anything.

Agents in Herd Studio know about Herd out of the box. They can read the dumps, queries and logs that your application just produced, reload the preview after a change, and run the [dev server](https://herd.laravel.com/docs/windows/herd-studio/dev-server.md), queue workers and terminals for you. You can even [build a new application from a prompt](https://herd.laravel.com/docs/windows/herd-studio/build-with-ai.md) and run several agents in parallel with [workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md).

### Claude Code, Codex, Cursor and others

If you already have a favorite agent, keep using it. Agents that run commands in your terminal can use the Herd CLI right away, because Herd adds `herd`, `php`, `composer`, `laravel` and `node` to your `PATH`. With the Herd MCP server, your agent gets structured access to your sites, services and PHP versions on top.

## Give your agent access to Herd

### The Herd MCP server

Herd ships with an MCP server that gives agents tools to find and install services, manage PHP versions, secure sites and debug requests. The easiest way to set it up is [Laravel Boost](https://boost.laravel.com), which installs the Herd MCP server for your agents automatically. You can also add it manually – see [AI Integrations](https://herd.laravel.com/docs/windows/advanced-usage/ai-integrations.md) for the configuration of Claude Code, Cursor and other clients.

### The Herd CLI

The [Herd CLI](https://herd.laravel.com/docs/windows/advanced-usage/command-line.md) is the most powerful integration for agents. Every command explains itself via `herd help COMMAND`, and many commands support a `--json` option that returns structured output instead of tables.

| Your agent wants to… | Command |
| - | - |
| Check that everything is running | `herd status` |
| Find the URL, PHP version and services of a site | `herd site:info` |
| Read or change the `.env` file | `herd site:env get APP_URL` |
| See how to connect to the database | `herd db:connection` |
| Create a fresh database for a test | `herd db:use my_app_testing --create` |
| Switch the queue to Redis | `herd site:services queue redis` |
| Catch the email that the app just sent | `herd mail:wait --to=taylor@laravel.com` |
| Click the verification link in that email | `herd mail:links MAIL_ID` |
| Read the queries of the last request | `herd insights:list --type=query` |
| Find N+1 queries, slow queries and errors | `herd insights:analyze` |
| Run a command with the site's PHP version | `herd php artisan migrate` |
| Open the site in the browser | `herd open` |

### Tell your agent about Herd

Agents work best when they know which tools they have. Add a short section to the instructions file of your project – `AGENTS.md`, `CLAUDE.md` or your agent's equivalent – so that your agent reaches for Herd instead of guessing:

```markdown AGENTS.md theme={null}
## Local development with Laravel Herd

This project runs on Laravel Herd. The app is available at its `.test` domain,
run `herd site:info` to get the URL, PHP version and connected services.

- Use `herd php` and `herd composer` so commands use this site's PHP version.
- Use `herd db:connection` to find the database credentials.
- After sending an email, use `herd mail:latest` or `herd mail:wait` to read it
  and `herd mail:links <id>` to get links like verification URLs.
- Use `herd insights:list` to read dump() output, queries and logs of recent requests
  and `herd insights:analyze` to find N+1 queries, slow queries and errors.
- Use `herd status` if something doesn't respond.
- Run `herd list` to see all commands and pass `--json` for structured output.
```

## Workflows that just work

### Test the full sign-up flow

A classic task that agents struggle with: registering a user and verifying the email address. With Herd, your agent submits the form, waits for the email, and follows the link – all from the terminal.

```bash theme={null}
herd mail:wait --to=new-user@example.com --subject="Verify Email Address"
herd mail:links 3f2a9c...
```

`mail:wait` only returns mails that arrive after the command started, so the agent never picks up an old email by accident. Learn more about the [mail server](https://herd.laravel.com/docs/windows/herd-pro-services/mail.md).

### Debug with Insights

When a page is slow or returns the wrong data, your agent can add a `dump()`, reload the page and read what happened – including every executed query – without you copying anything from the browser.

```bash theme={null}
herd insights:list
herd insights:list --type=query
herd insights:watch --json
```

`herd insights:analyze` goes one step further and points your agent to N+1 queries, duplicate and slow queries, errors and slow requests – with the file and line that caused them. Learn more about [Insights](https://herd.laravel.com/docs/windows/debugging/insights.md).

If an error ends up in your log file, open it in the [Log Viewer](https://herd.laravel.com/docs/windows/debugging/logs.md) and click "Fix with AI" to hand the entry with its stack trace directly to an agent in Herd Studio.

### Set up services and databases

Agents can check which database a site uses, create new databases and switch services without touching configuration files by hand. [Herd Pro](https://herd.laravel.com/checkout) users can even install services like MySQL, Redis or Meilisearch from the command line.

```bash theme={null}
herd db:connection
herd db:list
herd services:create redis
herd site:services cache redis
```

If you want every developer – and every agent – on your team to get the same setup, add a [`herd.yml`](https://herd.laravel.com/docs/windows/sites/herd-yaml) file to your repository. `herd init` installs the right PHP version and services in one step.

### Let agents work in parallel

When one agent works on a feature, another one can fix a bug at the same time. [Workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) give each agent its own copy of the application on its own branch and domain – optionally with its own database – so they never overwrite each other's changes.

```bash theme={null}
herd workspace fix-checkout --database=clone
herd workspaces
herd workspace:merge fix-checkout --delete
```

### Share and ship

When your agent builds a webhook integration, run `herd share` to get a public URL via [Expose](https://herd.laravel.com/docs/windows/sites/sharing-sites.md) that services like Stripe can call. Once everything works, deploy the application to production with the [Laravel Cloud integration](https://herd.laravel.com/docs/windows/integrations/laravel-cloud.md).

## Tips

* **Run your agent in the project directory.** Most Herd commands detect the site from the current directory, so your agent doesn't need to pass site names.
* **Keep Herd running.** Commands like `herd status`, `herd site:info`, `herd mail:*` and `herd insights:*` talk to the Herd app.
* **Pass arguments instead of answering prompts.** Some commands ask questions when you omit arguments. Agents usually can't answer interactive prompts, so Herd tells them which argument or option to pass instead.
* **Turn on runtime context.** Run `herd insights:capture on` so that `dump()` calls, queries, logs and jobs end up in Herd, where your agent can read them.
