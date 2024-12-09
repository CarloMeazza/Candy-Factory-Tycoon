import pygame
from Constants import Constants
from classes.tools.GameDatabase import GameDatabase as GDB
from classes.models.GameModels import Game, Production

# from classes.tools.GameSaveManager import GameSaveManager
from classes.tools.formatLargeNumber import format_large_number


class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, index_card: int, loading_bar):
        """
        Inizializza una carta con una barra di caricamento.

        :param x: Coordinata X della carta
        :param y: Coordinata Y della carta
        :param width: Larghezza della carta
        :param height: Altezza della carta
        :param loading_bar: Istanza di LoadingBar associata alla carta
        """
        super().__init__()
        self.GDB = GDB()
        save_game = self.GDB.load_game_save()
        self.save_game: Game = Game.from_db(save_game[0], save_game[1])

        self.index = index_card
        self.production: Production = self.save_game.factory.productions[self.index]

        self.font = pygame.freetype.Font(
            Constants.FONTS["regular_comic"], 20
        )  # Font used for text
        self.Bfont = pygame.freetype.Font(
            Constants.FONTS["bold"], 24
        )  # Font used for text
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill((82, 39, 28))  # Colore di sfondo della carta

        # Barra di caricamento
        self.loading_bar = loading_bar

    def update(self, production: Production):
        """
        Updates the card's product data and refreshes the loading bar state.

        :param save_game: The game state with updated production information.
        """
        self.production = production
        self.loading_bar.update()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the card and its loading bar.

        :param surface: The surface to draw on.
        """
        if self.production.active:
            self.image.fill((82, 39, 28))  # Fill the background with a dark brown
        else:
            self.image.fill((104, 128, 123))

        # Draw the loading bar on the card surface
        if self.production.active:
            self.image.blit(self.loading_bar.image, self.loading_bar.rect.topleft)

        # Draw the stored amount of the product on the card
        self.prod_surface, self.prod_rect = self.font.render(
            f"{format_large_number(self.production.stored)}", (241, 170, 105)
        )
        self.prod_rect.topleft = (10, 10)
        self.image.blit(self.prod_surface, self.prod_rect)

        # Draw the level of the product on the card
        self.stored_surface, self.stored_rect = self.font.render(
            f"Level: {self.production.production_lvl}", (241, 170, 105)
        )
        self.stored_rect.bottomleft = (10, self.rect.h - 15)
        self.image.blit(self.stored_surface, self.stored_rect)

        # Draw the card on the screen
        surface.blit(self.image, self.rect.topleft)
