from collections import deque


class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    This agent uses only the current percept.
    It does not store history or internal state.
    """

    def sense_and_act(self, percept):
        # IF food is ahead THEN move forward
        if percept.get("food_here", False):
            return "Forward"

        # IF there is a wall ahead THEN turn left
        if percept.get("wall_ahead", False):
            return "TurnLeft"

        # ELSE move forward
        return "Forward"


class ModelBasedAgent:
    """
    Model-Based Agent.

    This agent maintains an internal state so it can remember
    previously visited cells and avoid repeatedly following
    the same path.
    """

    def __init__(self):
        # Internal state
        self.estimated_position = (0, 0)

        # Current direction of the agent
        self.facing = "Right"

        # Remember cells that have already been visited
        self.visited_cells = {(0, 0)}

        # Remember which directions have been tried
        # from each estimated cell
        self.tried_directions = {}

        # Remember the previous action
        self.last_action = None

    def _left_of(self, direction):
        directions = ["Up", "Left", "Down", "Right"]
        index = directions.index(direction)
        return directions[(index + 1) % 4]

    def _right_of(self, direction):
        directions = ["Up", "Right", "Down", "Left"]
        index = directions.index(direction)
        return directions[(index + 1) % 4]

    def _position_after_move(self, position, direction):
        x, y = position

        if direction == "Up":
            return (x, y + 1)

        if direction == "Down":
            return (x, y - 1)

        if direction == "Left":
            return (x - 1, y)

        if direction == "Right":
            return (x + 1, y)

        return position

    def _update_state(self, percept):
        """
        Update the internal state using:
        - the previous action
        - the current percept

        This is the model-based part of the agent.
        """

        # If the previous action was movement
        if self.last_action in ("Up", "Down", "Left", "Right"):

            self.facing = self.last_action

            # If there was no wall, assume movement succeeded
            if not percept.get("wall_ahead", False):

                self.estimated_position = self._position_after_move(
                    self.estimated_position,
                    self.last_action
                )

                self.visited_cells.add(
                    self.estimated_position
                )

        # If the previous action was turning
        elif self.last_action == "TurnLeft":

            self.facing = self._left_of(self.facing)

        elif self.last_action == "TurnRight":

            self.facing = self._right_of(self.facing)

    def sense_and_act(self, percept):
        """
        Sense the environment, update internal memory,
        then choose an action.
        """

        # Step 1: Update internal state
        self._update_state(percept)

        current_position = self.estimated_position

        left_direction = self._left_of(self.facing)
        right_direction = self._right_of(self.facing)

        # Get the directions already tried from this cell
        tried = self.tried_directions.setdefault(
            current_position,
            set()
        )

        # --------------------------------------------------
        # RULE 1:
        # IF food is ahead THEN move forward
        # --------------------------------------------------
        if percept.get("food_here", False):

            action = "Forward"

            tried.add(self.facing)

            self.last_action = action

            return action

        # --------------------------------------------------
        # RULE 2:
        # IF wall ahead THEN choose another direction
        # using memory
        # --------------------------------------------------
        if percept.get("wall_ahead", False):

            if self.last_action == "TurnLeft":

                action = "TurnRight"

            elif self.last_action == "TurnRight":

                action = "TurnLeft"

            elif left_direction not in tried:

                action = "TurnLeft"

            elif right_direction not in tried:

                action = "TurnRight"

            else:

                action = "TurnRight"

            self.last_action = action

            return action

        # --------------------------------------------------
        # RULE 3:
        # IF the cell ahead has already been visited
        # THEN choose an alternate route
        # --------------------------------------------------

        forward_cell = self._position_after_move(
            current_position,
            self.facing
        )

        if forward_cell in self.visited_cells:

            if right_direction not in tried:

                action = "TurnRight"

            elif left_direction not in tried:

                action = "TurnLeft"

            else:

                action = "TurnRight"

            self.last_action = action

            return action

        # --------------------------------------------------
        # RULE 4:
        # OTHERWISE explore forward
        # --------------------------------------------------

        tried.add(self.facing)

        action = "Forward"

        self.last_action = action

        return action


class SearchAgent:
    """
    Breadth-First Search agent.

    This class is retained so that the existing Practical 3
    functionality continues to work.
    """

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):

        start = tuple(start_pos)
        goal = tuple(goal_pos)

        blocked = {
            tuple(wall)
            for wall in walls
        }

        width, height = grid_size

        # Start is already the goal
        if start == goal:
            return []

        # Invalid start or goal
        if start in blocked or goal in blocked:
            return None

        # Queue contains:
        # (current_position, path_taken)
        queue = deque()

        queue.append(
            (start, [])
        )

        visited = {start}

        moves = [
            ((0, 1), "Up"),
            ((0, -1), "Down"),
            ((-1, 0), "Left"),
            ((1, 0), "Right")
        ]

        while queue:

            position, path = queue.popleft()

            for (dx, dy), action in moves:

                next_position = (
                    position[0] + dx,
                    position[1] + dy
                )

                # Check grid boundaries
                if not (
                    0 <= next_position[0] < width
                    and
                    0 <= next_position[1] < height
                ):
                    continue

                # Check walls
                if next_position in blocked:
                    continue

                # Check whether already visited
                if next_position in visited:
                    continue

                new_path = path + [action]

                # Goal found
                if next_position == goal:
                    return new_path

                visited.add(next_position)

                queue.append(
                    (
                        next_position,
                        new_path
                    )
                )

        # No path exists
        return None