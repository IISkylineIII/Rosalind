import numpy as np
import copy

class TwoBreakOnGenome:
    def __init__(self):
        genome, i0, i1, j0, j1 = self._inputGenomeFromFile()
        genome = self.twoBreakOnGenome(genome, i0, i1, j0, j1)
        self.printGenome(genome)

    def _inputGenomeFromFile(self):
        with open('rosalind_ba6k (4).txt', 'r') as f:
            data = [line.strip() for line in f.readlines()]
        
        d0 = data[0].split(')(')
        genome = []
        for d in d0:
            d = d.replace('(', '').replace(')', '').split()
            genome.append([int(e) for e in d])
        
        i0, i1, j0, j1 = [int(d) for d in data[1].split(',')]
        return genome, i0, i1, j0, j1

    def chromosomeToCycle(self, chromosome):
        nodes = []
        for i in chromosome:
            if i > 0:
                nodes.extend([2 * i - 1, 2 * i])
            else:
                nodes.extend([-2 * i, -2 * i - 1])
        return nodes

    def cycleToChromosome(self, nodes):
        chromosome = []
        for j in range(0, len(nodes), 2):
            if nodes[j] < nodes[j + 1]:
                chromosome.append(nodes[j + 1] // 2)
            else:
                chromosome.append(-nodes[j] // 2)
        return chromosome

    def printGenome(self, genome):
        result = ''
        for chromosome in genome:
            result += '(' + ' '.join(['+' + str(x) if x > 0 else str(x) for x in chromosome]) + ')'
        print(result)

    def coloredEdges(self, genome):
        edges = set()
        for chromosome in genome:
            nodes = self.chromosomeToCycle(chromosome)
            nodes.append(nodes[0])
            for j in range(len(chromosome)):
                edges.add((nodes[2 * j + 1], nodes[2 * j + 2]))
        return edges

    def twoBreakOnGraph(self, edges, i0, i1, j0, j1):
        edges.discard((i0, i1))
        edges.discard((i1, i0))
        edges.discard((j0, j1))
        edges.discard((j1, j0))
        edges.add((i0, j0))
        edges.add((i1, j1))
        return edges

    def groupNodes(self, edges):
        parent = {}
        rank = {}
        for u, v in edges:
            for node in [u, v]:
                if node not in parent:
                    parent[node] = node
                    rank[node] = 0

        def find(u):
            if parent[u] != u:
                parent[u] = find(parent[u])
            return parent[u]

        def union(u, v):
            u_root = find(u)
            v_root = find(v)
            if u_root == v_root:
                return
            if rank[u_root] > rank[v_root]:
                parent[v_root] = u_root
            else:
                parent[u_root] = v_root
                if rank[u_root] == rank[v_root]:
                    rank[v_root] += 1

        for u, v in edges:
            union(u, v)
            if u % 2 == 0:
                union(u, u - 1)
            else:
                union(u, u + 1)
            if v % 2 == 0:
                union(v, v - 1)
            else:
                union(v, v + 1)

        nodesID = {node: find(node) for node in parent}
        nodesSets = set(nodesID.values())
        return nodesSets, nodesID

    def buildEdgeDict(self, edges, nodesSet, nodesID):
        edgeDict = {}
        for u, v in edges:
            id = nodesID[u]
            if id not in edgeDict:
                edgeDict[id] = {}
            edgeDict[id][u] = v
            edgeDict[id][v] = u
        return edgeDict

    def twoBreakOnGenome(self, genome, i0, i1, j0, j1):
        edges = self.twoBreakOnGraph(self.coloredEdges(genome), i0, i1, j0, j1)
        nodesSet, nodesID = self.groupNodes(edges)
        edgeDict = self.buildEdgeDict(edges, nodesSet, nodesID)
        nodesDict = {}
        for id, eDict in edgeDict.items():
            nodesDict[id] = []
            currNode0 = list(eDict.keys())[0]
            while eDict:
                nodesDict[id].append(currNode0)
                currNode1 = currNode0 + 1 if currNode0 % 2 else currNode0 - 1
                nodesDict[id].append(currNode1)
                newNode = eDict[currNode1]
                del eDict[currNode0]
                del eDict[currNode1]
                currNode0 = newNode
        newGenome = [self.cycleToChromosome(nodes) for nodes in nodesDict.values()]
        newGenome.sort(key=lambda x: abs(x[0]))
        return newGenome

if __name__ == "__main__":
    TwoBreakOnGenome()
