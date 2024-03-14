from typing import List
import math
import numpy as np
from utils import normalize


class Discontinuity:
    def __init__(
        self,
        vertices: List[List[int]],
        normal: List[int] = None,
        two_ways: bool = True,
        color: List[float] = None,
    ):
        self.vertices = vertices
        self.faces = [[]]
        self.normal = normal
        self.pos = [0.0, 0.0, 0.0]
        self.color = color
        self.min_region = []
        self.max_region = []

        for ind, value in enumerate(self.vertices):
            self.faces[0].append(ind)
            self.pos[0] += value[0]
            self.pos[1] += value[1]
            self.pos[2] += value[2]

        self.pos[0] /= len(self.vertices)
        self.pos[1] /= len(self.vertices)
        self.pos[2] /= len(self.vertices)

        if two_ways:
            temp_faces = []
            for face in self.faces:
                temp_faces.append(list(reversed(face)))

            self.faces = self.faces + temp_faces

    def calculate_regions(self):
        min_x = min(self.vertices, key=lambda x: x[0])[0]
        min_y = min(self.vertices, key=lambda x: x[1])[1]
        min_z = min(self.vertices, key=lambda x: x[2])[2]

        max_x = max(self.vertices, key=lambda x: x[0])[0]
        max_y = max(self.vertices, key=lambda x: x[1])[1]
        max_z = max(self.vertices, key=lambda x: x[2])[2]

        self.max_region = [max_x, max_y, max_z]
        self.min_region = [min_x, min_y, min_z]

    def baecher(
        self,
        dip: int,
        dip_direction: int,
        fisher_constant: int,
        distribution_size: str,
        mean_fracture_size: int,
        sigma_fracture_size: int,
    ):
        if distribution_size not in ["log", "exp", "det"]:
            raise ValueError(
                "The value distribution_size is not one of the 'log', 'exp', 'det' values."
            )
        if fisher_constant > 0 and fisher_constant < 2:
            raise ValueError("fisher_constant value mustn't be between 0 and 2")

        self.calculate_regions()

        dip *= math.pi / 180
        dip_direction *= math.pi / 180

        exponential_distribution = np.random.exponential(1.0 / mean_fracture_size)
        lognormal_distribution = np.random.lognormal(
            mean_fracture_size, sigma_fracture_size
        )

        pole_all_rotated = np.zeros((3, 1))
        if fisher_constant >= 2:
            kapa = 0
            echis = (math.pi / 2) - dip
            if dip_direction >= 0 and dip_direction < math.pi:
                kapa = dip_direction + math.pi
            if dip_direction >= math.pi and dip_direction <= 2 * math.pi:
                kapa = dip_direction - math.pi
            pole_mean = [
                math.cos(kapa) * math.cos(echis),
                -math.sin(kapa) * math.cos(echis),
                -math.sin(echis),
            ]
            fisher_dip_dev_angle = math.acos(
                (fisher_constant + math.log(1 - np.random.uniform())) / fisher_constant
            )
            echis = (math.pi / 2) - (dip - fisher_dip_dev_angle)
            pole_dip_rotated = [
                math.cos(kapa) * math.cos(echis),
                -math.sin(kapa) * math.cos(echis),
                -math.sin(echis),
            ]
            random_angle = (math.pi * 2) * np.random.uniform()
            # print(np.dot(pole_mean, random_angle))

            # rot_correct_unit_vec = [random_angle, pole_mean] / np.linalg.norm(
            #     [random_angle, pole_mean]
            # )
            # rot_correct_unit_vec = np.dot(pole_mean, random_angle) / np.linalg.norm(
            #     np.dot(pole_mean, random_angle)
            # )
            # rot_correct_unit_vec = pole_mean / np.linalg.norm(pole_mean)
            rot_correct_unit_vec = normalize(np.dot(pole_mean, random_angle))
            pole_all_rotated = np.cross(rot_correct_unit_vec, pole_dip_rotated)
            print(pole_all_rotated)

        elif fisher_constant <= 0:
            random_dip = 90 * np.random.uniform()
            random_dip_direction = 2 * math.pi * np.random.uniform()
            kapa = 0
            echis = (math.pi / 2) - random_dip

            if random_dip_direction >= 0 and random_dip_direction < math.pi:
                kapa = random_dip_direction + math.pi
            if random_dip_direction >= math.pi and random_dip_direction <= 2 * math.pi:
                kapa = random_dip_direction - math.pi
            pole_dip_rotated = [
                math.cos(kapa) * math.cos(echis),
                -math.sin(kapa) * math.cos(echis),
                -math.sin(echis),
            ]

        width = 1
        height = 1
        rand_coord_x = self.min_region[0] - np.random.uniform() * (
            self.max_region[0] - self.min_region[0]
        )
        rand_coord_y = self.min_region[1] - np.random.uniform() * (
            self.max_region[1] - self.min_region[1]
        )
        rand_coord_z = self.min_region[2] - np.random.uniform() * (
            self.max_region[2] - self.min_region[2]
        )

        if distribution_size == "log":
            return {
                "pos": [rand_coord_x, rand_coord_y, rand_coord_z],
                "unit_vector": pole_all_rotated,
                "value": lognormal_distribution,
            }
        elif distribution_size == "exp":
            return {
                "pos": [rand_coord_x, rand_coord_y, rand_coord_z],
                "unit_vector": pole_all_rotated,
                "value": exponential_distribution,
            }
        elif distribution_size == "det":
            return {
                "pos": [rand_coord_x, rand_coord_y, rand_coord_z],
                "unit_vector": pole_all_rotated,
                "value": mean_fracture_size,
            }
