import math, copy


class Circle:
    def __init__(self, radius: int = 1, segment: int = 32, two_ways: bool = True):
        self.type = "circle"
        self.radius = radius
        self.segment = segment

        self.faces = []
        self.vertices = [[0.0, 0.0, 0.0]]
        theta_length = 2 * math.pi

        for i in range(segment):
            self.vertices.append(
                [
                    math.cos(i / segment * theta_length),
                    math.sin(i / segment * theta_length),
                    0.0,
                ]
            )

        for i in range(1, segment):
            self.faces.append([0, i, i + 1])

        self.faces.append([0, segment, 1])

        if two_ways:
            temp_faces = []
            for face in self.faces:
                temp_faces.append([face[0], face[2], face[1]])

            self.faces = self.faces + temp_faces

    def rotate(self, dip: int, dip_direction: int):
        deg_to_rad = math.pi / 180
        temp_vertices = copy.deepcopy(self.vertices)
        for ind, vertex in enumerate(self.vertices):
            # --- Dip Rotate ---
            temp_vertices[ind] = self.product(
                [
                    [math.cos(dip * deg_to_rad), 0, math.sin(dip * deg_to_rad)],
                    [0, 1, 0],
                    [-math.sin(dip * deg_to_rad), 0, math.cos(dip * deg_to_rad)],
                ],
                self.vertices[ind],
            )
            # --- Dip Direction Rotate
            temp_vertices[ind] = self.product(
                [
                    [1, 0, 0],
                    [
                        0,
                        math.cos(dip_direction * deg_to_rad),
                        -math.sin(dip_direction * deg_to_rad),
                    ],
                    [
                        0,
                        math.sin(dip_direction * deg_to_rad),
                        math.cos(dip_direction * deg_to_rad),
                    ],
                ],
                temp_vertices[ind],
            )
        self.vertices = temp_vertices

    def product(self, matris: list, pos: list) -> list:
        temp_pos = [0, 0, 0]
        for i in range(3):
            temp_pos[i] = (
                matris[i][0] * pos[0] + matris[i][1] * pos[1] + matris[i][2] * pos[2]
            )
        return temp_pos
