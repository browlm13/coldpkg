#!/usr/bin/env python3
"""
Direct-entropy-as-private-key mode:
- Input: 32-byte hex private key
- Output: 24-word mnemonic that encodes that raw 32 bytes (BIP39 encoding)
- Roundtrip verify: decode words back and compare raw hex
"""
import sys, binascii
from mnemonic import Mnemonic

if len(sys.argv)!=2:
    print("Usage: python3 hex_to_mnemonic.py <64hex>")
    sys.exit(1)
hexin = sys.argv[1].strip()
raw = binascii.unhexlify(hexin)
m = Mnemonic("english")
mn = m.to_mnemonic(raw)
print("MNEMONIC:\n", mn)
rec = m.to_entropy(mn)
print("Recovered hex:", binascii.hexlify(rec).decode())
assert rec == raw, "Roundtrip failed!"
print("OK: mnemonic encodes the exact raw private hex.")
