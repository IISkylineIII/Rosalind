from Bio import Phylo
from io import StringIO

def read_fasta(fasta_text):
    seqs = {}
    name = None
    seq = []
    for line in fasta_text.strip().split('\n'):
        if line.startswith('>'):
            if name:
                seqs[name] = ''.join(seq)
            name = line[1:].strip()
            seq = []
        else:
            seq.append(line.strip())
    if name:
        seqs[name] = ''.join(seq)
    return seqs

def get_parents(tree):
    parents = {}
    for clade in tree.find_clades(order='level'):
        for child in clade.clades:
            parents[child] = clade
    return parents

def get_path_down(tree, start, end, parents):
    path = []
    found = False
    def dfs(node):
        nonlocal found
        if found:
            return
        path.append(node)
        if node == end:
            found = True
            return
        for c in node.clades:
            dfs(c)
            if found:
                return
        if not found:
            path.pop()
    dfs(start)
    if found:
        return path
    else:
        return None

def find_reversals(tree, seqs):
    parents = get_parents(tree)
    results = []
    seq_len = len(next(iter(seqs.values())))
    name_to_node = {clade.name: clade for clade in tree.find_clades() if clade.name}
    for i in range(seq_len):
        substitutions = []
        for clade in tree.find_clades(order='level'):
            for child in clade.clades:
                if clade.name and child.name:
                    p_sym = seqs[clade.name][i]
                    c_sym = seqs[child.name][i]
                    if p_sym != c_sym:
                        substitutions.append((clade, child, i, p_sym, c_sym))
        for (s, t, pos, orig_sym, sub_sym) in substitutions:
            def dfs_find_reversions(node, path_nodes):
                for child in node.clades:
                    if child.name and node.name:
                        node_sym = seqs[node.name][pos]
                        child_sym = seqs[child.name][pos]
                        if node_sym == sub_sym and child_sym == orig_sym:
                            path_t_to_v = get_path_down(tree, t, node, parents)
                            if path_t_to_v:
                                all_sub_sym = all(seqs[n.name][pos] == sub_sym for n in path_t_to_v if n.name)
                                if all_sub_sym:
                                    results.append(
                                        (t.name, child.name, pos + 1, f"{orig_sym}->{sub_sym}->{orig_sym}")
                                    )
                        dfs_find_reversions(child, path_nodes + [child])
            dfs_find_reversions(t, [t])
    return results


filename = 'rosalind_rsub (2).txt'

with open(filename, 'r') as f:
    lines = f.readlines()

newick = lines[0].strip()
fasta_text = ''.join(lines[1:])

tree = Phylo.read(StringIO(newick), "newick")
seqs = read_fasta(fasta_text)

reversals = find_reversals(tree, seqs)

for first, reverted, pos, sub in reversals:
    print(first, reverted, pos, sub)
