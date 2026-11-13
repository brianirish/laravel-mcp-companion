Source: https://laravel.com/cloud/docs/private-cloud/build-configuration.md

# Build configuration

Install additional software into your application's build image.

## Introduction

Private Cloud customers may install additional software, known as add-ons, into their application's build image beyond Laravel Cloud's supported PHP extensions. Add-ons are useful when your application depends on a PHP extension or other system-level software, such as media processing libraries or monitoring agents, that is not included in the default build image.

> [!NOTE]
>
> Laravel must enable build add-ons for your organization. If you do not see the "Build configuration" section in your environment's settings, [contact support](https://laravel.com/cloud/docs/support) to request access.

## Managing add-ons

You configure add-ons per environment. Laravel determines which add-ons are available to your organization, and the "Add-ons" selector lists them.

**1. Open the environment's settings**

Navigate to **Environment > Settings > General** and find the **Build configuration** section.

**2. Select your add-ons**

Open the "Add-ons" selector and choose the add-ons your application needs. The available options are scoped to your organization.

**3. Save and redeploy**

Save your changes and trigger a new deployment. Like PHP version and extension changes, Laravel Cloud bakes add-ons into a freshly built image, so changes take effect only after you redeploy the environment.

The first deployment that includes a new add-on may take longer than usual while Laravel Cloud builds and caches the updated build image. Subsequent deployments use the cached image.

After the deployment finishes, you may confirm that a PHP extension add-on is loaded by running `php -m` from the environment's **Commands** tab.

## Available add-ons

The following add-ons are available:

* Datadog
* FFmpeg
* Kafka
* Puppeteer
* wkhtmltopdf

> [!NOTE]
>
> Additional add-ons are available on request. [Contact us](https://laravel.com/cloud/docs/support) if your application requires software that is not in this list.

## Configuring Datadog

Once the Datadog add-on is enabled for your environment, you must configure it before your application will send traces to Datadog. You have two options:

* Send traces to a remote Datadog trace agent that you host and manage yourself.
* Run a local Datadog trace agent inside each of your application's instances.

Create the configuration files using your environment's build commands. If you run a local agent, also configure it as a background process. After changing your configuration, redeploy the environment for the changes to take effect.

> [!NOTE]
>
> The local trace agent does not currently work with [managed queues](https://laravel.com/cloud/docs/queues). If your environment uses managed queues, send traces to a remote agent instead.

### Sending traces to a remote agent

Datadog's trace agent may run on infrastructure that you host outside of Laravel Cloud. Laravel Cloud connects to it from stable egress IP addresses, so you may restrict access to the agent using IP allowlists. For Private Cloud environments, use the dedicated egress IP addresses Laravel provided during onboarding, rather than the addresses [documented for Laravel Cloud's public platform](https://laravel.com/cloud/docs/network#ip-addresses).

PHP loads its Datadog configuration when the process starts, so the best place for it is a `php.ini` file. Add the following to your build commands, updating `datadog.trace.agent_url` with the protocol, hostname, and port of your remote agent:

```bash theme={null}
cat > /usr/local/etc/php/conf.d/99-datadog.ini <<'EOF'
datadog.trace.agent_url = https://your-hostname.tld:8126
datadog.trace.agent_connect_timeout = 2000
datadog.trace.agent_timeout = 5000
datadog.service = foo-bar-api
datadog.env = staging
datadog.trace.sample_rate = 1.0
datadog.trace.enabled = On
EOF
```

### Running a local trace agent

Alternatively, you may run the trace agent locally within each application instance. This approach requires three steps: configuring PHP, configuring the trace agent, and running the agent as a background process.

**1. Configure PHP**

Add a `php.ini` file through your build commands, as you would for a remote agent. Point `datadog.trace.agent_url` at `localhost`, or remove the setting entirely to use the default:

```bash theme={null}
cat > /usr/local/etc/php/conf.d/99-datadog.ini <<'EOF'
datadog.trace.agent_url = http://localhost:8126
datadog.trace.agent_connect_timeout = 2000
datadog.trace.agent_timeout = 5000
datadog.service = foo-bar-api
datadog.env = staging
datadog.trace.sample_rate = 1.0
datadog.trace.enabled = On
EOF
```

**2. Configure the trace agent**

Add your Datadog API key to the environment as a custom environment variable or linked secret, such as `DD_API_KEY`. Then update your build commands to write the trace agent's configuration file:

```bash theme={null}
cat > /opt/datadog-agent/etc/datadog.yaml <<'EOF'
log_level: "warn"
remote_configuration:
  enabled: false
EOF

echo "api_key: $DD_API_KEY" >> /opt/datadog-agent/etc/datadog.yaml
```

Adjust the variable name if you used something other than `DD_API_KEY`.

**3. Run the trace agent**

On each App or Worker compute cluster that runs your application, configure a custom background process with the `datadog-trace-agent` command.

### Adding further configuration

You may add any additional Datadog settings to either file: the `99-datadog.ini` file for PHP configuration and the `datadog.yaml` file for the trace agent. To see the PHP options available for the `.ini` file, run `php --info | grep datadog` from the environment's **Commands** tab. To find environment variables that help identify your application within Datadog, run `printenv | grep LARAVEL_CLOUD`.

> [!TIP]
>
> If you would prefer application monitoring built for Laravel without managing agents or external configuration, take a look at [Laravel Nightwatch](https://laravel.com/nightwatch).
