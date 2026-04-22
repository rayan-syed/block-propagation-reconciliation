from src.protocols.graphene import GrapheneProtocol


class GrapheneFallbackProtocol(GrapheneProtocol):
    def __init__(
        self,
        tx_size=250,
        txid_size=8,
        cell_size=12,
        iblt_hashes=3,
        iblt_factor=12,
        delta=0.5,
        max_search_a=64,
        fixed_a=None,
    ):
        # tx_size = bytes per full transaction sent during fallback recovery
        # txid_size = bytes per txid used to tell the receiver which extras to drop

        super().__init__(
            cell_size=cell_size,
            iblt_hashes=iblt_hashes,
            iblt_factor=iblt_factor,
            delta=delta,
            max_search_a=max_search_a,
            fixed_a=fixed_a,
        )

        self.tx_size = tx_size
        self.txid_size = txid_size

    def run(self, block, mempool):
        base_result, reconstructed, block_set = self._run_graphene(block, mempool)

        # if standard Graphene succeeds, no fallback is needed
        if base_result["success"]:
            result = dict(base_result)
            result["protocol"] = "graphene_fallback"
            result["base_bytes_sent"] = base_result["bytes_sent"]
            result["fallback_used"] = False
            result["fallback_bytes"] = 0
            result["missing_count"] = 0
            result["extra_count"] = 0
            return result

        # fallback recovery:
        # - send missing transactions in full
        # - send extra txids so the receiver can drop false positives
        missing = block_set - reconstructed
        extra = reconstructed - block_set

        fallback_bytes = len(missing) * self.tx_size + len(extra) * self.txid_size

        result = dict(base_result)
        result["protocol"] = "graphene_fallback"
        result["bytes_sent"] = base_result["bytes_sent"] + fallback_bytes
        result["success"] = True
        result["base_bytes_sent"] = base_result["bytes_sent"]
        result["fallback_used"] = True
        result["fallback_bytes"] = fallback_bytes
        result["missing_count"] = len(missing)
        result["extra_count"] = len(extra)

        return result
