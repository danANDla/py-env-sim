import numpy as np
import operator
from numpy.typing import NDArray

from primitives.core import transforms, Vector, Force, Point
from engine import Engine

class RocketBody:
    dims: list[float]
    current_coordinates: np.ndarray
    # main_vector: Vector

    def __init__(
        self, dims: tuple[float, float] = (5, 25), weight: float = 90, tilt: float = 0
    ) -> None:
        self.dims = [dims[0], dims[1]]
        self.weight = weight
        self.tilt = tilt

        self.current_coordinates = np.array([0, 0], dtype=np.float128)
        self.prev_coordinates = np.array([0, 0], dtype=np.float128)
        self.current_vector = transforms.rotate(tilt, Vector())
        self.prev_vector = transforms.rotate(tilt, Vector())

    def get_mass_centre(self):
        return self.current_vector.origins

    def add_tilt(self, angle):
        self.tilt += angle
        transforms.rotate_ip(angle, self.current_vector)

class Rocket:
    forces: list[Force]
    engines: list[Engine]
    hold_inplace: bool
    resulting_linear_acceleration: NDArray[np.float128]
    body_model: RocketBody

    def add_force(self, force: Force):
        self.forces.append(force)

    def __init__(
        self, forces: list[Force], engines: list[Engine], initial_tilt: float = 0
    ):
        # delta movement of a rocket from prev step
        self.delta_coordinates = np.array([0, 0], dtype=np.float128)
        self.delta_angle = 0.0
        self.current_linear_speed: np.ndarray = np.array([0, 0], dtype=np.float128)
        self.current_rotation_speed: float = 0.0
        self.prev_linear_speed = np.array([0, 0], dtype=np.float128)
        self.prev_rotation_speed: float = 0.0
        self.zero_vector = np.array([0, 0], dtype=np.float128)
        self.resulting_linear_acceleration = np.array([0, 0], dtype=np.float128)

        self.body_model = RocketBody(tilt=initial_tilt)

        self.prev_time = 0
        self.forces = forces
        self.engines = engines

        self.hold_inplace = True

    def release(self):
        self.hold_inplace = False

    def _time_step(self, time_step: float):
        self.prev_time += time_step

        self.prev_linear_speed: np.ndarray = self.current_linear_speed.copy()
        self.prev_rotation_speed: float = self.current_rotation_speed
        self.body_model.prev_coordinates = self.body_model.current_coordinates.copy()
        self.body_model.prev_vector = self.body_model.current_vector.copy()

        real_linear_acceleration = self.zero_vector.copy()
        real_rotation_acceleration: float = 0.0

        for force in self.forces:
            arg_list: list[float] = []
            for parameter_name in force.attribute_names:
                arg_list.append(operator.attrgetter(parameter_name)(self))
            real_linear_acceleration = force.update(real_linear_acceleration, *arg_list)  # type: ignore

        for engine in self.engines:
            engine_force_vector = engine.renew_force_vector(
                self.body_model.current_vector
            )
            engine_power = engine.current_force
            force_vector = engine_force_vector.dims * -1.0 * engine_power
            force_scalar = float(np.sqrt(force_vector[0] ** 2 + force_vector[1] ** 2))

            real_linear_acceleration += force_vector / self.body_model.weight

            rotation_moment = force_scalar * engine_force_vector.distance_to(
                Point(
                    (
                        self.body_model.get_mass_centre()[0],
                        self.body_model.get_mass_centre()[1],
                    )
                )
            )
            inertia_moment = (
                self.body_model.dims[0]
                * self.body_model.dims[1]
                * (self.body_model.dims[0] ** 2 + self.body_model.dims[1] ** 2)
                / 12
            )

            real_rotation_acceleration += rotation_moment / inertia_moment

        self.resulting_linear_acceleration = real_linear_acceleration

        if not self.hold_inplace:
            self.current_linear_speed += real_linear_acceleration * time_step
            self.current_rotation_speed += real_rotation_acceleration * time_step

            self.delta_coordinates = (
                self.current_linear_speed * time_step
                + self.prev_linear_speed * time_step
            ) / 2
            self.delta_angle = (
                self.current_rotation_speed * time_step
                + self.prev_rotation_speed * time_step
            ) / 2
            self.body_model.current_coordinates += self.delta_coordinates
            self.body_model.add_tilt(self.delta_angle)

    def revert_timestep_move(self):
        self.current_linear_speed = self.prev_linear_speed.copy()
        self.current_rotation_speed = self.prev_rotation_speed
        self.body_model.current_coordinates = self.body_model.prev_coordinates.copy()
        self.body_model.current_vector = self.body_model.prev_vector.copy()
