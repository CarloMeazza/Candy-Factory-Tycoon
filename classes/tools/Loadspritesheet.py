import pygame
from typing import List, Dict, Union, Tuple


def load_spritesheet(
    image_path: str, rows: int, cols: int, colorkey: Tuple[int, int, int] = (0, 0, 0)
) -> List[pygame.Surface]:
    """
    Loads a spritesheet and extracts frames arranged in a grid pattern.
    """
    try:
        sheet = pygame.image.load(image_path).convert_alpha()
        sheet.set_colorkey(colorkey)
        sprite_width = sheet.get_width() // cols
        sprite_height = sheet.get_height() // rows
        sprites = [
            sheet.subsurface(
                pygame.Rect(
                    col * sprite_width, row * sprite_height, sprite_width, sprite_height
                )
            )
            for row in range(rows)
            for col in range(cols)
        ]
        return sprites
    except Exception as e:
        print(f"Error loading spritesheet: {e}")
        return []


def load_irregular_spritesheet(
    image_path: str,
    frames_info: List[Dict[str, int]],
    colorkey: Tuple[int, int, int] = (0, 0, 0),
) -> List[Union[pygame.Surface, None]]:
    """
    Loads an irregular spritesheet and extracts frames based on individual coordinates.

    Args:
        image_path (str): Path to the spritesheet image file.
        frames_info (List[Dict[str, int]]): List of dictionaries containing 'x', 'y', 'width', and 'height' for each frame.
        colorkey (Tuple[int, int, int], optional): Color key for transparency. Defaults to (0, 0, 0).

    Returns:
        List[Union[pygame.Surface, None]]: A list of frames or None if extraction failed.
    """
    try:
        sheet = pygame.image.load(image_path).convert_alpha()
        sheet.set_colorkey(colorkey)
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        return []

    sprites = []
    for i, frame_info in enumerate(frames_info):
        # Validate frame_info
        try:
            x = frame_info["x"]
            y = frame_info["y"]
            width = frame_info["width"]
            height = frame_info["height"]
        except KeyError as e:
            print(f"Frame {i} is missing a required key: {e}")
            sprites.append(None)
            continue

        # Check bounds
        if x + width > sheet.get_width() or y + height > sheet.get_height():
            print(
                f"Frame {i} with ({x}, {y}, {width}, {height}) exceeds the spritesheet bounds."
            )
            sprites.append(None)
            continue

        # Extract frame
        try:
            frame_rect = pygame.Rect(x, y, width, height)
            sprite = sheet.subsurface(frame_rect)
            sprites.append(sprite)
        except ValueError as e:
            print(f"Error extracting frame {i} at ({x}, {y}, {width}, {height}): {e}")
            sprites.append(None)

    return sprites


# Example usage:
# frames_info = [
#     {'x': 0, 'y': 0, 'width': 32, 'height': 32},
#     {'x': 32, 'y': 0, 'width': 48, 'height': 48},
#     {'x': 0, 'y': 32, 'width': 64, 'height': 64}
# ]
# sprites = load_irregular_spritesheet('path/to/spritesheet.png', frames_info)
