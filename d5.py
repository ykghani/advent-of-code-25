'''Advent of Code 2025 Day 5 - Cafeteria'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 5

puzzle = Puzzle(year= YEAR, day= DAY)
input_data = puzzle.input_data.splitlines()

fresh_ingredient_ranges = []
ingredients = []

for line in input_data:
    line = line.strip()
    if '-' in line:
        start, end = line.split('-')
        fresh_ingredient_ranges.append(range(int(start), int(end) + 1))
    
    elif line == "":
        continue
    
    else:
        ingredients.append(int(line))

print(f"Total ingredients to review: {len(ingredients)}")
print(f"Total fresh ingredient ranges: {len(fresh_ingredient_ranges)}")

fresh_ingredients = [
    ingredient for ingredient in ingredients
    if any(ingredient in r for r in fresh_ingredient_ranges)
]

print(f"Part one: {len(fresh_ingredients)}")
puzzle.answer_a = len(fresh_ingredients)

#Part Two
sorted_ranges = sorted(fresh_ingredient_ranges, key= lambda r: r.start)
consolidated_ranges = [sorted_ranges[0]]

for r in sorted_ranges[1:]:
    last = consolidated_ranges[-1]
    if r.start <= last.stop: #Overlapping range
        if r.stop > last.stop:
            consolidated_ranges[-1] = range(last.start, r.stop)
    else:
        consolidated_ranges.append(r)

part_two = sum(len(r) for r in consolidated_ranges)
print(f"Part 2: {part_two}")
puzzle.answer_b = part_two