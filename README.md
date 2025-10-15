coldpkg — air-gapped Python tooling for cold wallet generation
=============================================================

Purpose
-------
This package contains audited Python scripts and vendored Python wheels to be used
on an air-gapped machine for secure wallet generation, verification, and address derivation.

Package layout
--------------
coldpkg/
├─ scripts/                    # Python tools
│  ├─ make_mnemonic.py
│  ├─ hex_to_mnemonic.py
│  ├─ derive_and_verify.py
│  └─ helpers.py
├─ tools/                      # bootstrap + packaging helpers (run online)
│  ├─ package_for_airgap.sh
│  ├─ verify_and_install_on_airgap.sh
│  └─ gen_checksums.sh
├─ docs/
│  ├─ README.md                # human-facing top doc (also repo README)
│  └─ AIRGAP.md                # step-by-step offline workflow
├─ tests/
│  ├─ test_vectors.json
│  └─ run_tests.sh
├─ requirements.txt            # pinned deps (exact versions)
├─ requirements-hashes.txt     # same deps WITH sha256 hashes (see below)
├─ .gitignore
└─ Makefile                    # convenience targets (build/package/test)

How to prepare (online machine)
--------------------------------
1. Run `package_for_airgap.sh /path/to/outdir` (edit PACKAGES in script if necessary).
2. Copy the produced tarball `coldpkg-YYYYMMDD.tar.gz` to a USB and move to air-gapped machine.
3. Verify tarball integrity on receiving machine (compare size and, if possible, checksums).

How to install (air-gapped machine)
-----------------------------------
1. Extract tarball: `tar -xzf coldpkg-YYYYMMDD.tar.gz`
2. `cd coldpkg`
3. Run: `./verify_and_install_on_airgap.sh`
   - This verifies checksums and installs wheels into a Python venv using only local files.
4. Activate the venv: `source venv/bin/activate`
5. Run scripts as needed, e.g.:
   - `python3 scripts/make_mnemonic.py --bytes 32` (entropy -> 24 words)
   - `python3 scripts/hex_to_mnemonic.py <64 hex chars>` (direct raw priv -> words)
   - `python3 scripts/derive_and_verify.py "<mnemonic words>"`

Security notes
--------------
- Do not install anything from the internet on the air-gapped machine.
- Verify checksums before installing. If you GPG-sign checksums, verify signatures.
- After generating mnemonic and engraving on metal plate, reboot the air-gapped machine to clear RAM.
- Only copy public outputs (addresses, public keys) off the air-gapped machine.

Support
-------
This is a simple packaging system. If you change libraries, re-run the packager and recalc checksums.
