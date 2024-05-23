import sys
import networkx as nx
import numpy as np
import random

filename = sys.argv[1]

DAG = nx.read_gml(filename)

mapping = {str(node): int(node) for node in DAG.nodes()}
DAG = nx.relabel_nodes(DAG, mapping)

topo = list(nx.topological_sort(DAG))

nodes = len(DAG)
coeff = sys.argv[2]
if len(sys.argv) > 3:
    depth = sys.argv[3]
else:
    depth = len(nx.dag_longest_path(DAG))
edges = []
for edge in DAG.edges():
    edges.append(edge)
All_mem = 0
for i in range(nodes):
    All_mem += int(DAG.nodes()[i]['parameter'])

gen_cp_parse = filename[9:-4] # To parse graphgml/ and .gml (adjust on your need)

def generate_cp(nodes, depth, edges):
    nodes = int(nodes)
    depth = int(depth)
    code = "from ortools.sat.python import cp_model\n"
    code += "import time\n"
    code += "\n"
    code += "def main() -> None:\n"
    code += "\tmodel = cp_model.CpModel()\n"
    code += f"\tvar_upper_bound1 = {depth}\n"
    code += f"\tvar_upper_bound2 = 1\n"
    code += f"\tvar_upper_bound3 = {depth-1}*{nodes}*{depth}\n"
    code += f"\tvar_upper_bound4 = {All_mem}\n"
    for n in range(nodes):
        code += f"\tv{n} = model.NewIntVar(1, var_upper_bound1, \"v{n}\")\n"
    for n in range(nodes):
        for d in range(depth):
            code += f"\tvs{n}_{d} = model.NewIntVar(0, var_upper_bound2, \"vs{n}_{d}\")\n"
    for d in range(depth-1):
        code += f"\tm{d} = model.NewIntVar(0, var_upper_bound3, \"m{d}\")\n"
        for i in range(len(edges)):
            code += f"\tm{d}_{i} = model.NewIntVar(0, var_upper_bound3, \"m{d}_{i}\")\n"
            code += f"\tcc{i}_{d}_a = model.NewIntVar(0, var_upper_bound3, \"cc{i}_{d}_a\")\n"
            code += f"\tcc{i}_{d}_b = model.NewIntVar(0, var_upper_bound3, \"cc{i}_{d}_b\")\n"
            code += f"\tcc{i}_{d}_c = model.NewIntVar(0, var_upper_bound3, \"cc{i}_{d}_c\")\n"
    code += f"\tr = model.NewIntVar(0, var_upper_bound4, \"r\")\n"
    for n in range(nodes):
        code += f"\tmodel.Add(vs{n}_0"
        for d in range(depth-1):
            code += f" + vs{n}_{d+1}"
        code += " == 1)\n"
        code += f"\tmodel.Add(vs{n}_0"
        for d in range(depth-1):
            code += f" + {d+2} * vs{n}_{d+1}"
        code += f" - v{n} == 0)\n"
    for d in range(depth):
        ns0 = int(DAG.nodes()[0]['parameter'])
        code += f"\tmodel.Add({ns0} * vs0_{d}"
        for n in range(nodes-1):
            code += f" + {int(DAG.nodes()[n+1]['parameter'])} * vs{n+1}_{d}"
        code += " - r <= 0)\n"
    for i,e in enumerate(edges):
        code += f"\tmodel.Add(v{e[0]} - v{e[1]} <= 0)\n"
        code += f"\tmodel.Add(vs{e[0]}_0 - cc{i}_0_a == 0)\n"
        code += f"\tmodel.Add(vs{e[1]}_1"
        for d in range(depth-2):
            code += f" + vs{e[1]}_{d+2}"
        code += f" - cc{i}_0_b == 0)\n"
        code += f"\tmodel.Add(cc{i}_0_a + cc{i}_0_b - cc{i}_0_c == 1)\n"
        a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
        if a > 0:
            a = 1
        code += f"\tmodel.Add({a} * cc{i}_0_c - m0_{i} == 0)\n"
    for d in range(depth-3):
        for i,e in enumerate(edges):
            code += f"\tmodel.Add(vs{e[0]}_0"
            for dp in range(d+1):
                code += f" + vs{e[0]}_{dp+1}"
            code += f" - cc{i}_{d+1}_a == 0)\n"
            code += f"\tmodel.Add(vs{e[1]}_{dp+2}"
            for dpr in range(depth-dp-3):
                code += f" + vs{e[1]}_{dpr+dp+3}"
            code += f" - cc{i}_{d+1}_b == 0)\n"
            code += f"\tmodel.Add(cc{i}_{d+1}_a + cc{i}_{d+1}_b - cc{i}_{d+1}_c == 1)\n"
            a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
            if a > 0:
                a = 1
            code += f"\tmodel.Add({a} * cc{i}_{d+1}_c - m{d+1}_{i} == 0)\n"
    
    for i,e in enumerate(edges):
        code += f"\tmodel.Add(vs{e[0]}_0"
        for dp in range(depth-2):
            code += f" + vs{e[0]}_{dp+1}"
        code += f" - cc{i}_{depth-2}_a == 0)\n"
        code += f"\tmodel.Add(vs{e[1]}_{dp+2} - cc{i}_{depth-2}_b == 0)\n"
        code += f"\tmodel.Add(cc{i}_{depth-2}_a + cc{i}_{depth-2}_b - cc{i}_{depth-2}_c == 1)\n"
        a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
        if a > 0:
            a = 1
        code += f"\tmodel.Add({a} * cc{i}_{depth-2}_c - m{depth-2}_{i} == 0)\n"

    for d in range(depth-1):
        code += f"\tmodel.Add(m{d}_{0}"
        for i in range(len(edges)-1):
                code += f" + m{d}_{i+1}"
        code += f" - m{d} == 0)\n"
    
    code += f"\tobjective = {coeff} * r"
    for d in range(depth-1):
        code += f" + m{d}"
    code += "\n"
    code += "\tmodel.Minimize(objective)\n"
    code += "\tsolver = cp_model.CpSolver()\n"

    code += "\tclass IntermediateSolutionPrinter(cp_model.CpSolverSolutionCallback):\n"
    code += "\t\tdef __init__(self, objective):\n"
    code += "\t\t\tcp_model.CpSolverSolutionCallback.__init__(self)\n"
    code += "\t\t\tself._objective = objective\n"
    code += "\t\t\tself._solution_count = 0\n"
    code += "\t\t\tself._start_time = time.time()\n"
    code += "\t\tdef on_solution_callback(self):\n"
    code += "\t\t\tself._solution_count += 1\n"
    code += "\t\t\tprint(\"Solution #%i:\" % self._solution_count)\n"
    code += "\t\t\tprint(f\"  Objective value: {self.Value(self._objective)}\")\n"
    code += "\t\t\tcurrent_time = time.time()\n"
    code += "\t\t\telapsed_time = current_time - self._start_time\n"
    code += "\t\t\tprint(f\"  Time elapsed: {elapsed_time:.5f} seconds\")\n"
    code += "\t\t\tprint(\"-----------------\")\n"

    code += "\tsolution_printer = IntermediateSolutionPrinter(objective)\n"
    code += "\tstatus = solver.SolveWithSolutionCallback(model, solution_printer)\n"

    code += "\tif status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:\n"
    code += "\t\tprint(f\"Minimum of objective function: {solver.ObjectiveValue()}\\n\")\n"
    code += "\telse:\n"
    code += "\t\tprint(\"No solution found.\")\n"

    code += "\tprint(f\"Wall time: {solver.WallTime()} s\")\n"

    code += "if __name__ == \"__main__\":\n"
    code += "\tmain()"

    return code

generated_code = generate_cp(nodes, depth, edges)

with open(gen_cp_parse+f"_{coeff}_cp.py", "w") as file:
        file.write(generated_code)

