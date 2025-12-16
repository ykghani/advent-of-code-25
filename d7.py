'''Advent of Code 2025 Day 7 - Laboratories'''
from aocd.models import Puzzle
from functools import lru_cache

YEAR = 2025
DAY = 7

puzzle = Puzzle(year= YEAR, day= DAY)
input_data = puzzle.input_data.splitlines()

grid = {}
splitters = []
beams = []
row_dim, col_dim = len(input_data), len(input_data[0].strip())

for row, line in enumerate(input_data):
    line = line.strip()
    for col, char in enumerate(line):
        if char == 'S':
            beams.append((row, col))
        elif char == '^':
            splitters.append((row, col))
        
        grid[(row, col)] = char

def check_state(beams, grid= grid): 
    '''Returns list of all coordiantes to be updated based on contact with splitters or otherwise'''
    updates = set()
    activated_splitters = set()
    for beam_loc in sorted(beams, key= lambda c: c[1]):
        n_row, n_col = beam_loc[0] + 1, beam_loc[1]
        if (n_row, n_col) not in grid:
            continue
        
        if grid[(n_row, n_col)] == '.':
            updates.add((n_row, n_col))
        
        if grid[(n_row, n_col)] == '^': #SPLITTER CASE
            left, right = n_col - 1, n_col + 1
            if left >= 0:
                updates.add((n_row, left))
            
            if right < col_dim:
                updates.add((n_row, right))
            
            activated_splitters.add((n_row, n_col))
    return updates, len(activated_splitters)

def update_state(updates: dict, grid= grid):
    '''Updates the grid based on the input dict and returns:
    1. The number of new beam splits that occurred
    2. The latest position of all beams '''
    latest_beams = set()
    
    for coord in updates: 
            grid[coord] = '|'
            latest_beams.add(coord)
    
    return latest_beams

def print_grid(grid= grid, r_dim= row_dim, c_dim = col_dim) -> None:
    for r in range(r_dim):
        line = []
        for c in range(c_dim):
            line.append(grid[r, c])
        print(''.join(line))
        
    return

@lru_cache(maxsize=None)
def count_timelines(r, c):
    if c < 0 or c >= col_dim:
        return 0
    
    if r >= row_dim:
        return 0
    
    # Bottom row - complete timeline
    if r == row_dim - 1:
        return 1
    
    current = grid[(r, c)]
    
    if current == 'S':
        return count_timelines(r + 1, c)
    
    if current == '.':
        return count_timelines(r + 1, c)
    
    if current == '^':
        return count_timelines(r + 1, c - 1) + count_timelines(r + 1, c + 1)
    
    return 0

part_one = False
if part_one:
    total_splits = 0
    for _ in range(row_dim - 1):
        updates, new_splits = check_state(beams)
        total_splits += new_splits
        beams = update_state(updates)
        
    print(f"Beam split total of: {total_splits} times")
    puzzle.answer_a = total_splits
else:
    r, c = beams[0][0], beams[0][1]
    result = count_timelines(r, c)
    print(f"Part 2 answer: {result}")
    puzzle.answer_b = result