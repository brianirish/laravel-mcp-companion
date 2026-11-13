Source: https://laravel.com/cloud/docs/base-images.md

# Base images

System packages and bundled tools available in Laravel Cloud's runtime base images.

Laravel Cloud builds your application on a base image for its [runtime](https://laravel.com/cloud/docs/runtimes). Each image includes the language runtime and system packages used to build dependencies and run your application.

This reference lists packages explicitly installed by Cloud's base image definitions. It also lists bundled tools that aren't installed through the operating system's package manager. It does not list every inherited package or transitive dependency.

> [!NOTE]
>
> Package versions can differ between image releases and existing deployments. For the complete installed package list and exact versions in your deployment, [inspect your environment](#inspect-your-environment).

## PHP

The PHP-FPM and Octane images include PHP, Composer, Node.js, npm, and Yarn Classic. PHP-FPM uses Nginx. Octane uses FrankenPHP with Caddy instead.

Both PHP images include ImageMagick 7, compiled from source, with the `magick` command and compatibility commands such as `convert` and `identify`. They also include Ghostscript and Poppler utilities for document processing.

### Shared PHP packages

The following packages are explicitly installed in both PHP images:

| Purpose | Packages |
| - | - |
| Repository access and certificates | `gnupg`, `curl`, `ca-certificates`, `git`, `openssh-client` |
| Archives | `zip`, `unzip`, `7zip` |
| System tools | `vim-tiny`, `procps`, `dnsutils`, `cron` |
| Native builds | `python3-minimal`, `python-is-python3`, `make`, `g++`, `autoconf` |
| Database clients | `default-mysql-client`, `postgresql-client-18`, `msodbcsql18`, `mssql-tools18`, `libgssapi-krb5-2` |
| Document processing | `ghostscript`, `poppler-utils` |
| Shared libraries | `libbrotli1`, `libgomp1`, `libltdl7`, `libxml2` |
| Image libraries | `libwebp7`, `libjpeg62-turbo`, `libpng16-16`, `libtiff6`, `libfreetype6`, `libfontconfig1`, `liblcms2-2` |
| Additional image formats | `libopenjp2-7`, `libgif7`, `libavif15`, `libheif1`, `libde265-0` |
| HEIF codec plugins | `libheif-plugin-libde265`, `libheif-plugin-x265`, `libheif-plugin-aomdec`, `libheif-plugin-aomenc` |

The HEIF library and its codec plugins come from Debian's Bookworm backports repository. PHP-FPM also explicitly installs `nginx` and `gettext-base`.

The images install additional runtime libraries required by their compiled PHP extensions. Development packages used only to compile PHP extensions or ImageMagick in the image builder are not part of this list. See [PHP extensions](https://laravel.com/cloud/docs/environments#php-extensions) for extension availability.

## Shared packages for other runtimes

The Node.js, Bun, Deno, Go, Python, Ruby, and Rust images explicitly install the following packages. Each runtime's section lists its additional packages and bundled tools.

| Purpose | Packages |
| - | - |
| Repository access and certificates | `gnupg`, `curl`, `ca-certificates`, `git` |
| Archives | `zip`, `unzip` |
| Configuration templates | `gettext-base` |
| Shared libraries | `libbrotli1` |
| Database client | `postgresql-client-18` |
| Web server | `nginx` |

These images include Node.js, npm, and Yarn for frontend asset builds, even when your application's primary language is not JavaScript. In the Go, Python, Ruby, and Rust images, changing the language version does not change the bundled Node.js version.

## Node.js

The Node.js image includes Node.js, npm, Yarn, and pnpm, in addition to the [shared packages](#shared-packages-for-other-runtimes).

| Purpose | Additional packages |
| - | - |
| Native builds | `make`, `g++`, `autoconf`, `python3-minimal`, `python-is-python3` |

The Python packages support native Node.js dependency builds through `node-gyp`.

## Bun

The Bun image includes Bun, Node.js, npm, Yarn, and Deno. It also bundles the `vercel`, `create-hono`, and `create-elysia` command-line tools.

In addition to the [shared packages](#shared-packages-for-other-runtimes), the image explicitly installs `make`, `g++`, and `autoconf`. Cloud does not install Python in this image, so dependencies that build native modules with `node-gyp` may fail.

## Deno

The Deno image includes Deno, Node.js, npm, Yarn, and Bun. It also bundles the `vercel`, `create-hono`, and `create-elysia` command-line tools.

In addition to the [shared packages](#shared-packages-for-other-runtimes), the image explicitly installs `make`, `g++`, and `autoconf`. Cloud does not install Python in this image, so dependencies that build native modules with `node-gyp` may fail.

## Go

The Go image includes the Go toolchain, Node.js, npm, and Yarn Classic, in addition to the [shared packages](#shared-packages-for-other-runtimes).

| Purpose | Additional packages |
| - | - |
| Native builds | `make`, `g++`, `autoconf` |

The image inherits additional build tools from the upstream Go image. Cloud does not add Python to this image, so dependencies that build native modules with `node-gyp` may fail.

## Python

The Python image includes Python, pip, Node.js, npm, and Yarn Classic, in addition to the [shared packages](#shared-packages-for-other-runtimes).

| Purpose | Additional packages |
| - | - |
| Native builds | `make`, `g++`, `autoconf`, `pkg-config` |
| PostgreSQL development headers | `libpq-dev` |
| MySQL development headers | `default-libmysqlclient-dev` |
| Foreign function interface headers | `libffi-dev` |

Cloud installs uv, Poetry with its export plugin, or Pipenv during your application build when the corresponding dependency files require them. These tools are not preinstalled in the base image.

## Ruby

The Ruby image includes Ruby, RubyGems, Bundler, Node.js, npm, Yarn Classic, Bun, Deno, and Corepack. Corepack's package manager shims are not enabled by default. The image also bundles the Spinel Ruby compiler and its `spin` command.

The following packages are installed in addition to the [shared packages](#shared-packages-for-other-runtimes):

| Purpose | Additional packages |
| - | - |
| Native builds | `make`, `g++`, `autoconf`, `pkg-config` |
| Database headers | `libpq-dev`, `libsqlite3-dev`, `default-libmysqlclient-dev` |
| YAML and XML headers | `libyaml-dev`, `libxml2-dev`, `libxslt1-dev` |
| Encryption and network headers | `libssl-dev`, `libcurl4-openssl-dev`, `libgpgme-dev`, `libsodium-dev` |
| Other development headers | `zlib1g-dev`, `libffi-dev`, `libgmp-dev` |
| Compression tools | `bzip2`, `xz-utils` |
| Time zone data | `tzdata` |
| Image processing | `libvips42` |
| Memory allocator | `libjemalloc2` |

The Ruby image includes libvips for Rails image variants. Its dependencies include ImageMagick and Poppler shared libraries, but not their command-line tools. The image does not include FFmpeg, Chromium, or wkhtmltopdf by default. Adding a gem does not install those system tools. See the [Rails image-processing guidance](https://laravel.com/cloud/docs/deploy-guides/ruby#jobs-variants-and-previews) for Active Storage configuration.

## Rust

The Rust image includes `rustc`, Cargo, rustup, Clippy, rustfmt, Node.js, npm, and Yarn Classic, in addition to the [shared packages](#shared-packages-for-other-runtimes).

| Purpose | Additional packages |
| - | - |
| Native builds | `build-essential`, `pkg-config`, `cmake` |
| TLS and compression development headers | `libssl-dev`, `zlib1g-dev` |
| Database development headers | `libpq-dev`, `default-libmysqlclient-dev`, `libsqlite3-dev` |

Clang and libclang are not included by default. Crates that require them need an alternative that works with the installed toolchain. See the [Rust deploy guide](https://laravel.com/cloud/docs/deploy-guides/rust) for build configuration.

## Static sites

Static site generators use their language's image during the build. The final image starts from the Node.js base image and serves the generated files with Nginx. It includes the [Node.js image's packages](#node-js), but does not start a Node.js application server.

Only the generated web root carries over from the build stage. Language tools, application dependencies, and add-ons from the build stage do not carry over to the serving image. Plain HTML sites use the Node.js serving image without a language build step.

## Optional add-ons

FFmpeg, Chromium, and wkhtmltopdf are not default tools in the images described here. An add-on can provide software that your base image does not include.

Available add-ons appear under **General Settings > Build configuration > Add-ons**. Cloud filters this list by your environment's language and organization. Saving an add-on selection requires a redeployment to install it in your application's image.

Your build commands run without root privileges, so they cannot install system packages with `apt-get`. If a required tool is missing and no suitable add-on is available, use an alternative dependency or perform that processing in a separate service.

Add-ons marked **Private Cloud** are available to all Private Cloud organizations. Add-ons marked **On request** require Laravel to grant your organization access. Organizations outside Private Cloud need that access for every add-on, including those marked **Private Cloud**. If an add-on you need does not appear in your environment's settings, [contact support](https://laravel.com/cloud/docs/support) to request access.

### Shared add-ons

The following add-ons support PHP-FPM, Octane, Node.js, Bun, Deno, Go, Python, Ruby, and Rust:

| Add-on | Access |
| - | - |
| Puppeteer | Private Cloud |
| FFmpeg | Private Cloud |
| wkhtmltopdf | Private Cloud |
| MuPDF | On request |
| qpdf | On request |
| LibreOffice | On request |
| c2patool | On request |

The Puppeteer add-on supplies Chromium with browser libraries and fonts. Your application still declares its own Puppeteer package dependency.

### PHP-FPM and Octane

PHP environments also support the following language-specific add-ons:

| Add-on | Access |
| - | - |
| ImageMagick | Private Cloud |
| Kafka | Private Cloud |
| Datadog | On request |
| Oracle DB | On request |
| GnuPG | On request |
| FFI | On request |
| Valkey Glide | On request |

The PHP base images already include the ImageMagick 7 command-line tools. The ImageMagick add-on adds the `imagick` PHP extension so your application can call ImageMagick from PHP code. The PHP Datadog add-on provides the Datadog PHP tracer and trace agent.

### Ruby

Ruby also supports a separate Datadog add-on (`datadog-ruby`). This add-on is available on request.

### Static sites

Plain HTML sites do not support build add-ons. For static site generators, selected add-ons apply only during the language build. They do not carry over to the final serving image.

## Inspect your environment

The exact installed inventory includes inherited packages, resolved dependencies, and any selected add-ons. From your environment's [**Commands** tab](https://laravel.com/cloud/docs/environments#commands), you may list installed operating system packages and their versions:

```sh theme={null}
dpkg-query -W
```

This command lists packages tracked by `dpkg`. It does not list tools copied into the image or compiled from source, such as Composer or the PHP image's ImageMagick installation. Check those tools directly, for example in a PHP environment:

```sh theme={null}
php --version
composer --version
node --version
magick --version
```

Your application's Composer, npm, pip, Bundler, or Cargo dependencies are separate from the base image inventory.
