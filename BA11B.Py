mass_table = {
    'G': 57,  'A': 71,  'S': 87,  'P': 97,  'V': 99,
    'T': 101, 'C': 103, 'I': 113, 'L': 113, 'N': 114,
    'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131,
    'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186
}

mass_to_aa = {}
for aa, mass in mass_table.items():
    mass_to_aa.setdefault(mass, []).append(aa)

def spectrum_graph(ions):
    ions = sorted(ions)
    graph = {}
    for w in ions:
        edges = []
        for v in ions:
            diff = v - w
            if diff > 0 and diff in mass_to_aa:
                aa = mass_to_aa[diff][0]  # primeiro aminoácido válido
                edges.append({"n": v, "l": aa})
        graph[w] = edges
    return graph

def full(ions):
    def infer_peptide(w, seq, seen):
        # Parada: comprimento do peptídeo igual à metade do espectro (pois cada aa adiciona uma massa)
        if len(seq) == len(ions) // 2:
            yield seq
        for k in graph[w]:
            if k["n"] not in seen:
                yield from infer_peptide(k["n"], seq + k["l"], seen + [w])

    graph = spectrum_graph(ions)
    yield from infer_peptide(min(ions), "", [])

def decode_ideal_spectrum(spectrum):
    ions = [0] + sorted(spectrum)
    peptides = list(full(ions))
    return peptides[0] if peptides else None

new_spectrum = [
    71, 101, 168, 232, 239, 361, 368, 458, 481, 571, 609, 670, 772, 783,
    898, 928, 1041, 1061, 1164, 1188, 1278, 1302, 1405, 1425, 1538, 1568,
    1683, 1694, 1796, 1857, 1895, 1985, 2008, 2098, 2105, 2227, 2234, 2298,
    2365, 2395, 2466
]

result = decode_ideal_spectrum(new_spectrum)
print(result)
