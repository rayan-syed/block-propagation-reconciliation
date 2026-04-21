from src.experiments.sweeps import sweep
from src.protocols.full_block import FullBlockProtocol
from src.core.set_generator import generate_sender_receiver_sets


def test_sweep():
    protocol = FullBlockProtocol(tx_size=250)

    df = sweep(
        protocol=protocol,
        sweep_param="overlap",
        values=[0.0, 1.0],
        fixed_params={"block_size": 100, "mempool_size": 200, "overlap": 1.0},
        trials=2,
        generator=generate_sender_receiver_sets,
        seed=42,
    )

    assert len(df) == 4
    assert set(df["overlap"]) == {0.0, 1.0}
