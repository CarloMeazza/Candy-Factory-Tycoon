import pygame
import traceback
from Constants import Constants
import classes.statemanager as StateManager


def main() -> None:
    """
    Main function to run the game.

    This function initializes the Pygame library, sets up the display screen,
    initializes the state manager with various game states, and runs the game loop.

    :return: None
    """
    # Initialize Pygame
    pygame.init()

    # Set up the display screen with specified width and height, and enable fullscreen mode
    screen: pygame.Surface = pygame.display.set_mode(
        (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
    )
    # Set the window title
    pygame.display.set_caption("Candy Factory Tycoon")

    # Check if the screen was initialized successfully
    if screen is None:
        raise RuntimeError("Error initializing screen.")

    # Initialize the state manager with the screen and game states
    state_manager: StateManager.SM = StateManager.SM(
        screen,
        {
            "SPLASH": StateManager.Splash(),
            "GAMEPLAY": StateManager.GamePlay(),
        },
        "SPLASH",
    )

    # Check if the state manager was initialized successfully
    if state_manager is None:
        raise RuntimeError("Error initializing state manager.")
    try:
        # Run the main game loop
        state_manager.run()
    except Exception as e:
        # Handle any exceptions that occur during the game loop
        traceback.print_exc()
    finally:
        # Quit Pygame and the program gracefully
        pygame.quit()
        quit()


if __name__ == "__main__":
    main()
