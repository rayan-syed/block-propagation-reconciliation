from src.core.hash_utils import stable_hash


class CompactBlockProtocol:
    def __init__(
        self, tx_size=8, short_id_size=6, header_size=80, nonce_size=8, prefilled=1
    ):
        # tx_size = bytes per full transaction ID in our simulation
        # short_id_size = 6 bytes in BIP 152
        # header_size = 80-byte Bitcoin block header
        # nonce_size = 8-byte compact block nonce
        # prefilled = number of full transactions sent directly (coinbase by default)

        self.tx_size = tx_size
        self.short_id_size = short_id_size
        self.header_size = header_size
        self.nonce_size = nonce_size
        self.prefilled = prefilled

    def _short_id(self, tx, nonce):
        # simulate a 6-byte short transaction ID
        mod = 256**self.short_id_size
        return stable_hash(tx, nonce, mod)

    def run(self, block, mempool):
        block_list = list(block)
        n = len(block_list)

        if n == 0:
            return {
                "protocol": "compact_block",
                "bytes_sent": self.header_size + self.nonce_size,
                "success": True,
                "block_size": 0,
                "missing_count": 0,
                "recovered_from_mempool": 0,
                "prefilled_count": 0,
            }

        # prefill the first transaction to mimic coinbase handling
        prefilled_count = min(self.prefilled, n)
        prefilled = block_list[:prefilled_count]
        short_id_txs = block_list[prefilled_count:]

        # fixed nonce for deterministic simulation
        nonce = 1

        # sender transmits compact block sketch
        bytes_sent = self.header_size + self.nonce_size
        bytes_sent += len(short_id_txs) * self.short_id_size
        bytes_sent += len(prefilled) * self.tx_size

        # receiver builds short-id lookup from its mempool
        mempool_map = {}
        for tx in mempool:
            sid = self._short_id(tx, nonce)
            if sid not in mempool_map:
                mempool_map[sid] = tx

        reconstructed = list(prefilled)
        missing = []

        for tx in short_id_txs:
            sid = self._short_id(tx, nonce)

            if sid in mempool_map:
                reconstructed.append(mempool_map[sid])
            else:
                missing.append(tx)

        # request missing transactions and receive them in full
        bytes_sent += len(missing) * self.tx_size

        reconstructed.extend(missing)
        success = set(reconstructed) == set(block_list)

        return {
            "protocol": "compact_block",
            "bytes_sent": bytes_sent,
            "success": success,
            "block_size": n,
            "missing_count": len(missing),
            "recovered_from_mempool": len(short_id_txs) - len(missing),
            "prefilled_count": prefilled_count,
        }
