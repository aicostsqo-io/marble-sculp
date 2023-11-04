import math


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
