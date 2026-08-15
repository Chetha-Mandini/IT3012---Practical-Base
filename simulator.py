from grid_game import GridHuntGame
from agent import (
    SimpleReflexAgent,
    ModelBasedAgent
)


def run_agent(agent, title):

    environment = GridHuntGame()

    print("=" * 50)
    print(title)
    print("=" * 50)

    while not environment.is_done():

        # Agent receives only its local percept
        percept = environment.get_percept(agent)

        # Agent chooses an action
        action = agent.sense_and_act(
            percept
        )

        # Environment executes the action
        environment.execute_action(
            agent,
            action
        )

        print(
            f"Percept: {percept}"
        )

        print(
            f"Action: {action}"
        )

        print(
            f"Score: {environment.score}"
        )

        print(
            f"Steps: {environment.steps}"
        )

        print("-" * 30)

    print(
        f"Game Over!"
    )

    print(
        f"Final Score: {environment.score}"
    )

    print(
        f"Total Steps: {environment.steps}"
    )

    print()


def run_grid_hunt():

    # ------------------------------------------
    # Test Simple Reflex Agent
    # ------------------------------------------

    simple_agent = SimpleReflexAgent()

    run_agent(
        simple_agent,
        "SIMPLE REFLEX AGENT"
    )

    # ------------------------------------------
    # Test Model-Based Agent
    # ------------------------------------------

    model_agent = ModelBasedAgent()

    run_agent(
        model_agent,
        "MODEL-BASED AGENT"
    )


if __name__ == "__main__":

    run_grid_hunt()