import numpy as np
import sys

sys.path.append("/home/mattykurlzz/itmo/cs_project/py-env-sim/src")
from primitives.vector import Vector

class Transforms:
    """class provides basic vector transformations"""

    def rotate_ip(self, angle: float, transformant: Vector):
        transform_matrix = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        transformant.dims = transformant.dims @ transform_matrix.T

    def rotate(self, angle: float, transformant: Vector):
        new_vector = transformant.copy()
        self.rotate_ip(angle, new_vector)
        return new_vector

    def move_along(self, deltas: np.ndarray, transformant: Vector) -> Vector:
        new_vector = transformant.copy()
        angle = np.arctan(new_vector.dims[0] / new_vector.dims[1])

        transform_matrix = np.array(
            [[np.cos(angle), np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )

        new_vector.origins.coords = (
            new_vector.origins.coords + deltas @ transform_matrix
        )
        return new_vector


if __name__ == "__main__":
    import math
    vector = Vector()
    print(vector.origins.coords, vector.dims)
    transforms = Transforms()

    vector = transforms.rotate(math.radians(180), vector)
    print(vector.origins.coords, vector.dims)
    vector = transforms.move_along(np.array([0, -10]), vector)
    print(vector.origins.coords, vector.dims)