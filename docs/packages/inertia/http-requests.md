Source: https://inertiajs.com/docs/v3/the-basics/http-requests.md

# HTTP Requests

Not every request needs to trigger an Inertia page visit. For calls to an external API or fetching data from a non-Inertia endpoint, the `useHttp` hook provides the same developer experience as `useForm`, but for standalone HTTP requests.

## Basic Usage

The `useHttp` hook accepts initial data and returns reactive state along with methods for making HTTP requests.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { useHttp } from '@inertiajs/vue3'

const http = useHttp({
    query: '',
})

function search() {
    http.get('/api/search', {
        onSuccess: (response) => {
            console.log(response)
        },
    })
}
</script>

<template>
    <input v-model="http.query" @input="search" />
    <div v-if="http.processing">Searching...</div>
</template>
```

```jsx React icon="react" theme={null}
import { useHttp } from '@inertiajs/react'

export default function Search() {
    const { data, setData, get, processing } = useHttp({
        query: '',
    })

    function search(e) {
        setData('query', e.target.value)
        get('/api/search', {
            onSuccess: (response) => {
                console.log(response)
            },
        })
    }

    return (
        <>
            <input value={data.query} onChange={search} />
            {processing && <div>Searching...</div>}
        </>
    )
}
```

```svelte Svelte icon="s" theme={null}
<script>
import { useHttp } from '@inertiajs/svelte'

const http = useHttp({
    query: '',
})

function search() {
    http.get('/api/search', {
        onSuccess: (response) => {
            console.log(response)
        },
    })
}
</script>

