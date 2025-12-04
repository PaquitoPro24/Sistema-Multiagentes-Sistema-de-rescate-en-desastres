from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .agents import DroneAgent
from .environment import Environment


@dataclass
class SimulationMetrics:
    steps: int = 0
    rescued: int = 0
    discovered: int = 0
    coverage: float = 0.0


@dataclass
class Simulation:
    environment: Environment
    agents: List[DroneAgent]
    step_limit: int
    metrics: SimulationMetrics = field(default_factory=SimulationMetrics)

    def run(self) -> SimulationMetrics:
        for agent in self.agents:
            agent.perceive()

        for current_step in range(1, self.step_limit + 1):
            for agent in self.agents:
                agent.communicate(self.agents)
                agent.step()

            self.metrics.steps = current_step
            rescued_now = self._rescue_victims()
            if rescued_now == len(self.environment.victims):
                break

        self.metrics.discovered = len(set().union(*(a.knowledge.victims for a in self.agents)))
        visited_union = set().union(*(a.visited for a in self.agents))
        self.metrics.coverage = len(visited_union) / (self.environment.width * self.environment.height)
        return self.metrics

    def _rescue_victims(self) -> int:
        rescued_victims = [
            pos
            for pos in self.environment.victims
            if any(agent.position == pos for agent in self.agents)
        ]
        self.metrics.rescued = len(rescued_victims)
        return self.metrics.rescued
