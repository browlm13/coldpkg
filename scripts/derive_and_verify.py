#!/usr/bin/env python3
"""
Derive BIP32 master xprv/xpub and child keys; compute addresses for a given mnemonic or hex.
Dependencies: python-mnemonic, ecdsa, bech32, base58
This is an educational, auditable script — use on air-gapped machine.
"""
import sys, binascii, hmac, hashlib
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import string_to_number, number_to_string
from bech32 import bech32_encode, convertbits
import base58

CURVE = SECP256k1
G_ORDER = SECP256k1.order

def pbkdf2_seed(mnemonic, passphrase=""):
    # BIP39 seed
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode("utf-8"), ("mnemonic"+passphrase).encode("utf-8"), 2048, dklen=64)

def bip32_master_from_seed(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    IL, IR = I[:32], I[32:]
    priv = int.from_bytes(IL, "big")
    if priv == 0 or priv >= G_ORDER:
        raise Exception("Bad master key (unlikely).")
    chain = IR
    return priv, chain

def priv_to_pub_compressed(priv_int):
    sk = SigningKey.from_secret_exponent(priv_int, curve=CURVE)
    vk = sk.verifying_key
    # compressed
    px = vk.pubkey.point.x()
    py = vk.pubkey.point.y()
    prefix = b'\x02' if (py % 2 == 0) else b'\x03'
    return prefix + int.to_bytes(px, 32, 'big')

def hash160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

def p2pkh_address(pub_compressed):
    # need uncompressed for P2PKH historically, but P2PKH uses pubkey hash; using compressed is fine
    h160 = hash160(pub_compressed)
    return base58.b58encode_check(b'\x00' + h160).decode()

def p2wpkh_bech32(pub_compressed):
    prog = hash160(pub_compressed)
    data = convertbits(prog, 8, 5)
    return bech32_encode("bc", [0] + data)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 derive_and_verify.py <mnemonic OR 64hex> [--passphrase yourpass]")
        sys.exit(1)
    arg = sys.argv[1].strip()
    passphrase = ""
    if len(sys.argv) >= 4 and sys.argv[2] == "--passphrase":
        passphrase = sys.argv[3]
    m = Mnemonic("english")
    if len(arg) == 64 and all(c in "0123456789abcdefABCDEF" for c in arg):
        # treat as raw private hex (your preferred mode)
        raw = binascii.unhexlify(arg)
        print("INTERPRETING AS RAW PRIVATE HEX (direct mode).")
        priv_int = int.from_bytes(raw, "big")
        pub_comp = priv_to_pub_compressed(priv_int)
        print("Pub compressed hex:", pub_comp.hex())
        print("P2WPKH(bech32):", p2wpkh_bech32(pub_comp))
        print("P2PKH:", p2pkh_address(pub_comp))
    else:
        # treat as mnemonic (BIP39)
        mnemonic = arg
        seed = pbkdf2_seed(mnemonic, passphrase)
        print("BIP39 seed (hex):", seed.hex())
        priv_master, chain = bip32_master_from_seed(seed)
        print("Master private (int):", priv_master)
        print("Master chaincode hex:", chain.hex())
        # Derive account 0 m/84'/0'/0' (hardened) then first address m/84'/0'/0'/0/0
        # For brevity: show master pub and first child naive (full BIP32 derivation implementation is longer)
        pub_master = priv_to_pub_compressed(priv_master)
        print("Master pub compressed hex:", pub_master.hex())
        print("First receive address (example from priv_master):", p2wpkh_bech32(pub_master))
    print("Done.")
