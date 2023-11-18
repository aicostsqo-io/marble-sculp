from typing import List
import numpy as np
import random, math


def calculate_normal_plane(A: List[int], B: List[int], C: List[int]) -> List[int]:
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    AB = B - A
    AC = C - A

    return np.cross(AB, AC)


def sort_points(pts):
    pts = np.array(pts)
    centroid = np.sum(pts, axis=0) / pts.shape[0]
    vector_from_centroid = pts - centroid
    vector_angle = np.arctan2(vector_from_centroid[:, 1], vector_from_centroid[:, 0])
    sort_order = np.argsort(vector_angle)
    return pts[sort_order, :]


def calculate_dip_and_dip_direction_from_unit_vec(unit_vector: List[int]):
    dip_disc = math.acos(unit_vector[2]) * (180 / math.pi)
    dip_direction = math.atan2(unit_vector[0], unit_vector[1]) * (180 / math.pi)
    return [dip_disc / 2, dip_direction / 2]
