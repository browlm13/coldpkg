#!/usr/bin/env bash
set -euo pipefail
# Usage: ./verify_and_install_on_airgap.sh
ROOT="$(pwd)"
LIBS="$ROOT/libs"
SCRIPTS="$ROOT/scripts"

echo "Verifying wheel checksums and script checksums..."
if [ ! -f "$ROOT/libs_checksums.txt" ]; then
  echo "Missing libs_checksums.txt"
  ls -la
  exit 1
fi
if [ ! -f "$ROOT/scripts_checksums.txt" ]; then
  echo "Missing scripts_checksums.txt"
  exit 1
fi

# Verify libs checksums
echo "Checking libs..."
cd "$LIBS"
sha256sum -c ../libs_checksums.txt || { echo "Lib checksum failed"; exit 1; }
cd "$ROOT"

# Verify scripts checksums
echo "Checking scripts..."
cd "$SCRIPTS"
sha256sum -c ../scripts_checksums.txt || { echo "Script checksum failed"; exit 1; }
cd "$ROOT"

# Create venv
echo "Creating python venv..."
python3 -m venv venv
source venv/bin/activate

# Install wheels from local directory
echo "Installing wheels from local libs..."
pip install --no-index --find-links="$LIBS" mnemonic ecdsa bech32 base58 || { echo "pip install failed"; exit 1; }

echo "Installation complete. Run scripts from the venv (source venv/bin/activate)."
echo "Run a smoke test: python3 scripts/make_mnemonic.py --bytes 16"
