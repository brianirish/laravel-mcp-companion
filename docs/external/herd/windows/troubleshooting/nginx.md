Source: https://herd.laravel.com/docs/windows/troubleshooting/nginx.md

# Nginx Troubleshooting

## Nginx does not start

The most common problem why Nginx does not start is that different applications such as the IIS web server or Apache are
already using port 80 or 443 on your machine.

You can check that with the following terminal commands:

```ps1 theme={null}
netstat -aon | findstr :80
netstat -aon | findstr :443
```

These command should display an output that looks similar to this:

```ps1 theme={null}
  TCP    127.0.0.1:80           0.0.0.0:0              LISTENING       9920
  TCP    127.0.0.1:80           0.0.0.0:0              LISTENING       8752
  TCP    127.0.0.1:80           0.0.0.0:0              LISTENING       10064
  TCP    127.0.0.1:80           0.0.0.0:0              LISTENING       10228
```

If there are other applications using these ports and it's not pointing to 127.0.0.1, you can identify them by looking up the PID (the last number in the
output) in the Task Manager.
