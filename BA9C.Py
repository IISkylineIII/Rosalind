class Node:
    def __init__(self):
        self.children = {}  # chave: primeiro caractere da aresta; valor: (aresta, nó)
        # aresta será representada por (start_index, length)

def edge_label(text, edge):
    start, length = edge
    return text[start:start+length]

def suffix_tree(text):
    root = Node()

    for i in range(len(text)):
        current = root
        suffix_start = i

        while suffix_start < len(text):
            c = text[suffix_start]
            if c not in current.children:
                # cria nova aresta e nó folha
                current.children[c] = ((suffix_start, len(text) - suffix_start), Node())
                break
            else:
                edge, next_node = current.children[c]
                label = edge_label(text, edge)
                # verificar o maior prefixo comum entre label e o sufixo começando em suffix_start
                lcp = 0
                while (lcp < len(label) and
                       suffix_start + lcp < len(text) and
                       text[suffix_start + lcp] == label[lcp]):
                    lcp += 1

                if lcp == len(label):
                    # andar para o próximo nó
                    current = next_node
                    suffix_start += lcp
                else:
                    # dividir a aresta
                    existing_edge = edge
                    existing_node = next_node

                    # criar nó intermediário
                    mid_node = Node()

                    # aresta para o nó intermediário (prefixo comum)
                    current.children[c] = ((existing_edge[0], lcp), mid_node)

                    # aresta remanescente para o nó existente
                    rem_start = existing_edge[0] + lcp
                    rem_length = existing_edge[1] - lcp
                    mid_node.children[text[rem_start]] = ((rem_start, rem_length), existing_node)

                    # aresta para o novo nó folha com o sufixo restante
                    new_start = suffix_start + lcp
                    new_length = len(text) - new_start
                    mid_node.children[text[new_start]] = ((new_start, new_length), Node())
                    break
    return root

def collect_edges(node, text):
    edges = []
    for c in node.children:
        edge, child = node.children[c]
        edges.append(edge_label(text, edge))
        edges.extend(collect_edges(child, text))
    return edges


# Exemplo com o dataset de exemplo
text = "ATAAATG$"
root = suffix_tree(text)
edges = collect_edges(root, text)

for e in edges:
    print(e)
