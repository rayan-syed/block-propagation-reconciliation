from src.experiments.runner import run_trials
from src.protocols.full_block import FullBlockProtocol
from src.core.set_generator import generate_sender_receiver_sets


def test_runner_returns_dataframe():
    protocol = FullBlockProtocol()

    df = run_trials(
        protocol=protocol,
        block_size=100,
        mempool_size=200,
        overlap=1.0,
        trials=5,
        generator=generate_sender_receiver_sets,
        seed=42,
    )

    assert len(df) == 5
    assert "protocol" in df.columns
    assert "bytes_sent" in df.columns
    assert "success" in df.columns
