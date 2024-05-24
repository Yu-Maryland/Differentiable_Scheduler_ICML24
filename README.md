# Differentiable Combinatorial Scheduling at Scale (ICML'24)

## Overview
This repository contains the implementation and scripts used for the experiments in the ICML'24 paper "Differentiable Combinatorial Scheduling at Scale". The experiments involve synthetic Directed Acyclic Graphs (DAGs) formulated as random workloads and real world EPFL design edgelists.

## Directory Structure (graphgml only for now)
```plaintext
graphgml: Contains synthetic graphs with random node weights and uniform edge weights.
el: Contains selected EPFL edgelist (modified format for this experiment use).
el_mapped: Contains select EPFL edgelist after technology mapping (To model more complex tasks).
```

## Scripts and Usage

### `gen_lp_graph_w_attr.py`
This script generates LP files based on the design (synthetic DAGs in .gml format).
- **Usage:** 
  ```bash
  python3 gen_lp_graph_w_attr.py <ratio> <depth> <name_design>
  ```
  - **Parameters:**
    - `ratio`: The ratio number added to the resource while optimizing.
    - `depth`: The number of preset levels for the design.
    - `name_design`: The name of the design.

### `gen_cp_graph_w_attr.py`
This script generates code for Constraint Programming (CP) based on the design.
- **Usage:** 
  ```bash
  python3 gen_cp_graph_w_attr.py <ratio> <depth> <name_design>
  ```
  - **Parameters:**
    - `ratio`: The ratio number added to the resource while optimizing.
    - `depth`: The number of preset levels for the design.
    - `name_design`: The name of the design.

### `parse_graph_w_attr.py`
This script parses design files and generates a differentiable scheduler neural network file. It is primarily part of the differentiable scheduler general solver but can be used separately for debugging.
- **Usage:** 
  ```bash
  python3 parse_graph_w_attr.py <name_design>
  ```
  - **Parameters:**
    - `name_design`: The name of the design.

### `scheduling_graph_w_attr_solver.sh`
This is the general solver for differentiable and combinatorial scheduling.
- **Usage:** 
  ```bash
  bash scheduling_graph_w_attr_solver.sh <temp> <lr> <depth> <batch> <name_design> <ratio>
  ```
  - **Parameters:**
    - `temp`: The initial temperature for the Gumbel Softmax function.
    - `lr`: The initial learning rate for the optimizer.
    - `depth`: The number of preset levels for the design.
    - `batch`: The batch size for neural network training.
    - `name_design`: The name of the design.
    - `ratio`: The ratio number added to the resource while optimizing.

## How to Run Experiments
To run the experiments on synthetic DAGs as described in the ICML'24 paper, use the provided scripts with the appropriate parameters as outlined above. Ensure all dependencies are installed and properly configured.
- CPLEX version: IBM(R) ILOG(R) CPLEX(R) Interactive Optimizer 22.1.1.0
- Gurobi version: gurobi10.0.3
- CP-SAT version: Google OR-Tools


## License

## Acknowledgments
