from src.experiments.sweep_overlap import sweep_overlap
from src.protocols.full_block import FullBlockProtocol
from src.core.set_generator import generate_sender_receiver_sets


def test_sweep_overlap():
    protocol = FullBlockProtocol()

    df = sweep_overlap(
        protocol=protocol,
        block_size=100,
        mempool_size=200,
        overlaps=[0.0, 0.5, 1.0],
        trials=2,
        generator=generate_sender_receiver_sets,
        seed=42,
    )

    assert len(df) == 6
    assert set(df["overlap"]) == {0.0, 0.5, 1.0}
