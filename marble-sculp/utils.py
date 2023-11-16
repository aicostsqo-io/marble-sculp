from typing import List
import numpy as np


def calculate_normal_plane(A: List[int], B: List[int], C: List[int]) -> List[int]:
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    AB = B - A
    AC = C - A

    return np.cross(AB, AC)
