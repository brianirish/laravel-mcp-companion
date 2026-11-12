Source: https://laravel.com/forge/docs/api-reference/filtering.md

# Filtering & Sorting

> Learn how to filter and sort data in the Laravel Forge API.

## Filtering

Several endpoints support filtering to allow you to retrieve only the data you need. For example, you can filter servers by name:

```http theme={null}
GET /orgs/coinfly/servers?filter[name]=conifly-web
```

> [!NOTE]
>
> Individual endpoints may support filtering on different fields. Check the documentation for the specific endpoint you are working with.

## Sorting

You can sort the results of an endpoint by passing the `sort` parameter. You must provide a comma-separated list of fields to sort by.

```http theme={null}
GET /orgs/coinfly/servers?sort=php_version
```

To reverse order the results, prefix the field with a hyphen (`-`):

```http theme={null}
GET /orgs/coinfly/servers?sort=-php_version
```

> [!NOTE]
>
> Individual endpoints may support sorting on different fields. Check the documentation for the specific endpoint you are working with.
