from typing import List


class Marble:
    def __init__(self, size: List[int] = [1, 1, 1], pos: List[int] = [0, 0, 0]):
        self.type = "marble"
        self.size = size
        self.pos = pos
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

        self.move(-(size[0] / 2), -(size[1] / 2), -(size[2] / 2))
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
