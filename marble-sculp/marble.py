import matplotlib.pyplot as plt

from plane import Plane


class Marble:
    def __init__(self, pos: list = [0, 0, 0]):
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
            [0, 1, 2, 3],  # ABCD
            [1, 2, 6, 5],  # BCFG
            [0, 3, 7, 4],  # ADHE
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

    def move(self, x: int, y: int, z: int):
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append([vertex[0] + x, vertex[1] + y, vertex[2] + z])
        self.vertices = new_vertices

    def convert_obj(self):
        data = ""
        for vertex in self.vertices:
            data += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"

        for plane_vertex in self.plane.vertices:
            data += f"v {plane_vertex[0]} {plane_vertex[1]} {plane_vertex[2]}\n"

        plane_vertex_start = len(self.vertices)
        temp_faces = ""
        for point in self.plane.face:
            temp_faces += f"{point+plane_vertex_start+1} "
        data += f"f {temp_faces}\n"

        for face in self.faces:
            temp_faces = ""
            for point in face:
                temp_faces += f"{point+1} "
            data += f"f {temp_faces}\n"

        with open("./object.obj", "w") as fp:
            fp.write(data)


marb = Marble()
# marb.move(-0.5, -0.5, -0.5)
marb.convert_obj()
