# Forge - Sites/User-Isolation

*Source: https://forge.laravel.com/docs/sites/user-isolation*

---

## On this page
- [Introduction](#introduction)
- [Sudo access](#sudo-access)
- [Connecting via SFTP](#connecting-via-sftp)
Sites
# User Isolation
Copy page
Learn how to isolate your sites on Laravel Forge.
Copy page
## [​](#introduction) Introduction
By default, Laravel Forge uses the default `forge` user that is created as part of the server’s initial provisioning process for all deployments, daemons, scheduled jobs, PHP-FPM, and other processes.
Via Laravel Forge’s “User Isolation” feature, Forge will create a separate user for a given site. This is particularly useful when combined with a project like WordPress in order to prevent plugins from maliciously accessing content in your `forge` user (or other isolated user) owned directories.
The `forge` user is considered a “super user” and is therefore able to read all files within isolated user directories.
## [​](#sudo-access) Sudo access
Like the `forge` user, newly created isolated users also have limited sudo access. They may reload the PHP-FPM services requiring a password:
```
sudo -S service php8.5-fpm reload
```
If you need further sudo access, you should log in as the `forge` user and switch to the `root` user using the `sudo su` or the `sudo -i` command.
## [​](#connecting-via-sftp) Connecting via SFTP
You can connect to your server via SFTP as the isolated user. We recommend using an SFTP client such as [Transmit](https://panic.com/transmit/) or [Filezilla](https://filezilla-project.org/). However, before getting started, you should first [upload your SSH key to the server](/docs/ssh) for the isolated user.
Was this page helpful?
YesNo
[Network](/docs/sites/network)[Laravel](/docs/sites/laravel)
⌘I