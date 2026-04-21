import math

from src.structures.bloom import BloomFilter
from src.structures.iblt import IBLT


class GrapheneProtocol:
    def __init__(
        self,
        tx_size=8,
        cell_size=12,
        iblt_hashes=3,
        iblt_factor=12,
        delta=0.5,
        max_search_a=64,
    ):
        # tx_size = bytes per txid in our simulation
        # cell_size = bytes per IBLT cell (matches common Graphene-style accounting)
        # iblt_hashes = number of IBLT hash functions
        # iblt_factor = conservative sizing factor for our simplified IBLT
        # delta = slack so we size for a* = (1 + delta) a
        # max_search_a = max a value to search over

        self.tx_size = tx_size
        self.cell_size = cell_size
        self.iblt_hashes = iblt_hashes
        self.iblt_factor = iblt_factor
        self.delta = delta
        self.max_search_a = max_search_a

    def _bloom_bytes(self, n, fp_rate):
        bits = -n * math.log(fp_rate) / (math.log(2) ** 2)
        return math.ceil(bits / 8)

    def _iblt_cells(self, a):
        a_star = (1 + self.delta) * a
        return max(1, math.ceil(self.iblt_factor * a_star))

    def _search_best_a(self, n, m):
        # Graphene searches over expected false positives a
        # and derives bloom FPR from a / (m - n)

        outside = m - n

        # if mempool is no larger than block, Graphene loses its usual advantage
        # but we still return a safe fallback
        if outside <= 0:
            return 1, 0.01, self._iblt_cells(1)

        best = None

        max_a = min(self.max_search_a, outside)

        for a in range(1, max_a + 1):
            fp_rate = a / outside

            # bloom FPR must be strictly between 0 and 1
            if fp_rate <= 0 or fp_rate >= 1:
                continue

            bloom_bytes = self._bloom_bytes(n, fp_rate)
            iblt_cells = self._iblt_cells(a)
            iblt_bytes = iblt_cells * self.cell_size

            total = bloom_bytes + iblt_bytes

            if best is None or total < best[0]:
                best = (total, a, fp_rate, iblt_cells)

        if best is None:
            return 1, 0.01, self._iblt_cells(1)

        _, a, fp_rate, iblt_cells = best
        return a, fp_rate, iblt_cells

    def run(self, block, mempool):
        block_set = set(block)
        mempool_set = set(mempool)

        n = len(block_set)
        m = len(mempool_set)

        if n == 0:
            return {
                "protocol": "graphene",
                "bytes_sent": 0,
                "success": True,
                "block_size": 0,
                "mempool_size": m,
                "a": 0,
                "fp_rate": 0,
                "bloom_bytes": 0,
                "iblt_bytes": 0,
                "candidate_size": 0,
                "decoded_pos": 0,
                "decoded_neg": 0,
            }

        a, fp_rate, iblt_cells = self._search_best_a(n, m)

        # sender builds bloom filter over the block
        bloom = BloomFilter(n=n, fp_rate=fp_rate)
        bloom.build(block_set)

        # sender builds IBLT over the block
        sender_iblt = IBLT(
            size=iblt_cells, k=self.iblt_hashes, seeds=list(range(self.iblt_hashes))
        )
        for tx in block_set:
            sender_iblt.add(tx)

        # receiver filters mempool through bloom
        candidate = {tx for tx in mempool_set if bloom.query(tx)}

        # receiver builds IBLT over candidate set
        receiver_iblt = IBLT(
            size=iblt_cells, k=self.iblt_hashes, seeds=list(range(self.iblt_hashes))
        )
        for tx in candidate:
            receiver_iblt.add(tx)

        # subtract and peel
        diff = sender_iblt.subtract(receiver_iblt)
        success, pos, neg = diff.peel()

        # sender - receiver:
        # pos = block txs missing from candidate
        # neg = false positives that passed bloom
        reconstructed = (candidate - neg) | pos
        exact = reconstructed == block_set

        bloom_bytes = self._bloom_bytes(n, fp_rate)
        iblt_bytes = iblt_cells * self.cell_size

        return {
            "protocol": "graphene",
            "bytes_sent": bloom_bytes + iblt_bytes,
            "success": success and exact,
            "block_size": n,
            "mempool_size": m,
            "a": a,
            "fp_rate": fp_rate,
            "bloom_bytes": bloom_bytes,
            "iblt_bytes": iblt_bytes,
            "candidate_size": len(candidate),
            "decoded_pos": len(pos),
            "decoded_neg": len(neg),
        }
