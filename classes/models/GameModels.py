from dataclasses import dataclass, field
from typing import List, Dict, Union
import pygame


@dataclass
class Production:
    active: bool = False
    product_name: str = ""
    production_time: int = 0
    production_lvl: int = 0
    next_lvl_cost: int = 0
    stored: int = 0
    multiplier: float = 0.0

    @staticmethod
    def from_db_row(row):
        """Creates a Production instance from a database row."""
        return Production(
            active=bool(row[2]),
            product_name=row[3],
            production_time=row[4],
            production_lvl=row[5],
            next_lvl_cost=row[6],
            stored=row[7],
            multiplier=row[8],
        )

    def to_db_tuple(self, game_save_id):
        """Converts the Production instance into a tuple for database insertion."""
        return (
            game_save_id,
            int(self.active),
            self.product_name,
            self.production_time,
            self.production_lvl,
            self.next_lvl_cost,
            self.stored,
            self.multiplier,
        )


@dataclass
class Factory:
    productions: List[Production] = field(default_factory=list)

    @staticmethod
    def from_db_rows(rows):
        """Creates a Factory instance from database rows of productions."""
        productions = [Production.from_db_row(row) for row in rows]
        return Factory(productions=productions)


@dataclass
class Game:
    coins: int = 0
    last_save_time: str = "N/A"
    production_for_seconds: int = 0
    prestige: int = 0
    bufs: Dict[str, int] = field(default_factory=dict)
    factory: Factory = field(default_factory=Factory)

    @staticmethod
    def from_db(save_row, production_rows):
        """Creates a Game instance from database rows."""
        factory = Factory.from_db_rows(production_rows)
        return Game(
            coins=save_row[1],
            last_save_time=save_row[2],
            production_for_seconds=save_row[3],
            prestige=save_row[4],
            factory=factory,
        )

    def to_db_tuple(self):
        """Converts the Game instance into a tuple for database insertion."""
        return (
            self.coins,
            self.last_save_time,
            self.production_for_seconds,
            self.prestige,
        )


@dataclass
class Product:
    name: str = ""
    img: Union[str, pygame.Surface] = ""
    base_cost: int = 0
    base_time: int = 0
    factory_number: int = 0

    @staticmethod
    def from_db_row(row):
        """Creates a Product instance from a database row."""
        return Product(
            name=row[1],
            img=row[2],
            base_cost=row[3],
            base_time=row[4],
            factory_number=row[5],
        )

    def to_db_tuple(self):
        """Converts the Product instance into a tuple for database insertion."""
        return (
            self.name,
            self.img,
            self.base_cost,
            self.base_time,
            self.factory_number,
        )
