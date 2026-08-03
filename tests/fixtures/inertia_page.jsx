import React from 'react'
import dedent from 'dedent-js'
import { A, Code, H1, H2, Layout, P, Strong } from '@/Components'

const meta = {
  title: 'Routing',
  links: [
    { url: '#top', name: 'Introduction' },
    { url: '#shorthand-routes', name: 'Shorthand routes' },
    { url: '#generating-urls', name: 'Generating URLs' },
  ],
}

const Page = () => {
  return (
    <>
      <H1>Routing</H1>
      <P>
        When using Inertia, all of your application's routes are defined server-side. This means that you don't need
        Vue Router or React Router. Instead, you can simply define Laravel routes and return Inertia responses from
        those routes.
      </P>
      <H2>Shorthand routes</H2>
      <P>
        If you have a page that doesn't need a corresponding controller method, like an FAQ or about page, you can
        route directly to a component via the <Code>Route::inertia()</Code> method.
      </P>
      <pre><code>Route::inertia('/about', 'About');
Route::inertia('/faq', 'Faq');</code></pre>
      <H2>Generating URLs</H2>
      <P>
        Some server-side frameworks allow you to generate URLs from named routes. However, you will not have access to
        those helpers client-side. Here are a couple ways to still use named routes with Inertia.
      </P>
      <ul>
        <li>Generate URLs server-side and include them as props.</li>
        <li>Use a tool like <a href="https://github.com/tighten/ziggy">Ziggy</a> to make named routes available client-side.</li>
      </ul>
      <P>
        The first option is to generate URLs server-side and then pass them to the page as <Strong>props</Strong>.
      </P>
    </>
  )
}

Page.layout = page => <Layout children={page} meta={meta} />

export default Page
