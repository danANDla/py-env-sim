from typing import Callable
import numpy as np

class Force:
    value_lambda: Callable[..., np.ndarray]
    attribute_names: list[str]

    def __init__(self, value_lambda: Callable[..., np.ndarray], attributes: list[str]):
        self.value_lambda = value_lambda
        self.attribute_names = attributes

    def update(self, *args) -> np.ndarray:  # type: ignore
        return self.value_lambda(*args)
