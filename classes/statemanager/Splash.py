import pygame
from classes.statemanager import State
from Constants import Constants


class Splash(State):
    def __init__(self) -> None:
        """
        Initializes a new Splash state.

        :return: None
        """
        super().__init__()
        self.next_state = "GAMEPLAY"

        # Load the background image
        self.background_image = pygame.image.load(
            f"{Constants.IMG_DIR}fabbrica1.png"
        ).convert()
        # Scale the background image to the screen size
        self.background_image = pygame.transform.scale(
            self.background_image,
            (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT),
        )

        # Set up the font
        self.Bfont.size = 36
        # Set up the text surface and rect
        self.text_surface, self.text_rect = self.Bfont.render(
            "Press spacebar to continue", (255, 255, 255)
        )
        # Center the text on the screen
        self.text_rect.center = (
            Constants.SCREEN_WIDTH // 2,
            Constants.SCREEN_HEIGHT - 70,
        )

        # Set up the font
        self.Bfont.size = 45
        self.title_surface, self.title_rect = self.Bfont.render(
            "Candy Factory Tycoon", (245, 189, 102)
        )
        self.title_rect.center = (Constants.SCREEN_WIDTH // 2, 80)

        self.title2_surface, self.title2_rect = self.Bfont.render(
            "Candy Factory Tycoon", (45, 20, 22)
        )
        self.title2_rect.center = (Constants.SCREEN_WIDTH // 2 + 3, 83)

    def get_event(self, event: pygame.event.Event) -> None:
        """
        Handles a single event.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.QUIT:
            self.GDB.close()
            # Quit the game if the user closes the window
            self.quit = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Continue to the next state if the user presses the spacebar
            self.done = True

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the background and text on the screen.

        :param screen: The Pygame Surface to draw on.
        """
        # Draw the background image at the top-left corner
        screen.blit(self.background_image, (0, 0))

        # Draw the text surface at the specified position
        screen.blit(self.title2_surface, self.title2_rect)
        screen.blit(self.title_surface, self.title_rect)
        screen.blit(self.text_surface, self.text_rect)
