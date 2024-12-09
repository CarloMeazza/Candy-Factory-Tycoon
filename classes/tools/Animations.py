import pygame
from typing import List, Tuple


class Animation(pygame.sprite.Sprite):
    def __init__(
        self,
        frames: List[pygame.Surface],
        pos: Tuple[int, int] = (0, 0),
        frame_duration: float = 0.25,
        pause_duration: float = 1.0,
        loop: bool = True,
    ) -> None:
        """
        Initializes an Animation with the given frames, position, and timing settings.

        Args:
            frames (List[pygame.Surface]): A list of frames for the animation.
            pos (Tuple[int, int], optional): The initial position of the animation. Defaults to (0, 0).
            frame_duration (float, optional): Duration of each frame in seconds. Defaults to 0.25.
            pause_duration (float, optional): Pause at the end of the animation cycle in seconds. Defaults to 1.0.
            loop (bool, optional): Whether the animation should loop. Defaults to True.
        """
        super().__init__()
        self.frames = frames
        self.loop = loop
        self.finished = False
        self.frame_duration_ms = frame_duration * 1000  # Convert to milliseconds
        self.pause_duration_ms = pause_duration * 1000  # Convert to milliseconds

        # Animation state
        self.current_frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.cycle_start_time = pygame.time.get_ticks()

        # Current frame image and position
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def _should_update_frame(self, current_time: int) -> bool:
        """Checks if enough time has passed to update the frame."""
        return current_time - self.last_update_time > self.frame_duration_ms

    def _should_pause_cycle(self, current_time: int) -> bool:
        """Checks if the animation cycle should pause at the end."""
        return (
            self.current_frame_index == 0
            and current_time - self.cycle_start_time < self.pause_duration_ms
        )

    def update(self) -> None:
        """
        Updates the current frame of the animation if timing conditions are met.
        """
        current_time = pygame.time.get_ticks()

        # Stop updating if the animation is not looping and reached the last frame
        if not self.loop and self.current_frame_index == len(self.frames) - 1:
            self.finished = True
            return

        # Update frame if enough time has passed
        if self._should_update_frame(current_time):
            self.last_update_time = current_time
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

            # Handle pause at the end of the cycle
            if self._should_pause_cycle(current_time):
                self.current_frame_index = len(self.frames) - 1  # Lock to last frame
            elif self.current_frame_index == 0:
                self.cycle_start_time = current_time  # Reset cycle timer

            # Update the current frame image
            self.image = self.frames[self.current_frame_index]

    @property
    def is_finished(self):
        return self.finished
