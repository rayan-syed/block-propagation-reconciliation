import os
import matplotlib.pyplot as plt


def plot_experiment(df, experiment_name, x_col, output_dir):
    summary = (
        df.groupby(["protocol_name", x_col])["bytes_sent"]
        .mean()
        .reset_index()
        .sort_values(x_col)
    )

    label_map = {
        "full_block": "Full Block",
        "compact_block": "Compact Block",
        "graphene": "Graphene",
    }

    title_map = {
        "block_size_sweep": "Communication Cost vs Block Size",
        "mempool_size_sweep": "Communication Cost vs Mempool Size",
        "overlap_sweep": "Communication Cost vs Overlap",
    }

    plt.figure(figsize=(7, 5))

    for protocol_name in ["full_block", "compact_block", "graphene"]:
        if protocol_name not in summary["protocol_name"].values:
            continue

        sub = summary[summary["protocol_name"] == protocol_name]

        plt.plot(
            sub[x_col],
            sub["bytes_sent"],
            marker="o",
            label=label_map[protocol_name],
        )

    plt.yscale("log")
    plt.xlabel(x_col.replace("_", " ").title())
    plt.ylabel("Communication Cost (bytes)")
    plt.title(title_map.get(experiment_name, experiment_name))
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(output_dir, f"{experiment_name}.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"saved plot: {out_path}")
