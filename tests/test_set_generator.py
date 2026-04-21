from src.core.set_generator import *


def test_sizes():
    block, mempool = generate_sender_receiver_sets(100, 200, 0.5)
    assert len(block) == 100
    assert len(mempool) == 200


def test_full_overlap():
    block, mempool = generate_sender_receiver_sets(100, 200, 1.0)
    assert block.issubset(mempool)


def test_zero_overlap():
    block, mempool = generate_sender_receiver_sets(100, 200, 0.0)
    assert len(block & mempool) == 0
