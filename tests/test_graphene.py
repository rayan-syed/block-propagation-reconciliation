from src.protocols.graphene import GrapheneProtocol


def test_graphene_full_overlap():
    block = set(range(100))
    mempool = set(range(500))

    protocol = GrapheneProtocol()
    result = protocol.run(block, mempool)

    assert result["protocol"] == "graphene"
    assert result["success"]
    assert result["block_size"] == 100
    assert result["mempool_size"] == 500
    assert result["bytes_sent"] > 0


def test_graphene_smaller_than_full_block():
    block = set(range(100))
    mempool = set(range(500))

    protocol = GrapheneProtocol(tx_size=8)
    result = protocol.run(block, mempool)

    full_block_bytes = 100 * 8

    assert result["success"]
    assert result["bytes_sent"] < full_block_bytes


# more realistic graphene test
def test_graphene_with_partial_overlap():
    block = set(range(100))
    mempool = set(range(20, 500))  # missing 20 block txs: 0..19

    protocol = GrapheneProtocol()
    result = protocol.run(block, mempool)

    assert result["protocol"] == "graphene"
    assert result["block_size"] == 100
    assert result["mempool_size"] == 480
    assert result["bytes_sent"] > 0
