Source: https://nightwatch.laravel.com/docs/guides/other-providers.md

# Other Providers

> Get started with Nightwatch on other hosting providers

## Installation

Before diving into provider-specific configurations, ensure you have completed the initial setup steps outlined in our [quick start guide](https://nightwatch.laravel.com/docs/start-guide.md).

If you're looking for an easier way to deploy Nightwatch, consider using [Laravel Cloud](https://nightwatch.laravel.com/docs/guides/cloud.md) or [Laravel Forge](https://nightwatch.laravel.com/docs/guides/forge.md), which offer streamlined setup processes.

## Linux servers

The instructions below are tailored for Ubuntu systems. If you're running a different Linux distribution, you may need to adjust the commands accordingly.

After installing the Nightwatch package via Composer, add your environment variables to your application's `.env` file:

```bash theme={null}
NIGHTWATCH_TOKEN=your-api-key
NIGHTWATCH_REQUEST_SAMPLE_RATE=0.1
NIGHTWATCH_COMMAND_SAMPLE_RATE=1.0
NIGHTWATCH_EXCEPTION_SAMPLE_RATE=1.0
```

> [!NOTE]
>
> Important: If you add or modify the `NIGHTWATCH_TOKEN` after starting the
> service, you will need to restart the service for the changes to take effect.

### Running as a systemd service

For production deployments, we recommend running the Nightwatch agent as a systemd service since systemd is installed by default on every Ubuntu system. This ensures the agent starts automatically on boot and restarts if it ever crashes.

First, create a new service file:

```bash theme={null}
sudo nano /etc/systemd/system/nightwatch-agent.service
```

Then, add the following configuration:

```ini theme={null}
[Unit]
Description=Laravel Nightwatch Agent
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/your-app
ExecStart=/usr/bin/php artisan nightwatch:agent
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Finally, enable and start the service:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl enable nightwatch-agent
sudo systemctl start nightwatch-agent
```

You can check the service status at any time:

```bash theme={null}
sudo systemctl status nightwatch-agent
```

### Using Supervisor

If you prefer Supervisor over systemd, follow these steps to set it up:

```bash theme={null}
sudo apt install supervisor
```

Create a configuration file:

```bash theme={null}
sudo nano /etc/supervisor/conf.d/nightwatch-agent.conf
```

Add the configuration:

```ini theme={null}
[program:nightwatch-agent]
process_name=%(program_name)s
command=php /var/www/your-app/artisan nightwatch:agent
directory=/var/www/your-app
autostart=true
autorestart=true
user=www-data
numprocs=1
redirect_stderr=true
stdout_logfile=/var/log/supervisor/nightwatch-agent.log
```

Update Supervisor and start the process:

```bash theme={null}
sudo supervisorctl reread
sudo supervisorctl update
```

## Monitoring

### Health checks

The Nightwatch agent includes a built-in status command:

```bash theme={null}
php artisan nightwatch:status
```

This command exits with a non-zero status code if there are any connectivity issues, making it ideal for monitoring scripts.
