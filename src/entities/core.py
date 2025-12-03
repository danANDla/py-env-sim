from immovable.core import *
from engine import *
from rocket import *

class SimEnvironment:
    rockets: list[Rocket]
    land: Land

    def __init__(self, rockets: list[Rocket]) -> None:
        self.rockets = rockets
        self.land = Land()

    def time_step(self, time_step: float):
        for rocket in self.rockets:
            rocket._time_step(time_step)
