'''Advent of Code 2025 Day 8 - Playground'''
from aocd.models import Puzzle
from functools import reduce

YEAR = 2025
DAY = 8
puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.splitlines()
input_data = puzzle.input_data.splitlines()

def euclidian_distance(p, q) -> int:
    '''Returns straight-line distance between 2 points'''
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2) ** (0.5)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1 for _ in range(n)]
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX == rootY:
            return False #already in same set
        
        if self.size[rootX] < self.size[rootY]: # type: ignore
            self.parent[rootX] = rootY
            self.size[rootY] += self.size[rootX]
        else:
            self.parent[rootY] = rootX
            self.size[rootX] += self.size[rootY]
        
        return True
    
    def get_size(self, x):
        root = self.find(x)
        return self.size[root]
    
    @property
    def part_one(self):
        n = 3 
        circuit_sizes = [self.size[i] for i in range(len(self.parent)) if self.parent[i] == i]
        sorted_sizes = sorted(circuit_sizes, reverse= True)
        return reduce(lambda x, y: x * y, sorted_sizes[: n])
        

points = []
for line in input_data:
    p = tuple(int(c) for c in line.split(','))
    points.append(p)

distances = []
for i in range(len(points)):
    p = points[i]
    for j in range(i + 1, len(points)):
        q = points[j]
        dist = euclidian_distance(p, q)
        distances.append((dist, i, j))

distances.sort()

uf = UnionFind(len(points)) #initializes UF with all points from circuit boxes

successful_connections = 0
counter = 0
LIMIT = 1000
for dist, i, j in distances:
    if uf.union(i, j):
        successful_connections += 1
    
    counter += 1
    if counter == LIMIT:
        break

print(f'Part 1: {uf.part_one}')
puzzle.answer_a = uf.part_one