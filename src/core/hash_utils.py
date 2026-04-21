import hashlib


# stable hashing for consistent experiments and tests
def stable_hash(x, seed, size):
    data = f"{x}-{seed}".encode()
    h = hashlib.blake2b(data, digest_size=8).digest()
    return int.from_bytes(h, "big") % size
