import random
from collections import deque


# ──────────────────────────────────────────────
# Practical 1 – Simple Reflex Agent
# ──────────────────────────────────────────────
class SimpleReflexAgent:
    """
    A Condition-Action (reflex) agent.
    Reacts purely to the current percept with no memory of history.
    """

    def sense_and_act(self, percept: dict) -> str:
        """
        Condition-Action rules:
          • wall_ahead → turn (Left or Right)
          • food_here  → stay / collect (Stay)
          • otherwise  → move forward (Up)
        """
        if percept.get('wall_ahead', False):
            # Must not move forward — pick a perpendicular direction
            return random.choice(['Left', 'Right'])

        if percept.get('food_here', False):
            # Stand on the food cell to collect it
            return 'Stay'

        # Default: keep moving forward
        return 'Up'


# ──────────────────────────────────────────────
# Practical 2 – Model-Based Agent
# ──────────────────────────────────────────────
class ModelBasedAgent:
    """
    A model-based reflex agent that maintains an internal state
    so it can escape loops and avoid repeating failed actions.
    """

    def __init__(self):
        self._last_action: str | None = None
        self._tried_actions: list[str] = []
        self._step_count: int = 0

    def sense_and_act(self, percept: dict) -> str:
        self._step_count += 1

        if percept.get('wall_ahead', False):
            # Build pool of alternatives excluding the last failed move
            alternatives = [a for a in ['Up', 'Down', 'Left', 'Right']
                            if a != self._last_action]
            # Also prefer actions not recently tried to break longer loops
            fresh = [a for a in alternatives if a not in self._tried_actions[-3:]]
            action = random.choice(fresh) if fresh else random.choice(alternatives)
        elif percept.get('food_here', False):
            action = 'Stay'
        else:
            action = 'Up'

        # Update internal model
        self._tried_actions.append(action)
        self._last_action = action
        return action


# ──────────────────────────────────────────────
# Practical 3 – Search Agent (BFS)
# ──────────────────────────────────────────────
class SearchAgent:
    """
    An offline planning agent that uses Breadth-First Search (BFS)
    to find the shortest path in a static maze.
    """

    # Map from (dx, dy) displacement to action label
    _MOVES = {
        (0,  1): 'Up',
        (0, -1): 'Down',
        (-1, 0): 'Left',
        (1,  0): 'Right',
    }

    def bfs_search(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        walls: list[tuple[int, int]],
        grid_size: tuple[int, int],
    ) -> list[str] | None:
        """
        Returns the shortest list of action strings from *start* to *goal*,
        or None if the goal is unreachable.

        Parameters
        ----------
        start     : (col, row) starting position
        goal      : (col, row) goal position
        walls     : list of (col, row) wall positions
        grid_size : (width, height) of the grid
        """
        width, height = grid_size
        wall_set = set(map(tuple, walls))

        if tuple(goal) in wall_set:
            return None

        # BFS queue: each entry is (current_position, path_so_far)
        queue = deque([(tuple(start), [])])
        visited = {tuple(start)}

        while queue:
            pos, path = queue.popleft()

            if pos == tuple(goal):
                return path

            for (dx, dy), action in self._MOVES.items():
                nx, ny = pos[0] + dx, pos[1] + dy
                npos = (nx, ny)

                # Bounds check
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                # Wall / visited check
                if npos in wall_set or npos in visited:
                    continue

                visited.add(npos)
                queue.append((npos, path + [action]))

        # No path found
        return None


# ──────────────────────────────────────────────
# Greedy Grid Agent (kept for simulator.py)
# ──────────────────────────────────────────────
class GreedyGridAgent:
    """
    A simple greedy agent that moves towards the nearest food pellet.
    Falls back to random movement when no food is sensed nearby.
    """

    def __init__(self):
        self._actions = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept.get('agent_pos', [0, 0])

        # If there is a smells_toxin warning, avoid moving into the danger zone
        if percept.get('smells_toxin', False):
            # Retreat: pick a random perpendicular direction
            return random.choice(self._actions)

        # Sniff out food direction if agent_pos is known
        # (A real greedy agent would need the food map; here we default to sweep)
        return random.choice(self._actions)