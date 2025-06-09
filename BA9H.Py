def suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    return [pos for (suf, pos) in suffixes]

def pattern_matching(text, patterns):
    sa = suffix_array(text)
    result_positions = set()

    def binary_search_left(pattern):
        low, high = 0, len(sa)
        while low < high:
            mid = (low + high) // 2
            suffix = text[sa[mid]:]
            if suffix < pattern:
                low = mid + 1
            else:
                high = mid
        return low

    def binary_search_right(pattern):
        low, high = 0, len(sa)
        while low < high:
            mid = (low + high) // 2
            suffix = text[sa[mid]:]
            # Aqui comparamos com pattern + chr(255) para pegar o limite superior
            # porque "$" é o menor caractere, e precisamos garantir que pegue
            # todos sufixos que começam com pattern
            if suffix.startswith(pattern) or suffix <= pattern + chr(255):
                low = mid + 1
            else:
                high = mid
        return low

    for pattern in patterns:
        left = binary_search_left(pattern)
        right = binary_search_right(pattern)
        for i in range(left, right):
            if text.startswith(pattern, sa[i]):
                result_positions.add(sa[i])

    return sorted(result_positions)

# Teste com o dataset de exemplo
text = "AATCGGGTTCAATCGGGGT"
patterns = ["ATCG", "GGGT"]

positions = pattern_matching(text, patterns)
print(" ".join(map(str, positions)))
