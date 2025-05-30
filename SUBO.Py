import regex

s = """CCGATTAAGCCGATGGCTGTTGCGATTCAACCGGTCAGCGCTACAGGTCCGATTAAGCCG
ATGGCTGTTGCGATTCAACCGGTCAGTTCACCCTGATGCCGATTATTCACTCAAGTACCT
CACCCATCCTGAAGTCGAGGCCTAGCTATACCGGCGCAGACAGGAACCACCATACGAACC
GATTAAGCCGATGGCTGTTGCGATTCAACCGGTCCCCCTGACGACCCCATTCGTGGACGG
TTGGCTGTGAGTCAGGGAAATGTGGGCGCACTCCTGGGAGCGCGCCAGCGTACCGCAATT
GTTATAATCCTTGTGATCAATCTACGCCGTGACGAGACTTATGTACGCTATGTCCAAAGA
TATATTAGAGTCCTCTGTTGTCGGACAAAAAGTATAGTGTCGGCAAACCGCCGTCTCTCG
ACGGGATACACCGCAAGAGGTCTGATCTCGTAACTTACACAGAGTATACAGCTCTAGCTT
TTCGGTAGCAACCTTGTAGTCAAGGGAAATGAAACGCGTAGGCTCGCTCGCGGTTGTTTC
TATACCGTCAAATCCTTACGAGCTGTAAAATTTACGACACCGTCTGATGTCTGGGCGGAG
TTAATTCCTTTAGATTGAATTGTCCGATTAAGCCGATGGCTGTTGCGATTCAACCGGTCA
CTATTAACGATCATACCGCAGAAGACATAGACCTGTCTTTTGTCTATCGATACTCCTCAT
CGTCGCCACACAAGTATGCCTTCAGACATACTCAGCGCTGGGTCCCTCACGATACAAACA
GCCCTTTGAAGTTGTGGCACATTTGACTATGGTCAATGACCCTACGCGGCGTCATCAAAG
GCGTTGTTAAACGTCCGATTAAGCCGATGGCTGTTGCGATTCAACCGGTCTATCGTGCCG
GTCCGATTAAGCCGATGGCTGTTGCGATTCAACCGGTCTGGCCCGTGACTTATGCGAATG
ACCGGGCTGCCAGATTACAATAAAATAACCTGC""".replace('\n', '')

t = """TATTGAGGAAGGTTAAGGGACCTCTATACGTCTTCTTAGCTCTGCTAACCGCTCCCCAGT
CGGTGTACGGAGTTATTTTTATGAGTCCGATTAAGCCGATGGCTGTTGCGATTCAACCGG
TCGAGCGTTGCACTGCTTACCAGCTTATACGCAAAAAGTCTGTTGCGCTCTGATTCTTGA
AAAAGGAGGTATTCCTGTTTCGGTGTTTTGCCGCTAACTCTCCCCCACGGAGGGGCCCCA
CTTCTGTGCTCAGTGTAGATCACGCAATCCTCGGTTGAACCCGGGAAGACTGGTCGTACA
CCTTCCGATTAAGCCGATGGCTGTTGCGATTCAACCGGTCTTAAAACAGCTCACTCCCAG
AGCGTTAAATCTCGCAACGAGACGTTTAATAAACCGTGTACTCCACAACCCGGCCACCTC
CTTGCTTGCGCAGGTTACGACATTGCATACTCACTAGCACAATGGAGACATTGTCGTCAA
CGCTTAGAGGCCACCTATCTTCACACATCATAGTCCCTCTCTAAAAGTCCATGTGGTTCC
GATTAAGCCGATGGCTGTTGCGATTCAACCGGTCACGCACTCACATCCGATTAAGCCGAT
GGCTGTTGCGATTCAACCGGTCTGGTCCTCAACGCTGTATCAAAGAGTGCGTTGTTCACT
GCTAATCCAATTTCGCGTGCACACCGAAGCAATGATTCCTAGGACTAGCTAGTAATTGAG
TGTGAACCAATCCCGTTCTTCATCCTCGGTGCCAAAATGCTCGGGTCATCGTCTAGGGGT
CAACATCGGGGTGAGGACTCCCCCAAACGTTGATCAAGTCCGATTAAGCCGATGGCTGTT
GCGATTCAACCGGTCTATCAATACC""".replace('\n', '')

def find_approx_occurrences(seq, pattern, max_substitutions=3):
    pattern_fuzzy = f"({pattern}){{s<={max_substitutions}}}"
    matches = regex.finditer(pattern_fuzzy, seq, overlapped=True)
    return [m.start() for m in matches]

substring_sizes = range(32, 41)
best_candidate = None
best_counts = (0, 0)  # (count_s, count_t)
best_total = 0

for size in substring_sizes:
    for i in range(len(s) - size + 1):
        candidate = s[i:i+size]
        count_s = len(find_approx_occurrences(s, candidate, 3))
        count_t = len(find_approx_occurrences(t, candidate, 3))
        total = count_s + count_t
        if total > best_total and count_s > 0 and count_t > 0:
            best_total = total
            best_candidate = candidate
            best_counts = (count_s, count_t)

print(f"Substring encontrada (tamanho {len(best_candidate)}): {best_candidate}")
print(f"Ocorrências em s: {best_counts[0]}")
print(f"Ocorrências em t: {best_counts[1]}")
print(f"Total: {best_counts[0]} {best_counts[1]}")
