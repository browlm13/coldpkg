#!/usr/bin/env bash
# simple helper: generate checksums for a directory
DIR=${1:-.}
find "$DIR" -type f -maxdepth 1 -name '*.whl' -print0 | xargs -0 sha256sum > "$DIR/checksums.sha256"
