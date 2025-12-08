from typing import Callable
import numpy as np

from primitives.vector import Vector

class Engine:
    maximum_force: float
    minimum_force: float
    current_force: float
    force_vector_transforms: list[Callable[[Vector], Vector]]
    current_vector: Vector

    def __init__(
        self,
        max_force: float,
        min_force: float,
        force_vector_transforms: list[Callable[[Vector], Vector]],
    ):
        self.maximum_force = max_force
        self.minimum_force = min_force
        self.current_force = 0.0
        self.force_vector_transforms = force_vector_transforms

    def renew_force_vector(self, main_vector: Vector) -> Vector:
        self.current_vector = main_vector
        for transform in self.force_vector_transforms:
            self.current_vector = transform(self.current_vector)
        return self.current_vector

    def turn_on(self):
        self.current_force = self.minimum_force

    def set_force(self, force: float):
        if force <= self.maximum_force and force >= self.minimum_force:
            self.current_force = force
