'''Advent of Code 2025 Day 1 - Secret Entrance'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 1 

puzzle = Puzzle(year= YEAR, day= DAY)

input_data = puzzle.input_data.splitlines()

cur_val = 50
part_one_answer = 0
part_two_answer = 0

for instruction in input_data:
    dir, mag = instruction[0], int(instruction[1:])
    
    part_two_answer += mag // 100
    mag = mag % 100 
    
    if dir == 'R':
        if cur_val + mag > 99: #Crossing case
            new_val = 0 + (cur_val + mag - 100)
            if cur_val != 0 and new_val != 0:
                part_two_answer += 1
            cur_val = new_val
        else:
            cur_val += mag
    else:
        if cur_val - mag < 0: #Crossing case
            new_val = 100 - (mag - cur_val)
            if cur_val != 0 and new_val != 0:
                part_two_answer += 1
            cur_val = new_val
        else:
            cur_val -= mag
    
    if cur_val == 0:
        part_one_answer += 1
        part_two_answer += 1

print(f"Part one is: {part_one_answer}")
print(f"Part two answer: {part_two_answer}")