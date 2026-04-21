import pandas as pd


def run_trials(protocol, block_size, mempool_size, overlap, trials, generator, seed=0):
    rows = []

    for t in range(trials):
        block, mempool = generator(
            block_size=block_size,
            mempool_size=mempool_size,
            overlap=overlap,
            seed=seed + t,
        )

        result = protocol.run(block, mempool)

        row = {
            "trial": t,
            "block_size": block_size,
            "mempool_size": mempool_size,
            "overlap": overlap,
        }

        row.update(result)
        rows.append(row)

    return pd.DataFrame(rows)
