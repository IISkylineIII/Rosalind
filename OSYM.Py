def ReadFASTA(file_path):
    fasta = []
    with open(file_path, 'r') as file:
        label = None
        seq = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if label:
                    fasta.append((label, seq))
                label = line[1:]
                seq = ''
            else:
                seq += line
        if label:
            fasta.append((label, seq))
    return fasta


def semiglobal_alignment(v, w, sigma):
    '''Returns the semiglobal alignment of v and w and the associated score.'''
    S = [[0 for j in range(len(w) + 1)] for i in range(len(v) + 1)]
    backtrack = [[0 for j in range(len(w) + 1)] for i in range(len(v) + 1)]

    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            match = 1 if v[i - 1] == w[j - 1] else -1
            scores = [S[i - 1][j] - sigma, S[i][j - 1] - sigma, S[i - 1][j - 1] + match]
            S[i][j] = max(scores)
            backtrack[i][j] = scores.index(S[i][j])

    last_row_index = max(range(len(w) + 1), key=lambda x: S[len(v)][x])
    last_column_index = max(range(len(v) + 1), key=lambda x: S[x][len(w)])
    if S[len(v)][last_row_index] >= S[last_column_index][len(w)]:
        i = len(v)
        j = last_row_index
    else:
        i = last_column_index
        j = len(w)
    max_score = S[i][j]

    insert_indel = lambda word, i: word[:i] + '-' + word[i:]

    v_aligned, w_aligned = v, w

    for _ in range(len(v) - i):
        w_aligned += '-'
    for _ in range(len(w) - j):
        v_aligned += '-'

    while i * j != 0:
        if backtrack[i][j] == 0:
            i -= 1
            w_aligned = insert_indel(w_aligned, j)
        elif backtrack[i][j] == 1:
            j -= 1
            v_aligned = insert_indel(v_aligned, i)
        else:
            i -= 1
            j -= 1

    for _ in range(i):
        w_aligned = insert_indel(w_aligned, 0)
    for _ in range(j):
        v_aligned = insert_indel(v_aligned, 0)

    return str(max_score), v_aligned, w_aligned


def main():
    word1, word2 = [fasta[1] for fasta in ReadFASTA('rosalind_smgb.txt')]

    alignment = semiglobal_alignment(word1, word2, 1)

    print('\n'.join(alignment))
    with open('output/101_SMGB.txt', 'w') as output_data:
        output_data.write('\n'.join(alignment))


if __name__ == '__main__':
    main()
