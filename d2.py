'''Advent of Code 2025 Day 2- Gift Shop'''
from aocd.models import Puzzle

YEAR = 2025
DAY = 2

puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.split(',')
input_data = puzzle.input_data.strip().split(',')

def compute_LPS_array(pattern):
    n = len(pattern)
    lps = [0] * n
    
    length = 0
    i = 0
    
    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                #fall back in pattern
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def LPSsearch(pat, txt):
    n = len(txt)
    m = len(pat)
    
    lps = compute_LPS_array(pat)
    res = []
    
    i, j = 0, 0
    while i < n:
        #If chars match, move both pointers forward
        if txt[i] == pat[j]: 
            i += 1
            j += 1
            
            #if entire pattern matches store start index in res
            if j == m:
                res.append(i - j)
                
                #use LPS table to skip unnecessary indices
                j = lps[i - 1]
        else: #mismatch
            if j != 0:
                j = lps[j - 1]
            else: 
                i += 1
    return res

part_one = 0
for inp in input_data:
    start_id, end_id = inp.split('-')
    for n in range(int(start_id), int(end_id) + 1):
        text = str(n)
        if text[: len(text) //2] == text[len(text) // 2: ]:
            part_one += int(text)

print(part_one)
puzzle.answer_a = part_one