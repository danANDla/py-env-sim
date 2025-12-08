from entities import rocket
from entities.core import SimEnvironment
import pygame
import numpy as np

class Animation:
    def __init__(self, fps: int | str = 60) -> None:
        pygame.init()
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (self.infoObject.current_w / 2, self.infoObject.current_h / 2)
        )
        self.clock = pygame.time.Clock()
        self.running = True

        self.center_offset = (
            int(self.infoObject.current_w / 4),
            int(self.infoObject.current_h / 4)
        )

        self.dt = 0

        if type(fps) == str:
            fps = int(fps)

        self.fps = fps

    def update(self, env: SimEnvironment):
        self.screen.fill("white")

        rockets = env.rockets
        for myrocket in rockets:
            rocket_x = -myrocket.body_model.current_coordinates[0] + self.center_offset[0]
            rocket_y = -myrocket.body_model.current_coordinates[1] + self.center_offset[1]

            rocket_surface = pygame.Surface(myrocket.body_model.dims, pygame.SRCALPHA)
            rect = pygame.draw.rect(rocket_surface, "black", rocket_surface.get_rect())
            rect.center = (rocket_x, rocket_y)
            angle = myrocket.body_model.tilt * 180 / np.pi

            pygame.draw.rect(
                self.screen,
                "black",
                (
                    0,
                    self.center_offset[1] + myrocket.body_model.dims[1],
                    self.center_offset[0] * 2,
                    self.center_offset[1] * 2,
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

            self.screen.blit(rotated_surface, rotated_rect)
            pygame.display.flip()

            print(myrocket.body_model.current_coordinates)

    def __del__(self):
        pygame.quit()
