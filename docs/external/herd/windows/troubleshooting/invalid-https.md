Source: https://herd.laravel.com/docs/windows/troubleshooting/invalid-https.md

# Certificate Date issues (HTTPS)

# Resolving Issues with HTTPS Connections

## NET::ERR\_CERT\_DATE\_INVALID

Herd creates a self-signed root certificate when you secure your first site locally. Unfortunately, this root certificate
expires after one year and if you are reading this help article, this likely just happened on your machine. You
can fix this by deleting the expired certificate, it's at:

```
C:\Users\{USERNAME}\.config\herd\config\valet\CA
```

After deleting this file, you need to secure your sites again by either running `herd unsecure` and `herd secure` in their
folders or go to "Sites > Select a Site > Uncheck HTTPS > Check HTTPS".

We're working on a solution to automatically renew the certificate in the future, but for now, you need to do this manually.
