#creates a polygon object and algorithmically creates random polygons given a 
#number of vertices as well as the dimensions of which they can be placed

import cmu_112_graphics_openCV
import random
import math

class Polygon():
    def __init__(self, edges, width, height):

        #minimum 3 sides
        self.edges = edges if edges > 2 else 3

        if edges >= 5: 
            self.difficulty = "Easy"
        elif 5 < edges <= 8: 
            self.difficulty = "Medium"
        else:
            self.difficulty = "Hard"
        

        self.points = []
        for _ in range(edges):
            cx = width // 2
            cy = height // 2

            theta = random.randint(0, 360)
            r = random.randint(0, min(cx, cy))

            x = cx + r * math.cos(theta * (180 / math.pi))
            y = cy + r * math.sin(theta * (180 / math.pi))

            self.points.append((x, y, theta))
