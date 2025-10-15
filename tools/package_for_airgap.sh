#!/usr/bin/env bash
set -euo pipefail
# USAGE: ./package_for_airgap.sh /path/to/target/dir
# Example: ./package_for_airgap.sh /tmp/coldpkg_out

OUTDIR=${1:-./coldpkg_out}
SCRIPTDIR="$(pwd)/scripts"   # where your scripts live locally
DOCSDIR="$(pwd)/doc"
LIBS_DIR="$OUTDIR/coldpkg/libs"
SCRIPTS_OUT="$OUTDIR/coldpkg/scripts"
DOC_OUT="$OUTDIR/coldpkg/doc"
TESTS_OUT="$OUTDIR/coldpkg/tests"

mkdir -p "$LIBS_DIR" "$SCRIPTS_OUT" "$DOC_OUT" "$TESTS_OUT"

echo "Copying scripts..."
cp -a "$SCRIPTDIR"/* "$SCRIPTS_OUT/"

echo "Copying docs..."
if [ -d "$DOCSDIR" ]; then
  cp -a "$DOCSDIR"/* "$DOC_OUT/" || true
fi

# Packages to vendor: add/remove as you like
PACKAGES=("mnemonic" "ecdsa" "coincurve" "bech32" "base58") 
# Note: coincurve may need libsecp256k1: pip will fetch wheels if available; ensure compatibility with air-gapped OS.

echo "Downloading wheels (and dependencies) into $LIBS_DIR ..."
python3 -m pip download "${PACKAGES[@]}" -d "$LIBS_DIR"

echo "Copy README template"
cat > "$OUTDIR/coldpkg/README.md" <<'README'
Coldpkg - air-gapped python package bundle
See docs/AIRGAP.md in this folder after extraction.
README

# Generate checksums for libs and scripts
echo "Generating checksums..."
(cd "$LIBS_DIR" && sha256sum * > "$OUTDIR/coldpkg/libs_checksums.txt")
(cd "$SCRIPTS_OUT" && sha256sum * > "$OUTDIR/coldpkg/scripts_checksums.txt")

# Make a tarball you can copy to USB
TS=$(date +%Y%m%d)
TARFILE="$OUTDIR/coldpkg-$TS.tar.gz"
echo "Creating tarball $TARFILE ..."
tar -czf "$TARFILE" -C "$OUTDIR" coldpkg

echo "Done. Copy $TARFILE to your USB drive."
echo "Important: verify the sha256 sums printed above before transferring to air-gapped machine."
