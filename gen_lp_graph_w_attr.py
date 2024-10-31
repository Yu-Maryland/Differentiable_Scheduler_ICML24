import sys
import networkx as nx
import numpy as np
import random

filename = sys.argv[1]

DAG = nx.read_gml(filename)

mapping = {str(node): int(node) for node in DAG.nodes()}
DAG = nx.relabel_nodes(DAG, mapping)
nodes = len(DAG)

topo = list(nx.topological_sort(DAG))
coeff = sys.argv[2]
if len(sys.argv) > 3:
        depth = sys.argv[3]
else:
        depth = len(nx.dag_longest_path(DAG))
edges = []
for edge in DAG.edges():
        edges.append(edge)

gen_lp_parse = filename[9:-4] # To pass graphgml/ and .gml

def generate_lp(nodes, depth, edges):
        nodes = int(nodes)
        depth = int(depth)
        code = '''Minimize'''
        code += "\n"
        code += f" obj1: {coeff} r"
        for d in range(depth-1):
                code += f" + m{d}"
        code += "\n"
        code += "Subject To\n"
        for n in range(nodes):
                    code += f" st{n}: vs{n}_0"
                    for d in range(depth-1):
                            code += f" + vs{n}_{d+1}"
                    code += f" = 1\n"
                    code += f" no{n}: vs{n}_0"
                    for d in range(depth-1):
                            code += f" + {d+2} vs{n}_{d+1}"
                    code += f" - v{n} = 0\n"
        for d in range(depth):
                    ns0 = int(DAG.nodes()[0]['parameter'])
                    code += f" de{d}: {ns0} vs0_{d}"
                    for n in range(nodes-1):
                            code += f" + {int(DAG.nodes()[n+1]['parameter'])} vs{n+1}_{d}"
                    code += f" - r <= 0\n"
        for i,e in enumerate(edges):
                    code += f" ed{i}: v{e[0]} - v{e[1]} <= 0\n"
                    code += f" c{i}c0a: vs{e[0]}_0 - cc{i}_0_a = 0\n"
                    code += f" c{i}c0b: vs{e[1]}_1"
                    for d in range(depth-2):
                            code += f" + vs{e[1]}_{d+2}"
                    code += f" - cc{i}_0_b = 0\n"
                    code += f" c{i}c0c: cc{i}_0_a + cc{i}_0_b - cc{i}_0_c = 1\n"
                    a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
                    if a > 0:
                        a = 1
                    code += f" c{i}c0: {a} cc{i}_0_c - m0_{i} = 0\n"
        
        for d in range(depth-3):
                    for i,e in enumerate(edges):
                            code += f" c{i}c{d+1}a: vs{e[0]}_0"
                            for dp in range(d+1):
                                    code += f" + vs{e[0]}_{dp+1}"
                            code += f" - cc{i}_{d+1}_a = 0\n"
                            code += f" c{i}c{d+1}b: vs{e[1]}_{dp+2}"
                            for dpr in range(depth-dp-3):
                                    code += f" + vs{e[1]}_{dpr+dp+3}"
                            code += f" - cc{i}_{d+1}_b = 0\n"
                            code += f" c{i}c{d+1}c: cc{i}_{d+1}_a + cc{i}_{d+1}_b - cc{i}_{d+1}_c = 1\n"
                            a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
                            if a > 0:
                                a = 1
                            code += f" c{i}c{d+1}: {a} cc{i}_{d+1}_c - m{d+1}_{i} = 0\n"

        for i,e in enumerate(edges):
                    code += f" c{i}c{depth-2}a: vs{e[0]}_0"
                    for dp in range(depth-2):
                            code += f" + vs{e[0]}_{dp+1}"
                    code += f" - cc{i}_{depth-2}_a = 0\n"
                    code += f" c{i}c{depth-2}b: vs{e[1]}_{dp+2} - cc{i}_{depth-2}_b = 0\n"
                    code += f" c{i}c{depth-2}c: cc{i}_{depth-2}_a + cc{i}_{depth-2}_b - cc{i}_{depth-2}_c = 1\n"
                    a = int(DAG.edges()[int(e[0]), int(e[1])]['parameter'])
                    if a > 0:
                        a = 1
                    code += f" c{i}c{depth-2}: {a} cc{i}_{depth-2}_c - m{depth-2}_{i} = 0\n"

        for d in range(depth-1):
                    code += f" cc{d}: m{d}_{0}"
                    for i in range(len(edges)-1):
                            code += f" + m{d}_{i+1}"
                    code += f" - m{d} = 0\n"


        code += "Bounds\n"
        for n in range(nodes):
                    code += f" 1 <= v{n} <= {depth}\n"
        code += "General\n"
        for n in range(nodes):
                code += f" v{n}"
        code += f" r"
        for d in range(depth-1):
                code += f" m{d}"
                for i in range(len(edges)):
                        code += f" m{d}_{i}"
                        code += f" cc{i}_{d}_a"
                        code += f" cc{i}_{d}_b"
                        code += f" cc{i}_{d}_c"
        code += "\n"
        code += "Binaries\n"
        for n in range(nodes):
                for d in range(depth):
                        code += f" vs{n}_{d}"
        code += "\n"
        code += "End"

        return code

generated_code = generate_lp(nodes, depth, edges)

with open(gen_lp_parse+f"_{coeff}.lp", "w") as file:
        file.write(generated_code)

