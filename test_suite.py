import unittest

from agent import (
    SimpleReflexAgent,
    ModelBasedAgent,
    SearchAgent
)


class TestSimpleReflexAgent(
    unittest.TestCase
):

    def test_food_rule(self):

        agent = (
            SimpleReflexAgent()
        )

        percept = {
            "wall_ahead": False,
            "food_here": True
        }

        action = (
            agent.sense_and_act(
                percept
            )
        )

        self.assertEqual(
            action,
            "Forward"
        )

    def test_wall_rule(self):

        agent = (
            SimpleReflexAgent()
        )

        percept = {
            "wall_ahead": True,
            "food_here": False
        }

        action = (
            agent.sense_and_act(
                percept
            )
        )

        self.assertEqual(
            action,
            "TurnLeft"
        )


class TestModelBasedAgent(
    unittest.TestCase
):

    def test_model_agent_has_memory(self):

        agent = (
            ModelBasedAgent()
        )

        self.assertTrue(
            hasattr(
                agent,
                "visited_cells"
            )
        )

        self.assertTrue(
            hasattr(
                agent,
                "last_action"
            )
        )


class TestSearchAgent(
    unittest.TestCase
):

    def setUp(self):

        self.agent = (
            SearchAgent()
        )

        self.grid_size = (
            4,
            4
        )

        self.walls = []

        self.start = (
            0,
            0
        )

        self.goal = (
            3,
            3
        )

    def test_bfs_search(self):

        path = (
            self.agent.bfs_search(
                self.start,
                self.goal,
                self.walls,
                self.grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        # Shortest path on an empty 4x4 grid
        # from (0,0) to (3,3) is 6 moves.
        self.assertEqual(
            len(path),
            6
        )

    def test_dfs_search(self):

        path = (
            self.agent.dfs_search(
                self.start,
                self.goal,
                self.walls,
                self.grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        self.assertGreater(
            len(path),
            0
        )

    def test_ucs_search(self):

        path = (
            self.agent.ucs_search(
                self.start,
                self.goal,
                self.walls,
                self.grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

        # Every movement has cost 1,
        # therefore UCS should find the same
        # minimum-cost path length as BFS.
        self.assertEqual(
            len(path),
            6
        )

    def test_reached_prevents_loops(self):

        walls = [
            (1, 0),
            (1, 1)
        ]

        path = (
            self.agent.dfs_search(
                self.start,
                self.goal,
                walls,
                self.grid_size
            )
        )

        self.assertIsNotNone(
            path
        )

    def test_search_agent_configuration(self):

        self.assertEqual(
            self.agent.plan,
            []
        )

        self.assertEqual(
            self.agent.active_algo,
            "BFS"
        )


if __name__ == "__main__":

    print(
        "=== IT3012 Lab 3 Test Suite ==="
    )

    unittest.main(
        verbosity=2
    )