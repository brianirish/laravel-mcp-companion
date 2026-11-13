# Migrating to 0.15

0.15 is the breaking release before 1.0. It replaces 26 tools with 12, changes how errors are reported, and moves the code into a package.
This page lists what to change. [CHANGELOG.md](CHANGELOG.md) has the reasons.

If you use the server through an AI assistant and never call tools by name,
there is one thing to do: pull the new image (or reinstall), and if you keep
documentation in a Docker volume, recreate the volume (see below).

## Tool calls

| If you called | Call |
|---------------|------|
| `search_laravel_docs(include_external=false)` | `search_laravel_docs(sources=["core"])` |
| `search_external_laravel_docs(query, services)` | `search_laravel_docs(query, sources=["services"])` |
| `search_laravel_learning_resources(query)` | `search_laravel_docs(query, sources=["learning"])` |
| `find_laravel_docs_for_need(need)` | `search_laravel_docs(need)` |
| `get_doc_structure(filename)` | `read_laravel_doc_content(filename, mode="outline")` |
| `list_laravel_docs(version="12.x")` | `list_laravel_docs(name="12.x")` |
| `list_laravel_services()` | `list_laravel_docs(source="services")` |
| `list_laravel_learning_resources(source)` | `list_laravel_docs(source="learning")` for all of them, or `list_laravel_docs(name=source)` for the files of one |
| `update_external_laravel_docs(services)` | `update_laravel_docs(scope="services", names=services)` |
| `get_laravel_package_info(package_name)` | `get_laravel_package(name=package_name)` |
| `get_laravel_package_categories(category)` | `get_laravel_package(category=category)` |
| `get_features_for_laravel_package(package)` | `get_laravel_package(name=package)`, field `packages[0].features` |
| `get_related_laravel_packages(package)` | `get_laravel_package(name=package)`, field `packages[0].related` |
| `get_laravel_package_recommendations(use_case)` | `recommend_laravel_packages(use_case)` |
| `list_laravel_learning_paths()` | `get_laravel_learning_path()` |
| `list_laravel_categories()` | `browse_docs_by_category()` |
| `get_laravel_content_by_difficulty(difficulty)` | `browse_docs_by_category(difficulty=difficulty)` |
| `verify_laravel_feature(feature)` | No replacement. Search for the feature instead |

Unchanged in name and arguments: `read_laravel_doc_section`,
`read_laravel_doc_content`, `laravel_docs_info`, `compare_laravel_versions`,
`get_laravel_service_info`, `get_laravel_learning_path`,
`browse_docs_by_category`. Their results changed shape; see
[API.md](API.md).

`update_laravel_docs(version, force)` still works as it did; `scope` and `names`
are new and optional.

The three prompts (`laravel-authentication-setup`, `find-payment-solution` and
`laravel-forge-deployment`) are gone and have no replacement.

## Results

- **Search results** have `section` where they had `anchor`. Pass a result's
  `file` as `filename`, with its `section`, to `read_laravel_doc_section`. A search that finds nothing returns
  `count: 0` and an empty `results`; it used to return an error.
- **`laravel_docs_info`** always returns `versions` (a list, of one when you
  pass `version`) and `sources`. The per-version fields that were at the top
  level are inside `versions[]`, and `commit_sha` is `commit`, shortened to
  seven characters.
- **`compare_laravel_versions`** no longer includes `summary` or `metadata`.
  Count the lists it returns; the commit of each version is in
  `laravel_docs_info`.
- **`update_laravel_docs`** returns `{scope, results[]}` with an `outcome` of
  `updated`, `unchanged` or `failed` per source, where it returned a sentence.
- **Every tool** now returns structured content. Tools that returned a bare
  TOON or markdown string still return that text, with the same data as an
  object beside it.

## Errors

A failure is a result with `isError: true` and one object:

```json
{"error": {"code": "not_found", "message": "No section 'x' in queues.md", "details": {"available_sections": ["introduction"]}}}
```

Before, a failure was an ordinary result containing an `error` key, or a line
such as `Documentation file not found: ...`. If you matched on those strings,
branch on `error.code` instead. The codes are listed in [API.md](API.md).

## TOON text

The text encoding follows version 1.x of the `toon-format` library. Against
the 0.9 beta of that library, which earlier releases used:
an empty list is `key: []`, not `key[0]:`; a whole float is written without
`.0`; a string that begins with `#` is quoted. If you parse the text, parse
the structured content instead.

## Running it

- **From a clone:** `python laravel_mcp_companion.py` is now
  `python -m laravel_mcp_companion`, and `python docs_updater.py` is
  `python -m laravel_mcp_companion.docs_updater`. Dependencies install with
  `uv sync`; the `requirements.txt` files are gone.
- **Importing the code:** modules moved into the `laravel_mcp_companion`
  package. `import mcp_tools` becomes
  `from laravel_mcp_companion import mcp_tools`, and the server module is
  `laravel_mcp_companion.server`.
- **Docker:** the image runs as an unprivileged user (uid 10001). A named
  volume at `/app/docs` created by an older image is owned by root, so
  `--update-docs` cannot write to it. Remove it and let the next run recreate
  it: `docker volume rm laravel-mcp-docs`.
- **`:latest`** is now the newest release with that night's documentation. It
  used to be whatever was on `main`.

## Documentation that moved or went

- **Laravel Blog and Laravel News** are no longer fetched. Reads of
  `laravel-blog/...` and `laravel-news/...` return `not_found`.
- **Spatie** pages are for each package's current major (Laravel Permission
  v8, Laravel Backup v10), and there are more of them. Pages a package
  dropped are gone.
- **Livewire** pages are for 4.x, and there are 80 where there were 36. A
  page name is the one in the Livewire site's navigation, so a page Livewire 4
  renamed or dropped is gone under its old name. List the current ones with
  `list_laravel_docs(name="livewire")`.
