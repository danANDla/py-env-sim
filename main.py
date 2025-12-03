import numpy as np
import pygame, operator
from abc import ABC, abstractmethod

GRAVITY_CONST = 9.81

npdtype = np.float32

from typing import Callable, TypeVar, ParamSpec, Annotated
from numpy.typing import NDArray

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

def init_rocket() -> SimEnvironment:

    main_engine_transforms: Callable[[Vector], Vector] = lambda v: transforms.rotate(
        np.pi, transforms.move_along(np.array([0, -10]), v)
    )
    main_engine = Engine(200000, 58000, main_engine_transforms)

    rotating_engine_transforms: Callable[[Vector], Vector] = (
        lambda v: transforms.rotate(
            np.pi / 2, transforms.move_along(np.array([0, -10]), v)
        )
    )
    rotating_engine = Engine(1000, 1000, rotating_engine_transforms)

    def gravity_func(force: np.ndarray, mass: float) -> np.ndarray:
        force[1] -= GRAVITY_CONST * mass
        return force

    gravity = Force(gravity_func, ["body_model.weight"])

    myrocket = Rocket(
        forces=[gravity],
        engines=[main_engine, rotating_engine],
        initial_tilt=10 * (np.pi / 180),
    )

    for engine in myrocket.engines:
        engine.turn_on()

    env = SimEnvironment([myrocket])
    return env


def launch_sim(screen: pygame.Surface, center_offset: tuple[int, int]):
    running = True
    dt = 0
    fps = 60

    env = init_rocket()

    myrocket = env.rockets[0]

    rocket_x = myrocket.body_model.current_coordinates[0] + center_offset[0]
    rocket_y = myrocket.body_model.current_coordinates[1] + center_offset[1]

    rocket_surface = pygame.Surface(myrocket.body_model.dims, pygame.SRCALPHA)
    rect = pygame.draw.rect(rocket_surface, "black", rocket_surface.get_rect())
    rect.center = (rocket_x, rocket_y)
    angle = myrocket.body_model.tilt * 180 / np.pi

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(fps) / 1000  # todo
        env.time_step(dt)
        for rocket in env.rockets:
            if env.land.collides(
                Point(
                    (
                        rocket.body_model.current_coordinates[0],
                        rocket.body_model.current_coordinates[1],
                    )
                )
            ):
                rocket.revert_timestep_move()

        screen.fill("white")

        pygame.draw.rect(
            screen,
            "black",
            (
                0,
                center_offset[1] + myrocket.body_model.dims[1],
                center_offset[0] * 2,
                center_offset[1] * 2,
            ),
        )
        rect.move_ip(*(myrocket.delta_coordinates.astype(int) * -1))
        old_center = rect.center

        angle = myrocket.body_model.tilt * 180 / np.pi
        rotated_surface = pygame.transform.rotate(
            rocket_surface, angle=angle * -1 % 360
        )
        rotated_rect = rotated_surface.get_rect()
        rotated_rect.center = old_center

        screen.blit(rotated_surface, rotated_rect)
        pygame.display.flip()

        for engine in myrocket.engines:
            engine.set_force(engine.current_force + 500)

        if myrocket.resulting_linear_acceleration[1] >= 0:
            myrocket.release()

        print(myrocket.body_model.current_coordinates)


if __name__ == "__main__":
    pygame.init()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode(
        (infoObject.current_w / 2, infoObject.current_h / 2)
    )
    clock = pygame.time.Clock()
    running = True

    center_offset = (int(infoObject.current_w / 4), int(infoObject.current_h / 4))

    launch_sim(screen, center_offset)

    pygame.quit()
