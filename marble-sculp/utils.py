from typing import List
import numpy as np


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
