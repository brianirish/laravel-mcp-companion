# Vapor - Projects/Development

*Source: https://docs.vapor.build/projects/development*

---

- [Laravel Vapor home page](https://vapor.laravel.com)Search...⌘KAsk AI
[Support](/cdn-cgi/l/email-protection#3d4b5c4d524f7d515c4f5c4b5851135e5250)
- [Platform Status](https://status.laravel.com/)
- [Dashboard](https://vapor.laravel.com)
- [Dashboard](https://vapor.laravel.com)

Search...NavigationProjectsDevelopment[Documentation](/introduction)[Knowledge Base](/kb/troubleshooting)- [Community](https://discord.com/invite/laravel)
- [Blog](https://blog.laravel.com/vapor)
##### Get Started

- [Introduction](/introduction)

##### Projects

- [The Basics](/projects/the-basics)
- [Environments](/projects/environments)
- [Deployments](/projects/deployments)
- [Development](/projects/development)
- [Domains](/projects/domains)

##### Resources

- [Queues](/resources/queues)
- [Storage](/resources/storage)
- [Networks](/resources/networks)
- [Databases](/resources/databases)
- [Caches](/resources/caches)
- [Logs](/resources/logs)

##### Integrations

- [Sentry](/integrations/sentry)

##### Other

- [Abuse](/abuse)

Projects# Development

Learn how to develop applications for Laravel Vapor.

## [​](#binary-responses)Binary Responses

To return binary responses, such as PDF downloads, from your Vapor application, your HTTP response should include the `X-Vapor-Base64-Encode` header:

CopyAsk AI```
return $response->withHeaders([
    'X-Vapor-Base64-Encode' => 'True',
]);

```

Lambda limits responses to 6MB. If you need to serve a larger file, consider returning a signed, temporary S3 URL that your user may use to download the file directly from S3.

## [​](#configuring-openssl)Configuring OpenSSL

To use certain OpenSSL functions such as [openssl_pkey_new](https://www.php.net/manual/en/function.openssl-pkey-new.php), you must create an `openssl.cnf` configuration file and instruct Vapor to load it via the `OPENSSL_CONF` environment variable. For example, this environment variable will instruct Vapor to load an `openssl.cnf` file from the root of your project:

CopyAsk AI```
OPENSSL_CONF="/var/task/openssl.cnf"

```

An example `openssl.cnf` file is available below:

CopyAsk AI```
dir = certificates

[ ca ]
default_ca = CA_default

[ CA_default ]
serial = $dir/serial
database = $dir/index.txt
new_certs_dir = $dir/newcerts
certificate  = $dir/cacert.pem
private_key = $dir/private/cakey.pem
default_days = 36500
default_md  = sha256
preserve = no
email_in_dn  = no
nameopt = default_ca
certopt = default_ca
policy = policy_match

[ policy_match ]
commonName = supplied
countryName = optional
stateOrProvinceName = optional
organizationName = optional
organizationalUnitName = optional
emailAddress = optional

[ req ]
default_bits = 2048
default_keyfile = priv.pem
default_md = sha256
distinguished_name = req_distinguished_name
req_extensions = v3_req
encyrpt_key = no

[ req_distinguished_name ]

[ v3_ca ]
basicConstraints = CA:TRUE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer:always

[ v3_req ]
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash

```

## [​](#%E2%80%9Cafter-response%E2%80%9D-jobs)“After Response” Jobs

In typical Laravel applications, you may dispatch jobs that will be executed after the HTTP response is sent to the browser:

CopyAsk AI```
Route::get('/', function () {
    dispatch(function () {
        Mail::to('[[email protected]](/cdn-cgi/l/email-protection)')->send(new WelcomeMessage);
    })->afterResponse();

    return view('home');
});

```

However, we recommend that you always dispatch jobs to your queue workers when using Vapor. Vapor is not able to execute a job after sending a response to the browser; therefore, attempting to do so will cause your application to appear slower to the end user.

## [​](#inertia-ssr)Inertia SSR

Currently, Inertia server-side rendering (SSR) is not available on Vapor environments due to constraints of AWS Lambda. For applications requiring [Inertia with SSR capabilities](https://inertiajs.com/server-side-rendering), we recommend:

- **[Laravel Cloud](https://cloud.laravel.com/docs/compute#inertia-ssr)** - Our fully-managed Laravel application platform.

- **[Laravel Forge](https://forge.laravel.com/docs/sites/applications#inertia-server-side-rendering)** - Our VPS server management platform.

Was this page helpful?

YesNo[Deployments](/projects/deployments)[Domains](/projects/domains)On this page
- [Binary Responses](#binary-responses)
- [Configuring OpenSSL](#configuring-openssl)
- [“After Response” Jobs](#%E2%80%9Cafter-response%E2%80%9D-jobs)
- [Inertia SSR](#inertia-ssr)

[Laravel Vapor home page](https://vapor.laravel.com)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)Platform

[Dashboard](https://vapor.laravel.com/)[Status](https://status.laravel.com/)Legal and Compliance

[Term of Service](https://vapor.laravel.com/terms)[Privacy Policy](https://vapor.laravel.com/privacy)[x](https://x.com/laravelphp)[github](https://github.com/laravel)[discord](https://discord.com/invite/laravel)[linkedin](https://linkedin.com/company/laravel)AssistantResponses are generated using AI and may contain mistakes.