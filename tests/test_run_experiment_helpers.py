from scripts.run_experiments import expand_experiment


def test_expand_overlap_experiment():
    experiment = {
        "mode": "overlap",
        "block_size": 100,
        "mempool_size": 200,
        "values": [0.0, 0.5, 1.0],
    }

    configs = expand_experiment(experiment)

    assert len(configs) == 3
    assert configs[0]["block_size"] == 100
    assert configs[0]["mempool_size"] == 200
    assert configs[2]["overlap"] == 1.0


def test_expand_block_size_with_factor():
    experiment = {
        "mode": "block_size",
        "overlap": 1.0,
        "mempool_factor": 5,
        "values": [50, 100],
    }

    configs = expand_experiment(experiment)

    assert configs == [
        {"block_size": 50, "mempool_size": 250, "overlap": 1.0},
        {"block_size": 100, "mempool_size": 500, "overlap": 1.0},
    ]
