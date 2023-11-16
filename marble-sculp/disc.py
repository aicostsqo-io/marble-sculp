from typing import List


class Discontinuity:
    def __init__(self, vertices: List[List[int]]):
        self.vertices = vertices
        self.faces = [[]]

        for ind, value in enumerate(self.vertices):
            self.faces[0].append(ind)
