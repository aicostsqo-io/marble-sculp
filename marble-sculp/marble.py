from typing import List
import math
import numpy as np


class Marble:
    def __init__(
        self,
        size: List[int] = [1, 1, 1],
        pos: List[int] = [0, 0, 0],
        rotation: List[int] = [0, 0, 0],
    ):
        self.type = "marble"
        self.size = size
        self.pos = pos
        self.color = None
        self.volume = size[0] * size[1] * size[2]
        self.vertices = [
            [0, 0, 0],  # A 0
            [size[0], 0, 0],  # B 1
            [size[0], size[1], 0],  # C 2
            [0, size[1], 0],  # D 3
            [0, 0, size[2]],  # E 4
            [size[0], 0, size[2]],  # F 5
            [size[0], size[1], size[2]],  # G 6
            [0, size[1], size[2]],  # H 7
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

        # Rotate the marble
        if rotation[0] != 0 or rotation[1] != 0 or rotation[2] != 0:
            self.rotate(rotation[0], rotation[1], rotation[2])

        # self.move(-(size[0] / 2), -(size[1] / 2), -(size[2] / 2))
        if pos[0] != 0 or pos[1] != 0 or pos[2] != 0:
            self.move(pos[0], pos[1], pos[2])

    @staticmethod
    def from_points(vertices: List[int], faces: List[int], volume: float = 0):
        mrb = Marble()
        mrb.volume = volume
        mrb.vertices = vertices
        mrb.faces = faces
        mrb.edges = []
        for face in mrb.faces:
            mrb.edges.append([face[0], face[1]])
            mrb.edges.append([face[1], face[2]])
            mrb.edges.append([face[2], face[0]])
        return mrb

    def move(self, x: float, y: float, z: float):
        self.pos = [x, y, z]
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append([vertex[0] + x, vertex[1] + y, vertex[2] + z])
        self.vertices = new_vertices

    def rotate(self, angle_x: float, angle_y: float, angle_z: float):

        new_vertices = []
        for vertex in self.vertices:
            new_vertex = vertex
            # Rotate around x-axis
            if angle_x != 0:
                new_x = [
                    [1, 0, 0],
                    [0, math.cos(angle_x), -math.sin(angle_x)],
                    [0, math.sin(angle_x), math.cos(angle_x)],
                ]
                new_vertex = np.dot(new_x, new_vertex)

            # Rotate around y-axis
            if angle_y != 0:
                new_y = [
                    [math.cos(angle_y), 0, math.sin(angle_y)],
                    [0, 1, 0],
                    [-math.sin(angle_y), 0, math.cos(angle_y)],
                ]
                new_vertex = np.dot(new_y, new_vertex)

            # Rotate around z-axis
            if angle_z != 0:
                new_z = [
                    [math.cos(angle_z), -math.sin(angle_z), 0],
                    [math.sin(angle_z), math.cos(angle_z), 0],
                    [0, 0, 1],
                ]
                new_vertex = np.dot(new_z, new_vertex)

            new_vertices.append(new_vertex)

        self.vertices = new_vertices
