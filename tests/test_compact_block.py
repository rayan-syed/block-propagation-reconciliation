from src.protocols.compact_block import CompactBlockProtocol


def test_compact_block_full_overlap():
    block = set(range(100))
    mempool = set(range(200))

    protocol = CompactBlockProtocol(tx_size=8)
    result = protocol.run(block, mempool)

    expected = 80 + 8 + 1 * 8 + 99 * 6

    assert result["protocol"] == "compact_block"
    assert result["bytes_sent"] == expected
    assert result["success"]
    assert result["missing_count"] == 0
    assert result["prefilled_count"] == 1


def test_compact_block_partial_overlap():
    block = set(range(100))
    mempool = set(range(80))

    protocol = CompactBlockProtocol(tx_size=8)
    result = protocol.run(block, mempool)

    expected = 80 + 8 + 1 * 8 + 99 * 6 + 20 * 8

    assert result["protocol"] == "compact_block"
    assert result["bytes_sent"] == expected
    assert result["success"]
    assert result["missing_count"] == 20
    assert result["prefilled_count"] == 1
