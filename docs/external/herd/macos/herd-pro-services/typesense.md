Source: https://herd.laravel.com/docs/macos/herd-pro-services/typesense.md

# Typesense

# Set up Typesense for Laravel Scout

Typesense is a lightning-fast open source search engine for your application, working perfectly with [Laravel Scout](https://laravel.com/docs/11.x/scout). It allows you to add a search engine with great relevancy, typo correction, and more to your application by simply adding the `Searchable` Trait to a model.

Herd makes setting up a Typesense service super easy:


## Connecting from your Laravel application

Like with all Herd services, you can configure the port as well as the service name of your Typesense instance and then add the following environment variables to your `.env` file.

```env theme={null}
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=LARAVEL-HERD
TYPESENSE_HOST=localhost
```

If you're using a different port, you can simply copy the connections details from the right side of the service settings. The Typesense detail view also gives you a quick access to the logs of the service.


When using the Typesense with Laravel Scout you will need to install the Typesense PHP SDK via the Composer package manager:

```bash theme={null}
composer require typesense/typesense-php
```

You can find additional information about using Laravel Scout with Typesense in the [Laravel documentation](https://laravel.com/docs/11.x/scout#typesense)
