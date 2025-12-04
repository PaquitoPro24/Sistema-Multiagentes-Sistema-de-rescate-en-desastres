# Sistema Multiagentes para Rescate en Desastres

Proyecto educativo que simula un equipo de drones coordinados para localizar y asistir a víctimas en un área afectada. Los agentes cooperan al compartir conocimiento del entorno, cubrir más terreno y planificar rutas hacia objetivos de manera distribuida.

## Características
- **Agentes móviles cooperativos**: Drones que parten de una base común, exploran la cuadrícula, detectan obstáculos y reportan víctimas.
- **Coordinación distribuida**: Cada agente mantiene conocimiento local y lo fusiona con el resto del equipo en cada iteración.
- **Búsqueda heurística**: Planificación de rutas con A* y heurística Manhattan para alcanzar víctimas o celdas sin explorar.
- **Entorno configurable**: Tamaño del mapa, número de víctimas, obstáculos, agentes y semilla de aleatoriedad ajustables desde CLI.
- **Métricas de desempeño**: Pasos ejecutados, víctimas detectadas/rescatadas y porcentaje de cobertura del área.

## Estructura del código
- `src/environment.py`: Modelo del entorno (celdas, obstáculos, víctimas) y utilidades como distancia Manhattan.
- `src/agents.py`: Implementación de los drones, intercambio de conocimiento y planificación con A*.
- `src/simulation.py`: Bucle de simulación y cálculo de métricas.
- `src/main.py`: CLI para configurar y ejecutar la simulación.

## Requisitos
- Python 3.10+

## Uso rápido
```bash
python -m src.main --agents 4 --width 12 --height 12 --victims 5 --obstacles 15 --steps 80 --seed 42
```

Salida esperada (ejemplo):
```
Mapa inicial:
B . . . . . . . # . . .
. . . # . . . . . . . .
. . . . . # . . . V # .
... (líneas omitidas) ...

Resultados de la simulación:
Pasos ejecutados: 48
Víctimas rescatadas: 3/5
Víctimas detectadas: 4/5
Cobertura del área: 63.33%
```

Ajusta los parámetros para experimentar con diferentes densidades de obstáculos, equipos de drones y límites de tiempo. El proyecto está pensado para explorar conceptos de coordinación multiagente, búsqueda heurística y comunicación en entornos dinámicos.
