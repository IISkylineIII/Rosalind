import queue
import numpy as np

class SmallParsimony:  
    def __init__(self):
        n, adj, nodes, lastEdge = self._input()
        s = self.runSmallParsimony(n, adj, nodes, lastEdge)
        self.printResults(s, adj, nodes)
        
    def _input(self):
        filename = 'rosalind_ba7g (3).txt'  # arquivo de entrada fixo
        with open(filename, 'r') as f:
            data = f.read().strip().split('\n')
        
        n = int(data[0])
        adj = [dict() for _ in range(n)]
        nodes = ['' for _ in range(n)]
        currNode = 0
        for d in data[1:]:
            d = d.split('->')
            try:
                p = int(d[0])
            except:
                p = currNode
                nodes[p] = d[0]
                currNode += 1
            try:
                c = int(d[1])
            except:
                continue
            if p > len(adj)-1 or c > len(adj)-1:
                adj.extend([dict() for _ in range(max([p,c]) - len(adj) + 1)])
            adj[p][c] = 0
            adj[c][p] = 0
        nodes.extend(['' for _ in range(len(adj) - n + 1)])
        lastEdge = [int(i) for i in data[-1].split('->')]
        return n, adj, nodes, lastEdge
    
    def printResults(self, s, adj, nodes):
        print(s)
        for i, d in enumerate(adj):
            for j, w in d.items():
                print(nodes[i] + '->' + nodes[j] + ':' + str(w))
    
    def charIndConversion(self):
        char2ind = {'A':0, 'C':1, 'G':2, 'T':3}
        ind2char = {0:'A', 1:'C', 2:'G', 3:'T'}
        return char2ind, ind2char
    
    def singleSmallParsimony(self, n, adjC, adjP, adj, nodes, char2ind, ind2char, charInd):
        s = [[np.inf]*4 for _ in range(len(adjC))]
        backtrack = [[(-1, -1) for _ in range(4)] for __ in range(len(adjC))]
        processed = [0 for _ in range(len(adjC))]
        ripe = set()
        for i in range(n):
            s[i][char2ind[nodes[i][charInd]]] = 0
            processed[i] = 1
            if len(adjP[i]) > 0:
                ripe.add(adjP[i][0])
        
        while len(ripe) > 0:
            v = ripe.pop()
            for k in range(4):
                l = [s[adjC[v][0]][i] + (0 if k == i else 1) for i in range(4)]
                r = [s[adjC[v][1]][i] + (0 if k == i else 1) for i in range(4)]
                largmin = np.argmin(l)
                rargmin = np.argmin(r)
                backtrack[v][k] = (largmin, rargmin)
                s[v][k] = l[largmin] + r[rargmin]
            processed[v] = 1
            if len(adjP[v]) > 0 and all([processed[u] for u in adjC[adjP[v][0]]]):
                ripe.add(adjP[v][0])
        
        ind = np.argmin(s[v])
        nodes[v] += ind2char[ind]
        smin = s[v][ind]

        q = queue.Queue()
        q.put((v, ind))
        while not q.empty():
            v, k = q.get()
            if len(adjC[v]) > 0:
                u, w = adjC[v]
                l, r = backtrack[v][k]
                
                if k != l:
                    adj[v][u] += 1
                    adj[u][v] += 1
                if k != r:
                    adj[v][w] += 1
                    adj[w][v] += 1
                if len(adjC[u]) > 0:
                    nodes[u] += ind2char[l]
                    nodes[w] += ind2char[r]
                    q.put((u, l))
                    q.put((w, r))        
        return smin
    
    def runSmallParsimony(self, n, adj, nodes, lastEdge):
        def dist(v, w):
            d = 0
            l = len(v)
            for i in range(l):
                if v[i] != w[i]:
                    d += 1
            return d

        char2ind, ind2char = self.charIndConversion()
        root = len(adj)
        del adj[lastEdge[0]][lastEdge[1]]
        del adj[lastEdge[1]][lastEdge[0]]
        adj.append(dict())
        adj[root][lastEdge[0]] = 0
        adj[lastEdge[0]][root] = 0
        adj[root][lastEdge[1]] = 0
        adj[lastEdge[1]][root] = 0
        adjC = [[] for _ in range(len(adj))]
        adjP = [[] for _ in range(len(adj))]
        for p in range(n, len(adj)):
            c = sorted(list(adj[p].keys()))
            adjC[p].append(c[0])
            adjC[p].append(c[1])
            adjP[c[0]].append(p)
            adjP[c[1]].append(p)
        s = 0
        for i in range(len(nodes[0])):
            s += self.singleSmallParsimony(n, adjC, adjP, adj, nodes, char2ind, ind2char, i)
        d = dist(nodes[lastEdge[0]], nodes[lastEdge[1]])
        del adj[root]
        del adj[lastEdge[0]][root]
        del adj[lastEdge[1]][root]
        adj[lastEdge[0]][lastEdge[1]] = d
        adj[lastEdge[1]][lastEdge[0]] = d
        return s

if __name__ == "__main__":
    SmallParsimony()
