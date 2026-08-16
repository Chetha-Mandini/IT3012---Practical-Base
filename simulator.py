from agent import SearchAgent
from visual_grid_game import VisualGridHuntGame


def run_search_agent(
    algorithm
):

    print("=" * 60)

    print(
        "Running Search Agent:",
        algorithm
    )

    print("=" * 60)

    # Create agent
    agent = SearchAgent()

    # Select algorithm
    agent.active_algo = (
        algorithm
    )

    # Create environment
    environment = (
        VisualGridHuntGame(
            width=12,
            height=12,
            num_food=5,
            num_opponents=0,
            agent=agent
        )
    )

    while not environment.is_done():

        # Get current percept
        percept = (
            environment.get_percept()
        )

        # Agent generates/executes plan
        action = (
            agent.sense_and_act(
                percept
            )
        )

        # Execute physical action
        environment.execute_action(
            action
        )

        print(
            f"Step: {environment.steps}"
        )

        print(
            f"Action: {action}"
        )

        print(
            f"Position: "
            f"{environment.agent_pos}"
        )

        print(
            f"Remaining food: "
            f"{len(environment.food_positions)}"
        )

        print("-" * 30)

    print()

    print(
        f"{algorithm} finished."
    )

    print(
        f"Final Score: "
        f"{environment.score}"
    )

    print(
        f"Total Steps: "
        f"{environment.steps}"
    )

    print()


def run_all_algorithms():

    # BFS
    run_search_agent(
        "BFS"
    )

    # DFS
    run_search_agent(
        "DFS"
    )

    # UCS
    run_search_agent(
        "UCS"
    )


if __name__ == "__main__":

    run_all_algorithms()