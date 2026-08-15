class GridHuntGame:
    """
    Grid environment for testing the agents.

    The environment is partially observable because the agent
    does NOT receive its global coordinates.
    """

    def __init__(self, width=4, height=4):

        self.width = width
        self.height = height

        # Actual global position.
        # The agent cannot directly see this.
        self.agent_pos = [0, 0]

        # Food locations
        self.food_positions = {
            (1, 2),
            (2, 3),
            (3, 0),
            (2, 1)
        }

        # Wall locations
        self.walls = {
            (1, 1),
            (2, 2)
        }

        # Agent's actual orientation
        self.facing = "Right"

        self.score = 0
        self.steps = 0

    def _forward_position(self):
        """
        Calculate the position immediately ahead of the agent.
        """

        x, y = self.agent_pos

        if self.facing == "Up":
            y += 1

        elif self.facing == "Down":
            y -= 1

        elif self.facing == "Left":
            x -= 1

        elif self.facing == "Right":
            x += 1

        return (x, y)

    def get_percept(self, agent=None):
        """
        Return ONLY local information.

        The agent does NOT receive:
            - agent_pos
            - food_positions
            - wall coordinates
            - score

        It only receives:
            wall_ahead
            food_here
        """

        forward = self._forward_position()

        wall_ahead = (
            forward[0] < 0
            or forward[0] >= self.width
            or forward[1] < 0
            or forward[1] >= self.height
            or forward in self.walls
        )

        food_here = (
            forward in self.food_positions
        )

        return {
            "wall_ahead": wall_ahead,
            "food_here": food_here
        }

    def execute_action(self, agent, action):
        """
        Execute an action selected by the agent.
        """

        self.steps += 1

        # Turn left
        if action == "TurnLeft":

            directions = [
                "Up",
                "Left",
                "Down",
                "Right"
            ]

            index = directions.index(
                self.facing
            )

            self.facing = directions[
                (index + 1) % 4
            ]

            return

        # Turn right
        if action == "TurnRight":

            directions = [
                "Up",
                "Right",
                "Down",
                "Left"
            ]

            index = directions.index(
                self.facing
            )

            self.facing = directions[
                (index + 1) % 4
            ]

            return

        # Normal movement
        direction = self.facing

        # Also support direct directional actions
        if action in (
            "Up",
            "Down",
            "Left",
            "Right"
        ):
            direction = action
            self.facing = action

        new_pos = list(
            self.agent_pos
        )

        if direction == "Up":
            new_pos[1] += 1

        elif direction == "Down":
            new_pos[1] -= 1

        elif direction == "Left":
            new_pos[0] -= 1

        elif direction == "Right":
            new_pos[0] += 1

        # Boundary collision
        if (
            new_pos[0] < 0
            or new_pos[0] >= self.width
            or new_pos[1] < 0
            or new_pos[1] >= self.height
        ):

            self.score -= 5
            return

        # Wall collision
        if tuple(new_pos) in self.walls:

            self.score -= 5
            return

        # Successful movement
        self.agent_pos = new_pos

        # Food collection
        if tuple(self.agent_pos) in self.food_positions:

            self.food_positions.remove(
                tuple(self.agent_pos)
            )

            self.score += 20

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 40
        )