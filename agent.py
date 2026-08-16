from collections import deque
import heapq


class SimpleReflexAgent:
    """
    Simple Reflex Agent.

    Uses only the current percept.
    It does not maintain memory or history.
    """

    def sense_and_act(self, percept):

        # IF food is ahead THEN move forward
        if percept.get("food_here", False):
            return "Forward"

        # IF wall is ahead THEN turn left
        if percept.get("wall_ahead", False):
            return "TurnLeft"

        # ELSE move forward
        return "Forward"


class ModelBasedAgent:
    """
    Model-Based Agent.

    Maintains an internal state containing:
    - estimated position
    - facing direction
    - visited cells
    - tried directions
    - previous action
    """

    def __init__(self):

        self.estimated_position = (0, 0)

        self.facing = "Right"

        self.visited_cells = {(0, 0)}

        self.tried_directions = {}

        self.last_action = None

    def _left_of(self, direction):

        directions = [
            "Up",
            "Left",
            "Down",
            "Right"
        ]

        index = directions.index(direction)

        return directions[
            (index + 1) % 4
        ]

    def _right_of(self, direction):

        directions = [
            "Up",
            "Right",
            "Down",
            "Left"
        ]

        index = directions.index(direction)

        return directions[
            (index + 1) % 4
        ]

    def _position_after_move(
        self,
        position,
        direction
    ):

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

        if self.last_action in (
            "Up",
            "Down",
            "Left",
            "Right"
        ):

            self.facing = self.last_action

            if not percept.get(
                "wall_ahead",
                False
            ):

                self.estimated_position = (
                    self._position_after_move(
                        self.estimated_position,
                        self.last_action
                    )
                )

                self.visited_cells.add(
                    self.estimated_position
                )

        elif self.last_action == "TurnLeft":

            self.facing = self._left_of(
                self.facing
            )

        elif self.last_action == "TurnRight":

            self.facing = self._right_of(
                self.facing
            )

    def sense_and_act(self, percept):

        self._update_state(percept)

        current_position = (
            self.estimated_position
        )

        left_direction = self._left_of(
            self.facing
        )

        right_direction = self._right_of(
            self.facing
        )

        tried = self.tried_directions.setdefault(
            current_position,
            set()
        )

        # IF food is ahead
        if percept.get(
            "food_here",
            False
        ):

            action = "Forward"

            tried.add(self.facing)

            self.last_action = action

            return action

        # IF wall is ahead
        if percept.get(
            "wall_ahead",
            False
        ):

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

        # Check whether forward cell was visited
        forward_cell = (
            self._position_after_move(
                current_position,
                self.facing
            )
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

        # Otherwise explore forward
        tried.add(self.facing)

        action = "Forward"

        self.last_action = action

        return action


class SearchAgent:
    """
    Goal-Based / Planning Agent.

    Uses:
        BFS - Breadth-First Search
        DFS - Depth-First Search
        UCS - Uniform-Cost Search

    The agent receives the global world model and creates
    an offline plan before physically executing it.
    """

    def __init__(self):

        # Complete sequence of actions to execute
        self.plan = []

        # Change this to:
        # "BFS"
        # "DFS"
        # "UCS"
        self.active_algo = "BFS"

        # Agent's internally tracked position
        self.current_position = (0, 0)

    # =====================================================
    # Common helper
    # =====================================================

    def _get_neighbors(
        self,
        position,
        walls,
        grid_size
    ):
        """
        Return valid neighboring cells.

        Each result contains:
            next_position
            action
            cost
        """

        width, height = grid_size

        x, y = position

        neighbors = [
            (
                (x, y + 1),
                "Up",
                1
            ),
            (
                (x, y - 1),
                "Down",
                1
            ),
            (
                (x - 1, y),
                "Left",
                1
            ),
            (
                (x + 1, y),
                "Right",
                1
            )
        ]

        valid_neighbors = []

        for next_position, action, cost in neighbors:

            nx, ny = next_position

            # Boundary check
            if not (
                0 <= nx < width
                and
                0 <= ny < height
            ):
                continue

            # Wall check
            if next_position in walls:
                continue

            valid_neighbors.append(
                (
                    next_position,
                    action,
                    cost
                )
            )

        return valid_neighbors

    # =====================================================
    # BFS
    # =====================================================

    def bfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Breadth-First Search.

        Uses FIFO queue:
            deque.popleft()

        Explores shallowest nodes first.
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        if start_pos == goal_pos:
            return []

        # FIFO frontier
        frontier = deque()

        frontier.append(
            (
                start_pos,
                []
            )
        )

        # Reached set prevents cycles
        reached = {
            start_pos
        }

        while frontier:

            current, path = (
                frontier.popleft()
            )

            for (
                next_position,
                action,
                cost
            ) in self._get_neighbors(
                current,
                walls,
                grid_size
            ):

                if next_position in reached:
                    continue

                new_path = (
                    path + [action]
                )

                # Goal found
                if next_position == goal_pos:
                    return new_path

                reached.add(
                    next_position
                )

                frontier.append(
                    (
                        next_position,
                        new_path
                    )
                )

        return None

    # =====================================================
    # DFS
    # =====================================================

    def dfs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Depth-First Search.

        Uses LIFO stack:
            list.pop()

        Explores deeper nodes first.
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        if start_pos == goal_pos:
            return []

        # LIFO frontier
        frontier = [
            (
                start_pos,
                []
            )
        ]

        # Reached set
        reached = {
            start_pos
        }

        while frontier:

            current, path = (
                frontier.pop()
            )

            if current == goal_pos:
                return path

            neighbors = self._get_neighbors(
                current,
                walls,
                grid_size
            )

            # Reverse so that the search has
            # a predictable direction when
            # using stack.pop()
            for (
                next_position,
                action,
                cost
            ) in reversed(neighbors):

                if next_position in reached:
                    continue

                reached.add(
                    next_position
                )

                new_path = (
                    path + [action]
                )

                frontier.append(
                    (
                        next_position,
                        new_path
                    )
                )

        return None

    # =====================================================
    # UCS
    # =====================================================

    def ucs_search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):
        """
        Uniform-Cost Search.

        Uses a priority queue ordered by
        total path cost g(n).
        """

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = {
            tuple(wall)
            for wall in walls
        }

        if start_pos == goal_pos:
            return []

        # Priority queue:
        # (cost, counter, position, path)
        frontier = []

        counter = 0

        heapq.heappush(
            frontier,
            (
                0,
                counter,
                start_pos,
                []
            )
        )

        # Best known cost for each state
        reached = {
            start_pos: 0
        }

        while frontier:

            (
                current_cost,
                _,
                current,
                path
            ) = heapq.heappop(
                frontier
            )

            # Ignore outdated queue entries
            if (
                current_cost
                > reached.get(
                    current,
                    float("inf")
                )
            ):
                continue

            # Goal found
            if current == goal_pos:
                return path

            for (
                next_position,
                action,
                step_cost
            ) in self._get_neighbors(
                current,
                walls,
                grid_size
            ):

                new_cost = (
                    current_cost
                    + step_cost
                )

                # Add state if this is
                # the cheapest path found
                if (
                    next_position not in reached
                    or
                    new_cost
                    < reached[next_position]
                ):

                    reached[
                        next_position
                    ] = new_cost

                    new_path = (
                        path + [action]
                    )

                    counter += 1

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            counter,
                            next_position,
                            new_path
                        )
                    )

        return None

    # =====================================================
    # Find closest food
    # =====================================================

    def _find_closest_food(
        self,
        start_pos,
        food_positions
    ):
        """
        Select the closest food using Manhattan distance.
        """

        if not food_positions:
            return None

        start_x, start_y = (
            start_pos
        )

        closest_food = min(
            food_positions,
            key=lambda food: (
                abs(
                    food[0] - start_x
                )
                +
                abs(
                    food[1] - start_y
                )
            )
        )

        return tuple(
            closest_food
        )

    # =====================================================
    # Select search algorithm
    # =====================================================

    def _search(
        self,
        start_pos,
        goal_pos,
        walls,
        grid_size
    ):

        if self.active_algo == "BFS":

            return self.bfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        elif self.active_algo == "DFS":

            return self.dfs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        elif self.active_algo == "UCS":

            return self.ucs_search(
                start_pos,
                goal_pos,
                walls,
                grid_size
            )

        else:

            raise ValueError(
                "Unknown search algorithm: "
                + str(self.active_algo)
            )

    # =====================================================
    # Sense and Act
    # =====================================================

    def sense_and_act(self, percept):
        """
        Create a complete offline plan if the current
        plan is empty.

        Then execute one action at a time.
        """

        # -------------------------------------------------
        # If no plan exists, create one
        # -------------------------------------------------

        if not self.plan:

            grid_size = percept.get(
                "grid_size"
            )

            walls = percept.get(
                "walls",
                []
            )

            all_food = percept.get(
                "all_food",
                []
            )

            # No food remaining
            if not all_food:

                return "Stay"

            # Find closest food
            goal = (
                self._find_closest_food(
                    self.current_position,
                    all_food
                )
            )

            if goal is None:

                return "Stay"

            # Run selected search algorithm
            new_plan = self._search(
                self.current_position,
                goal,
                walls,
                grid_size
            )

            # If no path exists
            if new_plan is None:

                return "TurnRight"

            # Store complete plan
            self.plan = list(
                new_plan
            )

        # -------------------------------------------------
        # Execute first action from plan
        # -------------------------------------------------

        action = self.plan.pop(0)

        # Update our tracked position
        # because search actions are cardinal movements.
        if action in (
            "Up",
            "Down",
            "Left",
            "Right"
        ):

            x, y = (
                self.current_position
            )

            if action == "Up":
                y += 1

            elif action == "Down":
                y -= 1

            elif action == "Left":
                x -= 1

            elif action == "Right":
                x += 1

            self.current_position = (
                x,
                y
            )

        return action