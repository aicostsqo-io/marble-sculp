class Plane:
    def __init__(self, width: int = 2, height: int = 2):
        self.vertices = [
            [0, 0, 0],
            [0, 0, width],
            [0, height, width],
            [0, height, 0],
        ]

        self.face = [0, 1, 2, 3]

        self.edges = []
        self.edges.append([self.face[0], self.face[1]])
        self.edges.append([self.face[1], self.face[2]])
        self.edges.append([self.face[2], self.face[3]])
        self.edges.append([self.face[3], self.face[0]])

        self.move(0, -(height / 4), -(width / 4))

    def move(self, x: int, y: int, z: int):
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append([vertex[0] + x, vertex[1] + y, vertex[2] + z])
        self.vertices = new_vertices
