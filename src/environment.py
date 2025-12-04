from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable, List, Optional, Set, Tuple


class CellType(Enum):
    EMPTY = auto()
    OBSTACLE = auto()
    VICTIM = auto()
    BASE = auto()


Coordinate = Tuple[int, int]


@dataclass
class Environment:
    width: int
    height: int
    base: Coordinate
    victims: Set[Coordinate] = field(default_factory=set)
    obstacles: Set[Coordinate] = field(default_factory=set)

    def in_bounds(self, pos: Coordinate) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, pos: Coordinate) -> bool:
        return pos in self.obstacles

    def is_victim(self, pos: Coordinate) -> bool:
        return pos in self.victims

    def neighbors(self, pos: Coordinate) -> List[Coordinate]:
        x, y = pos
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [p for p in candidates if self.in_bounds(p) and not self.is_blocked(p)]

    def cell_type(self, pos: Coordinate) -> CellType:
        if pos == self.base:
            return CellType.BASE
        if pos in self.victims:
            return CellType.VICTIM
        if pos in self.obstacles:
            return CellType.OBSTACLE
        return CellType.EMPTY

    @classmethod
    def generate_random(
        cls,
        width: int,
        height: int,
        num_victims: int,
        num_obstacles: int,
        seed: Optional[int] = None,
    ) -> "Environment":
        rng = random.Random(seed)
        base = (0, 0)
        coordinates = [(x, y) for x in range(width) for y in range(height) if (x, y) != base]
        rng.shuffle(coordinates)

        victims = set(coordinates[:num_victims])
        obstacles = set()
        for pos in coordinates[num_victims:]:
            if len(obstacles) >= num_obstacles:
                break
            obstacles.add(pos)

        return cls(width=width, height=height, base=base, victims=victims, obstacles=obstacles)

    def describe(self) -> List[str]:
        """Return a string grid for reporting purposes."""
        grid = [["."] * self.height for _ in range(self.width)]
        for ox, oy in self.obstacles:
            grid[ox][oy] = "#"
        for vx, vy in self.victims:
            grid[vx][vy] = "V"
        bx, by = self.base
        grid[bx][by] = "B"
        return [" ".join(grid[x][y] for x in range(self.width)) for y in range(self.height)]


def manhattan(a: Coordinate, b: Coordinate) -> int:
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def parse_coordinates(entries: Iterable[str]) -> Set[Coordinate]:
    parsed: Set[Coordinate] = set()
    for entry in entries:
        x_str, y_str = entry.split(",")
        parsed.add((int(x_str), int(y_str)))
    return parsed
