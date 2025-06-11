def read_input(filename):
    with open(filename, 'r') as f:
        spectrum = list(map(int, f.readline().strip().split()))
        proteome = f.readline().strip()
    return spectrum, proteome

# Tabela massa inteira padrão
mass_table = {
    'A':71, 'C':103, 'D':115, 'E':129, 'F':147,
    'G':57, 'H':137, 'I':113, 'K':128, 'L':113,
    'M':131, 'N':114, 'P':97,  'Q':128, 'R':156,
    'S':87, 'T':101, 'V':99,  'W':186, 'Y':163
}

def prefix_masses(peptide):
    prefix = [0]
    for aa in peptide:
        prefix.append(prefix[-1] + mass_table[aa])
    return prefix

def score_peptide(peptide, spectrum):
    prefix = prefix_masses(peptide)
    total_score = 0
    for mass in prefix:
        if mass < len(spectrum):
            total_score += spectrum[mass]
    return total_score

def find_best_peptide(spectrum, proteome):
    best_score = -1
    best_peptide = ""
    n = len(proteome)
    for i in range(n):
        for j in range(i+1, n+1):
            peptide = proteome[i:j]
            # Verifica se todos aminoácidos têm massa (para segurança)
            if all(aa in mass_table for aa in peptide):
                score = score_peptide(peptide, spectrum)
                if score > best_score:
                    best_score = score
                    best_peptide = peptide
    return best_peptide, best_score

if __name__ == "__main__":
    filename = "rosalind_ba11f (3).txt"
    spectrum, proteome = read_input(filename)
    best_peptide, best_score = find_best_peptide(spectrum, proteome)
    print("Melhor Peptídeo:", best_peptide)
    print("Score:", best_score)
