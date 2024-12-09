import pygame


class TileMap:
    def __init__(self, tile_data, map_data, tile_dimension, y_offset=0):
        """
        Initializes a new TileMap object with the given parameters.

        Args:
            tile_data (list[dict]): A list of dictionaries containing information about each tile.
                Each dictionary should have the following entries:
                    index (int): The index of the tile in the tileset.
                    image_path (str): The path to the image of the tile.
            map_data (list[list[int]]): A 2D list of tile indices representing the map.
            tile_dimension (tuple[int, int]): A tuple containing the width and height of each tile.
            y_offset (int, optional): An optional offset in y direction. Defaults to 0.
        """
        self.tile_images = {}
        width, height = tile_dimension

        empty_tile_image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.tile_images[0] = {
            "image": empty_tile_image,
            "width": width,
            "height": height,
        }

        # Iterate over the tile data and load the images
        for tile in tile_data:
            index = tile["index"]
            image_path = tile["image_path"]

            image = pygame.image.load(image_path).convert_alpha()

            self.tile_images[index] = {"image": image, "width": width, "height": height}

        # Store the map data
        self.map_data = map_data
        self.y_offset = y_offset

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the map on the given screen.

        This method iterates over the map data and draws each tile at the
        appropriate position on the screen. The y offset is added to the
        calculated y position of each tile.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        for y, row in enumerate(self.map_data):
            for x, tile_index in enumerate(row):
                # Get the tile information from the tile_images dictionary
                tile_info = self.tile_images[tile_index]
                # Get the image, width and height of the tile
                tile_image = tile_info["image"]
                width = tile_info["width"]
                height = tile_info["height"]

                # Calculate the screen position of the tile
                screen_x = x * width
                # Add the y offset to the screen y position
                screen_y = (y * height) + self.y_offset

                # Draw the tile on the screen
                screen.blit(tile_image, (screen_x, screen_y))

    # Esempio di tile_data
    # tile_data = [
    #     {'index': 1, 'image_path': 'path/to/tile_01.png'},
    #     {'index': 2, 'image_path': 'path/to/tile_02.png'},
    #     {'index': 3, 'image_path': 'path/to/tile_03.png'}
    # ]

    # # Esempio di map_data
    # map_data = [
    #     [1, 1, 1, 2, 2],
    #     [1, 0, 1, 2, 0],
    #     [3, 3, 3, 0, 0]
    # ]

    # # Crea l'istanza di TileMap
    # tile_map = TileMap(tile_data, map_data, (32, 32), y_offset=0)
