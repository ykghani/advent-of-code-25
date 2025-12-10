'''Advent of Code 2025 Day 4 - Printing Department'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 4

puzzle = Puzzle(year= YEAR, day= DAY)
input_data = puzzle.input_data.splitlines()

grid = {}
for row, line in enumerate(input_data):
    line = line.strip()
    for col, char in enumerate(line):
        grid[(row, col)] = char

def update_state(coords_to_update: set, grid= grid):
    '''Modifies the state of the input grid in place'''
    for coord in coords_to_update:
        grid[coord] = '.'
        
    return grid

def check_state(grid= grid) -> set:
    '''Returns set of all coordinates to be updated'''
    accessible_rolls = set()
    for coord in grid.keys():
        row, col = coord
        test_coords = [(row + i, col + j) for i in range(-1, 2) for j in range(-1, 2)
                    if (row + i, col + j) != (row, col)]
        surrounding_rolls = 0
        for loc in test_coords:
            if loc in grid:
                surrounding_rolls += 1 if grid[loc] == '@' else 0
        
        if grid[coord] == '@' and surrounding_rolls < 4:
            accessible_rolls.add(coord)
    
    return accessible_rolls

total_rolls_removed = 0

#Part One
accessible_rolls = check_state(grid)
print(f"Part one: {len(accessible_rolls)}")
puzzle.answer_a  = len(accessible_rolls)

#Part Two
total_rolls_removed += len(accessible_rolls)
grid = update_state(accessible_rolls)
while True:
    accessible_rolls = check_state(grid)
    grid = update_state(accessible_rolls)
    if len(accessible_rolls) == 0:
        break
    else:
        total_rolls_removed += len(accessible_rolls)
    accessible_rolls.clear()

print(f"Part two: {total_rolls_removed}")
puzzle.answer_b = total_rolls_removed