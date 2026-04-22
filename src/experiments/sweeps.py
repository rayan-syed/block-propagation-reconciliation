import pandas as pd

from src.experiments.runner import run_trials


def sweep(protocol_builder, protocol_spec, configs, trials, generator, seed=0):
    dfs = []

    for config in configs:
        spec = {**protocol_spec, **config}

        protocol = protocol_builder(spec)

        df = run_trials(
            protocol=protocol,
            block_size=config["block_size"],
            mempool_size=config["mempool_size"],
            overlap=config["overlap"],
            trials=trials,
            generator=generator,
            seed=seed,
        )

        for k, v in config.items():
            df[k] = v

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)
