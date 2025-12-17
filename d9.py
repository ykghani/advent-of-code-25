'''Advent of Code 2025 Day 9 - Movie Theatre'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 9
puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.splitlines()
input_data = puzzle.input_data.splitlines()

def calculate_area(p: tuple, q: tuple) -> int:
    '''Returns area of rectangle formed by 2 points'''
    if p[0] <= q[0]:
        x_dim = q[0] - p[0] + 1
    else:
        x_dim = p[0] - q[0] + 1
    
    if p[1] <= q[1]:
        y_dim = q[1] - p[1] + 1
    else:
        y_dim = p[1] - q[1] + 1
    
    return x_dim * y_dim

points = [tuple(int(c) for c in line.split(',')) for line in input_data]

max_area = 0
for i in range(len(points)):
    p = points[i]
    for j in range(i, len(points)):
        q = points[j]
    
        area = calculate_area(p, q)
        if area > max_area:
            max_area = area

print(f"Part one: {max_area}")
puzzle.answer_a = max_area