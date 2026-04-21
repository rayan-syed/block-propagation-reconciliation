import math
from src.core.hash_utils import stable_hash


class BloomFilter:
    def __init__(self, n, fp_rate, seeds=None):
        # n = expected number of elements
        # fp_rate = desired false positive rate

        self.n = n
        self.fp_rate = fp_rate

        # compute size (bits)
        self.m = max(1, int(-n * math.log(fp_rate) / (math.log(2) ** 2)))

        # number of hash functions
        self.k = max(1, int((self.m / n) * math.log(2)))

        # bit array
        self.bits = [0] * self.m

        # hash seeds
        if seeds is None:
            self.seeds = list(range(self.k))
        else:
            self.seeds = seeds

    def _hash(self, x, seed):
        return stable_hash(x, seed, self.m)

    def add(self, x):
        for seed in self.seeds:
            idx = self._hash(x, seed)
            self.bits[idx] = 1

    def query(self, x):
        for seed in self.seeds:
            idx = self._hash(x, seed)
            if self.bits[idx] == 0:
                return False
        return True

    def build(self, items):
        for x in items:
            self.add(x)
