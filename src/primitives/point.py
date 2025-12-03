import numpy as np
from numpy.typing import NDArray

class Point:
    coords: NDArray[np.float128]

    def __init__(self, coords: tuple[float, float] = (0, 0)) -> None:
        self.coords = np.array([*coords])

    def from_array(self, coords: NDArray[np.float128]) -> "Point":
        if len(coords) < 2:
            raise RuntimeError("passed array contains than 2 objects")
        self.coords = np.array([coords[0], coords[1]])
        return self

    def copy(self) -> "Point":
        return Point().from_array(self.coords.copy())
 
    def __getitem__(self, idx: int) -> float:
        return self.coords[idx]
