Source: https://herd.laravel.com/docs/windows/troubleshooting/composer.md

# Composer SSL problems

# SSL certificate problem: unable to get local issuer certificate

This is a common problem when using Avast antivirus and others but sometimes also happens with some `cURL` versions.

## Solving problems with cURL

You can check if your CA bundle is up to date by running `composer diagnose -vvv`. Look for `Checked CA file ...` or
`Checked directory ...` and you'll see where Composer is looking for your CA bundle. You can get a new Certificate
from [cURL](https://curl.se/docs/caextract.html) if this
is a problem.

## Mitigating antivirus issues

If using a different CA bundle doesn't help, you can try disabling antivirus and firewall to see if that helps.

There are verified issues with Avast and others and they block Composer – there's nothing that we can do with Herd to
solve this problem, but you can disable HTTPS scanning in your antivirus software.

### Avast

In Avast, please go to
"Protection > Core Shields > Web Shield > **uncheck** Enable HTTPS scanning" and that should help.

### Norton

In Norton, please go to "Security > Advanced > Safe Web > Settings" and **disable** HTTPS scanning and QUIC/HTTP3 scanning.

If changing the settings in your antivirus software does help, please report
this to your antivirus vendor so that they can implement a fix and allow enabling these protections again.

You can read more about this at the [official Composer docs](https://getcomposer.org/doc/articles/troubleshooting.md#ssl-certificate-problem-unable-to-get-local-issuer-certificate).
