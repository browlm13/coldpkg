#!/usr/bin/env python3
"""
Generate mnemonic from entropy. Supports:
 - os.urandom entropy
 - dice/cards/manual entropy (paste)
Outputs mnemonic and verifies roundtrip.
Requires: python-mnemonic library (but script uses direct mapping if you vendor wordlist).
"""
import os, sys, binascii
import argparse
from mnemonic import Mnemonic

def generate_from_os(bytes_len=32):
    return os.urandom(bytes_len)

def generate_from_hex(hexstr):
    return binascii.unhexlify(hexstr)

def main():
    p = argparse.ArgumentParser(description="Create BIP39 mnemonic from entropy (offline-ready).")
    p.add_argument("--bytes", type=int, default=32, choices=[16,20,24,28,32], help="entropy bytes (32 -> 24 words)")
    p.add_argument("--hex", help="Use provided hex entropy instead of os.urandom")
    p.add_argument("--dice", action="store_true", help="(Manual mode) paste base-6 dice string after prompt")
    p.add_argument("--passphrase", default="", help="Optional passphrase (do NOT store with plate).")
    args = p.parse_args()

    if args.hex:
        raw = generate_from_hex(args.hex)
    elif args.dice:
        s = input("Paste dice rolls (1..6 digits continuous): ").strip()
        # Convert base-6 string to bytes (pad/truncate to requested bytes)
        val = 0
        for ch in s:
            if ch not in "123456": raise SystemExit("Bad dice")
            val = val*6 + (int(ch)-1)
        raw = val.to_bytes(args.bytes, 'big')[-args.bytes:]
    else:
        raw = generate_from_os(args.bytes)

    m = Mnemonic("english")
    mnemonic = m.to_mnemonic(raw)
    print("\nMNEMONIC:\n")
    print(mnemonic)
    print("\n--- Roundtrip verification ---")
    ent = m.to_entropy(mnemonic)
    print("Entropy hex:", binascii.hexlify(ent).decode())
    assert ent == raw, "Roundtrip mismatch!"
    seed = m.to_seed(mnemonic, passphrase=args.passphrase)
    print("Seed (hex, PBKDF2):", binascii.hexlify(seed).decode())
    print("\nWRITE THESE WORDS DOWN. Reboot system after engraving to clear memory.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
