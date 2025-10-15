# helpers.py -- tiny utilities (hash160, bech32 wrapper via library, base58)
import hashlib

def sha256(b): return hashlib.sha256(b).digest()
def ripemd160(b): return hashlib.new('ripemd160', b).digest()
def hash160(b): return ripemd160(sha256(b))

# base58 check encode (use installed base58 lib in derive script where needed)
# Bech32 encode will be used from bech32 lib in derive script.
