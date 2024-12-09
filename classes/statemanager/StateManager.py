import pygame
import pygame.freetype
from Constants import Constants
from classes.tools.GameDatabase import GameDatabase as GDB


class State:
    def __init__(self):
        """
        Initializes a new state with default values.

        Attributes:
            done (bool): Flag indicating if the state is complete.
            quit (bool): Flag indicating if the program should exit.
            next_state (str or None): Name of the next state to transition to.
            screen_rect (pygame.Rect): Rect representing the screen surface rectangle.
            persist (dict): Dictionary to maintain information between states.
            font (pygame.freetype.Font): Font object used for text rendering.
        """
        self.done = False  # Flag indicating if the state is complete
        self.quit = False  # Flag indicating if the program should exit
        self.next_state: str | None = None  # Name of the next state
        self.GDB = GDB()
        self.screen_rect = (
            pygame.display.get_surface().get_rect()
        )  # Rect of the screen surface
        self.persist = {}  # Dictionary to maintain information between states
        self.font = pygame.freetype.Font(
            Constants.FONTS["regular"], 24
        )  # Font used for text
        self.Bfont = pygame.freetype.Font(
            Constants.FONTS["bold"], 24
        )  # Font used for text

    def on_start(self, persistent: dict):
        """
        This method is called when a state resumes being active.
        Allows information to be passed between states.

        Args:
            persistent (dict): A dictionary containing the information to pass to this state.
        """
        self.persist = persistent

    def get_event(self, event: pygame.event.Event):
        """
        Handles a single event.

        Args:
            event: The event to handle.
        """
        pass

    def on_update(self, dt: float):
        """
        Updates the state. This method is called by the SM object once per frame.

        Args:
            dt (float): Time since the last frame in milliseconds.
        """

    def draw(self, surface: pygame.Surface):
        """
        Draws everything to the screen.

        Args:
            surface: The Pygame rendering surface.
        """
        pass


class SM:
    def __init__(
        self, screen: pygame.Surface, states: dict[str, State], start_state: str
    ):
        """
        Initializes a new state machine with the given parameters.

        Args:
            screen (pygame.Surface): The Pygame screen surface.
            states (dict[str, State]): A dictionary mapping state names to their corresponding State objects.
            start_state (str): Name of the initial active state.

        Attributes:
            done (bool): Flag indicating if the runtime loop is complete.
            clock (pygame.time.Clock): Clock to control frames per second (FPS).
            fps (int): Frames per second (FPS) frequency.
            states (dict[str, State]): Dictionary mapping state names to their corresponding State objects.
            state_name (str): Name of the current active state.
            state (State): The current active state object.
        """
        self.done = False  # Flag indicating if the runtime loop is complete
        self.screen = screen  # The Pygame screen surface
        self.clock = pygame.time.Clock()  # Clock to control frames per second (FPS)
        self.fps = Constants.FPS  # Frames per second (FPS) frequency
        self.states = states  # Dictionary mapping state names to their corresponding State objects
        self.state_name = start_state  # Name of the initial active state
        self.state = self.states[self.state_name]  # The current active state object

    def event_loop(self):
        """
        Passes events for handling by the current state.
        """
        for event in pygame.event.get():
            self.state.get_event(event)

    def next_state(self):
        """
        Switches to the next state.
        """
        current_state = self.state_name  # Current state name
        next_state = self.state.next_state  # Next state name
        self.state.done = False  # Reset the done flag for the current state
        self.state_name = next_state  # Update the current state name
        persistent = (
            self.state.persist
        )  # Get the persistent data from the current state
        self.state = self.states[next_state]  # Set the next state as active
        self.state.on_start(persistent)  # Start the next state with persistent data

    def update(self, dt: float):
        """
        Checks for a next state and updates the currently active state.

        Args:
            dt (float): Time elapsed since the last frame in milliseconds.
        """
        if self.state.quit:
            self.done = True  # Set the done flag if the program should exit
        elif self.state.done:
            self.next_state()  # Switch to the next state
        self.state.on_update(dt)  # Update the current active state

    def draw(self):
        """
        Passes the rendering surface to the currently active State class for drawing.
        """
        self.screen.fill((156, 74, 33))
        self.state.draw(self.screen)

    def run(self):
        """
        The runtime loop of the state machine will end here.
        """
        while not self.done:
            dt = self.clock.tick(
                self.fps
            )  # Get time elapsed since the last frame in milliseconds
            self.event_loop()  # Handle events
            self.update(dt)  # Update the current state
            self.draw()  # Draw on the screen surface
            pygame.display.flip()  # Update the screen surface
