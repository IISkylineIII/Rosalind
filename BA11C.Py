# Tabela de massas inteiras dos aminoácidos padrão
mass_table = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99,
    'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
    'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131,
    'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186
}

def build_spectrum_graph(spectrum):
    spectrum = [0] + sorted(spectrum)  # Garantir que 0 esteja no início
    edges = []
    for i in range(len(spectrum)):
        for j in range(i+1, len(spectrum)):
            diff = spectrum[j] - spectrum[i]
            # Verifica se essa diferença é massa de algum aminoácido
            for aa, mass in mass_table.items():
                if mass == diff:
                    edges.append(f"{spectrum[i]}->{spectrum[j]}:{aa}")
                    break
    return edges

# Exemplo de entrada do problema
input_spectrum = [57, 71, 154, 185, 301, 332, 415, 429, 486]

# Construir o grafo
graph_edges = build_spectrum_graph(input_spectrum)

# Imprimir o resultado
for edge in graph_edges:
    print(edge)
