def greedy_sorting(permutation):
    def reverse_sublist(perm, start, end):
        # Reverte a sublista e inverte os sinais dos elementos
        sub = perm[start:end+1]
        sub = [-x for x in sub[::-1]]
        return perm[:start] + sub + perm[end+1:]

    result = []
    perm = permutation[:]
    n = len(perm)

    for i in range(n):
        correct = i + 1
        if perm[i] != correct:
            # Procura o índice j onde está ±correct
            try:
                j = perm.index(correct)
            except ValueError:
                j = perm.index(-correct)
            # Reverte de i até j
            perm = reverse_sublist(perm, i, j)
            result.append(perm[:])

        # Se o elemento em perm[i] está negativo, faz a troca de sinal
        if perm[i] == -correct:
            perm[i] = correct
            result.append(perm[:])

    return result


# Exemplo de entrada
permutation = [-3, 4, 1, 5, -2]

steps = greedy_sorting(permutation)

# Formatar saída como o Rosalind pede
def format_perm(perm):
    return "(" + " ".join(f"{'+' if x>0 else ''}{x}" for x in perm) + ")"

for step in steps:
    print(format_perm(step))
