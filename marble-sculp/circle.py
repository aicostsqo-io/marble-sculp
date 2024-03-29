import math, copy
import numpy as np
from typing import List
from disc import Discontinuity
from utils import calculate_normal_plane, sort_points


class Circle:
    def __init__(self, radius: int = 1, segment: int = 32, two_ways: bool = True):
        self.type = "circle"
        self.radius = radius
        self.segment = segment
        self.two_ways = two_ways
        self.pos = [0.0, 0.0, 0.0]
        self.constant = 0
        self.color = None

        self.faces = []
        self.vertices = [self.pos]
        self.normal = [0, 0, 1]

        self._reset_rotation(two_ways)

    def move(self, x: int, y: int, z: int):
        self.pos = [x, y, z]
        self.constant = -np.array(self.pos).dot(self.normal)
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append([vertex[0] + x, vertex[1] + y, vertex[2] + z])
        self.vertices = new_vertices

    def _reset_rotation(self, two_ways: bool = True):
        self.faces = []
        self.vertices = [[0.0, 0.0, 0.0]]
        theta_length = 2 * math.pi
        for i in range(self.segment):
            self.vertices.append(
                [
                    math.cos(i / self.segment * theta_length) * self.radius,
                    math.sin(i / self.segment * theta_length) * self.radius,
                    0.0,
                ]
            )

        self.move(self.pos[0], self.pos[1], self.pos[2])

        for i in range(1, self.segment):
            self.faces.append([0, i, i + 1])

        self.faces.append([0, self.segment, 1])

        if two_ways:
            temp_faces = []
            for face in self.faces:
                temp_faces.append([face[0], face[2], face[1]])

            self.faces = self.faces + temp_faces

    def rotate(self, dip: int, dip_direction: int):
        self._reset_rotation(self.two_ways)
        self._dip = dip
        self._dip_direction = dip_direction

        deg_to_rad = math.pi / 180
        temp_vertices = copy.deepcopy(self.vertices)
        for ind, vertex in enumerate(self.vertices):
            # --- Dip Rotate ---
            temp_vertices[ind] = np.dot(
                [
                    [math.cos(dip * deg_to_rad), 0, math.sin(dip * deg_to_rad)],
                    [0, 1, 0],
                    [-math.sin(dip * deg_to_rad), 0, math.cos(dip * deg_to_rad)],
                ],
                self.vertices[ind],
            )

            # --- Dip Direction Rotate
            temp_vertices[ind] = np.dot(
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

        self.normal = calculate_normal_plane(
            self.vertices[1], self.vertices[2], self.vertices[3]
        )

    def intersections(
        self,
        edges: List[List[int]],
        vertices: List[List[int]],
        color: List[float] = None,
    ):
        lines = [[vertices[i[0]], vertices[i[1]]] for i in edges]
        intersection_list = []
        for line in lines:
            start_sign = (
                self.normal[0] * line[0][0]
                + self.normal[1] * line[0][1]
                + self.normal[2] * line[0][2]
                + self.constant
            )
            # start_sign = np.array(self.normal).dot(line[0]) + self.constant
            end_sign = (
                self.normal[0] * line[1][0]
                + self.normal[1] * line[1][1]
                + self.normal[2] * line[1][2]
                + self.constant
            )
            # end_sign = np.array(self.normal).dot(line[1]) + self.constant
            # print(start_sign, end_sign)
            if (start_sign < 0 and end_sign > 0) or (end_sign < 0 and start_sign > 0):
                direction = np.array(line[1]) - np.array(line[0])
                # denominator = np.array(self.normal).dot(direction)
                denominator = (
                    self.normal[0] * direction[0]
                    + self.normal[1] * direction[1]
                    + self.normal[2] * direction[2]
                )
                # print(denominator)
                # print((np.array(line[0]).dot(self.normal) + self.constant))
                # print("===")

                t = -(np.array(line[0]).dot(self.normal) + self.constant) / denominator
                # print(t)

                if t < 0 or t > 1:
                    # print(t)
                    continue

                # print(line[0], direction, t)
                temp_coord = [line[0][0], line[0][1], line[0][2]]
                temp_coord[0] += direction[0] * t
                temp_coord[1] += direction[1] * t
                temp_coord[2] += direction[2] * t

                if temp_coord not in intersection_list:
                    intersection_list.append(temp_coord)

        if not intersection_list:
            return None
        # self._reset_rotation()

        return Discontinuity(sort_points(intersection_list), self.normal, color=color)
