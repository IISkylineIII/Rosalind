from functools import cache

def masses():
    return {
        'A': 71, 'C': 103, 'D': 115, 'E': 129, 'F': 147,
        'G': 57, 'H': 137, 'I': 113, 'K': 128, 'L': 113,
        'M': 131, 'N': 114, 'P': 97, 'Q': 128, 'R': 156,
        'S': 87, 'T': 101, 'V': 99, 'W': 186, 'Y': 163
    }

def dict_size(sv, T, max_score):
    mass = list(masses().values())  # Lista de massas inteiras

    sv = [0] + sv  # Adiciona zero no início para índice consistente
    n = len(sv) - 1

    @cache
    def size(i, t):
        # Base: quando tamanho 0 e score 0 => 1 (sequência vazia)
        if i == 0 and t == 0:
            return 1
        # Casos impossíveis
        if t < 0 or i <= 0:
            return 0
        # Soma sobre todas as massas possíveis
        total = 0
        for m in mass:
            if i - m >= 0:
                total += size(i - m, t - sv[i])
        return total

    # Soma para todos os scores entre T e max_score
    return sum(size(n, x) for x in range(T, max_score + 1))


def main(file):
    with open(file) as f:
        sv_line = f.readline().strip()
        T_line = f.readline().strip()
        max_score_line = f.readline().strip()

    sv = list(map(int, sv_line.split()))
    T = int(T_line)
    max_score = int(max_score_line)

    result = dict_size(sv, T, max_score)
    print(result)


if __name__ == "__main__":
    main("rosalind_ba11h (3).txt")
