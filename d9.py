'''Advent of Code 2025 Day 9 - Movie Theatre'''
from aocd.models import Puzzle
from functools import lru_cache

YEAR = 2025
DAY = 9
puzzle = Puzzle(year= YEAR, day= DAY)

# input_data = puzzle.examples[0].input_data.splitlines()
input_data = puzzle.input_data.splitlines()

def calculate_area(p: tuple, q: tuple) -> int:
    '''Returns area of rectangle formed by 2 points'''
    if p[0] <= q[0]:
        x_dim = q[0] - p[0] + 1
    else:
        x_dim = p[0] - q[0] + 1
    
    if p[1] <= q[1]:
        y_dim = q[1] - p[1] + 1
    else:
        y_dim = p[1] - q[1] + 1
    
    return x_dim * y_dim

points = [tuple(int(c) for c in line.split(',')) for line in input_data]
points_tuple = tuple(points)

max_area = 0
for i in range(len(points)):
    p = points[i]
    for j in range(i, len(points)):
        q = points[j]
    
        area = calculate_area(p, q)
        if area > max_area:
            max_area = area

print(f"Part one: {max_area}")
# puzzle.answer_a = max_area

green_and_red_tiles = set(points)
for i in range(len(points)):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % len(points)]
    
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            green_and_red_tiles.add((x1, y))
    
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            green_and_red_tiles.add((x, y1))

#Figure out starting point 
avg_x = sum(p[0] for p in points) // len(points)
avg_y = sum(p[1] for p in points) // len(points)
center_point = (avg_x, avg_y)

#Flood fill

def flood_fill(start, boundary) -> set: 
    queue = [start]
    visited = set()
    while queue:
        x, y = queue.pop()
        
        if (x, y) in visited:
            continue
        
        visited.add((x, y))
        
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        for neighbor in neighbors:
            if neighbor not in boundary and neighbor not in visited:
                queue.append(neighbor)
    
    return visited

# visited = flood_fill(center_point, green_and_red_tiles)

def is_point_on_boundary(point):
    return point in green_and_red_tiles

def has_interior_intersection(p1, p2):
    x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
    
    x_interior = range(x1 + 1, x2)
    y_interior = range(y1 + 1, y2)
    
    for i in range(len(points)):
        v1 = points[i]
        v2 = points[(i + 1) % len(points)]
        
        if v1[1] == v2[1]: #Horizontal edge
            edge_y = v1[1]
            if edge_y in y_interior:
                edge_x_min, edge_x_max = min(v1[0], v2[0]), max(v1[0], v2[0])
                for x in range(edge_x_min + 1, edge_x_max):
                    if x in x_interior:
                        return True
        
        if v1[0] == v2[0]:
            edge_x = v1[0]
            if edge_x in x_interior:
                edge_y_min, edge_y_max = min(v1[1], v2[1]), max(v1[1], v2[1])
                for y in range(edge_y_min + 1, edge_y_max):
                    if y in y_interior:
                        return True
    return False

@lru_cache(maxsize= None)
def is_inside_or_on_boundary(point):
    if point in green_and_red_tiles:
        return True
    return is_point_in_polygon(point, points_tuple)

def is_point_in_polygon(point, vertices):
    num_intersections = 0
    num_vertices = len(vertices)
    
    for i in range(num_vertices):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % num_vertices]
        if ((v1[1] > point[1]) != (v2[1] > point[1])) and \
            (point[0] < (v2[0] - v1[0]) * (point[1] - v1[1]) / (v2[1] - v1[1]) + v1[0]):
            num_intersections += 1

    return num_intersections % 2 == 1

# valid_tiles = visited | green_and_red_tiles

def calc_corners(p1, p2) -> list:
    '''Returns list of 4 corners of rectange'''
    x1, y1 = p1
    x2, y2 = p2
    return [p1, p2, (x2, y1), (x1, y2)]

def rectangles_edges_valid(p1, p2):
    """Check if all 4 edges of rectangle are inside polygon (don't cross boundary except at corners)"""
    x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])
    
    corners = {(x1, y1), (x1, y2), (x2, y1), (x2, y2)}
    
    # Check all 4 edges of the rectangle
    # Top and bottom edges
    for x in range(x1, x2 + 1):
        if not is_inside_or_on_boundary((x, y1)):
            return False
        if not is_inside_or_on_boundary((x, y2)):
            return False
    
    # Left and right edges  
    for y in range(y1 + 1, y2):
        if not is_inside_or_on_boundary((x1, y)):
            return False
        if not is_inside_or_on_boundary((x2, y)):
            return False
    
    return True

def is_rectangle_fully_inside(p1, p2):
    corners = calc_corners(p1, p2)
    
    if not all(is_inside_or_on_boundary(c) for c in corners):
        return False
    
    if not rectangles_edges_valid(p1, p2):
        return False
    
    return True 

def is_rectangle_valid(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    corner3 = (x1, y2)
    corner4 = (x2, y1)
    
    if not (is_point_on_boundary(corner3) or is_point_on_boundary(corner4)):
        return False
    
    if has_interior_intersection(p1, p2):
        return False
    
    return True

part_two_area = 0
for i in range(len(points)):
    p = points[i]
    for j in range(i + 1, len(points)):
        q = points[j]
        
        area = calculate_area(p, q)
        if area <= part_two_area:
            continue
        
        if is_rectangle_valid(p, q):
            part_two_area = area

print(f"Part two answer: {part_two_area}")
# puzzle.answer_b = part_two_area