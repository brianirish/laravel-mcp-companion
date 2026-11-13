"""Build hook: put the documentation corpus and server.json in the wheel.

The corpus lives at the repository root in `docs/`, where the nightly sync
writes it and the Docker image reads it. A wheel has no repository root, so
the corpus is copied into the package as `laravel_mcp_companion/docs/`, which
is where `laravel_mcp_companion.resource_path` looks first. Every entry of
`docs/` is included except the project's own working notes, so a new Laravel
version directory needs no change here.
"""

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

NOT_CORPUS = {"superpowers"}


def bundled_files(root: Path) -> dict[str, str]:
    """Repository paths to copy into the wheel, mapped to where they land."""
    files = {
        str(entry): f"laravel_mcp_companion/docs/{entry.name}"
        for entry in sorted((root / "docs").iterdir())
        if entry.name not in NOT_CORPUS
    }
    files[str(root / "server.json")] = "laravel_mcp_companion/server.json"
    return files


class CorpusBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # An editable install points back at the checkout, where the corpus is
        # already beside the package. Copying it would only leave a stale
        # duplicate in site-packages.
        if version == "editable":
            return
        build_data["force_include"].update(bundled_files(Path(self.root)))
