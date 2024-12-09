import sqlite3
import os
from threading import Lock


class GameDatabase:
    _instance = None
    _lock = Lock()  # Ensures thread-safety for the singleton pattern

    def __new__(cls, db_name="game_save.db"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(db_name)
            return cls._instance

    def _initialize(self, db_name):
        # Create a directory for save files if it doesn't exist
        save_dir = "saves"
        os.makedirs(save_dir, exist_ok=True)

        # Full path to the database file
        db_path = os.path.join(save_dir, db_name)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates all required tables in the database if they don't already exist."""
        # Main table for game save data
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_save (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coins INTEGER NOT NULL,
                last_save_time TEXT NOT NULL,
                production_for_seconds INTEGER NOT NULL,
                prestige INTEGER NOT NULL
            )
            """
        )

        # Table for factory production data
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS factory_productions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_save_id INTEGER,
                active INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                production_time INTEGER NOT NULL,
                production_lvl INTEGER NOT NULL,
                next_lvl_cost INTEGER NOT NULL,
                stored INTEGER NOT NULL,
                multiplier REAL NOT NULL,
                FOREIGN KEY (game_save_id) REFERENCES game_save(id)
            )
            """
        )

        # Table for product information
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                img TEXT NOT NULL,
                base_cost INTEGER NOT NULL,
                base_time INTEGER NOT NULL,
                factory_number INTEGER NOT NULL
            )
            """
        )
        self.connection.commit()

    def insert_game_save(self, coins, last_save_time, production_for_seconds, prestige):
        """Inserts a new game save into the database."""
        self.cursor.execute(
            """
            INSERT INTO game_save (coins, last_save_time, production_for_seconds, prestige)
            VALUES (?, ?, ?, ?)
            """,
            (coins, last_save_time, production_for_seconds, prestige),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def insert_factory_production(
        self,
        game_save_id,
        active,
        product_name,
        production_time,
        production_lvl,
        next_lvl_cost,
        stored,
        multiplier,
    ):
        """Inserts a new factory production record linked to a specific game save."""
        self.cursor.execute(
            """
            INSERT INTO factory_productions (game_save_id, active, product_name, production_time, production_lvl, next_lvl_cost, stored, multiplier)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                game_save_id,
                active,
                product_name,
                production_time,
                production_lvl,
                next_lvl_cost,
                stored,
                multiplier,
            ),
        )
        self.connection.commit()

    def load_game_save(self):
        """Loads the most recent game save along with its factory production data."""
        self.cursor.execute("SELECT * FROM game_save ORDER BY id DESC LIMIT 1")
        save = self.cursor.fetchone()
        if save:
            self.cursor.execute(
                "SELECT * FROM factory_productions WHERE game_save_id = ?", (save[0],)
            )
            productions = self.cursor.fetchall()
            return save, productions
        return None, []

    def delete_game_save(self, save_id):
        """Deletes a game save and its associated factory production records."""
        self.cursor.execute("DELETE FROM game_save WHERE id = ?", (save_id,))
        self.cursor.execute(
            "DELETE FROM factory_productions WHERE game_save_id = ?", (save_id,)
        )
        self.connection.commit()

    def insert_product(self, name, img, base_cost, base_time, factory_number):
        """Inserts a new product into the database. Avoids duplication based on name."""
        try:
            self.cursor.execute(
                """
                INSERT INTO products (name, img, base_cost, base_time, factory_number)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, img, base_cost, base_time, factory_number),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Product with name '{name}' already exists.")

    def get_product_by_name(self, name):
        """Fetches a product record by its name."""
        self.cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        return self.cursor.fetchone()
    
    def get_product_by_factory_number(self, factory_number):
        """Fetches a product record by its factory number."""
        self.cursor.execute("SELECT * FROM products WHERE factory_number = ?", (factory_number,))
        return self.cursor.fetchall()

    def load_products(self):
        """Loads all products from the database."""
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        """Deletes a product from the database by its ID."""
        self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.connection.commit()

    def close(self):
        """Closes the database connection and resets the singleton instance."""
        if self.connection:
            self.connection.close()
            GameDatabase._instance = None

    # Esempio di utilizzo
    # if __name__ == "__main__":
    #     db = GameDatabase()

    #     # Inserimento dati
    #     save_id = db.insert_game_save(100, datetime.now().isoformat(), 0, 0)

    #     # Produzioni di esempio
    #     productions = [
    #         {
    #             "active": False,
    #             "product_name": "",
    #             "production_time": 0,
    #             "production_lvl": 0,
    #             "next_lvl_cost": 0,
    #             "stored": 0,
    #             "multiplier": 1.1,
    #         },
    #         {
    #             "active": False,
    #             "product_name": "",
    #             "production_time": 0,
    #             "production_lvl": 0,
    #             "next_lvl_cost": 0,
    #             "stored": 0,
    #             "multiplier": 1.2,
    #         },
    #     ]

    #     for prod in productions:
    #         db.insert_factory_production(
    #             save_id,
    #             prod["active"],
    #             prod["product_name"],
    #             prod["production_time"],
    #             prod["production_lvl"],
    #             prod["next_lvl_cost"],
    #             prod["stored"],
    #             prod["multiplier"],
    #         )

    #     # Caricamento dati
    #     game_save, factory_productions = db.load_game_save()
    #     print("Game Save:", game_save)
    #     print("Factory Productions:", factory_productions)

    #     db.close()

    """
    from platformdirs import user_data_dir
    import os

    # Ottieni il percorso dei dati utente per la piattaforma
    app_name = "NomeGioco"
    save_dir = user_data_dir(app_name, appauthor=False)
    os.makedirs(save_dir, exist_ok=True)

    db_path = os.path.join(save_dir, "game_save.db")
    connection = sqlite3.connect(db_path)
    print(f"Database salvato in: {db_path}")
    
    
    """
