from collections import defaultdict

def build_debruijn_graph(kmers):
    graph = defaultdict(list)
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        graph[prefix].append(suffix)
    return graph

def calculate_degrees(graph):
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for node in graph:
        out_degree[node] = len(graph[node])
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Garante que todos os nós estão presentes no in_degree
    for node in graph:
        if node not in in_degree:
            in_degree[node] = in_degree[node]  # seta zero se não existir

    return in_degree, out_degree

def maximal_non_branching_paths(graph):
    in_degree, out_degree = calculate_degrees(graph)
    paths = []

    visited_edges = set()

    for node in graph:
        if not (in_degree[node] == 1 and out_degree[node] == 1):
            if out_degree[node] > 0:
                for neighbor in graph[node]:
                    edge = (node, neighbor)
                    if edge in visited_edges:
                        continue
                    visited_edges.add(edge)
                    path = [node, neighbor]
                    while (in_degree[neighbor] == 1 and out_degree[neighbor] == 1):
                        next_node = graph[neighbor][0]
                        path.append(next_node)
                        visited_edges.add((neighbor, next_node))
                        neighbor = next_node
                    paths.append(path)

    # Check for isolated cycles
    for node in graph:
        if (in_degree[node] == 1 and out_degree[node] == 1):
            neighbor = graph[node][0] if graph[node] else None
            if neighbor is None:
                continue
            edge = (node, neighbor)
            if edge in visited_edges:
                continue
            path = [node, neighbor]
            visited_edges.add(edge)
            while (neighbor != node):
                if len(graph[neighbor]) == 0:
                    break
                next_node = graph[neighbor][0]
                edge = (neighbor, next_node)
                if edge in visited_edges:
                    break
                path.append(next_node)
                visited_edges.add(edge)
                neighbor = next_node
            paths.append(path)

    return paths

def path_to_string(path):
    result = path[0]
    for node in path[1:]:
        result += node[-1]
    return result

def generate_contigs(kmers):
    graph = build_debruijn_graph(kmers)
    paths = maximal_non_branching_paths(graph)
    contigs = [path_to_string(path) for path in paths]
    return contigs


# --------- Exemplo com os dados fornecidos ---------
kmers = [
    "ATG",
    "ATG",
    "TGT",
    "TGG",
    "CAT",
    "GGA",
    "GAT",
    "AGA"
]

result = generate_contigs(kmers)

for contig in result:
    print(contig)
