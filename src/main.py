from __future__ import annotations

import argparse
from typing import List

from .agents import DroneAgent
from .environment import Environment
from .simulation import Simulation


def create_agents(environment: Environment, total: int) -> List[DroneAgent]:
    agents: List[DroneAgent] = []
    for index in range(total):
        agent = DroneAgent(
            identifier=f"drone-{index}",
            position=environment.base,
            environment=environment,
        )
        agents.append(agent)
    return agents


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulación de coordinación de drones para rescate en desastres",
    )
    parser.add_argument("--agents", type=int, default=3, help="Número de drones cooperativos")
    parser.add_argument("--width", type=int, default=10, help="Ancho del mapa de búsqueda")
    parser.add_argument("--height", type=int, default=10, help="Alto del mapa de búsqueda")
    parser.add_argument("--victims", type=int, default=4, help="Víctimas a rescatar")
    parser.add_argument("--obstacles", type=int, default=10, help="Obstáculos aleatorios")
    parser.add_argument("--steps", type=int, default=50, help="Límite de pasos de simulación")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para reproducibilidad")

    args = parser.parse_args()

    environment = Environment.generate_random(
        width=args.width,
        height=args.height,
        num_victims=args.victims,
        num_obstacles=args.obstacles,
        seed=args.seed,
    )

    agents = create_agents(environment, args.agents)
    simulation = Simulation(environment=environment, agents=agents, step_limit=args.steps)
    metrics = simulation.run()

    print("Mapa inicial:")
    for row in environment.describe():
        print(row)

    print("\nResultados de la simulación:")
    print(f"Pasos ejecutados: {metrics.steps}")
    print(f"Víctimas rescatadas: {metrics.rescued}/{args.victims}")
    print(f"Víctimas detectadas: {metrics.discovered}/{args.victims}")
    print(f"Cobertura del área: {metrics.coverage:.2%}")


if __name__ == "__main__":
    main()
