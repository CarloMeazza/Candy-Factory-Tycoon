import pygame
import pygame.freetype
from Constants import Constants
from classes.statemanager import State
from classes.tools.Loadspritesheet import load_spritesheet
from classes.tools.Animations import Animation
from classes.tools.Card import Card
from classes.tools.SideMenu import Sidemenu
from classes.tools.LoadingBar import LoadingBar
from classes.tools.Leves import Levels
from classes.tools.formatLargeNumber import format_large_number as fln
from classes.tools.InitNewGame import InitNewGame
from classes.models.GameModels import Game


class GamePlay(State):
    def __init__(self) -> None:
        super().__init__()
        self.get_level = Levels()
        self.next_state = "GAMEPLAY"
        save_game = self.GDB.load_game_save()
        if save_game[0] == None:
            new_game = InitNewGame()
            save_game = new_game.new_game()
            products = new_game.add_products()
        self.save_game: Game = Game.from_db(save_game[0], save_game[1])

        # Load the background image
        self.background_image = pygame.image.load(
            f"{Constants.IMG_DIR}candy_factory_bg.png"
        ).convert()
        self.background_image = pygame.transform.scale(
            self.background_image,
            (Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT),
        )

        self.side_menu = Sidemenu(self.save_game)

        coin_sprites = load_spritesheet(
            f"{Constants.IMG_DIR}coin_spritesheet_32.png", 1, 10
        )
        self.coin_animation = Animation(coin_sprites, (25, 20), 0.2, 3)

        self.upgrade_img = pygame.image.load(f"{Constants.IMG_DIR}upgrade.png")
        self.upgrade_img = pygame.transform.scale(self.upgrade_img, (50, 50))
        self.upgrade_rect = self.upgrade_img.get_rect()
        self.upgrade_rect.topright = (Constants.SCREEN_WIDTH - 60, 10)

        self.settings_img = pygame.image.load(f"{Constants.IMG_DIR}settings.png")
        self.settings_img = pygame.transform.scale(self.settings_img, (50, 50))
        self.settings_rect = self.settings_img.get_rect()
        self.settings_rect.topright = (Constants.SCREEN_WIDTH - 10, 10)

        initial_x, initial_y = 550, 73
        card_space = 25
        self.cards = pygame.sprite.Group()
        index_card = 0
        for row in range(3):
            for col in range(3):
                x = initial_x + col * (192 + card_space)
                y = initial_y + row * (192 + card_space)
                loadingBar = LoadingBar(
                    0, 180, 195, 10, 2
                )  # max_time = self.save_game.factory[i].production_time
                card = Card(x, y, 192, 192, index_card, loadingBar)
                self.cards.add(card)
                index_card += 1

    def get_event(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        relative_mouse_pos = (
            mouse_pos[0] - self.side_menu.rect.x,
            mouse_pos[1] - self.side_menu.rect.y,
        )

        self.side_menu.event(event)

        if event.type == pygame.QUIT:
            # self.GameSave.save(self.save_game)
            self.GDB.close()
            self.quit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # for i, card in enumerate(self.cards):
            #     if card.rect.collidepoint(event.pos):
            #         product = self.save_game.factory["productions"][i].copy()
            #         self.save_game.factory["productions"][i] = self.get_level.get(
            #             product
            #         )
            # for i, (_, btn_rect) in enumerate(self.side_menu.btns):
            #     if btn_rect.collidepoint(relative_mouse_pos):
            #         product = self.save_game.factory.productions[i]
            #         self.save_game.factory.productions[i] = self.get_level.get(
            #             product, self.save_game.coins
            #         )
            if self.upgrade_rect.collidepoint(event.pos):
                self.side_menu.is_open = True

    def on_update(self, dt) -> None:
        self.coin_animation.update()
        self.side_menu.update(self.save_game)
        for i, card in enumerate(self.cards):
            # for _ in self.save_game.factory["productions"]:
            card.loading_bar.set_max_time(
                self.save_game.factory.productions[i].production_time
            )
            card.update(self.save_game.factory.productions[i])

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the background image at the top-left corner
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.coin_animation.image, self.coin_animation.rect)

        coins_surface, coins_rect = self.Bfont.render(
            f"{fln(self.save_game.coins)}", (82, 39, 28)
        )
        coins_rect.topleft = (
            self.coin_animation.rect.right + coins_rect.x + 15,
            self.coin_animation.rect.y + coins_rect.h // 2,
        )
        screen.blit(coins_surface, coins_rect)

        screen.blit(self.upgrade_img, self.upgrade_rect)
        screen.blit(self.settings_img, self.settings_rect)

        for card in self.cards:
            card.draw(screen)

        self.side_menu.draw(screen)
