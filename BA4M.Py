from collections import Counter
from itertools import product

def difference(pos, d):
    return Counter(abs(x - d) for x in pos)

def turnpike(dist, pos):
    if not dist:
        yield sorted(pos)
    else:
        for x in [max(dist), max(pos) - max(dist)]:
            xdist = difference(pos, x)
            if not (xdist - dist):
                yield from turnpike(dist - xdist, pos + [x])

def solve_turnpike(distance_list):
    dist_pos = list(filter(lambda x: x > 0, distance_list))
    dist_counter = Counter(dist_pos)
    
    max_point = max(distance_list)
    pos = [0, max_point]
    
    dist_counter.subtract(difference(pos, max_point))
    dist_counter += Counter()
    
    sol = next(turnpike(dist_counter, pos))
    return sol

def main():
    filename = "rosalind_ba4m (1).txt"  # ajuste o caminho se necessário
    with open(filename) as f:
        line = f.readline().strip()
        distances = list(map(int, line.split()))
    
    solution = solve_turnpike(distances)
    print(*solution)  # imprime sem vírgulas, só com espaços

if __name__ == "__main__":
    main()
