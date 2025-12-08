import numpy as np
from numpy.typing import NDArray

from primitives.point import Point

class Vector:
    dims: NDArray[np.float128]
    origins: Point

    def __init__(self):
        self.dims = np.array([0, 1])
        self.origins = Point((0, 0))

    def from_two_origins(self, from_vec: "Vector", to_vec: "Vector") -> "Vector":
        return Vector().from_two_points(from_vec.origins, to_vec.origins)

    def from_two_points(self, from_p: Point, to_p: Point) -> "Vector":
        new_vec = Vector()

        new_vec.origins = from_p.copy()
        new_vec.dims = to_p.coords - from_p.coords

        return new_vec

    def copy(self) -> "Vector":
        ret = Vector()
        ret.dims = self.dims.copy()
        ret.origins = self.origins.copy()
        return ret

    def get_scalar_len(self):
        return np.sqrt(np.square(self.dims).sum())

    def distance_to(self, point: Point):
        self_k = self.dims[1] / self.dims[0]  # todo: catch zero division
        self_b = self.origins.coords[1] + (-self.origins.coords[0] * self_k)

        other_k = -1 / self_k
        other_b = point.coords[1] - other_k * point.coords[0]

        x = (other_b - self_b) / (self_k - other_k)
        y = x * self_k + self_b

        len = Vector().from_two_points(Point((x, y)), point).get_scalar_len()
        return len
