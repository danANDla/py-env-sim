import pygame

class Animation:
    def __init__(self) -> None:
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
        self.fps = 60

    def __del__(self):
        pygame.quit()
