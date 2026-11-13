Source: https://nightwatch.laravel.com/docs/guides/docker.md

# Docker

> Get started with Nightwatch in containerized environments

## Overview

Containerized environments using Docker, Kubernetes, and other container orchestration tools are increasingly popular for deploying Laravel applications. While there are too many variations to cover every possible scenario, the principles of running the Nightwatch Agent on these platforms remain consistent.

This guide will demonstrate how to configure the Nightwatch package and agent in some common scenarios, and give some more general advice to adapt to your specific setup.

## Prerequisites

First, follow the regular steps in our [quick start guide](https://nightwatch.laravel.com/docs/start-guide.md) to begin.

## Recommended configuration

As outlined above, there are many possible variables and considerations when deploying Nightwatch alongside your containerized Laravel application. In most scenarios, however, the following approach will be the simplest and most effective.

**Step 1**

Choose the version of the official Nightwatch Agent container image which
corresponds to your Laravel Nightwatch package version (e.g.
`laravelphp/nightwatch-agent:v1`).

**Step 2**

Configure the Nightwatch Agent container to run as a sidecar alongside your
Laravel application container.

**Step 3**

Ensure that both the Laravel application and Nightwatch Agent container have
the `NIGHTWATCH_TOKEN` environment variable set to the same value.

> [!TIP]
>
> For examples of what this looks like in practice, see the
> [Examples](#examples) section below.

> [!NOTE]
>
> If you have concerns with how this approach fits your specific setup, or for
> more information, please read the sections below.

## Architecture

### Managing the Nightwatch agent service

There are three common patterns for running supporting services in containerized environments, all of which are supported by Nightwatch. You may be familiar with these from running services like Horizon, Reverb, etc, alongside your Laravel application, however there are some small differences in the nature of the Nightwatch Agent which make some setups more suitable than others.

#### Sidecar container (recommended)

Running the Nightwatch Agent alongside each Laravel application container in the same pod offers several benefits:

* Fast, secure communication between the application and agent
* Simplified handling of container lifecycle, scaling and versioning
* Flexibility and control over agent process lifecycle
* Minimal configuration

#### Background process

Some users prefer to run a single container per pod. While this is possible with the Nightwatch Agent it is not our recommended approach for a few reasons:

* Extra configuration required (supervisord, etc)
* Less control over process lifecycle/resource management in most scenarios
* Reduced visibility of process health in some scenarios

#### Agent service

It is also possible to run a set of agent containers as a separate service. While this may be suitable for some setups, in most cases the sidecar container approach is simpler and more performant. Reasons you might choose this approach include:

* Running an agent service for a Laravel application deployed outside of your containerized environment (e.g. to support Vapor or another serverless deployment type)
* Greater control over agent scaling and resource allocation in very large deployments (10s or 100s of containers)

> [!TIP]
>
> The Sidecar Container approach will be the best fit for most applications. We
> recommend using this pattern unless you understand the reasons for using
> another configuration.

### Choosing a Nightwatch agent container

There are also several ways of obtaining a suitable Nightwatch Agent container image:

#### Official agent container image (recommended)

The simplest approach for most people will be to use the Official Nightwatch Agent container image, which is available at [laravelphp/nightwatch-agent](https://hub.docker.com/r/laravelphp/nightwatch-agent) on Docker Hub. This is a lightweight image built specifically for running the Nightwatch Agent and includes all necessary dependencies.

#### Build from the agent Dockerfile

If you would like to build the image yourself, you can do so using `docker build -f vendor/laravel/nightwatch/agent/Dockerfile -t nightwatch-agent:latest vendor/laravel/nightwatch/agent` from your application directory. You can then push this image to your own container registry if needed.

#### Application container image

Since the Nightwatch Agent is included in the Laravel Nightwatch package, you can also run the agent from your existing Laravel application container, by using an alternate command or entrypoint which runs `php artisan nightwatch:agent` with the correct configuration (as applicable to your particular container build).

> [!TIP]
>
> When using the Official Nightwatch Agent container image, we recommend
> specifying a major version (e.g. `laravelphp/nightwatch-agent:v1`) to ensure
> compatibility with your Laravel Nightwatch package version, while still
> receiving the latest security updates and agent features.

> [!NOTE]
>
> You may also specify a minor or even patch version (e.g.
> `laravelphp/nightwatch-agent:v1.11`, or `laravelphp/nightwatch-agent:v1.11.5`)
> or even use the `latest` tag if desired, however any breaking changes to
> agent/package compatibility will always be accompanied by a major version
> increment.

### Requirements for all configurations

When using Nightwatch in a containerized environment, it is important to understand the necessary conditions for correct and secure operation:

* **Valid token set**: both your Laravel application, and the Nightwatch Agent must be configured with a valid (and matching) Nightwatch environment token, by default this can be done by providing the correct value in the `NIGHTWATCH_TOKEN` environment variable.
* **Minimum package version**: the `laravel/nightwatch` package in your application must be at least version `v1.11.0` to work with the Nightwatch Agent container.
* **Network communication between application and agent**: your Laravel app will need to be able to communicate with the agent over a TCP connection on the correct port (default is `2407`). In the Sidecar Container and Background Process scenarios no configuration should be needed, however other scenarios may need adjustments to firewall or load balancer configuration.
* **Ingest/Listen Configuration**: the Nightwatch package and Agent will need correct ingest/listen configuration. In the Sidecar Container and Background Process scenarios this should work without any change to configuration defaults, however in the Agent Service scenario you will need to set the `NIGHTWATCH_INGEST_URI` environment variable to the address of the agent service (e.g. `nightwatch-agent:2407`) on your application container, and a valid listen address/port combination on the agent container (e.g. `0.0.0.0:2407`).
* **Security of the Nightwatch Agent**: while the Nightwatch Agent service will validate and discard any payload which does not include a matching `NIGHTWATCH_TOKEN` hash, this is not designed to be an authentication mechanism, and as such the Nightwatch Agent should **only** be accessible from your application container, and not the public internet.

## Examples

> [!NOTE]
>
> The examples below contain the configuration for the app container and agent container. The app container configuration is a partial example, and actual configuration will vary depending on your environment.

### Local development using Docker Compose

```yaml theme={null}
version: "3.8"

services:
  app:
    # ...
    environment:
      - NIGHTWATCH_TOKEN=<your Nightwatch environment token>
      - NIGHTWATCH_INGEST_URI=nightwatch-agent:2407
    # ...
    networks:
      - sail

  nightwatch-agent:
    image: laravelphp/nightwatch-agent:latest
    environment:
      - NIGHTWATCH_TOKEN=<your Nightwatch environment token>
    healthcheck:
      test: php nightwatch-status
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 5s
    restart: unless-stopped
    networks:
      - sail
  
  # If you have separate containers for queue workers or schedulers, you would need to add the same environment variables.
  scheduler:
    # ...
    environment:
      - NIGHTWATCH_TOKEN=<your Nightwatch environment token>
      - NIGHTWATCH_INGEST_URI=nightwatch-agent:2407
    # ...
    networks:
      - sail
  
  worker:
    # ...
    environment:
      - NIGHTWATCH_TOKEN=<your Nightwatch environment token>
      - NIGHTWATCH_INGEST_URI=nightwatch-agent:2407
    # ...
    networks:
      - sail

networks:
  sail:
    driver: bridge
```

### Amazon ECS task definition with Terraform

> [!NOTE]
>
> This example shows how you can run the application container and agent container in the same task definition.
> If you have separate task definitions for queue workers, schedulers, or other services, you would need to add the agent container to each task definition to ensure all application components can send data to Nightwatch.

```yaml theme={null}
resource "aws_ecs_task_definition" "laravel-app" {
  # ...

  container_definitions = jsonencode([
    {
      name = "app"
      # ...

      environment = [
        {
          name = "NIGHTWATCH_REQUEST_SAMPLE_RATE"
          value = "0.1"
        },
        {
          name = "NIGHTWATCH_COMMAND_SAMPLE_RATE"
          value = "1.0"
        },
        {
          name = "NIGHTWATCH_EXCEPTION_SAMPLE_RATE"
          value = "1.0"
        },
      ]

      secrets = [
        {
          name = "NIGHTWATCH_TOKEN"
          valueFrom = "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/NIGHTWATCH_TOKEN"
        }
      ]
    },

    # If you have a separate task definition for queue workers or schedulers, you would need to add the same environment variables to that task definition as well.

    {
      name      = nightwatch-agent
      image     = "laravelphp/nightwatch-agent:v1"
      healthCheck = {
        command  = ["CMD-SHELL", "php nightwatch-status"]
        interval = 30
        retries  = 3
        timeout  = 5
      }
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.nightwatch_agent_log_group.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
      secrets = [
        {
          name = "NIGHTWATCH_TOKEN"
          valueFrom = "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/NIGHTWATCH_TOKEN"
        }
      ]
    },
  ])
}
```

### Deployment on Kubernetes (using application container image for Nightwatch agent)

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: laravel-app
  namespace: default
  labels:
    component: laravel-app
spec:
  replicas: 2
  strategy:
    type: Recreate
  selector:
    matchLabels:
      component: laravel-app
  template:
    metadata:
      name: laravel-app
      namespace: default
      labels:
        component: laravel-app
    spec:
      containers:
        - name: app
          image: myregistry/laravel-app:latest
          imagePullPolicy: Always
          env:
            - name: NIGHTWATCH_TOKEN
              secretKeyRef:
                name: nightwatch-token-secret
                key: production-token
            - name: NIGHTWATCH_REQUEST_SAMPLE_RATE
              value: "0.1"
            - name: NIGHTWATCH_COMMAND_SAMPLE_RATE
              value: "1.0"
            - name: NIGHTWATCH_EXCEPTION_SAMPLE_RATE
              value: "1.0"
          # ...
        - name: nightwatch-agent
          image: myregistry/laravel-app:latest
          imagePullPolicy: Always
          command: ["php", "artisan", "nightwatch:agent"]
          env:
            - name: NIGHTWATCH_TOKEN
              secretKeyRef:
                name: nightwatch-token-secret
                key: production-token
          livenessProbe:
            exec:
              command: ["php", "artisan", "nightwatch:status"]
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 30
            timeoutSeconds: 5
```
