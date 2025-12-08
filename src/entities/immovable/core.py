from abc import abstractmethod

from primitives.point import Point

class Immovable:
    @abstractmethod
    def collides(self, other_p: Point) -> bool:
        pass
