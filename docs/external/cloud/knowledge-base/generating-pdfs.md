Source: https://laravel.com/cloud/docs/knowledge-base/generating-pdfs.md

# Generating PDFs

Learn how to generate PDFs with Laravel in Laravel Cloud.

> [!NOTE]
>
> This guide is for Laravel applications.

You may generate PDFs in Laravel Cloud with [Cloudflare's Browser Rendering API](https://developers.cloudflare.com/browser-rendering/rest-api/pdf-endpoint/#convert-custom-html-to-pdf). To get started, generate a Cloudflare API token that has the `Account.Browser Rendering` permission and locate your Account ID from your Cloudflare dashboard URL.

## Using Laravel PDF

[Spatie's Laravel PDF](https://spatie.be/docs/laravel-pdf) package provides a convenient wrapper around Cloudflare's Browser Rendering API through its built-in Cloudflare driver. Your instances don't need Node.js or a Chrome binary.

First, install the package with Composer:

```bash theme={null}
composer require spatie/laravel-pdf
```

Then, add the following environment variables to your Cloud environment's environment variable settings:

```dotenv theme={null}
LARAVEL_PDF_DRIVER=cloudflare
CLOUDFLARE_API_TOKEN=your-api-token
CLOUDFLARE_ACCOUNT_ID=your-account-id
```

Once you configure these variables, you may generate PDFs using the `Pdf` facade. For example, the following controller method renders a view as a PDF and streams it as a download to the browser:

```php theme={null}
use Spatie\LaravelPdf\Facades\Pdf;

public function download()
{
    return Pdf::view('pdfs.invoice', ['invoice' => $invoice])
        ->format('a4')
        ->download('invoice.pdf');
}
```

For more information on available options such as custom paper sizes, margins, headers, and footers, see the [Laravel PDF documentation](https://spatie.be/docs/laravel-pdf).

## Using Laravel Cashier with Laravel PDF

Cashier's default invoice PDF renderer uses Dompdf, which does not work in Laravel Cloud.

To generate Cashier invoices on Cloud, install Spatie's Laravel PDF package and configure the Cloudflare environment variables as described in [Using Laravel PDF](#using-laravel-pdf):

```bash theme={null}
composer require spatie/laravel-pdf
```

Then, set Cashier to use its built-in Laravel PDF invoice renderer by adding the following environment variable to your Cloud environment's environment variable settings:

```dotenv theme={null}
CASHIER_INVOICE_RENDERER=Laravel\Cashier\Invoices\LaravelPdfInvoiceRenderer
```

Cashier resolves this renderer at runtime and uses Spatie Laravel PDF to generate invoice downloads.

## Manual usage

If you prefer to call the Cloudflare API directly without an additional dependency, add a `cloudflare` entry to your `services.php` config file:

```php theme={null}
'cloudflare' => [
    'api_token' => env('CLOUDFLARE_API_TOKEN'),
    'account_id' => env('CLOUDFLARE_ACCOUNT_ID'),
],
```

Next, set these environment variables in your Cloud environment's environment variable settings.

Now you may call the Cloudflare PDF API using Laravel's built-in `Http` facade. The following controller method renders a view to HTML and streams the response to the browser as a downloadable PDF:

```php theme={null}
use Illuminate\Support\Facades\Http;

public function download()
{
    return response()->streamDownload(function () {
        $token = config('services.cloudflare.api_token');
        $accountId = config('services.cloudflare.account_id');

        echo Http::withToken($token)
            ->post('https://api.cloudflare.com/client/v4/accounts/'.$accountId.'/browser-rendering/pdf', [
                'html' => view('view-to-render')->render(),
            ])
            ->body();
    }, 'file.pdf', [
        'Content-Type' => 'application/pdf',
    ]);
}
```
