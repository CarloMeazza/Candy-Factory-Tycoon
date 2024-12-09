import pygame
from Constants import Constants
from classes.models.GameState import Products


class MiniCard(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, index_card: int):
        """
        Initializes a new MiniCard object with the given parameters.

        Args:
            x (int): The x coordinate of the card.
            y (int): The y coordinate of the card.
            width (int): The width of the card.
            height (int): The height of the card.
            index_card (int): The index of the card in the list of products.
        """
        super().__init__()

        # Store the index of the card
        self.index = index_card

        # Load fonts
        self.font = pygame.freetype.Font(Constants.FONTS["regular_comic"], 20)
        self.bold_font = pygame.freetype.Font(Constants.FONTS["bold"], 24)

        # Create the card's rect and image
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))

        # Store the colors used in the card
        self.active_color = (82, 39, 28)  # Colore per i prodotti attivi
        self.text_color = (241, 170, 105)  # Colore del testo

    def update(self, product: Products) -> None:
        """
        Updates the card with the given product.

        Args:
            product (Products): The product to update the card with.
        """
        self.product = product
        # Store the product's image
        self.img = self.product.img
        # Scale the image to fit the card
        self.img = pygame.transform.scale(self.img, (100, 100))
        # Get the rect of the scaled image
        self.img_rect = self.img.get_rect()
        # Position the image in the center of the card
        self.img_rect.topleft = (
            self.rect.w // 2 - self.img_rect.w // 2,
            self.rect.h // 2 - self.img_rect.h // 2,
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the card and, if present, the loading bar.

        :param surface: The surface to draw on.
        """
        # Fill the card with the active color
        self.image.fill(self.active_color)

        # Draw the product image on the card
        self.image.blit(self.img, self.img_rect)

        # Blit the card onto the main surface
        surface.blit(self.image, self.rect.topleft)
