from src.core.hash_utils import stable_hash


class IBLT:
    def __init__(self, size, k=3, seeds=None):
        # size = number of cells
        # k = number of hash functions

        self.size = size
        self.k = k

        self.count = [0] * size
        self.key_sum = [0] * size

        # ensure same hash functions when needed
        if seeds is None:
            self.seeds = list(range(k))
        else:
            self.seeds = seeds

    def _hash(self, x, seed):
        return stable_hash(x, seed, self.size)

    def add(self, x):
        for seed in self.seeds:
            i = self._hash(x, seed)
            self.count[i] += 1
            self.key_sum[i] ^= x

    def remove(self, x):
        for seed in self.seeds:
            i = self._hash(x, seed)
            self.count[i] -= 1
            self.key_sum[i] ^= x

    def subtract(self, other):
        # subtract two IBLTs (must use same hashes)
        result = IBLT(self.size, self.k, seeds=self.seeds)

        for i in range(self.size):
            result.count[i] = self.count[i] - other.count[i]
            result.key_sum[i] = self.key_sum[i] ^ other.key_sum[i]

        return result

    def peel(self):
        # recover differences via peeling
        pos = set()  # elements in self but not other
        neg = set()  # elements in other but not self

        stack = [i for i in range(self.size) if abs(self.count[i]) == 1]

        max_steps = 10 * self.size * self.k
        steps = 0

        while stack:
            steps += 1
            if steps > max_steps:
                return False, pos, neg

            i = stack.pop()

            if self.count[i] == 0:
                continue

            if abs(self.count[i]) != 1:
                continue

            x = self.key_sum[i]

            if self.count[i] == 1:
                pos.add(x)
                self.remove(x)
            else:
                neg.add(x)
                self.add(x)

            # update affected cells
            for seed in self.seeds:
                j = self._hash(x, seed)
                if abs(self.count[j]) == 1:
                    stack.append(j)

        success = all(c == 0 for c in self.count)

        return success, pos, neg
