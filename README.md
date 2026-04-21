# block-propagation-reconciliation

A simulation framework for evaluating Graphene-based blockchain block propagation against baseline methods under varying mempool, block, and overlap conditions.

## Overview

This project simulates and compares three block propagation strategies:

- Full Block – sends all transactions directly  
- Compact Block – sends short transaction IDs and recovers missing transactions  
- Graphene – uses Bloom filters + IBLT for set reconciliation  

The framework measures communication cost (bytes sent) under different system conditions:
- block size  
- mempool size  
- overlap between sender and receiver  

Experiments are config-driven using YAML.

## How to Run

A python environment is required to run this project. Start by installing the requirements with:
```bash
pip install -r requirements.txt
```

After that experiments can be run with the following command from the project root:
```bash
python -m scripts.run_experiments --config configs/sample_experiments.yaml
```

Feel free to edit or create new YAML files (see `configs/sample_experiments.yaml`) to define new experiments. Parameters can include protocols to evaluate, experiment types, parameter ranges, and number of trials.

All results will be saved to `results/<run_name>/`. For now the results folder only includes `.csv` file outputs.

## Structure

```
src/
  core/                       # set generation
  structures/                 # Bloom filter, IBLT
  protocols/                  # Full, Compact, Graphene
  experiments/                # runner + sweeps

scripts/ 
  run_experiments.py          # script to run all experiments

configs/
  sample_experiments.yaml     # sample experiment configuration

tests/                        # unit tests for core components and experiments
```

## Notes

- Implementations are simplified abstractions of the original protocols and are designed for controlled experimental comparison rather than exact reproduction of production systems
- Graphene parameters are selected via cost minimization (search over a)
- Experiments are deterministic (fixed seeds)
- Standard Graphene (as implemented here) assumes full overlap between sender and receiver; partial overlap requires additional recovery mechanisms not included in this implementation for now. Thus, overlap < 1.0 will violate current assumptions
