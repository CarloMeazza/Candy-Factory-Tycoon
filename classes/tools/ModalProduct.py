import pygame
from typing import List
from Constants import Constants
from classes.tools.GameDatabase import GameDatabase as GDB
from classes.tools.formatLargeNumber import format_large_number as fln
from classes.models.GameModels import Game, Product
from classes.tools.products import products
from classes.tools.MiniCard import MiniCard


class ModalProduct:
    def __init__(self):

        self.production_number = 0
        self.GDB = GDB()
        save_game = self.GDB.load_game_save()
        self.save_game: Game = Game.from_db(save_game[0], save_game[1])
        products = self.GDB.load_products()
        self.products: List[Product] = []
        for p in products:
            self.products.append(Product.from_db_row(p))

        self.font = pygame.freetype.Font(Constants.FONTS["regular_comic"], 15)
        self.get_imgs()

        self.width = 500
        self.height = 500
        self.color = (241, 170, 105)
        self.open_speed = 30
        self.is_open = False

        # Superficie della modal
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x = (
            Constants.SCREEN_WIDTH
        )  # Posizione iniziale fuori schermo (a destra)
        self.rect.y = Constants.SCREEN_HEIGHT // 2 - self.height // 2

        # Bottone di chiusura
        self.close_img = pygame.image.load(f"{Constants.IMG_DIR}close.png")
        self.close_img = pygame.transform.scale(
            self.close_img, (30, 30)
        )  # Bottone più piccolo
        self.close_rect = self.close_img.get_rect(topright=(self.width - 10, 10))

        self.overlay_color = (0, 0, 0, 128)  # Colore nero semi-trasparente
        self.overlay_surface = pygame.Surface(
            (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self.overlay_surface.fill(self.overlay_color)

        self.cards = pygame.sprite.Group()

    def get_imgs(self):
        for prod in self.products:
            img = pygame.image.load(
                f"{Constants.IMG_DIR}candy_sprites/{prod.img}"
            ).convert_alpha()
            prod.img = img

    # def set(self):
    #     """Imposta la modal come aperta."""
    #     self.is_open = True
    #     self.rect.x = Constants.SCREEN_WIDTH  # Riposiziona fuori schermo per riaprire

    def pre_draw(self):
        index_card = 0
        self.cards = pygame.sprite.Group()
        if self.production_number and self.save_game != None:
            self.selected_production = []
            for p in self.products:
                if p.factory_number == self.production_number:
                    self.selected_production.append(p)

            for row in range(3):
                for col in range(3):
                    if row * 3 + col < len(self.selected_production):
                        x = 70 + col * (110 + 15)
                        y = 70 + row * (110 + 15)
                        card = MiniCard(x, y, 110, 110, index_card)
                        self.cards.add(card)
                        index_card += 1

    def event(self, event: pygame.event.Event):
        cursor = pygame.SYSTEM_CURSOR_ARROW
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

        if self.is_open:
            for card in self.cards:
                if card.rect.collidepoint(relative_mouse_pos):
                    cursor = pygame.SYSTEM_CURSOR_HAND
        
        if self.close_rect.collidepoint(relative_mouse_pos):
                cursor = pygame.SYSTEM_CURSOR_HAND

        if pygame.mouse.get_cursor() != cursor:
            pygame.mouse.set_cursor(cursor)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = (
                event.pos[0] - self.rect.x,
                event.pos[1] - self.rect.y,
            )
            if self.close_rect.collidepoint(mouse_pos):
                self.is_open = False  # Chiudi la modal

            if self.is_open:
                for card in self.cards:
                    if card.rect.collidepoint(mouse_pos):
                        print(card.product.name)

    def update(self, save_game):
        self.save_game = save_game
        if self.production_number and self.save_game != None:
            self.pre_draw()
            for i, card in enumerate(self.cards):
                card.update(self.selected_production[i])

        """Aggiorna la posizione della modal per gestire l'animazione."""

        target_x = (
            Constants.SCREEN_WIDTH // 2 - self.width // 2
            if self.is_open
            else Constants.SCREEN_WIDTH
        )

        if self.rect.x != target_x:
            direction = -1 if self.rect.x > target_x else 1
            self.rect.x += direction * self.open_speed

            # Assicurati di fermarti esattamente nella posizione desiderata
            if direction == -1 and self.rect.x < target_x:
                self.rect.x = target_x
            elif direction == 1 and self.rect.x > target_x:
                self.rect.x = target_x

    def draw(self, screen: pygame.Surface):
        """Disegna la modal se visibile."""
        if self.rect.x < Constants.SCREEN_WIDTH:  # Disegna solo se visibile
            # Blit del bottone di chiusura sulla superficie della modal
            screen.blit(self.overlay_surface, (0, 0))
            self.surface.fill(self.color)  # Reset della superficie
            self.surface.blit(self.close_img, self.close_rect)

            for card in self.cards:
                card.draw(self.surface)
            # Disegna la modal sullo schermo
            screen.blit(self.surface, self.rect)
