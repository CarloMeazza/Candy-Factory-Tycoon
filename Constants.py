from typing import Final


class Constants:
    VERSION: Final[str] = "0.0.1a"
    # Frames per second for the game loop
    FPS: Final[int] = 60
    # Width of the game screen
    SCREEN_WIDTH: Final[int] = 1720
    # Height of the game screen
    SCREEN_HEIGHT: Final[int] = 768
    # Interval in seconds for auto-saving game data
    AUTO_SAVE_INT: Final[int] = 30
    # Base directory for assets
    ASSETS: Final[str] = "assets/"
    # Dictionary containing paths to font files
    FONTS: Final[dict] = {
        "regular": f"{ASSETS}fonts/Atma-Regular.ttf",
        "bold": f"{ASSETS}fonts/Atma-Bold.ttf",
        "regular_comic": f"{ASSETS}fonts/ComicNeue-Regular.ttf",
        "symbols": f"{ASSETS}fonts/MaterialSymbolsOutlined-Regular.ttf",
    }
    # Directory for storing images
    IMG_DIR: Final[str] = f"{ASSETS}images/"
    # Directory for storing sound files
    SOUNDS: Final[str] = f"{ASSETS}sounds/"
    # Directory for saving game data
    SAVE_DIR: Final[str] = "save/"
