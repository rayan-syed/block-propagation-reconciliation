import pandas as pd
from src.experiments.runner import run_trials


def sweep(protocol, sweep_param, values, fixed_params, trials, generator, seed=0):
    dfs = []

    for value in values:
        params = fixed_params.copy()
        params[sweep_param] = value

        df = run_trials(
            protocol=protocol,
            block_size=params["block_size"],
            mempool_size=params["mempool_size"],
            overlap=params["overlap"],
            trials=trials,
            generator=generator,
            seed=seed,
        )

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
