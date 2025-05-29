import os
import tempfile
import platform

def write_tree(tree):
    f = tempfile.NamedTemporaryFile("w", delete=False)
    f.write(tree)
    f.close()
    return f.name

def main(file):
    _, tree1, tree2 = open(file).read().splitlines()
    f1 = write_tree(tree1)
    f2 = write_tree(tree2)
    bin_path = "/home/juan/Downloads/tqDist-1.0.2/bin/quartet_dist"
    
    print("Chamando:", bin_path, f1, f2)
    
    res = os.popen(f"{bin_path} {f1} {f2}").read().strip()
    
    print("Resultado bruto:", repr(res))
    
    try:
        result_int = int(res)
        print("Resultado convertido:", result_int)
        print("Resultado final (multiplicado por 2):", result_int * 2)
    except ValueError:
        print("Erro: resultado não é um inteiro válido.")

main("rosalind_qrtd (13).txt")
