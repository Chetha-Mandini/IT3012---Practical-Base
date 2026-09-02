"""
simulator.py – IT3012 Practical 1 & 2
Run the grid-hunt simulation using the GreedyGridAgent inside GridHuntGame.

Usage:
    python simulator.py
    python simulator.py --toxin      # enable toxin sensor (Part 2)
"""

import sys
from grid_game import GridHuntGame
from agent import GreedyGridAgent


def run_grid_hunt(expose_toxin_sensor: bool = False):
    env = GridHuntGame(expose_toxin_sensor=expose_toxin_sensor)
    agent = GreedyGridAgent()

    mode = "TOXIN SENSOR ON" if expose_toxin_sensor else "TOXIN SENSOR OFF (hidden)"
    print(f"=== IT3012 Grid Hunt Started – {mode} ===\n")

    while not env.is_done():
        percept = env.get_percept()          # Fixed: no agent argument
        action = agent.sense_and_act(percept)
        env.execute_action(action)           # Fixed: no agent argument

        toxin_info = ""
        if expose_toxin_sensor:
            toxin_info = f" | On Trap: {percept.get('smells_toxin', False)}"

        print(
            f"Step {env.steps:02d} | Pos: {percept['agent_pos']} "
            f"| Action: {action:5s} | Food Left: {percept['remaining_food']} "
            f"| Score: {percept['score']}{toxin_info}"
        )

    print(f"\nGame Over! Final Score: {env.score} after {env.steps} steps.")
    if env.toxic_traps:
        print(f"Hidden traps were at: {sorted(env.toxic_traps)}")


if __name__ == "__main__":
    expose = "--toxin" in sys.argv
    run_grid_hunt(expose_toxin_sensor=expose)