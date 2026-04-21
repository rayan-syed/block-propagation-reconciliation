from src.experiments.sweeps import sweep
from src.protocols.full_block import FullBlockProtocol
from src.core.set_generator import generate_sender_receiver_sets


def test_sweep_configs():
    protocol = FullBlockProtocol(tx_size=250)

    configs = [
        {"block_size": 100, "mempool_size": 200, "overlap": 0.0},
        {"block_size": 100, "mempool_size": 200, "overlap": 1.0},
    ]

    df = sweep(
        protocol=protocol,
        configs=configs,
        trials=2,
        generator=generate_sender_receiver_sets,
        seed=42,
    )

    assert len(df) == 4
    assert set(df["overlap"]) == {0.0, 1.0}
    assert set(df["block_size"]) == {100}
