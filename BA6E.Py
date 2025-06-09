def shared_kmers(k, s1, s2):
    from collections import defaultdict

    # Armazena as posições de todos os k-mers em s2
    s2_kmers = defaultdict(list)
    for j in range(len(s2) - k + 1):
        kmer = s2[j:j+k]
        s2_kmers[kmer].append(j)

    result = []

    for i in range(len(s1) - k + 1):
        kmer = s1[i:i+k]
        rev_kmer = reverse_complement(kmer)

        # Verifica se o kmer ou seu reverso estão em s2
        for j in s2_kmers.get(kmer, []):
            result.append((i, j))
        for j in s2_kmers.get(rev_kmer, []):
            result.append((i, j))

    return result

def reverse_complement(seq):
    complement = str.maketrans("ACGT", "TGCA")
    return seq.translate(complement)[::-1]

# Exemplo de uso com os dados fornecidos:
k = 13
s1 = "AAACTCATC"
s2 = "TTTCAAATC"

output = shared_kmers(k, s1, s2)
for pair in output:
    print(pair)
