Source: https://herd.laravel.com/docs/windows/herd-studio/ai-providers.md

# AI Providers

# Connecting AI Providers

Herd Studio doesn't come with its own AI subscription. Instead, you bring the AI provider that you already use. Herd ships with [opencode](https://opencode.ai) and uses it to talk to all AI providers, so you connect your provider once and every agent in Herd Studio can use its models.

> [!TIP]
>
> You don't need an AI subscription to get started. Herd ships with [opencode](https://opencode.ai), which offers free models that are available in Herd Studio right away – no account, no API key and no credit card required.

## Connecting a provider

You can connect providers in the AI tab of the Herd settings under "AI Providers", or during the onboarding.


Herd highlights the most popular providers:

* **Anthropic**: Claude models with an Anthropic API key.
* **OpenAI**: GPT models.
* **OpenCode**: curated models including Claude, GPT, Gemini and more.
* **GitHub Copilot**: models from your GitHub Copilot subscription.
* **Google**: Gemini models.
* **OpenRouter**: route requests across many model providers.

Click "Show all providers" to search the full catalogue of providers that opencode supports.

Depending on the provider, you connect either by signing in via your browser or by entering an API key. Some browser sign-ins finish automatically, others show a code that you paste back into Herd. Once connected, the provider shows its available models and a button to disconnect it.

> [!NOTE]
>
> If you already use opencode on your PC, Herd imports its provider sign-ins the first time Herd Studio starts. After that, Herd manages its providers separately, so connecting or disconnecting a provider in Herd doesn't change your own opencode installation.

## Using your Claude subscription

If you use [Claude Code](https://claude.com/product/claude-code) with a Claude Pro or Max plan, you can use this plan in Herd Studio as well. Herd detects the Claude Code installation on your PC and shows it as a separate "Claude Code" provider with all models of your plan – next to the "Anthropic" provider, which uses an API key.

Herd uses the [opencode-claude](https://github.com/openchamber/opencode-claude) plugin for this. It sends every request through the official Claude Agent SDK and the `claude` CLI on your machine, so Claude Code handles the communication with Anthropic and your sign-in stays with Claude Code. Herd never reads or stores your Claude credentials, and the usage counts towards the limits of your plan.

If Claude Code is not signed in yet, run `claude auth login` in your terminal. The Claude Code provider only works with a Claude plan. If your Claude Code uses an API key, connect the Anthropic provider with this key instead.

## Free models

opencode provides a selection of free models that are always available in Herd Studio, even if you didn't connect any provider. They are a great way to try Herd Studio and to build small features without paying for AI. Select one of the free opencode models in the model picker and start building.

When you need more powerful models, connect one of the providers above.

## Choosing a model

You select the model for an agent in Herd Studio or in the prompt field when you [build with AI](https://herd.laravel.com/docs/windows/herd-studio/build-with-ai.md). Herd remembers your last choice and uses it as default in the app and in Herd Studio.

For models that support it, you can also choose an effort level. Higher effort levels let the agent think longer before it answers, which helps with complex tasks but takes more time.
