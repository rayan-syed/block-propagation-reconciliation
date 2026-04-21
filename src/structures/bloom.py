import math
import random


class BloomFilter:
    def __init__(self, n, fp_rate):
        # n = expected number of elements
        # fp_rate = desired false positive rate

        self.n = n
        self.fp_rate = fp_rate

        # compute size (bits)
        self.m = int(-n * math.log(fp_rate) / (math.log(2) ** 2))

        # number of hash functions
        self.k = int((self.m / n) * math.log(2))

        # bit array
        self.bits = [0] * self.m

        # random seeds for hash functions
        self.seeds = [random.randint(0, 10**9) for _ in range(self.k)]

    def _hash(self, x, seed):
        return hash((x, seed)) % self.m

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
