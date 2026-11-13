# Spatie - Monitoring The Health Of All Backups/Creating Your Custom Health Check

Source: https://spatie.be/docs/laravel-backup/v10/monitoring-the-health-of-all-backups/creating-your-custom-health-check

SPATIE

Laravel Backup
==============

spatie.be/open-source

Docs

Laravel-backup

Monitoring-the-health-of-all-backups

Creating your custom health check

Creating your custom health check
=================================

You can create your own custom health check by letting a class extend `Spatie\Backup\Tasks\Monitor\HealthCheck`.

That base class contains one abstract method that you should implement.

```php
public function checkHealth(BackupDestination $backupDestination);
```
If your check determines that the backup is not healthy it should throw a `Spatie\Backup\Exceptions\InvalidHealthCheck` exception. The `HealthCheck` base class contains three helpful methods that helps you do this.

* `fail($message)`: will throw the right exception under the hood.
* `failIf(bool $condition, string $message)`: will throw the right exception if `$condition` is `true`
* `failUnless(bool $condition, string $message)`: will throw the right exception if `$condition` is `false`

You should register your custom health check in the `health_checks` key of the `backup.php` config file.

To see an example of a `HealthCheck`, go read the could of the `MaximumAgeInDays` and `MaximumStorageInMegabytes` health checks that are provided by the package.

Monitoring the health of all backups

Events

Help us improve this page