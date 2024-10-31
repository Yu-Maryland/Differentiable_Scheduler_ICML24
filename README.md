# Differentiable Combinatorial Scheduling at Scale (ICML'24)

## Overview
This repository contains the implementation and scripts used for the experiments in the ICML'24 paper "Differentiable Combinatorial Scheduling at Scale". The experiments involve synthetic Directed Acyclic Graphs (DAGs) formulated as random workloads and real world EPFL design edgelists.

![Combined Animation](./1000_sparse_combine_full.gif)

## Directory Structure
```plaintext
(TBD: el and el_mapped)
graphgml: Contains synthetic graphs with random node weights and uniform edge weights.
el: Contains selected EPFL edgelist (modified format for this experiment use).
el_mapped: Contains select EPFL edgelist after technology mapping (To model more complex tasks).
```

## Scripts and Usage

### `gen_lp_graph_w_attr.py`
This script generates LP files based on the design (synthetic DAGs in .gml format). Use CPLEX or Gurobi to run the .lp file and obtain the schedule of all nodes.
- **Usage:** 
  ```bash
  python3 gen_lp_graph_w_attr.py <name_design> <ratio> <depth> 
  ```
  - **Parameters:**
    - `name_design`: The name of the design.
    - `ratio`: The ratio number added to the resource while optimizing.
    - `depth`: The number of preset levels for the design.

- **Example:**
  ```bash
  python3 gen_lp_graph_w_attr.py graphgml/rand_graph_1000_1.gm l100 10 
  cplex -c read rand_graph_1000_1_100.lp optimize write rand_graph_1000_1_100.sol sol
  gurobi_cl rand_graph_1000_1_100.lp
  ```

### `gen_cp_graph_w_attr.py`
This script generates code for Constraint Programming (CP) based on the design. This code generator uses CP-SAT solver within Google OR-Tools python built-in library. A python file will be generated and simply run the generated .py file to obtain the schedule of all nodes. 
- **Usage:** 
  ```bash
  python3 gen_cp_graph_w_attr.py <name_design> <ratio> <depth> 
  ```
  - **Parameters:**
    - `ratio`: The ratio number added to the resource while optimizing.
    - `depth`: The number of preset levels for the design.
    - `name_design`: The name of the design.

- **Example:**
  ```bash
  python3 gen_cp_graph_w_attr.py graphgml/rand_graph_1000_1.gm l100 10 
  python3 rand_graph_1000_1_100_cp.py
  ```

### `parse_graph_w_attr.py`
This script parses design files and generates a differentiable scheduler neural network file. It is primarily part of the differentiable scheduler general solver but can be used separately for debugging.
- **Usage:** 
  ```bash
  python3 parse_graph_w_attr.py <depth> <ratio> <name_design>
  ```
  - **Parameters:**
    - `depth`: The number of preset levels for the design. Default: Longest path of DAG.
    - `ratio`: The ratio number added to the resource while optimizing.
    - `name_design`: The name of the design.

- **Example:**
  ```bash
  python3 parse_graph_w_attr.py 10 100 graphgml/rand_graph_1000_1.gml
  ```

### `scheduling_graph_w_attr_solver.sh`
This is the general solver for differentiable and combinatorial scheduling. The schedule of all nodes will be generated after executing all epochs.
- **Usage:** 
  ```bash
  bash scheduling_graph_w_attr_solver.sh <temp> <lr> <depth> <batch> <name_design> <ratio>
  ```
  - **Parameters:**
    - `temp`: The initial temperature for the Gumbel Softmax function.
    - `lr`: The initial learning rate for the optimizer.
    - `depth`: The number of preset levels for the design. Default: Longest path of DAG.
    - `batch`: The batch size for neural network training.
    - `name_design`: The name of the design.
    - `ratio`: The ratio number added to the resource while optimizing.

- **Example:**
  ```bash
  bash scheduling_graph_w_attr_solver.sh 50 1 10 250 graphgml/rand_graph_1000_1.gml 100

## How to Run Experiments
To run the experiments on synthetic DAGs as described in the ICML'24 paper, use the provided scripts with the appropriate parameters as outlined above. Ensure all dependencies are installed and properly configured.
- CPLEX version: IBM(R) ILOG(R) CPLEX(R) Interactive Optimizer 22.1.1.0
- Gurobi version: Gurobi 10.0.3
- CP-SAT version: Python built-in Google OR-Tools
- Python version: Python 3.8.16
- CUDA version: V11.5.119
- NetworkX version: NetworkX 3.1

## License

MIT License

## Acknowledgments

This work is supported by National Science Foundation (NSF) under NSF-2047176, NSF-2019336, NSF-2008144, and NSF-2229562 awards, and University of Maryland.

## Bibtex

```
@inproceedings{liu2024differentiable,
  title={Differentiable Combinatorial Scheduling at Scale},
  author={Liu, Mingju and Li, Yingjie and Yin, Jiaqi and Zhang, Zhiru and Yu, Cunxi},
  booktitle={Proceedings of the 41st International Conference on Machine Learning (ICML'24)},
  year={2024}
}
```
