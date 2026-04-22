from src.protocols.graphene_fallback import GrapheneFallbackProtocol


def test_graphene_fallback_full_overlap():
    block = set(range(100))
    mempool = set(range(500))

    protocol = GrapheneFallbackProtocol()
    result = protocol.run(block, mempool)

    assert result["protocol"] == "graphene_fallback"
    assert result["success"]
    assert result["fallback_used"] is False
    assert result["fallback_bytes"] == 0


def test_graphene_fallback_partial_overlap():
    block = set(range(100))
    mempool = set(range(20, 500))  # missing 0..19 from the block

    protocol = GrapheneFallbackProtocol(tx_size=250, txid_size=8)
    result = protocol.run(block, mempool)

    assert result["protocol"] == "graphene_fallback"
    assert result["success"]
    assert result["fallback_used"] is True
    assert result["missing_count"] > 0
    assert result["bytes_sent"] >= result["base_bytes_sent"]
