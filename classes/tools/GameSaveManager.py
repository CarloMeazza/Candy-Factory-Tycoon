import json, os
from threading import Timer
from Constants import Constants
from classes.models.GameState import Game, Factory, Production
from dataclasses import asdict


class GameSaveManager:
    def __init__(self, auto_save_interval: int = 60):
        """
        Initializes the GameSaveManager.
        Args:
            auto_save_interval (int): Interval in seconds for autosaving. Default is 60 seconds.
        """
        self.save_file_path = f"{Constants.SAVE_DIR}save.json"
        self.auto_save_interval = auto_save_interval
        self.auto_save_timer = None

    def create_or_load(self) -> dict:
        """
        Creates a new save file or loads an existing one.
        Returns:
            dict: The saved game data.
        """
        if os.path.exists(self.save_file_path):
            return self.load()
        else:
            return self.new_game_file()

    def load(self) -> dict:
        """
        Loads the game data from a file.
        Returns:
            dict: The loaded game data.
        """
        try:
            with open(self.save_file_path, "r") as file:
                data = json.load(file)
                return Game.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            print(
                f"Error loading save file {self.save_file_path}. Returning default data."
            )
            return self.new_game_file()

    def save(self, game_data: Game) -> None:
        """
        Saves the game data to a file.
        Args:
            game_data (dict): The game data to be saved.
        """
        try:
            with open(self.save_file_path, "w") as file:
                json.dump(game_data.to_dict(), file, indent=4)
            print(f"Game data saved successfully to {self.save_file_path}.")
        except IOError:
            print(f"Error saving game data to {self.save_file_path}.")

    def delete(self) -> None:
        """
        Deletes the save file.
        """
        try:
            os.remove(self.save_file_path)
            print(f"Save file {self.save_file_path} deleted successfully.")
        except FileNotFoundError:
            print(f"Save file {self.save_file_path} not found.")

    def start_auto_save(self, game_data: dict) -> None:
        """
        Starts the autosave timer.
        Args:
            game_data (dict): The game data to be saved periodically.
        """
        if self.auto_save_timer is not None:
            self.auto_save_timer.cancel()

        self.save(game_data)
        self.auto_save_timer = Timer(
            self.auto_save_interval, self.start_auto_save, args=(game_data,)
        )
        self.auto_save_timer.start()

    def stop_auto_save(self) -> None:
        """
        Stops the autosave timer.
        """
        if self.auto_save_timer is not None:
            self.auto_save_timer.cancel()
            print("Autosave stopped.")

    def new_game_file(self) -> Game:
        game = Game(
            coins=100,
            last_save_time="N/A",
            production_for_seconds=0,
            prestige=0,
            bufs={},
            factory=Factory(
                productions=[
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.1,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.2,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.3,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.4,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.6,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.7,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=1.8,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=2,
                    ),
                    Production(
                        active=False,
                        product_name="",
                        production_time=0,
                        production_lvl=0,
                        next_lvl_cost=0,
                        stored=0,
                        multipler=2.5,
                    ),
                ]
            ),
        )
        return game


"""
# Esempio di utilizzo (senza eseguire il codice)
if __name__ == "__main__":
    save_manager = GameSaveManager(
        save_file_path="savegame.json", auto_save_interval=60
    )
    game_data = save_manager.create_or_load()

    # Simulazione di un aggiornamento del gioco
    game_data["health"] -= 10
    game_data["coins"] += 5

    # Avvia l'autosalvataggio
    save_manager.start_auto_save(game_data)

    # Esempio di salvataggio manuale
    save_manager.save(game_data)

    # Esempio di cancellazione del file di salvataggio
    # save_manager.delete()

"""
