Source: https://laravel.com/forge/docs/api-reference/relationships.md

# Relationships & Includes

> Learn about relationships and includes in the Laravel Forge API.

## Relationships

Some resources in the Laravel Forge API have relationships to other resources. Available relationships can be found in the `relationships` object within each resource response.

```json theme={null}
// ...
{
  "relationships": {
    "tags": {
      "data": [
        {
          "type": "tags",
          "id": "<string>"
        }
      ]
    }
  }
},
// ...
```

## Includes

Relationships can be included in the response by using the `include` query parameter:

```http theme={null}
GET /orgs/coinfly/servers/1?include=tags
```

Multiple relationships can be included by separating them with a comma:

```http theme={null}
GET /orgs/coinfly/servers/1/sites?include=latestDeployment,tags
```
