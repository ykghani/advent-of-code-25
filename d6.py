'''Advent of Code 2025 Day 6 - Trash Compactor'''
from aocd.models import Puzzle
from functools import reduce

YEAR = 2025
DAY = 6

puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.splitlines()
input_data = puzzle.input_data.splitlines()

values = []

for line in input_data:
    values.append(line.strip().split())

grand_total = 0
for j in range(len(values[0])):
    if values[-1][j] == '+':
        subtotal = sum(int(values[x][j]) for x in range(0, len(values) - 1))
    else: #multiplication case
        subtotal = reduce(lambda x, y: x * y, (int(values[x][j]) for x in range(0, len(values) - 1)))
    
    grand_total += subtotal

print(f"Part one: {grand_total}")
puzzle.answer_a = grand_total