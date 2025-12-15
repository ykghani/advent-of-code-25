'''Advent of Code 2025 Day 6 - Trash Compactor'''
from aocd.models import Puzzle
from functools import reduce

YEAR = 2025
DAY = 6

puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.splitlines()
input_data = puzzle.input_data.splitlines()

lines = input_data
values = []

for line in input_data:
    values.append(line.strip().split())

grand_total = 0
for j in range(len(values[0])):
    if values[-1][j] == '+':
        args = [values[x][j] for x in range(0, len(values) - 1)]
        args = [int(c) for c in args]
        subtotal = sum(args)
    else: #multiplication case
        args = [values[x][j] for x in range(0, len(values) - 1)]
        args = [int(c) for c in args]
        subtotal = reduce(lambda x, y: x * y, args)
    
    grand_total += subtotal

print(f"Part one: {grand_total}")

#Part Two
operators = lines[-1]
rows = lines[:-1]

grand_total_p2 = 0
column = len(operators) - 2 
numbers = []

while column >= 0:
    while True:
        # Build number from this column (top to bottom)
        val = ''.join([row[column] if column < len(row) else ' ' for row in rows])
        val = val.replace(' ', '')
        numbers.append(int(val))
        
        op = operators[column] if column < len(operators) else ' '
        if op == ' ':
            column -= 1
        else:
            if op == '+':
                grand_total_p2 += sum(numbers)
            else:
                grand_total_p2 += reduce(lambda x, y: x * y, numbers)
            numbers = []
            column -= 2  
            break

print(f"Part two: {grand_total_p2}")   
puzzle.answer_b = grand_total_p2