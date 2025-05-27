from Bio import SeqIO, pairwise2
from io import StringIO

fasta_data = """>Rosalind_18
GACATGTTTGTTTGCCTTAAACTCGTGGCGGCCTAGCCGTAAGTTAAG
>Rosalind_23
ACTCATGTTTGTTTGCCTTAAACTCTTGGCGGCTTAGCCGTAACTTAAG
>Rosalind_51
TCCTATGTTTGTTTGCCTCAAACTCTTGGCGGCCTAGCCGTAAGGTAAG
>Rosalind_7
CACGTCTGTTCGCCTAAAACTTTGATTGCCGGCCTACGCTAGTTAGTTA
>Rosalind_28
GGGGTCATGGCTGTTTGCCTTAAACCCTTGGCGGCCTAGCCGTAATGTTT
"""

records = list(SeqIO.parse(StringIO(fasta_data), "fasta"))

def aligned_distance(seq1, seq2):
    # Faz alinhamento global simples, sem penalidade complexa
    alignments = pairwise2.align.globalxx(seq1, seq2)
    # Pega o primeiro alinhamento ótimo
    aln1, aln2, score, start, end = alignments[0]

    # Conta mismatches no alinhamento (desconsiderando gaps na contagem como mismatch)
    mismatches = 0
    for a, b in zip(aln1, aln2):
        if a != b:
            mismatches += 1
    return mismatches

avg_distances = []
for i, rec1 in enumerate(records):
    dist_sum = 0
    for j, rec2 in enumerate(records):
        if i != j:
            dist_sum += aligned_distance(rec1.seq, rec2.seq)
    avg_distances.append(dist_sum / (len(records) - 1))

odd_one_out_index = avg_distances.index(max(avg_distances))

print(records[odd_one_out_index].id)
