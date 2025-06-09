from collections import defaultdict, deque

def topological_ordering(edges):
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    nodes = set()

    # Construir o grafo e calcular grau de entrada
    for edge in edges:
        u, v = edge
        graph[u].append(v)
        in_degree[v] += 1
        nodes.add(u)
        nodes.add(v)

    # Encontrar nós com grau de entrada zero
    zero_in_degree = deque([node for node in nodes if in_degree[node] == 0])

    order = []
    while zero_in_degree:
        u = zero_in_degree.popleft()
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                zero_in_degree.append(v)

    # Se a ordem contém todos os nós, retornamos, senão tem ciclo
    if len(order) == len(nodes):
        return order
    else:
        return []  # Grafo não é acíclico

# Exemplo com o dataset de amostra
input_data = [
    (1, 2),
    (2, 3),
    (4, 2),
    (5, 3)
]

result = topological_ordering(input_data)
print(", ".join(map(str, result)))
