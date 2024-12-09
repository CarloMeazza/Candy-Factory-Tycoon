from classes.tools.GameDatabase import GameDatabase as GDB
from classes.models.GameModels import Game, Factory, Production, Product


class InitNewGame:
    def __init__(self):
        self.db = GDB()

    def new_game(self) -> Game:
        """Creates a new game instance and saves it to the database.

        Returns:
            Game: New game instance
        """
        # Initialize a new Game object
        game = Game(
            coins=100,  # starting coins
            last_save_time="N/A",  # last save time (not used yet)
            production_for_seconds=0,  # production value for the game
            prestige=0,  # current prestige level
            bufs={},  # buffer values for the game
            factory=Factory(
                productions=[
                    Production(
                        active=False,  # whether the production is active
                        product_name="",  # name of the product
                        production_time=0,  # production time
                        production_lvl=0,  # production level
                        next_lvl_cost=100 if idx == 0 else 0,  # cost of the next level
                        stored=0,  # stored amount of the product
                        multiplier=m,  # multiplier for the production
                    )
                    for idx, m in enumerate([1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 2, 2.5])
                ]
            ),
        )

        # Save the game to the database
        game_id = self.db.insert_game_save(*game.to_db_tuple())

        # Save factory productions linked to the game save
        for production in game.factory.productions:
            self.db.insert_factory_production(*production.to_db_tuple(game_id))

        return game

    def add_products(self) -> list[Product]:
        """Creates product entries in the database and returns a list of Product objects.

        Each product has a name, image path, base cost, base time, and factory number.
        The factory number is a unique identifier for the product in the game.
        The base cost and time are used to calculate the production value and production time.
        The image path is the path to the image file for the product in the assets folder.
        """

        products = [
            Product(
                name="Yellow Wrapped",
                img="wrappedsolid_yellow.png",
                base_cost=100,
                base_time=5,
                factory_number=1,
            ),
            Product(
                name="Red Wrapped",
                img="wrappedsolid_red.png",
                base_cost=100,
                base_time=5,
                factory_number=1,
            ),
            Product(
                name="Teal Star",
                img="star_teal.png",
                base_cost=600,
                base_time=7,
                factory_number=2,
            ),
            Product(
                name="Orange Star",
                img="star_orange.png",
                base_cost=600,
                base_time=7,
                factory_number=2,
            ),
            Product(
                name="Orange MM",
                img="mm_orange.png",
                base_cost=1200,
                base_time=9,
                factory_number=3,
            ),
            Product(
                name="Brown MM",
                img="mm_brown.png",
                base_cost=1200,
                base_time=9,
                factory_number=3,
            ),
            Product(
                name="Green Jelly",
                img="jelly_green.png",
                base_cost=2000,
                base_time=11,
                factory_number=4,
            ),
            Product(
                name="Blue Jelly",
                img="jelly_blue.png",
                base_cost=2000,
                base_time=11,
                factory_number=4,
            ),
            Product(
                name="Orange Heart",
                img="heart_orange.png",
                base_cost=3500,
                base_time=12,
                factory_number=5,
            ),
            Product(
                name="Green Heart",
                img="heart_green.png",
                base_cost=3500,
                base_time=12,
                factory_number=5,
            ),
            Product(
                name="Red Big Jelly",
                img="jellybig_red.png",
                base_cost=4500,
                base_time=14,
                factory_number=6,
            ),
            Product(
                name="Yellow Big Jelly",
                img="jellybig_yellow.png",
                base_cost=4500,
                base_time=14,
                factory_number=6,
            ),
            Product(
                name="Purple Lollipop",
                img="lollipop_purple.png",
                base_cost=6000,
                base_time=16,
                factory_number=7,
            ),
            Product(
                name="Rainbow Lollipop",
                img="lollipop_rainbow.png",
                base_cost=6000,
                base_time=16,
                factory_number=7,
            ),
            Product(
                name="Candy Corn",
                img="candycorn.png",
                base_cost=8000,
                base_time=18,
                factory_number=8,
            ),
            Product(
                name="Candy Cane",
                img="candycane.png",
                base_cost=8000,
                base_time=18,
                factory_number=8,
            ),
            Product(
                name="Blue Bean",
                img="bean_blue.png",
                base_cost=10000,
                base_time=20,
                factory_number=9,
            ),
            Product(
                name="Orange Bean",
                img="bean_orange.png",
                base_cost=10000,
                base_time=20,
                factory_number=9,
            ),
            Product(
                name="Candy Humbug",
                img="candyhumbug.png",
                base_cost=10000,
                base_time=20,
                factory_number=9,
            ),
        ]

        # Save products to the database
        for product in products:
            self.db.insert_product(*product.to_db_tuple())

        return products
