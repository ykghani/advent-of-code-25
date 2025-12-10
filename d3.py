'''Advent of Code 2025 Day 3- Lobby'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 3

puzzle = Puzzle(year= YEAR, day= DAY)

input_data = puzzle.input_data.splitlines()

def largest_joltage(inp: list, size= 12) -> int:
    '''Returns the largest joltage value that can be made from input line'''
    stack = []
    pops = len(inp) - size
    i = 0
    
    while i < len(inp):
        if i == 0:
            stack.append(inp[i])
        elif inp[i] <= stack[-1]:
            stack.append(inp[i])
        elif len(stack) > 0 and pops > 0: 
            while inp[i] > stack[-1] and pops > 0:
                del stack[-1]
                pops -= 1
                if not len(stack):
                    break 
            
            stack.append(inp[i])
        else:
            stack.append(inp[i])
        
        i += 1 
    
    stack = stack[: size]
    return int(''.join(str(s) for s in stack))

part_one, part_two = 0, 0
for bank in input_data:
    bank = list(map(int, bank))
    max_val = max(bank)
    max_index = bank.index(max_val)
    if max_index == len(bank) - 1: #case where max value is the last item in the list
        max_val = max(bank[: max_index] + bank[max_index + 1: ])
        max_index = bank.index(max_val)
    
    second_val = max(bank[max_index + 1: ])
    part_one += int(str(max_val) + str(second_val))
    temp = largest_joltage(bank)
    part_two += temp

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
puzzle.answer_a = part_one
puzzle.answer_b = part_two