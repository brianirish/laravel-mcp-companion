Source: https://inertiajs.com/docs/v3/advanced/typescript.md

# TypeScript

Inertia provides first-class TypeScript support. You may configure global types using declaration merging, and pass generics to hooks and router methods for type-safe props, forms, and state management.

## Using pnpm

Due to pnpm's strict dependency isolation, `@inertiajs/core` is not accessible at `node_modules/@inertiajs/core`. Instead, it's nested inside `.pnpm/`, which prevents TypeScript module augmentation from resolving the module.

You may fix this by configuring pnpm to [hoist the package](https://pnpm.io/settings#publichoistpattern). Add the following to your `.npmrc` file and run `pnpm install`.

```ini theme={null}
public-hoist-pattern[]=@inertiajs/core
```

Alternatively, you may add `@inertiajs/core` as a direct dependency in your project.

```bash theme={null}
pnpm add @inertiajs/core
```

## Global Configuration

You may configure Inertia's types globally by augmenting the `InertiaConfig` interface in the `@inertiajs/core` module. This is typically done in a `global.d.ts` file in your project's root or `types` directory.

```ts theme={null}
// global.d.ts
import '@inertiajs/core'

declare module "@inertiajs/core" {
  export interface InertiaConfig {
    sharedPageProps: {
      auth: { user: { id: number; name: string } | null };
      appName: string;
    };
    flashDataType: {
      toast?: { type: "success" | "error"; message: string };
    };
    errorValueType: string[];
    layoutProps: {
      title: string;
      showSidebar: boolean;
    };
    namedLayoutProps: {
      app: { title: string; theme: "light" | "dark" };
      content: { padding: string; maxWidth: string };
    };
  }
}
```

> [!NOTE]
>
> The `import` statement (or `export {}`) is required to make this file a module. Without it, `declare module` replaces the module definition instead of augmenting it. Your `tsconfig.json` also needs to include `.d.ts` files, so make sure a pattern like `"resources/js/**/*.d.ts"` is present in the `include` array.

### Shared Page Props

The `sharedPageProps` option defines the type of data that is [shared](https://inertiajs.com/docs/v3/data-props/shared-data.md) with every page in your application. With this configuration, `page.props.auth` and `page.props.appName` will be properly typed everywhere.

```ts theme={null}
sharedPageProps: {
    auth: { user: { id: number; name: string } | null }
    appName: string
}
```

### Flash Data

The `flashDataType` option defines the type of [flash data](https://inertiajs.com/docs/v3/data-props/flash-data.md) in your application.

```ts theme={null}
flashDataType: {
    toast?: { type: 'success' | 'error'; message: string }
}
```

### Error Values

By default, validation error values are typed as `string`. You may configure TypeScript to expect arrays instead for [multiple errors per field](https://inertiajs.com/docs/v3/the-basics/validation.md#multiple-errors-per-field).

```ts theme={null}
errorValueType: string[]
```

### Layout Props

The `layoutProps` option types the data accepted by `setLayoutProps()`. The `namedLayoutProps` option types the data accepted by `setLayoutProps('name', props)`, keyed by layout name.

```ts theme={null}
layoutProps: {
    title: string
    showSidebar: boolean
}
namedLayoutProps: {
    app: { title: string; theme: 'light' | 'dark' }
    content: { padding: string; maxWidth: string }
}
```

With this configuration, `setLayoutProps({ title: 'Dashboard' })` is type-checked, and `setLayoutProps('app', { theme: 'dark' })` validates both the layout name and its props.

You may also pass a generic type parameter directly to `setLayoutProps` for ad-hoc typing without configuring the global `InertiaConfig` interface.

```ts theme={null}
setLayoutProps<{ custom: string }>({ custom: 'value' })
setLayoutProps<{ collapsed: boolean }>('sidebar', { collapsed: true })
```

> [!NOTE]
>
> The next version of [Laravel
> Wayfinder](https://github.com/laravel/wayfinder/tree/next) may automatically
> generate these types for you by analyzing your Laravel application. It
> generates TypeScript types for shared props, page props, form requests, and
> Eloquent models. This version is currently in beta.

## Page Components

You may type the `import.meta.glob` result for better type safety when resolving page components.

```ts Vue icon="vuejs" theme={null}
import { createInertiaApp } from "@inertiajs/vue3";
import type { DefineComponent } from "vue";

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob<DefineComponent>("./Pages/**/*.vue");
    return pages[`./Pages/${name}.vue`]();
  },
  // ...
});
```

```tsx React icon="react" theme={null}
import { createInertiaApp, type ResolvedComponent } from "@inertiajs/react";

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob<ResolvedComponent>("./Pages/**/*.tsx");
    return pages[`./Pages/${name}.tsx`]();
  },
  // ...
});
```

```ts Svelte icon="s" theme={null}
import { createInertiaApp, type ResolvedComponent } from "@inertiajs/svelte";

createInertiaApp({
  resolve: (name) => {
    const pages = import.meta.glob<ResolvedComponent>("./Pages/**/*.svelte");
    return pages[`./Pages/${name}.svelte`]();
  },
  // ...
});
```

## Page Props

You may type page-specific props by passing a generic to `usePage()`. These are merged with your global `sharedPageProps`, giving you autocomplete and type checking for both shared and page-specific data.

```vue Vue icon="vuejs" theme={null}
<script setup lang="ts">
import { usePage } from "@inertiajs/vue3";

const page = usePage<{
  posts: { id: number; title: string }[];
}>();
</script>
```

```tsx React icon="react" theme={null}
import { usePage } from "@inertiajs/react";

export default function Posts() {
  const page = usePage<{
    posts: { id: number; title: string }[];
  }>();

  return (
    <ul>
      {page.props.posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

```svelte Svelte icon="s" theme={null}
<script lang="ts">
    import { usePage } from '@inertiajs/svelte'

    const page = usePage<{
        posts: { id: number; title: string }[]
    }>()
</script>
```

## Form Helper

The [form helper](https://inertiajs.com/docs/v3/the-basics/forms.md#form-helper) accepts a generic type parameter for type-safe form data and error handling. This provides autocomplete for form fields and errors, and prevents typos in field names.

```vue Vue icon="vuejs" theme={null}
<script setup lang="ts">
import { useForm } from "@inertiajs/vue3";

const form = useForm<{
  name: string;
  email: string;
  company: { name: string };
}>({
  name: "",
  email: "",
  company: { name: "" },
});
</script>
```

```tsx React icon="react" theme={null}
import { useForm } from "@inertiajs/react";

export default function CreateUser() {
  const form = useForm<{
    name: string;
    email: string;
    company: { name: string };
  }>({
    name: "",
    email: "",
    company: { name: "" },
  });

  return null;
}
```

```svelte Svelte icon="s" theme={null}
<script lang="ts">
    import { useForm } from '@inertiajs/svelte'

    const form = useForm<{
        name: string
        email: string
        company: { name: string }
    }>({
        name: '',
        email: '',
        company: { name: '' },
    })
</script>
```

### Nested Data and Arrays

Form types fully support nested objects and arrays. You may access and update nested fields using dot notation, and error keys are automatically typed to match.

```ts theme={null}
import { useForm } from "@inertiajs/react";

const form = useForm<{
  user: { name: string; email: string };
  tags: { id: number; label: string }[];
}>({
  user: { name: "", email: "" },
  tags: [],
});
```

## Form Component

The `<Form>` component accepts a generic type parameter for type-safe slot props. In React, you may pass the generic directly. In Vue and Svelte, you may use the `createForm` helper to create a typed form component.

```tsx React icon="react" theme={null}
import { Form } from "@inertiajs/react";

interface UserForm {
  name: string;
  email: string;
}

export default function CreateUser() {
  return (
    <Form<UserForm> action="/users" method="post">
      {({ errors }) => (
        <>
          <input type="text" name="name" />
          {errors.name && <div>{errors.name}</div>}
          <button type="submit">Create User</button>
        </>
      )}
    </Form>
  );
}
```

```vue Vue icon="vuejs" theme={null}
<script setup lang="ts">
import { createForm } from "@inertiajs/vue3";

interface UserForm {
  name: string;
  email: string;
}

const TypedForm = createForm<UserForm>();
</script>

<template>
  <TypedForm action="/users" method="post" #default="{ errors }">
    <input type="text" name="name" />
    <div v-if="errors.name">{{ errors.name }}</div>
    <button type="submit">Create User</button>
  </TypedForm>
</template>
```

```svelte Svelte icon="s" theme={null}
<script lang="ts">
    import { createForm } from '@inertiajs/svelte'

    interface UserForm {
        name: string
        email: string
    }

    const TypedForm = createForm<UserForm>()
</script>

<TypedForm action="/users" method="post">
    {#snippet children({ errors })}
        <input type="text" name="name" />
        {#if errors.name}<div>{errors.name}</div>{/if}
        <button type="submit">Create User</button>
    {/snippet}
</TypedForm>
```

The generic provides autocomplete and type checking for the `errors` object, `setError`, `clearErrors`, and other slot props that reference form fields.

### useFormContext

The `useFormContext()` function also accepts a generic type parameter, providing type-safe access to the form context from child components.

```tsx React icon="react" theme={null}
import { useFormContext } from "@inertiajs/react";

const form = useFormContext<UserForm>();
```

```vue Vue icon="vuejs" theme={null}
<script setup lang="ts">
import { useFormContext } from "@inertiajs/vue3";

const form = useFormContext<UserForm>();
</script>
```

```svelte Svelte icon="s" theme={null}
<script lang="ts">
    import { useFormContext } from '@inertiajs/svelte'

    const form = useFormContext<UserForm>()
</script>
```

## HTTP Helper

The [`useHttp`](https://inertiajs.com/docs/v3/the-basics/http-requests) hook accepts two generic type parameters: the form data type and an optional default response type.

```ts theme={null}
import { useHttp } from "@inertiajs/react";

interface UserForm {
  name: string;
  email: string;
}

interface UserResponse {
  id: number;
  name: string;
}

const http = useHttp<UserForm, UserResponse>({ name: "", email: "" });
```

## Layout Callbacks

The `LayoutCallback` type provides type safety for [layout callbacks](https://inertiajs.com/docs/v3/the-basics/layouts.md#callback-props). The callback receives the page's props (typed via your global `sharedPageProps` configuration) and should return a valid layout definition.

```tsx React icon="react" theme={null}
import type { LayoutCallback } from "@inertiajs/react";
import Layout from "./Layout";

const Profile = () => <h1>Profile</h1>;

const callback: LayoutCallback = (props) => {
  return [Layout, { title: props.auth.user?.name }];
};

Profile.layout = callback;

export default Profile;
```

```vue Vue icon="vuejs" theme={null}
<script lang="ts">
import Layout from "./Layout.vue";
import type { LayoutCallback } from "@inertiajs/vue3";

const callback: LayoutCallback = (props) => {
  return [Layout, { title: props.auth.user?.name }];
};

export default {
  layout: callback,
};
</script>
```

```svelte Svelte icon="s" theme={null}
<script module lang="ts">
    import Layout from './Layout.svelte'
    import type { LayoutCallback } from '@inertiajs/svelte'

    export const layout: LayoutCallback = (props) => {
        return [Layout, { title: props.auth.user?.name }]
    }
</script>
```

## Remembering State

The `useRemember` hook accepts a generic type parameter for type-safe local state persistence, providing autocomplete and ensuring values match the expected types.

```vue Vue icon="vuejs" theme={null}
<script setup lang="ts">
import { useRemember } from "@inertiajs/vue3";

const filters = useRemember<{
  search: string;
  status: "active" | "inactive" | "all";
}>({
  search: "",
  status: "all",
});
</script>
```

```tsx React icon="react" theme={null}
import { useRemember } from "@inertiajs/react";

export default function Users() {
  const [filters, setFilters] = useRemember<{
    search: string;
    status: "active" | "inactive" | "all";
  }>({
    search: "",
    status: "all",
  });

  return null;
}
```

```svelte Svelte icon="s" theme={null}
<script lang="ts">
    import { useRemember } from '@inertiajs/svelte'

    const filters = useRemember<{
        search: string
        status: 'active' | 'inactive' | 'all'
    }>({
        search: '',
        status: 'all',
    })
</script>
```

## Restoring State

The `router.restore()` method accepts a generic for typing state restored from [history](https://inertiajs.com/docs/v3/data-props/remembering-state.md#manually-saving-state).

```ts theme={null}
import { router } from "@inertiajs/react";

interface TableState {
  sortBy: string;
  sortDesc: boolean;
  page: number;
}

const restored = router.restore<TableState>("table-state");

if (restored) {
  console.log(restored.sortBy);
}
```

## Router Requests

Router methods accept a generic for typing request data, providing type checking for the data being sent.

```ts theme={null}
import { router } from "@inertiajs/react";

interface CreateUserData {
  name: string;
  email: string;
}

router.post<CreateUserData>("/users", {
  name: "John",
  email: "john@example.com",
});
```

## Scoped Flash Data

The `router.flash()` method accepts a generic for typing page or section-specific flash data, separate from the global `flashDataType` configuration.

```ts theme={null}
import { router } from "@inertiajs/react";

router.flash<{ paymentError: string }>({ paymentError: "Card declined" });
```

## Client-Side Visits

The `router.push()` and `router.replace()` methods accept a generic for typing [client-side visit](https://inertiajs.com/docs/v3/the-basics/manual-visits.md#client-side-visits) props.

```ts theme={null}
import { router } from "@inertiajs/react";

interface UserPageProps {
  user: { id: number; name: string };
}

router.push<UserPageProps>({
  component: "Users/Show",
  url: "/users/1",
  props: { user: { id: 1, name: "John" } },
});

router.replace<UserPageProps>({
  props: (current) => ({
    ...current,
    user: { ...current.user, name: "Updated" },
  }),
});
```
