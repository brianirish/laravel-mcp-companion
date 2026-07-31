# Harness triggers

**These files are a mirror, not the source of truth.** Harness stores triggers in
its own database, not in this repository — unlike the pipelines and input sets
alongside them, which are Remote (git-backed) and are read from here. Editing a
file in this directory changes nothing in Harness; edits have to be made in the
UI, then copied back here.

They are checked in anyway because triggers are load-bearing and were previously
invisible to review. A UI edit on 2026-07-30 stopped the release pipeline firing
for `v*` tags, which silently broke Docker image publishing: tag `v0.10.1` was
created but no image was ever built, leaving `:latest` stale. There was no pull
request, no diff, and nothing to restore from. A mirror gives us something to
diff against and to rebuild from.

## Mirrored here

| Trigger | Pipeline | Fires on |
|---------|----------|----------|
| `ci-push-trigger.yaml` | `ci` | Every push, any branch |

## Not yet mirrored

- **Release trigger** (`release` pipeline) — paste its YAML here when convenient.
- **Docs update cron** (`docs_update` pipeline) — scheduled, feeds `docs_update_cron_input_set`.

## What the release trigger must satisfy

Recorded here because it is currently misconfigured and this is the requirement
it has to meet, independent of the exact YAML:

- It feeds `release_tag_input_set`, which builds `type: tag` from `<+trigger.tag>`,
  so it must be a tag-ref trigger.
- It must match **both** tag families:
  - `v*` — software releases, which publish a Docker image and a GitHub Release
  - `docs-*` — documentation snapshots, which publish a Docker image only
- Matching only one family breaks the other. Matching only `docs-*` means version
  releases publish no image; matching only `v*` means documentation updates never
  reach `:latest`, which is the state that motivated this note.

After changing it, verify a tag of each kind produces an image:

```bash
gh api "user/packages/container/laravel-mcp-companion/versions?per_page=10" \
  --jq '.[] | "\(.created_at)  \(.metadata.container.tags | join(", "))"'
```

## Keeping this honest

A mirror that drifts is worse than none. Options, in rough order of preference:

1. Move triggers to Git-backed storage if this Harness version supports it, which
   removes the mirror problem entirely.
2. Re-copy the YAML here in the same change that edits a trigger in the UI.
