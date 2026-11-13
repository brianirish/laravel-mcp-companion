#!/usr/bin/env bash
# Arrange the checkout for an image build.
#
#   scripts/release_tree.sh <tag>
#
# A version tag (v1.2.3) is built exactly as tagged, and this script does
# nothing.
#
# A documentation tag (docs-YYYY-MM-DD) marks a nightly sync on main. Built as
# tagged, its image would carry every change merged to main since the last
# release, and because that image becomes `latest`, unreleased code would reach
# users the night it merged. So for a docs tag the tree is rearranged: the code
# of the newest released version, with the docs tag's docs/ directory. The
# image is then "the last release, with tonight's documentation".
#
# Release candidates and other pre-releases (v1.0.0-rc1) are never chosen.
#
#   scripts/release_tree.sh --moving-tag <tag>
#
# Prints the second tag the image should be pushed under. That is `latest` for
# a docs build and for the newest stable release. For anything else, a
# pre-release or a patch to an older line, it is the tag itself, so `latest`
# stays where it is.
set -euo pipefail

# Everything runs inside main() so that bash has read the whole file before the
# checkout below replaces it on disk.
newest_release() {
  git ls-remote --tags --refs origin 'v*' \
    | sed 's#.*refs/tags/##' \
    | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' \
    | sort -V \
    | tail -n 1 || true
}

moving_tag() {
  local tag="$1"
  case "$tag" in
    docs-*) echo "latest" ;;
    *)
      if [ "$tag" = "$(newest_release)" ]; then echo "latest"; else echo "$tag"; fi
      ;;
  esac
}

main() {
  if [ "${1:-}" = "--moving-tag" ]; then
    moving_tag "${2:?usage: release_tree.sh --moving-tag <tag>}"
    return 0
  fi

  TAG="${1:?usage: release_tree.sh <tag>}"

  case "$TAG" in
    docs-*) ;;
    *)
      echo "Building ${TAG} as tagged."
      return 0
      ;;
  esac

  RELEASE="$(newest_release)"

  if [ -z "$RELEASE" ]; then
    echo "No released version tag (vX.Y.Z) found on origin; refusing to build ${TAG}." >&2
    exit 1
  fi

  DOCS_COMMIT="$(git rev-parse HEAD)"

  # The pipeline's clone is shallow, so fetch the one commit that is needed.
  git fetch --quiet --depth=1 origin "refs/tags/${RELEASE}:refs/tags/${RELEASE}"
  git checkout --quiet --detach "$RELEASE"

  # Replace docs/ wholesale. Checking paths out over the release's copy would
  # leave behind pages the sync has since deleted.
  rm -rf docs
  git checkout --quiet "$DOCS_COMMIT" -- docs

  echo "Building ${TAG}: code from ${RELEASE}, documentation from ${TAG} (${DOCS_COMMIT})."
}

main "$@"
