Source: https://laravel.com/cloud/docs/knowledge-base/using-yarn-bun-pnpm.md

# Using Yarn, PNPM, or Bun

Learn how to use PNPM, Yarn, or Bun with Laravel Cloud and compare package managers.

Laravel Cloud installs and runs `npm` by default during deployments. If you prefer an alternative JavaScript package manager, such as Yarn, Bun, or PNPM, you can customize your build commands to use it.

For Laravel and Symfony applications, Laravel Cloud doesn't install these tools for you, but you can install them in your build commands. JavaScript applications, such as Next.js, Nuxt, and TanStack Start, can run on the Bun runtime directly. Laravel Cloud detects the Bun runtime automatically when your repository contains a `bun.lock`, `bun.lockb`, or `bunfig.toml` file. See [Runtimes](https://laravel.com/cloud/docs/runtimes#node-js-bun-and-deno) for details.

> [!NOTE]
>
> If you plan to use a different JavaScript package manager with the following examples, remove or comment out the default `npm` commands in your build commands before adding the custom commands.

#### Example: using Bun

If you would like to use Bun instead of npm, you can override the default build command in your environment's settings with the following:

```bash theme={null}
npm install -g bun
bun install
bun run build
```

#### Example: using Yarn

To use Yarn instead of npm:

```bash theme={null}
npm install -g yarn
yarn install
yarn run build
```

#### Example: using PNPM

To use PNPM instead of npm:

```bash theme={null}
npm install -g pnpm
pnpm install
pnpm run build
```

#### Approving PNPM build scripts

PNPM blocks `postinstall` and other build scripts for dependencies it doesn't recognize, so packages with native binaries (for example, `esbuild` or `sharp`) may silently fail to build. Watch for an "Ignored build scripts" warning in your build log.

Since Laravel Cloud's build step is non-interactive, approve these scripts locally first, then commit the resulting configuration so the approval is already in place when Cloud builds your application:

```bash theme={null}
pnpm approve-builds
```

On PNPM 11 and later, the command writes an `allowBuilds` map to `pnpm-workspace.yaml`. On PNPM 9 and 10, it writes an `onlyBuiltDependencies` array to the `pnpm` key in `package.json` instead. Commit the changed file to your repository.

> [!NOTE]
>
> A `.npmrc` with `auto-install-peers` or `node-linker=hoisted` does not approve build scripts and won't fix the problem. Use `pnpm approve-builds` instead.
