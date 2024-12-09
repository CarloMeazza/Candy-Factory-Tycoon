from typing import List
from classes.models.GameState import Production


class Levels:
    def __init__(self) -> None:
        """
        Initializes a Leves object.

        Args:
            None

        Attributes:
            initial_levels (List[int]): A list of initial level thresholds.

        Returns:
            None
        """
        self.initial_levels: List[int] = [25, 50, 75, 100]

    def get(self, production: Production, coins) -> Production:
        """
        Gets the next upgrade cost for the given production.

        Args:
            production (Production): A Production object containing current level and cost information.

        Returns:
            Production: The updated production object with the next upgrade cost calculated.
        """
        if coins < production.next_lvl_cost:
            return production
        if not production.active:
            production.active = True
        production.production_lvl += 1
        if production.production_lvl == self._get_next_step_lvl(
            production.production_lvl
        ):
            production = self._get_next_upgarade(production)
        return self._get_next_cost_lvl(production)

    def _get_next_cost_lvl(self, production: Production) -> Production:
        """
        Calculates the next level cost for the given production.

        Args:
            production (Production): The production object containing current level and cost information.

        Returns:
            Production: The updated production object with the next level cost calculated.
        """
        multipler: float = 1.5
        if production.production_lvl == self._get_next_step_lvl(
            production.production_lvl
        ):
            multipler += 1
        production.next_lvl_cost = round(production.next_lvl_cost * multipler, 4)
        return production

    def _get_prev_step_lvl(self, lvl: int) -> int:
        """
        Determines the previous step level for the given level.

        Args:
            lvl (int): The current level.

        Returns:
            int: The previous step level.
        """
        for level in self.initial_levels:
            if level <= lvl:
                prev_step_lvl = level
            else:
                break

        if prev_step_lvl == 0:
            return 0

        if lvl % 100 == 0:
            return lvl - 100

        return prev_step_lvl

    def _get_next_step_lvl(self, lvl: int) -> int:
        """
        Determines the next step level for the given level.

        Args:
            lvl (int): The current level.

        Returns:
            int: The next step level.
        """
        new_step_lvl: int = 0

        for level in self.initial_levels:
            if level >= lvl:
                new_step_lvl = level
                break

        if new_step_lvl == 0:
            new_step_lvl = (lvl // 100 + 1) * 100

        return new_step_lvl

    def _get_next_upgarade(self, production: Production) -> Production:
        """
        Calculates the next upgrade step for the given production.

        Args:
            production (Production): The production object containing current level and cost information.

        Returns:
            Production: The updated production object with the next upgrade step calculated.
        """
        production_lvl = production["production_lvl"]
        prev_step = self._get_prev_step_lvl(production_lvl)
        next_step = self._get_next_step_lvl(production_lvl)

        next_upgrade = production

        if production.production_time > 1:
            next_upgrade.production_time = max(1, production.production_time - 0.5)
        else:
            increment = (production_lvl + 1) / (next_step - prev_step)
            next_upgrade.production_lvl = production_lvl + increment

        return next_upgrade
