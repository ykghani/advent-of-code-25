'''Advent of Code 2025 Day 2- Gift Shop'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 2

puzzle = Puzzle(year= YEAR, day= DAY)

input_data = puzzle.input_data.strip().split(',')

def part_two_invalid(text) -> int: 
    '''Uses new pattern rules for part 2 and returns int value of invalid codes otherwise 0'''
    for pattern_len in range(1, len(text) // 2 + 1):
        if len(text) % pattern_len != 0: #pattern must divide equally
            continue
        
        if text == text[:pattern_len] * (len(text) // pattern_len):
            return int(text)
    
    return 0

part_one, part_two = 0, 0
for inp in input_data:
    start_id, end_id = inp.split('-')
    for n in range(int(start_id), int(end_id) + 1):
        text = str(n)
        if text[: len(text) //2] == text[len(text) // 2: ]:
            part_one += int(text)
        
        part_two += part_two_invalid(text)

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
puzzle.answer_a = part_one
puzzle.answer_b = part_two