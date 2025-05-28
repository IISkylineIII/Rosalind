import re
from collections import defaultdict


def parse_genome_graph(s):
    g = defaultdict(list)
    for component in re.findall(r"\((.+?)\)", s):
        component = list(map(int, component.split()))
        for i in range(len(component) - 1):
            g[component[i]].append(-component[i + 1])
            g[-component[i + 1]].append(component[i])
        g[component[-1]].append(-component[0])
        g[-component[0]].append(component[-1])
    return g


def format_perm(component):
    return "(" + " ".join(f"{i:+d}" for i in component) + ")"


def format_genome_graph(graph):
    nodes = set(graph.keys())
    components = []

    while nodes:
        node = nodes.pop()
        comp = []
        queue = [node]

        while queue:
            current = queue.pop()
            comp.append(current)
            for neighbor in graph[current]:
                if -neighbor not in comp and neighbor not in comp:
                    queue.append(-neighbor)

        nodes -= set(comp)
        nodes -= set(-x for x in comp)
        components.append(comp)

    return "".join(format_perm(c) for c in components)


def add_edge(graph, i, j):
    graph[i].append(j)
    graph[j].append(i)


def del_edge(graph, i, j):
    graph[i].remove(j)
    graph[j].remove(i)


def breakpoint_graph(p, q):
    bg = {}
    for node in p.keys():
        bg[node] = p[node] + q[node]
    return bg


def find_component(node, graph):
    queue = [node]
    visited = set()

    while queue:
        node = queue.pop(0)
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)

    return visited


def find_components(graph):
    nodes = set(graph.keys())
    while nodes:
        comp = find_component(next(iter(nodes)), graph)
        nodes -= comp
        yield comp


def non_trivial_cycle_nodes(graph):
    for c in find_components(graph):
        if len(c) > 2:
            return list(c)
    return None



def ba6d(P, Q):
    bg = breakpoint_graph(P, Q)
    nodes = non_trivial_cycle_nodes(bg)
    yield format_genome_graph(P)

    while nodes:
        j = nodes[0]
        i2 = Q[j][0]

        i = P[j][0]
        j2 = P[i2][0]

        del_edge(P, i, j)
        del_edge(P, i2, j2)

        add_edge(P, j, i2)
        add_edge(P, j2, i)

        yield format_genome_graph(P)

        bg = breakpoint_graph(P, Q)
        nodes = non_trivial_cycle_nodes(bg)


def main():
    with open("rosalind_ba6d.txt") as file:
        lines = file.read().splitlines()

    P = parse_genome_graph(lines[0])
    Q = parse_genome_graph(lines[1])

    for genome in ba6d(P, Q):
        print(genome)


if __name__ == "__main__":
    main()
