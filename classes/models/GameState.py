from dataclasses import dataclass, field, asdict
from typing import Dict, List, Union
from datetime import datetime
import json
import pygame


@dataclass
class Production:
    active: bool = False
    product_name: str = ""
    production_time: int = 0
    production_lvl: int = 0
    next_lvl_cost: int = 0
    stored: int = 0
    multipler: float = 0

    @staticmethod
    def from_dict(data: dict) -> "Production":
        return Production(**data)


@dataclass
class Factory:
    productions: List[Production] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> "Factory":
        productions = [Production.from_dict(p) for p in data.get("productions", [])]
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
    def from_dict(data: dict) -> "Game":
        factory = Factory.from_dict(data.get("factory", {}))
        return Game(
            coins=data.get("coins", 0),
            last_save_time=data.get("last_save_time", "N/A"),
            production_for_seconds=data.get("production_for_seconds", 0),
            prestige=data.get("prestige", 0),
            bufs=data.get("bufs", {}),
            factory=factory,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Products:
    name: str = ""
    img: Union[str, pygame.Surface] = ""
    base_cost: int = 0
    base_time: int = 0
    factory_number: int = 0


"""
game = Game(
    coins=100,
    last_save_time="2023-11-22T12:34:56",
    production_for_seconds=3600,
    prestige=0,
    bufs={"production_boost": 10, "coin_boost": 5},
    factory=Factory(
        productions=[
            Production(active=True, product_name="Product 1", production_time=300, production_lvl=2, next_lvl_cost=100, stored=50),
            # ... other production instances ...
        ]
    )
)


products = [
    Products(name="Prodotto 1", img="product_1.png", base_cost=50, base_time=5, factory_number=[0, 1]),
    Products(name="Prodotto 2", img="product_2.png", base_cost=75, base_time=6, factory_number=[1, 2]),
    # ...
]


"""
