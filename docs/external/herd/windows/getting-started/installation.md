Source: https://herd.laravel.com/docs/windows/getting-started/installation.md

# Installation

> [card] [Download Herd](https://herd.laravel.com/download/windows)
>
> Download Laravel Herd

> [card] [Purchase Herd Pro](https://herd.laravel.com/checkout)
>
> Purchase a license for Herd Pro

# Why Herd?

Herd is a blazing fast, native Laravel and PHP development environment for Windows.
It provides everything that you need to get started with Laravel development. It ships with PHP, [nginx](https://nginx.org/), and [Node.js](https://nodejs.org/).

You can integrate Herd with [Laravel Cloud](https://cloud.laravel.com) and [Laravel Forge](https://forge.laravel.com) and use a single tool from setting up your application locally to deploying it to production.

With [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md), you can bring the coding agents and AI providers that you already use and build Laravel applications right from your browser.

[Herd Pro](https://herd.laravel.com/windows/#features) completes your development environment with service management for databases, caches, and more. It comes with testing and debugging tools tailored to Laravel, and you'll love them when you're working on web applications every day.

After installing Herd, it routes all requests to `*.test` domains to applications on your local machine, and allows you to use composer, the Laravel installer, and Expose directly in your terminal.

More than 85,000 web developers use Herd every day to create awesome web applications for their users, and [they love it](https://herd.laravel.com/windows/#testimonials).

# Requirements

Herd requires Windows 10 or higher and needs administrator privileges during the setup process.

# Installation

You can download the latest version of Herd [here](https://herd.laravel.com/download/windows).

After downloading the installer, you need to run it with admin permissions so that the installer can add the HerdHelper service that is responsible for updating your hosts file and map directories and linked sites to `.test` domains.

Once Herd is installed, open it to start the onboarding process. The onboarding process downloads the latest PHP and Node.js versions and lets you choose whether Herd launches at login.

During the onboarding, you can [connect an AI provider](https://herd.laravel.com/docs/windows/herd-studio/ai-providers.md) to use Herd Studio. You can skip this step and connect providers later in the settings.

After the installation process is complete, you have a fully-functioning PHP and Laravel development environment. This means you can invoke the `herd`, `php`, `laravel`, and `composer` binaries from your terminal:

```shell theme={null}
herd --version
php --version
laravel --version
composer --version
node --version
```

When you finish the onboarding, Herd opens the [Applications window](https://herd.laravel.com/docs/windows/sites/managing-sites.md), where you can create your first application or link an existing project.


Herd does not alter any services on your system, and if it's not for you, you can easily switch back to your previous setup.

Users from a different setup or beginners can go to the next chapter and [learn how to manage your applications](https://herd.laravel.com/docs/windows/getting-started/applications.md) with Herd.

## Performance

Sometimes the Windows Defender likes to scan Herd folders and decreases your Herd performance. You can create an exclude rule for the Herd config folder for Windows Defender by adding the path `%USERPROFILE%\.config\herd` to it and mitigate this issue.

**1. Open Windows Security**

* Press the **Start** button and search for **"Windows Security"**.
* Alternatively, open it from the system tray in the bottom-right corner.

**2. Go to "Virus & threat protection"**

* In the Windows Security app, click **"Virus & threat protection"**.
* Scroll down and click **"Manage settings"** under the *Virus & threat protection settings* section.

**3. Navigate to Exclusions**

* Scroll down to **"Exclusions"**.
* Click **"Add or remove exclusions"**.

**4. Add a New Folder Exclusion**

* Click **"+ Add an exclusion"** → choose **"Folder"**.
* Enter or browse to the folder:

```
%USERPROFILE%\.config\herd
```

> This typically resolves to something like:
> `C:\Users\YourUsername\.config\herd`

**5. Confirm the Selection**

* Click **"Select Folder"** or confirm the prompt to save the exclusion.

After updating the exclusion, you should notice an improvement in Herd's performance as Windows Defender will no longer scan the specified folder.

# Activating Herd Pro

After purchasing a [Herd Pro](https://herd.laravel.com/checkout) license, open the settings and enter your email address and your license key in the "Herd Pro" tab. The tab also takes you to the settings for Mail and Insights.
