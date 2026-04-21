import pandas as pd

from src.experiments.runner import run_trials


def sweep_overlap(
    protocol, block_size, mempool_size, overlaps, trials, generator, seed=0
):
    dfs = []

    for overlap in overlaps:
        df = run_trials(
            protocol=protocol,
            block_size=block_size,
            mempool_size=mempool_size,
            overlap=overlap,
            trials=trials,
            generator=generator,
            seed=seed,
        )
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
