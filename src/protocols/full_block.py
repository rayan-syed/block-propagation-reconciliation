class FullBlockProtocol:
    def __init__(self, tx_size=8):
        # tx_size = bytes per transaction ID
        self.tx_size = tx_size

    def run(self, block, mempool=None):
        # sender transmits the full block directly
        bytes_sent = len(block) * self.tx_size

        reconstructed = set(block)
        success = reconstructed == block

        return {
            "protocol": "full_block",
            "bytes_sent": bytes_sent,
            "success": success,
            "block_size": len(block),
        }
