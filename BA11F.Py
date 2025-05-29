from math import inf

def mass():
    return {
        'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101,
        'C': 103, 'I': 113, 'L': 113, 'N': 114, 'D': 115,
        'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137,
        'F': 147, 'R': 156, 'Y': 163, 'W': 186
    }

def masses():
    return mass()

def peptide_mass(peptide, masses):
    return sum(masses[x] for x in peptide)

def peptide2vector(peptide, masses):
    vec = [0] * (peptide_mass(peptide, masses) + 1)
    for i in range(len(peptide) + 1):
        vec[peptide_mass(peptide[:i], masses)] = 1
    return vec[1:]

def peptide_identification(sv, proteome):
    m = masses()
    best_score = -inf
    best_peptide = ""
    for i in range(len(proteome)):
        for j in range(i + 1, len(proteome)):
            pv = peptide2vector(proteome[i:j], m)
            if len(pv) > len(sv):
                break
            if len(pv) == len(sv):
                score = sum(a * b for a, b in zip(pv, sv))
                if score > best_score:
                    best_score = score
                    best_peptide = proteome[i:j]
    return best_peptide, best_score


file_path = 'rosalind_ba11f (9).txt'

with open(file_path, 'r') as f:
    lines = f.read().splitlines()
    sv_str = lines[0]
    proteome = lines[1]

sv = list(map(int, sv_str.split()))

peptide, score = peptide_identification(sv, proteome)

print(peptide)
