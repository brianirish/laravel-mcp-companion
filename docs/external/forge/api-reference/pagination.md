Source: https://laravel.com/forge/docs/api-reference/pagination.md

# Pagination

> Learn how to handle pagination in the Laravel Forge API.

All API endpoints that return multiple items support cursor-based pagination.

By default, `30` items are returned per page. You can specify the number of items to return per page by passing the `page[size]` parameter.

```http theme={null}
GET /orgs/coinfly/servers?page[size]=30
```

Paginated responses include `meta` and `links` objects for navigating results:

```json theme={null}
{
  "data": [...],
  "meta": {
    "per_page": 30,
    "next_cursor": "eyJzZXJ2ZXJzLmlkIjozMCwiX3BvaW50c1RvTmV4dEl0ZW1zIjp0cnVlfQ",
    "prev_cursor": null
  },
  "links": {
    "next": "/api/orgs/coinfly/servers?page[size]=30&page[cursor]=eyJzZXJ2ZXJzLmlkIjozMCwiX3BvaW50c1RvTmV4dEl0ZW1zIjp0cnVlfQ",
    "prev": null
  }
}
```

To fetch the next or previous page, use the `page[cursor]` parameter with the value from either `meta.next_cursor` or `meta.prev_cursor` from a paginated response.

```http theme={null}
GET /orgs/coinfly/servers?page[size]=30&page[cursor]=eyJzZXJ2ZXJzLmlkIjozMCwiX3BvaW50c1RvTmV4dEl0ZW1zIjp0cnVlfQ
```

Note that `meta.prev_cursor` will be null on the first page and `meta.next_cursor` will be null on the last page.
