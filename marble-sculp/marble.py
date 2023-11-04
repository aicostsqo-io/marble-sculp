import matplotlib.pyplot as plt

from plane import Plane
from circle import Circle


class Marble:
    def __init__(self, pos: list = [0, 0, 0]):
        self.type = "marble"
        self.vertices = [
            [0, 0, 0],  # A 0
            [1, 0, 0],  # B 1
            [1, 1, 0],  # C 2
            [0, 1, 0],  # D 3
            [0, 0, 1],  # E 4
            [1, 0, 1],  # F 5
            [1, 1, 1],  # G 6
            [0, 1, 1],  # H 7
        ]
        self.faces = [
            [0, 3, 2, 1],  # ADCB
            [1, 2, 6, 5],  # BCGF
            [0, 4, 7, 3],  # AEHD
            [4, 5, 6, 7],  # EFGH
            [0, 1, 5, 4],  # ABFE
            [2, 3, 7, 6],  # CDHG
        ]
        self.edges = []
        for face in self.faces:
            self.edges.append([face[0], face[1]])
            self.edges.append([face[1], face[2]])
            self.edges.append([face[2], face[3]])
            self.edges.append([face[3], face[0]])

        self.plane = Plane()
        self.circle = Circle()

    def move(self, x: int, y: int, z: int):
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append([vertex[0] + x, vertex[1] + y, vertex[2] + z])
        self.vertices = new_vertices
