import pygame
from typing import List, Tuple
from Constants import Constants
from classes.models.GameModels import Game
from classes.tools.formatLargeNumber import format_large_number as fln
from classes.tools.ModalProduct import ModalProduct


class Sidemenu:
    def __init__(self, save_game: Game) -> None:
        """
        Initializes the Sidemenu with the given game state.

        :param save_game: The current game state.
        """
        # Set up fonts
        self.font = pygame.freetype.Font(Constants.FONTS["regular_comic"], 15)
        self.bold_font = pygame.freetype.Font(Constants.FONTS["bold"], 24)

        # Initialize modal and game state
        self.modal = ModalProduct()
        self.save_game = save_game

        # Sidemenu dimensions and properties
        self.width = 300
        self.height = Constants.SCREEN_HEIGHT
        self.color = (241, 170, 105)
        self.open_speed = 20
        self.is_open = False

        # Create and configure the sidemenu surface
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x = Constants.SCREEN_WIDTH

        # Load and configure the close button image
        self.close_img = pygame.image.load(f"{Constants.IMG_DIR}close.png")
        self.close_img = pygame.transform.scale(self.close_img, (50, 50))
        self.close_rect = self.close_img.get_rect(
            topright=(Constants.SCREEN_WIDTH - 10, 10)
        )

        # Initialize buttons
        self.btns = self._initialize_buttons()

    def _initialize_buttons(self) -> List[Tuple[pygame.Surface, pygame.Rect]]:
        """
        Initializes the buttons for the side menu.

        :return: A list of tuples containing the button surface and its rect.
        """
        buttons = []
        for i, product in enumerate(self.save_game.factory.productions):
            # Create a new button surface
            btn_surface = pygame.Surface((200, 60))
            # Fill the button with the correct color
            if product.active:
                # Green if the product is active
                btn_surface.fill((45, 20, 22))
            else:
                # Grey if the product is inactive
                btn_surface.fill((104, 128, 123))
            # Set the button rect to the correct position
            btn_rect = btn_surface.get_rect()
            btn_rect.topleft = (self.rect.w // 2 - btn_rect.w // 2, 70 * (i + 1))
            # Add the button to the list
            buttons.append((btn_surface, btn_rect))
        return buttons

    def event(self, event: pygame.event.Event) -> None:
        """
        Handles events related to the side menu.

        :param event: The event to be handled.
        """
        self.modal.event(event)
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        # Set the cursor to a hand if the user is hovering over a button
        if not self.modal.is_open:
            if self.btns:
                for _, btn_rect in self.btns:
                    if btn_rect.collidepoint(relative_mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break

            # Set the cursor to a hand if the user is hovering over the close button
            if self.close_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Change the cursor style if it is not already set
        if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Handle mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_rect.collidepoint(event.pos):
                self.is_open = False

            # Handle button clicks
            for i, (_, btn_rect) in enumerate(self.btns):
                if btn_rect.collidepoint(relative_mouse_pos):
                    print(f"Button {i+1} clicked")
                    if (
                        self.save_game.factory.productions[i].next_lvl_cost
                        >= self.save_game.coins
                    ):
                        self.modal.production_number = i + 1
                        self.modal.is_open = True

    def update(self, save_game: Game) -> None:
        """
        Update the state of the side menu and modal.

        :param save_game: The current game state.
        """
        # Update the modal with the new game state
        self.modal.update(save_game)
        # Update the side menu's game state
        self.save_game = save_game

        # Animate the opening of the side menu
        if self.is_open and self.rect.x > Constants.SCREEN_WIDTH - self.width:
            self.rect.x = max(
                Constants.SCREEN_WIDTH - self.width, self.rect.x - self.open_speed
            )
        # Animate the closing of the side menu
        elif not self.is_open and self.rect.x < Constants.SCREEN_WIDTH:
            self.rect.x = min(Constants.SCREEN_WIDTH, self.rect.x + self.open_speed)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the side menu and all its children onto the screen.

        :param screen: The Pygame rendering surface.
        """
        # Only draw the side menu if it is open
        if self.rect.x < Constants.SCREEN_WIDTH:
            screen.blit(self.surface, self.rect)

        # Draw the close button if the side menu is fully open
        if self.rect.x + self.width == Constants.SCREEN_WIDTH:
            screen.blit(self.close_img, self.close_rect)

            # Draw each button and its text
            for i, (btn_surface, btn_rect) in enumerate(self.btns):
                production = self.save_game.factory.productions[i]

                # Fill the button with a different color if it is active
                if production.active:
                    btn_surface.fill((45, 20, 22))
                else:
                    btn_surface.fill((104, 128, 123))

                # Draw the product name and level on the button
                name_surface, name_rect = self.font.render(
                    production.product_name, (241, 170, 105)
                )
                name_rect.topleft = (10, 10)
                btn_surface.blit(name_surface, name_rect)

                lvl_surface, lvl_rect = self.font.render(
                    f"Level: {production.production_lvl}", (241, 170, 105)
                )
                lvl_rect.topleft = (10, 35)
                btn_surface.blit(lvl_surface, lvl_rect)

                # Draw the cost to upgrade the product on the button
                self.font.size = 20
                cost_surface, cost_rect = self.font.render(
                    fln(production.next_lvl_cost), (241, 170, 105)
                )
                cost_rect.topleft = (
                    btn_rect.w - cost_rect.w - 5,
                    btn_rect.h // 2 - cost_rect.h // 2,
                )
                btn_surface.blit(cost_surface, cost_rect)

                # Blit the button onto the side menu surface
                self.surface.blit(btn_surface, btn_rect)

        # Draw the modal if it is open
        self.modal.draw(screen)
