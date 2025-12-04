from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set, Tuple
import heapq
import math

from .environment import Coordinate, Environment, manhattan


@dataclass
class SharedKnowledge:
    victims: Set[Coordinate] = field(default_factory=set)
    obstacles: Set[Coordinate] = field(default_factory=set)

    def merge(self, other: "SharedKnowledge") -> None:
        self.victims.update(other.victims)
        self.obstacles.update(other.obstacles)


@dataclass
class DroneAgent:
    identifier: str
    position: Coordinate
    environment: Environment
    knowledge: SharedKnowledge = field(default_factory=SharedKnowledge)
    visited: Set[Coordinate] = field(default_factory=set)
    current_path: List[Coordinate] = field(default_factory=list)

    def perceive(self) -> None:
        """Update local knowledge based on the current position."""
        if self.environment.is_victim(self.position):
            self.knowledge.victims.add(self.position)
        for neighbor in self.environment.neighbors(self.position):
            if self.environment.is_blocked(neighbor):
                self.knowledge.obstacles.add(neighbor)
        self.visited.add(self.position)

    def communicate(self, peers: Iterable["DroneAgent"]) -> None:
        for peer in peers:
            if peer is self:
                continue
            self.knowledge.merge(peer.knowledge)
            peer.knowledge.merge(self.knowledge)

    def choose_target(self) -> Optional[Coordinate]:
        visible_victims = [v for v in self.knowledge.victims if v not in self.visited]
        if visible_victims:
            visible_victims.sort(key=lambda v: manhattan(self.position, v))
            return visible_victims[0]

        unexplored_candidates = [
            (x, y)
            for x in range(self.environment.width)
            for y in range(self.environment.height)
            if (x, y) not in self.visited and (x, y) not in self.knowledge.obstacles
        ]
        if not unexplored_candidates:
            return None
        unexplored_candidates.sort(key=lambda pos: manhattan(self.position, pos))
        return unexplored_candidates[0]

    def plan_path(self, target: Coordinate) -> None:
        self.current_path = a_star_search(
            environment=self.environment,
            start=self.position,
            goal=target,
            blocked=self.knowledge.obstacles,
        )

    def step(self) -> None:
        if not self.current_path:
            target = self.choose_target()
            if target is None:
                return
            self.plan_path(target)

        if self.current_path:
            next_step = self.current_path.pop(0)
            self.position = next_step
            self.perceive()


def a_star_search(
    environment: Environment,
    start: Coordinate,
    goal: Coordinate,
    blocked: Set[Coordinate],
) -> List[Coordinate]:
    open_set: List[Tuple[float, Coordinate]] = []
    heapq.heappush(open_set, (0, start))
    came_from: Dict[Coordinate, Optional[Coordinate]] = {start: None}
    g_score: Dict[Coordinate, float] = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return _reconstruct_path(came_from, current)[1:]

        for neighbor in environment.neighbors(current):
            if neighbor in blocked:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, math.inf):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return []


def _reconstruct_path(
    came_from: Dict[Coordinate, Optional[Coordinate]], finish: Coordinate
) -> List[Coordinate]:
    path = [finish]
    current: Optional[Coordinate] = finish
    while current is not None:
        current = came_from[current]
        if current is not None:
            path.append(current)
    path.reverse()
    return path