<input bind:value={http.query} oninput={search} />
{#if http.processing}
    <div>Searching...</div>
{/if}
```

Unlike router visits, `useHttp` requests do not trigger page navigation or interact with Inertia's page lifecycle. They are plain HTTP requests that return JSON responses.

## Submitting Data

The hook provides `get`, `post`, `put`, `patch`, `delete`, and `query` convenience methods. A generic `submit` method is also available for dynamic HTTP methods.

```js Vue icon="vuejs" theme={null}
http.get(url, options)
http.post(url, options)
http.put(url, options)
http.patch(url, options)
http.delete(url, options)
http.query(url, options)
http.submit(method, url, options)
```

```js React icon="react" theme={null}
const { get, post, put, patch, delete: destroy, query, submit } = useHttp({ ... })

get(url, options)
post(url, options)
put(url, options)
patch(url, options)
destroy(url, options)
query(url, options)
submit(method, url, options)
```

```js Svelte icon="s" theme={null}
http.get(url, options)
http.post(url, options)
http.put(url, options)
http.patch(url, options)
http.delete(url, options)
http.query(url, options)
http.submit(method, url, options)
```

Each method returns a `Promise` that resolves with the parsed JSON response data. TypeScript users may [type the request data and response](https://inertiajs.com/docs/v3/advanced/typescript.md#http-helper).

### Pre-binding the Endpoint

You may pass the HTTP method and URL as the first two arguments to `useHttp()`, then call `submit()` without arguments to dispatch the request. This also unlocks real-time validation. See [Precognition](#precognition) for details.

```js Vue icon="vuejs" theme={null}
const response = await http.post('/api/comments', {
    onError: (errors) => {
        console.log(errors)
    },
})
```

```js React icon="react" theme={null}
const response = await post('/api/comments', {
    onError: (errors) => {
        console.log(errors)
    },
})
```

```js Svelte icon="s" theme={null}
const response = await http.post('/api/comments', {
    onError: (errors) => {
        console.log(errors)
    },
})
```

## Multiple Requests

Each `useHttp` instance tracks its own `processing`, `errors`, and other reactive state. When making independent requests, you may create a separate instance for each one so their states don't collide.

```js Vue icon="vuejs" theme={null}
const search = useHttp({ query: '' })
const upload = useHttp({ file: null })
```

```js React icon="react" theme={null}
const search = useHttp({ query: '' })
const upload = useHttp({ file: null })
```

```js Svelte icon="s" theme={null}
const search = useHttp({ query: '' })
const upload = useHttp({ file: null })
```

## Reactive State

The `useHttp` hook exposes the same reactive properties as `useForm`:

| Property | Type | Description |
| - | - | - |
| `errors` | `object` | Validation errors keyed by field name |
| `hasErrors` | `boolean` | Whether validation errors exist |
| `processing` | `boolean` | Whether a request is in progress |
| `progress` | `object \| null` | Upload progress with `percentage` and `total` |
| `wasSuccessful` | `boolean` | Whether the last request was successful |
| `recentlySuccessful` | `boolean` | `true` for two seconds after a successful request |
| `isDirty` | `boolean` | Whether the data differs from its defaults |

## Validation Errors

When a request returns a `422` status code, the hook automatically parses validation errors and makes them available through the `errors` property.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { useHttp } from '@inertiajs/vue3'

const http = useHttp({
    name: '',
    email: '',
})

function save() {
    http.post('/api/users')
}
</script>

<template>
    <input v-model="http.name" />
    <div v-if="http.errors.name">{{ http.errors.name }}</div>

    <input v-model="http.email" />
    <div v-if="http.errors.email">{{ http.errors.email }}</div>

    <button @click="save" :disabled="http.processing">Save</button>
</template>
```

```jsx React icon="react" theme={null}
import { useHttp } from '@inertiajs/react'

export default function CreateUser() {
    const { data, setData, post, errors, processing } = useHttp({
        name: '',
        email: '',
    })

    function save(e) {
        e.preventDefault()
        post('/api/users')
    }

    return (
        <form onSubmit={save}>
            <input value={data.name} onChange={e => setData('name', e.target.value)} />
            {errors.name && <div>{errors.name}</div>}

            <input value={data.email} onChange={e => setData('email', e.target.value)} />
            {errors.email && <div>{errors.email}</div>}

            <button type="submit" disabled={processing}>Save</button>
        </form>
    )
}
```

```svelte Svelte icon="s" theme={null}
<script>
import { useHttp } from '@inertiajs/svelte'

const http = useHttp({
    name: '',
    email: '',
})

function save() {
    http.post('/api/users')
}
</script>

<input bind:value={http.name} />
{#if http.errors.name}
    <div>{http.errors.name}</div>
{/if}

<input bind:value={http.email} />
{#if http.errors.email}
    <div>{http.errors.email}</div>
{/if}

<button onclick={save} disabled={http.processing}>Save</button>
```

## Displaying All Errors

By default, validation errors are simplified to the first error message for each field. You may chain `withAllErrors()` to receive all error messages as arrays, which is useful for fields with multiple validation rules.

```js Vue icon="vuejs" theme={null}
const http = useHttp({
    name: '',
    email: '',
}).withAllErrors()

// http.errors.name === ['Name is required.', 'Name must be at least 3 characters.']
```

```js React icon="react" theme={null}
const http = useHttp({
    name: '',
    email: '',
}).withAllErrors()

// http.errors.name === ['Name is required.', 'Name must be at least 3 characters.']
```

```js Svelte icon="s" theme={null}
const http = useHttp({
    name: '',
    email: '',
}).withAllErrors()

// http.errors.name === ['Name is required.', 'Name must be at least 3 characters.']
```

The same method is available on the [`useForm`](https://inertiajs.com/docs/v3/the-basics/forms#options-2) helper and the [`<Form>`](https://inertiajs.com/docs/v3/the-basics/forms#options) component.

## File Uploads

When the data includes files, the hook automatically sends the request as `multipart/form-data`. Upload progress is available through the `progress` property.

```vue Vue icon="vuejs" theme={null}
<script setup>
import { useHttp } from '@inertiajs/vue3'

const http = useHttp({
    file: null,
})

function upload() {
    http.post('/api/uploads')
}
</script>

<template>
    <input type="file" @change="http.file = $event.target.files[0]" />
    <progress v-if="http.progress" :value="http.progress.percentage" max="100" />
    <button @click="upload" :disabled="http.processing">Upload</button>
</template>
```

```jsx React icon="react" theme={null}
import { useHttp } from '@inertiajs/react'

export default function Upload() {
    const { setData, post, progress, processing } = useHttp({
        file: null,
    })

    return (
        <>
            <input type="file" onChange={e => setData('file', e.target.files[0])} />
            {progress && <progress value={progress.percentage} max="100" />}
            <button onClick={() => post('/api/uploads')} disabled={processing}>Upload</button>
        </>
    )
}
```

```svelte Svelte icon="s" theme={null}
<script>
import { useHttp } from '@inertiajs/svelte'

const http = useHttp({
    file: null,
})

function upload() {
    http.post('/api/uploads')
}
</script>

<input type="file" onchange={e => http.file = e.target.files[0]} />
{#if http.progress}
    <progress value={http.progress.percentage} max="100" />
{/if}
<button onclick={upload} disabled={http.processing}>Upload</button>
```

## Canceling Requests

You may cancel an in-progress request using the `cancel()` method.

```js Vue icon="vuejs" theme={null}
http.cancel()
```

```js React icon="react" theme={null}
const { cancel } = useHttp({ ... })

cancel()
```

```js Svelte icon="s" theme={null}
http.cancel()
```

## Optimistic Updates

The `useHttp` hook supports [optimistic updates](https://inertiajs.com/docs/v3/the-basics/optimistic-updates.md) via the `optimistic()` method. The callback receives the current data and should return a partial update to apply immediately.

```js Vue icon="vuejs" theme={null}
http.optimistic((data) => ({
    likes: data.likes + 1,
})).post('/api/likes')
```

```js React icon="react" theme={null}
const { optimistic, post } = useHttp({ likes: 0 })

optimistic((data) => ({
    likes: data.likes + 1,
}))
post('/api/likes')
```

```js Svelte icon="s" theme={null}
http.optimistic((data) => ({
    likes: data.likes + 1,
})).post('/api/likes')
```

The update is applied synchronously. If the request fails, the data is rolled back to its previous state.

## Event Callbacks

Each submit method accepts an options object with lifecycle callbacks:

```js theme={null}
http.post('/api/users', {
    onBefore: () => { ... },
    onStart: () => { ... },
    onProgress: (progress) => { ... },
    onSuccess: (data, response) => { ... },
    onError: (errors) => { ... },
    onHttpException: (response) => { ... },
    onNetworkError: (error) => { ... },
    onCancel: () => { ... },
    onFinish: () => { ... },
})
```

You may return `false` from `onBefore` to cancel the request.

### Accessing the HTTP response

The `onSuccess` callback receives the parsed response data as its first argument and the HTTP response object as its second argument. The response object contains `status`, `data`, and `headers` properties, which is useful when you need to inspect the status code or response headers.

```js theme={null}
http.post('/api/users', {
    onSuccess: (data, response) => {
        console.log(response.status) // 200, 201, etc.
    },
})
```

### HTTP exceptions

The `onHttpException` callback fires when the server returns a non-422 HTTP error, such as a `500` or `403`. The callback receives the HTTP response object, giving you access to the status code, response body, and headers.

```js theme={null}
http.post('/api/users', {
    onHttpException: (response) => {
        console.log(response.status) // 500, 403, etc.
        console.log(response.data)   // Response body
    },
})
```

### Network errors

The `onNetworkError` callback fires when the request fails due to a network issue, such as when the user loses their internet connection. The callback receives the `Error` object.

```js theme={null}
http.post('/api/users', {
    onNetworkError: (error) => {
        console.log(error.message)
    },
})
```

## Precognition

The `useHttp` hook supports [Laravel Precognition](https://laravel.com/docs/precognition) for real-time validation. Enable it by chaining `withPrecognition()` with the HTTP method and validation endpoint.

```js Vue icon="vuejs" theme={null}
import { useHttp } from '@inertiajs/vue3'

const http = useHttp({
    name: '',
    email: '',
}).withPrecognition('post', '/api/users')
```

```js React icon="react" theme={null}
import { useHttp } from '@inertiajs/react'

const http = useHttp({
    name: '',
    email: '',
}).withPrecognition('post', '/api/users')
```

```js Svelte icon="s" theme={null}
import { useHttp } from '@inertiajs/svelte'

const http = useHttp({
    name: '',
    email: '',
}).withPrecognition('post', '/api/users')
```

Once enabled, the `validate()`, `touch()`, `touched()`, `valid()`, and `invalid()` methods become available, working identically to [form precognition](https://inertiajs.com/docs/v3/the-basics/forms.md#precognition-1).

## History State

You may persist data and errors in browser history state by providing a remember key as the first argument.

```js Vue icon="vuejs" theme={null}
const http = useHttp('SearchData', {
    query: '',
})
```

```js React icon="react" theme={null}
const http = useHttp('SearchData', {
    query: '',
})
```

```js Svelte icon="s" theme={null}
const http = useHttp('SearchData', {
    query: '',
})
```

You may exclude sensitive fields from being stored in history state using the `dontRemember()` method.

```js theme={null}
const http = useHttp('Login', {
    email: '',
    token: '',
}).dontRemember('token')
```
