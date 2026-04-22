import argparse
import os

import yaml
import pandas as pd

from src.experiments.sweeps import sweep
from src.experiments.plotting import plot_experiment, plot_success
from src.protocols.full_block import FullBlockProtocol
from src.protocols.compact_block import CompactBlockProtocol
from src.protocols.graphene import GrapheneProtocol
from src.protocols.graphene_fallback import GrapheneFallbackProtocol
from src.core.set_generator import generate_sender_receiver_sets


def build_protocol(spec):
    name = spec["name"]

    if name == "full_block":
        return FullBlockProtocol(tx_size=spec.get("tx_size", 250))

    if name == "compact_block":
        return CompactBlockProtocol(
            tx_size=spec.get("tx_size", 250),
            short_id_size=spec.get("short_id_size", 6),
            header_size=spec.get("header_size", 80),
            nonce_size=spec.get("nonce_size", 8),
            prefilled=spec.get("prefilled", 1),
        )

    if name == "graphene":
        return GrapheneProtocol(
            cell_size=spec.get("cell_size", 12),
            iblt_hashes=spec.get("iblt_hashes", 3),
            iblt_factor=spec.get("iblt_factor", 12),
            delta=spec.get("delta", 0.5),
            max_search_a=spec.get("max_search_a", 64),
        )

    if name == "graphene_fallback":
        return GrapheneFallbackProtocol(
            tx_size=spec.get("tx_size", 250),
            txid_size=spec.get("txid_size", 8),
            cell_size=spec.get("cell_size", 12),
            iblt_hashes=spec.get("iblt_hashes", 3),
            iblt_factor=spec.get("iblt_factor", 12),
            delta=spec.get("delta", 0.5),
            max_search_a=spec.get("max_search_a", 64),
        )

    raise ValueError(f"unknown protocol: {name}")


def expand_experiment(experiment):
    mode = experiment["mode"]
    configs = []

    if mode == "overlap":
        block_size = experiment["block_size"]
        mempool_size = experiment["mempool_size"]

        for overlap in experiment["values"]:
            configs.append(
                {
                    "block_size": block_size,
                    "mempool_size": mempool_size,
                    "overlap": overlap,
                }
            )

    elif mode == "mempool_size":
        block_size = experiment["block_size"]
        overlap = experiment["overlap"]

        for mempool_size in experiment["values"]:
            configs.append(
                {
                    "block_size": block_size,
                    "mempool_size": mempool_size,
                    "overlap": overlap,
                }
            )

    elif mode == "block_size":
        overlap = experiment["overlap"]

        if "mempool_factor" in experiment:
            factor = experiment["mempool_factor"]

            for block_size in experiment["values"]:
                configs.append(
                    {
                        "block_size": block_size,
                        "mempool_size": factor * block_size,
                        "overlap": overlap,
                    }
                )
        else:
            mempool_size = experiment["mempool_size"]

            for block_size in experiment["values"]:
                configs.append(
                    {
                        "block_size": block_size,
                        "mempool_size": mempool_size,
                        "overlap": overlap,
                    }
                )

    else:
        raise ValueError(f"unknown experiment mode: {mode}")

    return configs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    output_dir = cfg.get("output_dir", "results")
    os.makedirs(output_dir, exist_ok=True)

    trials = cfg.get("trials", 3)
    seed = cfg.get("seed", 42)

    all_results = []

    for protocol_spec in cfg["protocols"]:
        protocol = build_protocol(protocol_spec)
        protocol_name = protocol_spec["name"]

        for experiment in cfg["experiments"]:
            experiment_name = experiment["name"]
            configs = expand_experiment(experiment)

            df = sweep(
                protocol=protocol,
                configs=configs,
                trials=trials,
                generator=generate_sender_receiver_sets,
                seed=seed,
            )

            df["experiment"] = experiment_name
            df["protocol_name"] = protocol_name

            out_path = os.path.join(
                output_dir, f"{protocol_name}__{experiment_name}.csv"
            )
            df.to_csv(out_path, index=False)

            print(f"\nSaved: {out_path}")
            print(df.groupby(experiment["group_by"])["bytes_sent"].mean())

            all_results.append(df)

    merged = pd.concat(all_results, ignore_index=True)
    merged_path = os.path.join(output_dir, "all_results.csv")
    merged.to_csv(merged_path, index=False)

    print(f"\nSaved: {merged_path}")

    fig_dir = os.path.join(output_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    for experiment in cfg["experiments"]:
        experiment_name = experiment["name"]
        x_col = experiment["group_by"]

        exp_df = merged[merged["experiment"] == experiment_name]
        plot_experiment(exp_df, experiment_name, x_col, fig_dir)
        plot_success(exp_df, experiment_name, x_col, fig_dir)


if __name__ == "__main__":
    main()
