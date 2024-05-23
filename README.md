# Differentiable Combinatorial Scheduling at Scale (ICML'24)

### Directory
```bash
graphgml: Synthetic graph with random node weights and random uniform edge weights.
```
### How to run?
```bash 
Various scripts to run our experiments on Synthetic DAGs listed in ICML24 paper as Random Workloads.

gen_lp_graph_w_attr.py: Run to generate lp file based on the design (edgelist or synthetic DAGs under .gml format).
To use (example): python3 gen_lp_w_attr.py #ratio #depth name_design (where ratio is the ratio number added to resource while optimizing, depth is the number of preset level for the design)

gen_cp_graph_w_attr.py: Code generator for Constraint Programming (CP) based on the design.
To use (example): python3 gen_cp_graph_w_attr.py #ratio #depth name_design.

parse_graph_w_attr.py: Code Generator to parse design files and generate differentiable scheduler neural network file.
To use (example): python3 parse_graph_w_attr.py name_design (Note that, this is part of the differentiable scheduler general solver, only use separately for debugging)

scheduling_graph_w_attr_solver.sh: General solver for differentiable and combinatorial scheduling.
To use (example): bash scheduling_graph_w_attr_solver.sh #temp #lr #depth #batch #name_desgin #ratio (where temp is the initial temperature for Gumbel Softmax function, lr is the initial learning rate for the optimizer, depth is the number of preset level for the design, batch is the batch size for neural network training, ratio is the ratio number added to resource while optmizing)
```
