# Spatie - Advanced Usage/Encrypt Backup Archives

Source: https://spatie.be/docs/laravel-backup/v10/advanced-usage/encrypt-backup-archives

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Advanced-usage

Encrypt backup archives

Encrypt backup archives
=======================

It's common to encrypt backups before storing them somewhere to prevent unauthorized access.
To do so you can configure this package to use client-side symmetric zip file password encryption before storing the archive somewhere.

By default you only have to define the `BACKUP_ARCHIVE_PASSWORD` environment variable in your `.env` file.

If you want to customize this you can configure the `backup.backup.password` and `backup.backup.encryption` keys in your `config/backup.php` file.

The supported encryption values are: `'none'`, `'default'`, `'aes128'`, `'aes192'`, `'aes256'`. When set to `'default'`, AES-256 will be used if available on your system.

Encryption is applied while the archive is being built by the `\Spatie\Backup\Tasks\Backup\Zip` class.
Encryption only runs when a password is set and the encryption algorithm is not `'none'`.

The `\Spatie\Backup\Listeners\EncryptBackupArchive` listener that previously did this is deprecated and no longer registered. If you registered this listener yourself, remove that registration. Otherwise the archive will be encrypted during the build and rewritten again by the listener.

It's important to try this workflow and also to decrypt a backup archive.
So you know that it works and you have a working backup restore solution.

**Warning:** the default MacOS app to (un)archive ZIPs seems unable to open/extract encrypted ZIP files.
You should use an app like The Unarchiver or BetterZip.

Binary database dumps with PostgreSQL

Isolated mode

Help us improve this page