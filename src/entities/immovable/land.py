from core import Immovable
from primitives.point import Point

class Land(Immovable):
    vpos: float

    def __init__(self) -> None:
        self.vpos = 0

    def collides(self, other_p: Point) -> bool:
        if other_p.coords[1] <= self.vpos:
            return True
        return False
