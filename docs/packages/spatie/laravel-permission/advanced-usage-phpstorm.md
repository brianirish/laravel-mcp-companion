# Spatie - Advanced Usage/Phpstorm

Source: https://spatie.be/docs/laravel-permission/v8/advanced-usage/phpstorm

SPATIE

Laravel Permission
==================

spatie.be/open-source

Docs

Laravel-permission

Advanced-usage

PhpStorm Interaction

PhpStorm Interaction
====================

### On this page

1. Extending PhpStorm

##Extending PhpStorm
--------------------

> **Note**
> When using Laravel Idea plugin all directives are automatically added.

You may wish to extend PhpStorm to support Blade Directives of this package.

1. In PhpStorm, open Preferences, and navigate to **Languages and Frameworks -> PHP -> Blade**
   (File | Settings | Languages & Frameworks | PHP | Blade)
2. Uncheck "Use default settings", then click on the `Directives` tab.
3. Add the following new directives for the laravel-permission package:

**role**

* has parameter = YES
* Prefix: `<?php if(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasRole', {`
* Suffix: `})): ?>`

--

**elserole**

* has parameter = YES
* Prefix: `<?php elseif(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasRole', {`
* Suffix: `})): ?>`

**endrole**

* has parameter = NO
* Prefix: blank
* Suffix: blank

--

**hasrole**

* has parameter = YES
* Prefix: `<?php if(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasRole', {`
* Suffix: `})): ?>`

--

**endhasrole**

* has parameter = NO
* Prefix: blank
* Suffix: blank

--

**hasanyrole**

* has parameter = YES
* Prefix: `<?php if(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasAnyRole', {`
* Suffix: `})): ?>`

--

**endhasanyrole**

* has parameter = NO
* Prefix: blank
* Suffix: blank

--

**hasallroles**

* has parameter = YES
* Prefix: `<?php if(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasAllRoles', {`
* Suffix: `})): ?>`

--

**endhasallroles**

* has parameter = NO
* Prefix: blank
* Suffix: blank

--

**unlessrole**

* has parameter = YES
* Prefix: `<?php if(! \\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasRole', {`
* Suffix: `})): ?>`

--

**endunlessrole**

* has parameter = NO
* Prefix: blank
* Suffix: blank

--

**hasexactroles**

* has parameter = YES
* Prefix: `<?php if(\\Spatie\\Permission\\PermissionServiceProvider::bladeMethodWrapper('hasExactRoles', {`
* Suffix: `})): ?>`

--

**endhasexactroles**

* has parameter = NO
* Prefix: blank
* Suffix: blank

UUID/ULID

Other

Help us improve this page