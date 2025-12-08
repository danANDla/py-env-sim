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

        # Zoom and pan variables
        self.zoom_scale = 1.0
        self.pan_offset = [0, 0]  # Additional offset for panning
        self.is_panning = False
        self.last_mouse_pos = (0, 0)
        
        self.center_offset = (
            int(self.infoObject.current_w / 4),
            int(self.infoObject.current_h / 4)
        )

        self.dt = 0

        if type(fps) == str:
            fps = int(fps)

        self.fps = fps

    def handle_events(self):
        """Handle pygame events for zoom and pan"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom in/out with mouse wheel
                mouse_pos_before = pygame.mouse.get_pos()
                
                # Calculate world position before zoom
                world_pos_before = self.screen_to_world(mouse_pos_before)
                
                # Adjust zoom scale
                if event.y > 0:  # Scroll up
                    self.zoom_scale *= 1.1
                elif event.y < 0:  # Scroll down
                    self.zoom_scale *= 0.9
                
                # Clamp zoom scale
                self.zoom_scale = max(0.1, min(10.0, self.zoom_scale))
                
                # Calculate world position after zoom
                world_pos_after = self.screen_to_world(mouse_pos_before)
                
                # Adjust pan offset to keep mouse position fixed in world space
                self.pan_offset[0] += (world_pos_after[0] - world_pos_before[0]) * self.zoom_scale
                self.pan_offset[1] += (world_pos_after[1] - world_pos_before[1]) * self.zoom_scale
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.is_panning = True
                    self.last_mouse_pos = event.pos
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.is_panning = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.is_panning:
                    # Calculate mouse movement
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    
                    # Update pan offset
                    self.pan_offset[0] += dx
                    self.pan_offset[1] += dy
                    
                    self.last_mouse_pos = event.pos
        
        return True

    def screen_to_world(self, screen_pos):
        """Convert screen coordinates to world coordinates"""
        x, y = screen_pos
        world_x = (x - self.center_offset[0] - self.pan_offset[0]) / self.zoom_scale
        world_y = (y - self.center_offset[1] - self.pan_offset[1]) / self.zoom_scale
        return (world_x, world_y)

    def world_to_screen(self, world_pos):
        """Convert world coordinates to screen coordinates"""
        x, y = world_pos
        screen_x = x * self.zoom_scale + self.center_offset[0] + self.pan_offset[0]
        screen_y = y * self.zoom_scale + self.center_offset[1] + self.pan_offset[1]
        return (screen_x, screen_y)

    def update(self, env: SimEnvironment):
        # Handle events (zoom and pan)
        if not self.handle_events():
            return

        self.screen.fill("white")

        rockets = env.rockets
        for myrocket in rockets:
            # Convert world coordinates to screen coordinates with zoom and pan
            rocket_screen_pos = self.world_to_screen(
                (-myrocket.body_model.current_coordinates[0],
                 -myrocket.body_model.current_coordinates[1])
            )
            
            # Scale rocket dimensions based on zoom
            scaled_dims = (
                int(myrocket.body_model.dims[0] * self.zoom_scale),
                int(myrocket.body_model.dims[1] * self.zoom_scale)
            )
            
            # Create rocket surface with scaled dimensions
            rocket_surface = pygame.Surface(scaled_dims, pygame.SRCALPHA)
            
            # Draw rocket rectangle
            pygame.draw.rect(rocket_surface, "black", rocket_surface.get_rect())
            
            # Calculate ground position (scaled and panned)
            ground_top = self.world_to_screen((0, myrocket.body_model.dims[1]))[1]
            ground_height = self.screen.get_height() - ground_top
            
            # Draw ground
            pygame.draw.rect(
                self.screen,
                "black",
                (
                    0,
                    ground_top,
                    self.screen.get_width(),
                    ground_height
                ),
            )
            
            # Rotate the rocket surface
            angle = myrocket.body_model.tilt * 180 / np.pi
            rotated_surface = pygame.transform.rotate(
                rocket_surface, angle=angle * -1 % 360
            )
            
            # Get the rectangle of the rotated surface and center it
            rotated_rect = rotated_surface.get_rect()
            rotated_rect.center = rocket_screen_pos
            
            # Blit the rotated rocket onto the screen
            self.screen.blit(rotated_surface, rotated_rect)
            
        pygame.display.flip()

    def __del__(self):
        pygame.quit()