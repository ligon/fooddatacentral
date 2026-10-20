#!/usr/bin/env bash
# Release the version named in pyproject.toml.
#
# Checks that the release is ready, stamps today's date into CITATION.cff,
# tags v<version>, pushes, and creates the GitHub release.  Publishing the
# release triggers .github/workflows/publish.yml, which uploads to PyPI.
#
# Bump the version first (e.g. `poetry version minor`, plus the version in
# CITATION.cff), commit, push, and wait for the Tests workflow to pass.  Then:
#
#   make release                       # release it
#   make release DRY_RUN=1             # run the checks, change nothing
#   make release NOTES="Drops Python 3.9."
#                                      # text placed above the generated notes

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

die() { echo "release: $*" >&2; exit 1; }
run() {
    if [ -n "${DRY_RUN:-}" ]; then echo "would run: $*"; else "$@"; fi
}

version=$(poetry version -s)
tag="v$version"
echo "Releasing fooddatacentral $version ($tag)"

# Where we are
[ "$(git rev-parse --abbrev-ref HEAD)" = master ] || die "not on master"
[ -z "$(git status --porcelain --untracked-files=no)" ] || die "uncommitted changes"
git fetch -q origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/master)" ] \
    || die "master and origin/master differ; push or pull first"

# The version is new
if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    die "tag $tag already exists; bump the version in pyproject.toml"
fi
if git ls-remote --exit-code --tags origin "refs/tags/$tag" >/dev/null; then
    die "tag $tag already exists on origin"
fi
if curl -sf -o /dev/null "https://pypi.org/pypi/fooddatacentral/$version/json"; then
    die "$version is already on PyPI"
fi
grep -qx "version: $version" CITATION.cff || die "CITATION.cff version is not $version"

# The release is sound.  Locally the live API tests skip without
# FDC_API_KEY, so also require CI (which has the key) to have passed.
ci=$(gh run list --workflow tests.yml --commit "$(git rev-parse HEAD)" -L 1 --json status,conclusion \
     --jq '.[0] | if . == null then "none" elif .status != "completed" then "running" else .conclusion end')
[ "$ci" = success ] || die "CI tests for HEAD: $ci (need success; see gh run list --workflow tests.yml)"
make -s readme-check
poetry run pytest -q

# Stamp the release date
today=$(date +%F)
if ! grep -qx "date-released: \"$today\"" CITATION.cff; then
    run sed -i "s/^date-released: .*/date-released: \"$today\"/" CITATION.cff
    run git commit -q -m "CITATION.cff: release date for $version" CITATION.cff
fi

run git tag -a "$tag" -m "fooddatacentral $version"
run git push -q origin master "$tag"
run gh release create "$tag" --verify-tag --title "$tag" --generate-notes ${NOTES:+--notes "$NOTES"}

if [ -z "${DRY_RUN:-}" ]; then
    echo "Released $tag.  PyPI upload: https://github.com/ligon/fooddatacentral/actions/workflows/publish.yml"
fi
