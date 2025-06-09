from collections import Counter
from itertools import combinations, product


def spectrum_convolution(spectrum):
    """Compute the convolution of a spectrum."""
    convolution = []
    for a in spectrum:
        for b in spectrum:
            if a > b:
                diff = a - b
                if 57 <= diff <= 200:  # Only valid amino acid masses
                    convolution.append(diff)
    return convolution


def get_top_m_masses(convolution, M):
    """Get the top M most frequent masses between 57 and 200 (with ties)."""
    counter = Counter(convolution)
    sorted_items = counter.most_common()
    result = []

    if M >= len(sorted_items):
        return [mass for mass, count in sorted_items]

    threshold = sorted_items[M - 1][1]
    for mass, count in sorted_items:
        if count >= threshold:
            result.append(mass)
        else:
            break
    return result


def linear_spectrum(peptide):
    """Compute the linear spectrum of a peptide."""
    prefix_mass = [0]
    for aa in peptide:
        prefix_mass.append(prefix_mass[-1] + aa)
    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i + 1, len(prefix_mass)):
            spectrum.append(prefix_mass[j] - prefix_mass[i])
    return sorted(spectrum)


def cyclic_spectrum(peptide):
    """Compute the cyclic spectrum of a peptide."""
    prefix_mass = [0]
    for aa in peptide:
        prefix_mass.append(prefix_mass[-1] + aa)
    peptide_mass = prefix_mass[-1]
    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i + 1, len(prefix_mass)):
            spectrum.append(prefix_mass[j] - prefix_mass[i])
            if i > 0 and j < len(prefix_mass) - 1:
                spectrum.append(peptide_mass - (prefix_mass[j] - prefix_mass[i]))
    return sorted(spectrum)


def score(peptide, spectrum, cyclic=True):
    """Compute the score of a peptide against a spectrum."""
    if cyclic:
        theo_spectrum = cyclic_spectrum(peptide)
    else:
        theo_spectrum = linear_spectrum(peptide)
    theo_counter = Counter(theo_spectrum)
    exp_counter = Counter(spectrum)
    return sum(min(theo_counter[k], exp_counter[k]) for k in theo_counter)


def trim(leaderboard, spectrum, N):
    """Trim the leaderboard to keep top N scoring peptides (with ties)."""
    scored = [(peptide, score(peptide, spectrum, cyclic=False)) for peptide in leaderboard]
    scored.sort(key=lambda x: x[1], reverse=True)
    if len(scored) <= N:
        return [x[0] for x in scored]

    threshold = scored[N - 1][1]
    return [pep for pep, sc in scored if sc >= threshold]


def convolution_cyclopeptide_sequencing(spectrum, M, N):
    """Main function to perform convolution cyclopeptide sequencing."""
    parent_mass = max(spectrum)
    convolution = spectrum_convolution(spectrum)
    amino_acids = get_top_m_masses(convolution, M)

    leaderboard = [[]]
    leader_peptide = []
    leader_score = 0

    while leaderboard:
        new_leaderboard = []
        for peptide in leaderboard:
            for mass in amino_acids:
                new_peptide = peptide + [mass]
                total_mass = sum(new_peptide)
                if total_mass == parent_mass:
                    sc = score(new_peptide, spectrum, cyclic=True)
                    if sc > leader_score:
                        leader_peptide = new_peptide
                        leader_score = sc
                if total_mass <= parent_mass:
                    new_leaderboard.append(new_peptide)
        leaderboard = trim(new_leaderboard, spectrum, N)

    return leader_peptide


# -------- Exemplo --------
M = 20
N = 60
spectrum = [57, 57, 71, 99, 129, 137, 170, 186, 194, 208, 228,
            265, 285, 299, 307, 323, 356, 364, 394, 422, 493]

result = convolution_cyclopeptide_sequencing(spectrum, M, N)
print('-'.join(map(str, result)))
