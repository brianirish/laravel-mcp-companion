"""Harness rejects a pipeline whose stage or step names contain characters
outside a small set, and it does so when a trigger fires, not when the YAML is
merged. Two step names with parentheses went in on 2026-08-03; from then on
every push produced INVALID_RUNTIME_INPUT_YAML in the trigger's event history
and no execution, so CI silently did not run for three months."""

import re
from pathlib import Path

import pytest

PIPELINES = sorted((Path(__file__).resolve().parents[2] / ".harness").rglob("pipelines/*.yaml"))

# The stricter of the two patterns Harness reported for step names.
HARNESS_NAME = re.compile(r"^[a-zA-Z_][-0-9a-zA-Z_\s]{0,127}$")


def _names(pipeline: Path) -> list[str]:
    names = []
    for line in pipeline.read_text().splitlines():
        match = re.match(r"^\s*name:\s*(.+?)\s*$", line)
        if match:
            names.append(match.group(1).strip("'\""))
    return names


def test_pipelines_are_found():
    assert {p.name for p in PIPELINES} >= {"ci.yaml", "docs_update.yaml", "release.yaml"}


@pytest.mark.parametrize("pipeline", PIPELINES, ids=lambda p: p.name)
def test_every_stage_and_step_name_is_one_harness_accepts(pipeline):
    rejected = [name for name in _names(pipeline) if not HARNESS_NAME.match(name)]
    assert rejected == []
