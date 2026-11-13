Source: https://herd.laravel.com/docs/macos/herd-studio/build-with-ai.md

# Build with AI

# Build with AI

Herd lets you go from an idea to a running Laravel application with a single prompt. Describe what you want to build, pick a starter kit and a model, and Herd creates the application and hands it to a coding agent that builds your idea in the background.

Before you start, [connect an AI provider](https://herd.laravel.com/docs/macos/herd-studio/ai-providers.md) or pick one of the free opencode models that ship with Herd.

## Creating a new application from a prompt

You can open the new application window in several ways:

* Select "New Application" from the Herd menu bar icon.
* Press the global "Create New Site" shortcut that you can set up in the [shortcut settings](https://herd.laravel.com/docs/macos/advanced-usage/shortcuts.md).
* Press `⌘N` or click the plus button in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md).
* Use the prompt field at the top of the Applications dashboard.

Describe your application in the prompt field, choose a name for it and select a starter kit: No Starter Kit, React, Vue, Svelte or Livewire. Herd shows whether the `.test` domain for your name is still available. Pick a model and click "Build" or press `⌘↩`.


Herd creates a new Laravel application in your default Herd directory and starts an agent that builds your idea. While the agent is working, you can close the window. Once the application is ready, click "Open Studio" to follow the agent's progress and continue working on the application in [Herd Studio](https://herd.laravel.com/docs/macos/herd-studio/overview.md).

If you leave the prompt empty, Herd creates a fresh application without an agent. Click "Advanced" to configure every option of the Laravel installer yourself, or "Link Existing App" to add an existing project to Herd. See [Applications](https://herd.laravel.com/docs/macos/getting-started/applications.md#via-the-gui) for more details.

## Changing an existing application

To ask an agent to change an existing application, select the application in the [Applications window](https://herd.laravel.com/docs/macos/sites/managing-sites.md). The inspector on the right side contains a "Build with AI" field. Describe the change or feature, pick a model, and send the prompt. Herd starts a new agent conversation for this site that you can follow in Herd Studio.


If an agent is already working on the site and the site is a git repository, you can check "Run in a new workspace". Herd then creates an isolated copy of the site on its own branch and domain so that both agents can work in parallel. Learn more about this in [Workspaces](https://herd.laravel.com/docs/macos/sites/workspaces.md).

## Fixing errors from your logs

The [Log Viewer](https://herd.laravel.com/docs/macos/debugging/logs.md) has a "Fix with AI" action for every log entry. Herd sends the entry with its stack trace and context to an agent, asks it to find the root cause in your codebase and fix it, and opens Herd Studio for the site.

## Dictation

On macOS 26 or later, you can dictate your prompts instead of typing them. Click the microphone button next to the prompt field in the new application window or in Herd Studio and start speaking.

Dictation runs completely on your Mac using Apple's speech recognition. Your audio never leaves your Mac. The first time you use dictation, macOS asks for permission to use the microphone and speech recognition, and downloads the speech model for your language.

You can select the dictation language in the AI tab of the settings. By default, Herd uses your system language.

> [!NOTE]
>
> If you denied microphone access, you can enable it in System Settings → Privacy & Security → Microphone.
