from classes.tools import load_spritesheet
from classes.Constants import Constants


class LoadAssets:
    def __init__(self):
        self.player_assets = {}
        self.enemies_assets = {}
        self.stage_assets = []

        self.get_assets()
        print(self.player_assets)

    def get_assets(self):
        # Player
        # knight
        knight = load_spritesheet(Constants.IMG_DIR + "knight.png", 5, 8)
        self.player_assets = {
            "knight": {
                "UP": knight[4:8],
                "DOWN": [knight[0], knight[0]],
                "LEFT": knight[8:16],
                "RIGHT": knight[16:24],
            }
        }

        # Enemies
        # goblin
        goblin = load_spritesheet(Constants.IMG_DIR + "goblin.png", 5, 11)
        self.enemies_assets = {"goblin": goblin}
        # bat
        bat = load_spritesheet(Constants.IMG_DIR + "bat-sprite.png", 4, 4)
        self.enemies_assets = {"bat": bat}




