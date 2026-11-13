Source: https://herd.laravel.com/docs/windows/changelog/index.md

# Changelog

**2.1.1**

2026-11-06

## Herd Studio, your way

Herd 2.1 lets you set up Herd Studio the way you work, globally and for each site. You find all options in Settings → AI and in each site's inspector.

* **Dev servers per site.** Every site has its own [auto-start](https://herd.laravel.com/docs/windows/herd-studio/dev-server.md) setting for `php artisan dev` and Vite, with a global default. Switching a site to Off stops its running servers right away.
* **Badge per site.** Choose which sites show the Herd Studio badge. If the badge can't load on a site, Herd tells you and lets you hide it right there.
* **One switch for [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md).** Turn Studio with its coding agents, terminals and dev servers on or off at any time, without restarting Herd.
* **[Workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) work independently of Studio**, from the CLI, the MCP server and the inspector.

## Workspaces in the Applications window

* Create a workspace from the inspector with "+" and no prompt
* Workspaces have a context menu with relevant actions

## Fixes and Improvements

* Settings has a new Advanced section with the Herd Server Port and the workspace base
* Browser and Studio buttons on every row of the [Applications](https://herd.laravel.com/docs/windows/getting-started/applications.md) list, Studio in the inspector's quick actions, and search finds a site by its project folder
* New "Free models" setting: turn it off to hide OpenCode's free models from every model picker
* Exceptions no longer go missing in `herd site:error`
* `herd processes` has a new `--all` flag and reports processes started by the dev stack correctly
* Pages no longer lose their Vite dev server when it runs on IPv6
* Fixed a GitHub Copilot login bug
* The Studio badge no longer breaks pages whose scripts include `</body>`
* Failed workspace creates and deletes show what went wrong, with a Retry
* When a workspace folder vanishes, Herd removes its site link
* `herd workspace` follows the "New workspaces start from" setting, and `--remote` overrides it per run
* `herd workspace --json` and `herd workspaces --json` print valid JSON again
* `herd unlink` of a site whose folder is gone now removes its link, config and isolation
* Fixed startup crashes when `devtools-autostart.json` was unreadable or open in another program
* No more error dialog when a page drops its Herd Studio connection before Herd has answered
* Updated the built-in `cacert.pem` bundle

**2.0.3**

2026-10-22

# Herd 2.0 is here!

After months of hard work, we are excited to show you a redesigned and new Herd experience.
This release brings a new applications window, Herd Studio, worktree support, automatic `artisan dev` support, Laravel Cloud support, self-healing, and much more!

## Herd Studio

We're introducing [Herd Studio](https://herd.laravel.com/docs/windows/herd-studio/overview.md)! The easiest way to interact with your agents right from your local sites.
Just click on the "Edit with Herd" badge on any of your sites and jump into an opencode-powered agent chat - with additional context to make sure your agents spend less time guessing.

## Parallel workspaces with separate databases for you and your agents

This one has been requested for quite a while! Herd now automatically detects available git worktrees and makes them available as a subdomain of your site - so every agent can automatically verify its work for you. The `herd` CLI also comes with a range of new commands to make copy-on-write creation of individual [site workspaces](https://herd.laravel.com/docs/windows/sites/workspaces.md) really easy.

## Artisan Dev support

Ever visited a local site only to find out that you still have to start a queue worker, Vite and more?
Those days are over as Herd can [automatically start](https://herd.laravel.com/docs/windows/herd-studio/dev-server.md) `php artisan dev` or `vite` for you when you visit your site locally. Click on the Herd Studio badge to quickly inspect the state of your commands, or jump into a terminal.

## Your applications have a new home

Herd 2.0 gives your [applications](https://herd.laravel.com/docs/windows/getting-started/applications.md) a dedicated window, so you can quickly create a new app, check out your agents' workspaces or deploy your apps.

## Laravel Cloud support

Herd has added [Laravel Cloud](https://herd.laravel.com/docs/windows/integrations/laravel-cloud.md) support - just connect your Cloud account with Herd and you can deploy your applications straight from Herd's UI.

And much more!

## Fixes and Improvements

* Fixed `herd php:update` and the Update button in Settings hanging forever after the download
* `herd php:update` no longer reinstalls a PHP version that is already up to date
* Fixed instances of Herd windows crashing on Windows 11 with Smart App Control turned on
* PHP updates now specify a better error message
* The Update button no longer disappears after a failed PHP update
* `herd php:update` exits with code 1 when the update is declined or fails
* Herd now starts when `config.json` is open in another program, for example Zed. Settings are saved once the file is free again
* Better validation on port fields
* Herd now shows a dialog when Windows can't open a site in the browser, for example when the default browser is no longer installed
* Fixed a blank tray popup after its page failed to load, and the tray popup can no longer be resized
* Fixed the Node settings page loading forever when nvm was locked by another process
* Fixed MCP settings and Herd Studio errors when antivirus software blocks `php.exe` or `git.exe` from starting
* Fixed several crashes in the Dumps window, Applications inspector, licensing page, site previews and agent notifications
* Restored the database shortcut in the site inspector
* Fixed `herd php:install 8.4` asking which version to install instead of installing 8.4
* `herd php:install`, `herd isolate` and `herd init` no longer switch your global PHP version
* Fixed PHP requests to secured `.test` sites over HTTPS failing with "certificate verify failed"
* Updated the bundled CA certificates so Herd and PHP no longer trust the leaked eMudhra intermediates
* Fixed Vite failing to load assets for sites linked through a symbolic link or junction
* The "Let's build something amazing" composer in the Applications window no longer takes up the top of the window permanently; it now opens when you click New or press Ctrl+N, or while you have no applications yet
* List mode in the Applications window now shows every application, not just favorites and recent apps
* The Applications window remembers its size, position and maximized state
* Double-clicking an application now opens the site itself; Open and Enter still go to Herd Studio
* Fixed an issue where dots in new application names were replaced with hyphens, so `console.example` became `console-example.test`
* Fixed framework detection for non-Laravel projects: Symfony, WordPress, Craft, Magento, Drupal and other frameworks are recognized again and show their icon, projects with a `public/` front controller get a driver, and Joomla and Contao drivers were added
* Fixed an issue where a parked folder with a number-only name like `2024` broke the hosts file update and stopped every `.test` site from resolving
* Fixed an issue where a locked file or a WSL folder inside a parked path stopped the hosts file from being updated on launch
* Parked paths that no longer exist are now skipped when writing the hosts file, and `herd park` stores the absolute path
* Fixed the New Application wizard failing when the sites folder is on a drive that is not connected
* Fixed errors on the PHP settings page while a PHP version was still installing or after a failed installation
* PHP installation failures now show the actual error message
* Fixed an error in the Mail window when opening a link to a mail that was deleted
* Fixed a "Could not get blob data" crash while capturing site previews
* Fixed an error reported when quitting Herd while PostgreSQL was still shutting down
* Herd no longer crashes when its internal API port cannot be opened; Settings → General shows the error instead
* Fixed errors when Windows blocked Herd from starting a helper process, for example through a security policy
* Fixed failed update downloads causing errors; the updater now shows a message and lets you retry instead of hanging on "Downloading update"
* Reduced the GPU usage of the animated background behind the empty Insights and Mail windows, which could sit at 90% GPU on integrated graphics
* Fixed an issue where sites without a recognized driver disappeared from the Applications window after updating to 2.0
* Fixed an issue where unlinking, securing or isolating a site failed silently; the Applications window now shows what went wrong
* Fixed the PHP version picker showing the new version even though switching the site's PHP version had failed
* Fixed a stale environment error in the application inspector when switching between sites
* Fixed an issue where a half-installed NVM (for example after a declined UAC prompt) was treated as installed and caused errors on the Node settings page; the Node page now offers to install NVM again
* Fixed errors on the Node settings page when Herd's NVM is not installed
* Fixed an issue where keyboard shortcuts consisting of modifier keys only could be saved and broke shortcut registration on every launch; invalid stored shortcuts are now cleared automatically
* Added support for Delete, Insert and numpad keys in keyboard shortcuts, and Herd now tells you when a key can't be used
* Claude Code is now shown as connected through its CLI in the AI settings, onboarding and What's New
* Fixed a crash when a site preview response was too large; site previews are now capped at 10 MB
* Fixed an issue where site preview snapshots failed when the disk was full

**1.30.0**

2026-08-19

## New features

* Added support for the PHP 8.6 beta
* Added [CPX](https://github.com/laravel/cpx) as a bundled command-line tool
* Service binaries can now be reinstalled from Settings → Services (currently available for PostgreSQL)
* Sites with internationalized domain names are now served correctly
* Added Node.js 24 LTS to the available Node versions

## Fixes and Improvements

* Fixed Herd writing duplicate extension entries in `php.ini`, causing "Module herd is already loaded" warnings
* Newer Expose binaries are no longer overwritten when Herd updates its bundled copy
* Updated the built-in Expose binary
* Updated the built-in Laravel Installer
* Updated the built-in Composer binary
* Updated the built-in `cacert.pem` bundle

**1.29.0**

2026-06-30

## New Features

* The Laravel Forge integration now supports organizations
* Added `herd php:update all` to update every installed PHP version in a single command
* Added a button to copy the mail server's environment variables directly from the Mail window

## Fixes and Improvements

* Migrated the Laravel Forge integration to the v2 API with granular OAuth scopes and automatic token refresh; integrations that need to update the scopes show a Reconnect option
* Fixed the Forge account settings link opening a 404 page
* Fixed a missing separator between multiple To and CC addresses in the mail viewer
* Fixed a mail server crash when a message had no valid Date header, and hardened email processing against errors
* Added the `.mjs` MIME type to the bundled Nginx config
* Improved Craft CMS log viewer detection
* Hardened site information parsing
* Security fixes
* Updated the built-in Forge binary
* Updated the built-in Composer binary
* Updated the built-in Laravel Installer
* Updated the built-in `cacert.pem` bundle

**1.28.0**

2026-03-31

## New features

* The site creation wizard now includes an option to install team support when using a starter kit with authentication
* Added `--update-env` flag to `herd link` that forces updating the `APP_URL` in your `.env` file, even when it already contains the current TLD

**1.27.0**

2026-03-25

## New features

* Added RustFS as a service for S3-compatible local storage
* Site creation wizard includes a "None" option for new Laravel apps without authentication

## Fixes and Improvements

* Fixed an issue where clicking dump links would not open PhpStorm correctly
* Fixed broken "Learn more" documentation links
* Updated the built-in `cacert.pem` bundle
* Updated the built-in Laravel Installer

**1.26.0**

2026-02-18

## New features

* Services can now be cloned directly from the context menu in Settings
* You can now manage services directly from the command line with new `herd services:*` commands: `list`, `create`, `clone`, `delete`, `start`, and `stop`
* Added `herd php:list` and `herd php:update` commands for managing PHP versions via CLI
* Added `herd laravel:update` command to automatically update the Laravel Installer without opening the GUI
* Added Svelte as a starter kit option in the site creation wizard

## Fixes and Improvements

* Fixed an issue where `herd share` didn't respect the `expose.yml` configuration file
* Fixed an issue where installed Node.js versions were not sorted by major version
* Fixed an issue where restarting the internal API server was not possible after changing the port
* Updated the built-in Composer binary
* Updated the built-in Laravel Installer

**1.25.0**

2026-01-19

## New features

* You can now toggle watching for "Dumps" individually
* Added "Laravel Boost" as an option in the site wizard

## Fixes and Improvements

* Running `herd link` (via CLI or GUI) will update your `.env` with the correct app URL
* Fixed an issue with myBB in combination with Herd
* Fixed an issue where running `herd init` would not work with MinIO
* Fixed an issue where installing Reverb would fail on PHP 8.5
* Dump settings are now disabled when general dump interception is paused
* Updated the built-in Expose binary
* Updated the built-in Laravel installer
* Updated the built-in Composer binary
* Updated the built-in `cacert.pem` file

**1.24.0**

2025-11-20

## New features

* Added full support for PHP 8.5

## Fixes and Improvements

* We fixed an issue where a Herd website error could cause your Pro license to become disabled during license verification checks

**1.23.0**

2025-11-04

## Fixes and Improvements

* Updated the Laravel installer and Composer to the latest versions
* Improved the onboarding process for new users
* Fixed deprecation warning that appeared when using Adminer
* Fixed an issue where the query interception would throw an error when no database version could be determined
* Updated MongoDB and Xdebug extension versions

**1.22.3**

2025-09-23

## Fixes and Improvements

* You can now run `herd db` via the CLI to open the current database connection in TablePlus.
* Herd Pro users can now install any available service version, not just the latest one.
* Updated Expose to the latest version
* Update the Laravel installer to the latest version
* Updated Composer to the latest version

**1.22.0**

2025-08-13

## New Features

Herd now ships with an MCP server that gives your AI clients tools and resources to interact with Herd, manage sites, services,
PHP versions and much more.

## Fixes and Improvements

* Fixed a bug where no error was shown when a PHP version could not be installed
* Updated the built-in cacert.pem file

**1.21.0**

2025-07-14

## New features

* You can now start using PHP 8.5 alpha1!
* The Dumps UI can now detect Laravel Cache activity
* Onboarding now allows users to select a different path to park instead of `~/Herd`

## Fixes and Improvements

* Fresh installations can now automatically exclude the Herd path from Windows Defender to improve PHP performance

**1.20.2**

2025-05-27

## Fixes and Improvements

* All network requests now make use of the system-wide proxy settings
* Searching for text within collapsible strings in the dumps window is now possible
* Updated the built-in cacert.pem file

We also skipped 1.20.1 to have consistent versioning across platforms.

**1.20.0**

2025-05-08

## New features

* The "Sites" window is now integrated into the settings and received a major design overhaul
* You can now add "aliases" (links) right from the sites UI, by right-clicking on a site in the list
* Sites with aliases/links now get grouped together
* You can now hide sites that do not have a valid driver
* Sites can be grouped individually
* The PHP ini settings can now be configured for each installed PHP version individually
* New instances of the "Reverb" service now contain a debugging dashboard that can be opened from the services window

## Fixes and Improvements

* Using `herd isolate` with a PHP version that is not yet installed, now installs the specified version
* We fixed an issue with the mailserver in combination with CC email recipients

**1.19.1**

2025-04-17

## Fixes and Improvements

* Fixed an issue where projects would not open with Cursor
* Fixed a log issue with MariaDB and folders containing spaces
* Fixed an issue where the "start at launch" option would be unchecked after installing an update
* Fixed an issue where not all site details were visible on the Sites window

**1.19.0**

2025-04-02

## New features

* You can now manually write the Hosts-file entries in case the Herd helper is not running on your system

## Fixes and Improvements

* Cursor is now added to the list of IDEs
* The site wizard now filters out project paths that no longer exist
* Newly created root certificate authorities are valid for 20 years instead of one
* We now detect when the root certificate authority expires
* We fixed an issue when trying to use MariaDB with a space in the username
* We increased the draggable area for the log viewer window

**1.18.0**

2025-03-11

## New features

* MariaDB is now available as a service to install (requires Herd Pro)
* You can now create a new Laravel project using a community starter kit
* We added support for a new custom URL that allows you to open the site wizard with your custom starter-kit prefilled

## Fixes and Improvements

* Updated the Laravel installer to the latest version
* Updated cacert.pem to the latest version
* We fixed an issue where connecting with Forge would not properly store the oauth token
* Fixed an issue where Xdebug would not properly work out-of-the-box without Herd Pro

**1.17.0**

2025-03-03

## New features

* The site wizard now allows you to choose whether you want to use Volt in combination with the new Livewire starter kit or not
* We added the ability to easily update the Laravel installer from the "PHP" settings

## Fixes and Improvements

* Updated the Laravel installer to the latest version
* Updated Composer to the latest version

**1.16.0**

2025-02-24

## New features

* We updated the site creation wizard to use the new Laravel Vue, React and Livewire starter kits
* We added a global shortcut option to quickly open the site creation wizard
* We added a "Create New Site" option in the menubar to quickly open the site creation wizard
* You can now right-click on your database services to copy the connection URL to your clipboard

## Fixes and Improvements

* Updated the Laravel installer to the latest version
* Updated Expose to the latest version
* Fixed an issue with Expose's `self-update` command

**1.15.0**

2025-02-19

## New features

* We added a new option to create secure Minio services
* This releases includes Expose 3.0 and allows you to configure the default Expose server and custom domain in your Herd settings

## Fixes and Improvements

* Updated composer to the latest version
* PHP 8.4 now includes the updated Redis and MongoDB extensions
* Fixed an error when using the log viewer in combination with PHP 8.4
* We improved the HerdHelper error reporting

**1.14.0**

2025-01-10

## New features

* The default PHP version for new Herd installations is now 8.4

## Fixes and Improvements

* Updated Expose to be PHP 8.4 compatible
* Updated composer to the latest version
* Updated the Laravel installer to the latest version
* When SSHing into a Forge server, you're no longer in the public folder
* UI improvements for the onboarding experience in combination with dark mode
* Fixed an issue when the only installed PHP version was 8.4
* Running herd ini in an isolated project now opens the isolated PHP version's ini file
* Fixed an issue that would show deprecation warnings in the Expose token configuration screen
* The app now notifies you when your Herd Pro license expires soon

**1.13.0**

2024-11-27

## New features

* We added PHP 8.4 compatible versions of Xdebug and our Herd dump interception feature

## Fixes and Improvements

* Updated composer to the latest version
* Added a check so that `composer self-update` will not be overwritten when restarting Herd
* Updated the built-in Laravel Installer

**1.12.0**

2024-11-13

## New Features

* We added a new `herd ini` CLI command that opens up the ini file in your configured IDE.

## Fixes and Improvements

* Improved PHP 8.4 support
* The installer output now properly scrolls to the bottom

**1.11.2**

2024-10-29

## Fixes and Improvements

* Running `herd coverage` now uses the correct php.ini file
* Added PHP 8.4 support for the built-in dump loader
* Opening Adminer for Laravel apps that use the default SQLite file now works properly
* We improved the TablePlus detection when opening it from the sites UI
* `herd init` will no longer add the folder name as a project alias
* Fixed an issue where the `herd_auto_prepend_file` directive would get ignored
* Fixed an issue when trying to intercept HTTP requests without cookies
* Using the dump features in combination with Lumen no longer throws an error
* Updated the Laravel Installer

**1.11.1**

2024-10-01

# Fixes and Improvements

* We added a "Watch via CLI" toggle in the dump settings, so queries no longer get sent to the dump UI when running PHP from the CLI (for example by running tests)
* Changing the maximum upload filesize, also sets post\_max\_size
* We fixed an issue where the Forge integration would show the light mode UI even though dark mode was active
* Updated the Laravel installer
* TablePlus can now be opened from the Sites page
* We fixed an issue where `herd coverage` and `herd debug` would not work as expected in some situations

**1.11.0**

2024-09-19

# New Features

* **Forge Integration:** Connect local sites with Laravel Forge and deploy them from the Herd UI or via CLI
* **Herd.yml:** Share site configurations with your team
* **Reverb TLS support:** Launch secure Reverb instances with effortless TLS certificates
* **Dump Improvements:** Dump Eloquent queries, outgoing HTTP requests, logs, jobs and Blade views without installing a package
* **MongoDB support:** MongoDB can now be installed as a Herd Pro services

# Fixes

* The `herd proxy` command is now fully functional
* The IDE can be started from the sites list again
* When running `herd secure`, you will only need to trust the CA certificate once. Future `herd secure` calls will no longer require your admin password.
* The PHP settings window can now be opened without the need of an internet connection
* We fixed an issue where the Herd installer could restart your computer
* The log viewer no longer shows "No sites found" when PHP 8.4 was installed

**1.10.0**

2024-08-20

## Features

* We’ve added support for PHP 8.4 Alpha to the PHP download manager
* When you open Adminer from a site, we use the database credentials from your `.env` file to populate the form
* If you’re using TablePlus, we open TablePlus instead of Adminer
* You can delete PHP versions via the context menu from the PHP settings
* The configuration for the API port of the Herd app is now under the general settings

## Fixes

* Redis supports spaces in usernames and honors config files
* Herd serves favicons now

**1.9.0**

2024-07-15

## Features

* Herd Pro: Services create and honor configuration files for MySQL, PostgresQL and redis
* Herd Pro: You can open the path of service binaries via right click from the service settings
* You can star a favorite sites within the Sites UI to sort it to the top
* Improved self-healing and logging capabilities for helper service

## Fixes

* Disable binary log files for MySQL service
* Add RTL support
* Fixed the global site menu shortcut

**1.8.0**

2024-06-25

## New Features

* The Sites UI has moved to its own window. You can check a preview of your site as well as update settings, open the database and much more!
* Single mails can now be deleted via the context menu
* Sites can now be deleted
* We integrated Adminer for easier database management
* We added a quick access section to the menu bar as well as the dashboard for Mails, Dumps, Logs and Sites

## Fixes and Updates

* We updated the Laravel Installer
* Fixed an issue where the HerdHelper service could not be installed, when the username contains a space
* You can now configure if Herd should open the Dashboard automatically when it starts
* Fixed crashing log viewer for non-existent directories
* Fixed NVM detection with spaces in paths
* Fixed a bug where sometimes not all services were shutdown correctly
* Fixed some layout bugs in dark mode

**1.7.2**

2024-06-17

# Fixes

* Fixed a problem with the Log Viewer
* Fixed an issue with NVM for users with spaces in their Windows username
* Properly shutting down services when closing or restarting Herd

**1.7.1**

2024-06-14

## Fixes

This update fixes an issue introduced in version 1.7.0 where nested dumps could not be properly clicked when changing the dump order

**1.7.0**

2024-06-14

## New Features

* The Herd dashboard now opens automatically when the app starts
* You can now change the sort order of `dump()` cards in the Dump UI
* Clicking on a dump location now opens your configured IDE
* Dump calls will now be grouped in the UI
* The font-size of dumps can be changed using CTRL +/-
* The log viewer is now framework agnostic and has support for WordPress log files

## Fixes and Updates

* The performance when mass deleting local mails has been improved
* We updated the built-in Composer versions
* We improved the HerdHelper service and added additional debugging information to it

**1.6.1**

2024-05-13

## Versioning

To reduce confusion and make it easier to track updates and fixes accross platforms, the Windows and macOS versions of Herd will now use the same version number. That's why this update is version 1.6.1.

## Fixes and Updates

* We updated the built-in Laravel installer and Composer version
* `herd stop` and `herd start` now properly starts and stops all services
* Fixed an issue where a username with a space would not properly detect the NVM installation
* `herd debug` now loads the regular `php.ini` as well
* We now add appropriate aliases to the `.bash_profile` file to improve using Herd with git bash
* Fixed an edge-case where the "open last folder" shortcut would not properly work
* Clicking on mail notifications now properly brings the Mail window to the front
* We fixed an issue where switching PHP versions would not restart debug PHP processes
* Debug PHP processes no longer get killed after a certain amount of requests
* Long site names and folder names now get truncated to avoid horizontal scrolling in the sites list
* PHP update notifications no longer show up every hour, when postponing the update
* We fixed an issue when trying to make HTTP requests to a locally secured site (cURL error 60)

**1.1.0**

2024-04-17

## New Features

* PostgreSQL 14, 15 and 16 are now available including PostGIS and pgrouting extensions
* We added a local "clear dump" shortcut (CTRL+K) when the "Dumps" window is focused
* You can now use the new `herd coverage` CLI command to start PHP scripts with code coverage enabled
* After installing a new PHP version, you can now use the version individually in the terminal (e.g. `php80 -v`, `php81 -v`, etc.)

## Fixes and Updates

* We updated the built-in Laravel Installer
* We updated the built-in Composer version
* "herd share" now properly passes additional arguments to Expose
* We fixed an issue where "herd unsecure" would not work properly
* A very bad internet connection no longer leads to deactivated Herd Pro licenses
* The Xdebug browser extension detection properly works with trace and profile mode
* Fixed some Laravel Reverb related environment variables
* Fixed an error where dumps would not show up in the "Dumps" window when triggered from NGINX
* Updating PHP no longer overwrites modifications made to the php.ini file
* It's now possible to "herd link" folders with spaces in their names

**1.0.1**

2024-03-28

* Fixed an issue where certain commands would not work on the first application start
* Fixed an issue where Xdebug could not be found for PHP 7.4
* `herd link` now prompts for elevated permissions
* `herd restart` no longer fails
* The `herd` CLI is no longer accessible if the desktop application is not running
* Increased the Dumps payload size
* Fixed an issue with opening the terminal in the last opened site
* The `exif` extension now automatically gets enabled when downloading a new PHP version
* Fixed an issue where PHP would stop after serving a certain amount of requests
* Usernames containing special characters and whitespace are now supported

**1.0.0**

2024-03-26

Initial release
