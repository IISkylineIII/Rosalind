import re
from copy import copy

def format_perm(perm):
    return "(" + " ".join([f"{x:+}" for x in perm]) + ")"

def ints(x):
    return list(map(int, x.split(", ")))

def cycle2chromosome(cycle):
    nodes = []
    for j1, j2 in zip(cycle[::2], cycle[1::2]):
        if j1 < j2:
            nodes.append(j2 // 2)
        else:
            nodes.append(-j1 // 2)
    return nodes

def first_key(g):
    return list(g.keys())[0]

def find_node_cycle(graph):
    start = first_key(graph)
    a = start
    component = []
    while graph:
        b = graph.pop(a)
        graph.pop(b)
        n = b + 1 if b % 2 == 1 else b - 1
        if n == start:
            return [b] + component + [a]
        component += [a, b]
        a = n

def find_node_cycles(graph):
    graph = copy(graph)
    for k, v in list(graph.items()):
        graph[v] = k
    while graph:
        yield find_node_cycle(graph)

def graph2genome(genome_graph):
    genome = []
    for nodes in find_node_cycles(genome_graph):
        genome.append(cycle2chromosome(nodes))
    return genome

def parse_edge_string(s):
    g = {}
    for x in re.findall(r"\((.+?)\)", s):
        a, b = ints(x)
        g[a] = b
    return g

def main():
    # Substitua o caminho pelo local correto do arquivo em seu sistema
    with open("rosalind_ba6i (2).txt") as f:
        s = f.read().strip()
    genome_graph = parse_edge_string(s)
    genome = graph2genome(genome_graph)
    print(*[format_perm(x) for x in genome], sep="")

if __name__ == "__main__":
    main()
