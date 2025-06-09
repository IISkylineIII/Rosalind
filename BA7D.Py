from collections import defaultdict

class Cluster:
    def __init__(self, nodes, age=0.0):
        self.nodes = nodes
        self.age = age

def upgma(distance_matrix, n):
    clusters = {i: Cluster([i]) for i in range(n)}
    ages = {i: 0.0 for i in range(n)}
    current_node = n
    D = {i: {j: distance_matrix[i][j] for j in range(n)} for i in range(n)}
    adj = defaultdict(list)

    while len(clusters) > 1:
        min_dist = float('inf')
        to_merge = (None, None)
        for i in clusters:
            for j in clusters:
                if i < j and D[i][j] < min_dist:
                    min_dist = D[i][j]
                    to_merge = (i, j)

        i, j = to_merge
        Ci, Cj = clusters[i], clusters[j]

        new_age = min_dist / 2
        Cnew = Cluster(Ci.nodes + Cj.nodes, age=new_age)
        clusters[current_node] = Cnew
        ages[current_node] = new_age

        adj[current_node].append((i, new_age - ages[i]))
        adj[current_node].append((j, new_age - ages[j]))
        adj[i].append((current_node, new_age - ages[i]))
        adj[j].append((current_node, new_age - ages[j]))

        # Calcula as distâncias do novo cluster para os outros antes de remover i e j
        D[current_node] = {}
        for k in clusters:
            if k != i and k != j and k != current_node:
                dist = (
                    len(Ci.nodes) * D[i][k] +
                    len(Cj.nodes) * D[j][k]
                ) / (len(Ci.nodes) + len(Cj.nodes))
                D[current_node][k] = dist
                D[k][current_node] = dist

        # Agora remove os clusters antigos
        del clusters[i]
        del clusters[j]

        # Remove as linhas antigas
        del D[i]
        del D[j]

        # Remove as colunas antigas
        for k in D:
            if i in D[k]:
                del D[k][i]
            if j in D[k]:
                del D[k][j]

        current_node += 1

    return adj

def print_adjacency(adj):
    for u in sorted(adj):
        for v, w in sorted(adj[u]):
            print(f"{u}->{v}:{w:.3f}")

def read_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    n = int(lines[0])
    matrix = []
    for line in lines[1:]:
        row = list(map(float, line.strip().split()))
        matrix.append(row)
    return n, matrix

# Reaproveita a função upgma e print_adjacency que já passamos antes

# Exemplo de uso:
filename = "rosalind_ba7d.txt"
n, matrix = read_input_file(filename)

adj = upgma(matrix, n)
print_adjacency(adj)
