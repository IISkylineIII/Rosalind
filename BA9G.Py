def suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    return [pos for (suf, pos) in suffixes]

# Lendo o arquivo
with open('rosalind_ba9g.txt', 'r') as f:
    text = f.read().strip()

# Caso não tenha o $ no final, adiciona
if not text.endswith('$'):
    text += '$'

sa = suffix_array(text)
print(", ".join(map(str, sa)))
