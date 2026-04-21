from src.protocols.full_block import FullBlockProtocol


def test_full_block():
    block = set(range(100))

    protocol = FullBlockProtocol(tx_size=8)
    result = protocol.run(block)

    assert result["protocol"] == "full_block"
    assert result["bytes_sent"] == 800
    assert result["success"]
    assert result["block_size"] == 100
