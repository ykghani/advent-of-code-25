'''Advent of Code 2025 Day 10 - Factory'''
from aocd.models import Puzzle
from pulp import * 
import numpy as np
import re


YEAR = 2025
DAY = 10
puzzle = Puzzle(year= YEAR, day= DAY)

input_data = puzzle.input_data.splitlines()

class Machine:
    def __init__(self, line):
        #Extract target state
        target_match = re.search(r'\[(.*?)\]', line)
        target_str = target_match.group(1)
        self.target_state = [1 if c == '#' else 0 for c in target_str]
        
        #Create button - toggle matrix
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        num_positions = len(self.target_state)
        
        self.buttons = []
        for match in button_matches:
            indices = [int(x) for x in match.split(',')]
            row = [1 if i in indices else 0 for i in range(num_positions)]
            self.buttons.append(row)
        
        #Extract joltage
        joltage_match = re.search(r'\{([0-9,]+)\}', line)
        self.joltage = [int(x) for x in joltage_match.group(1).split(',')]
        
        self.min_presses = 0
    
    def _create_augmented_matrix(self):
        buttons = np.array(self.buttons).T
        target = np.array(self.target_state).reshape(-1, 1)
        return np.column_stack([buttons, target])
    
    def rref_g2(self):
        M = self._create_augmented_matrix()
        rows, cols = M.shape
        current_row = 0
        
        for col in range(cols - 1):
            pivot_row = None
            for row in range(current_row, rows):
                if M[row, col] % 2 == 1: 
                    pivot_row = row
                    break
            
            if pivot_row is None:
                continue  # No pivot in this column (free variable)
            
            M[[current_row, pivot_row]] = M[[pivot_row, current_row]]
            
            for row in range(rows):
                if row != current_row and M[row, col] % 2 == 1:
                    M[row] = (M[row] + M[current_row]) % 2
            
            current_row += 1
        
        return M % 2
    
    def _identify_vars(self, rref):
        rows, cols = rref.shape
        pivot_cols = []
        
        for row in range(rows):
            for col in range(cols - 1): 
                if rref[row, col] == 1:
                    #check if this is the leading 1
                    if all(rref[row, :col] == 0):
                        pivot_cols.append(col)
                        break
        
        num_buttons = cols - 1
        free_cols = [c for c in range(num_buttons) if c not in pivot_cols]
        return pivot_cols, free_cols
    
    def _solve_for_free_vars(self, rref, free_cols, free_vals):
        rows, cols = rref.shape
        num_buttons = cols - 1
        sol = [0] * num_buttons
        
        for i, col in enumerate(free_cols):
            sol[col] = free_vals[i]
        
        for row in range(rows):
            pivot_col = None
            for col in range(num_buttons):
                if rref[row, col] == 1:
                    if all(rref[row, :col] == 0):
                        pivot_col = col
                        break
            
            if pivot_col is None:
                continue
        
            rhs = rref[row, -1]
            total = rhs
            
            for col in range(num_buttons):
                if col != pivot_col:
                    total = (total - rref[row, col] * sol[col]) % 2
            
            sol[pivot_col] = total % 2
    
        return sol
    
    def find_min_presses(self):
        rref = self.rref_g2()
        pivot_cols, free_cols = self._identify_vars(rref)
        
        if not free_cols:
            sol = self._solve_for_free_vars(rref, [], [])
            self.min_presses = sum(sol)
        
        min_presses = float('inf')
        
        num_free = len(free_cols)
        for i in range(2 ** num_free):
            free_vals = [(i >> bit) & 1 for bit in range(num_free)]
            
            sol = self._solve_for_free_vars(rref, free_cols, free_vals)
            total_presses = sum(sol)
            
            min_presses = min(min_presses, total_presses)
        
        self.min_presses = min_presses
        return min_presses
    
    def solve_part2(self):
        buttons_transposed = np.array(self.buttons).T
        num_buttons = buttons_transposed.shape[1]
        
        prob = LpProblem("ButtonPresses", LpMinimize)
        
        # Variables: integer, >= 0
        x = [LpVariable(f"b{i}", lowBound=0, cat='Integer') for i in range(num_buttons)]
        
        # Objective
        prob += lpSum(x)
        
        # Constraints
        for i, target in enumerate(self.joltage):
            prob += lpSum([buttons_transposed[i][j] * x[j] for j in range(num_buttons)]) == target
        
        prob.solve(PULP_CBC_CMD(msg=0, timeLimit=60))
        
        if prob.status == 1:  # Optimal
            return int(value(prob.objective))
        else:
            print(f"PuLP also failed: status {prob.status}")
            print(f"Machine joltage: {self.joltage}")
            return None

#Main Loop
part_one, part_two = 0, 0
for line in input_data:
    machine = Machine(line)
    result = machine.find_min_presses()
    part_one += result
    
    result2 = machine.solve_part2()
    part_two += result2

print(f"Part 1 answer: {part_one}")
puzzle.answer_a = part_one

print(f"Part 2 answer: {part_two}")
puzzle.answer_b = int(part_two)