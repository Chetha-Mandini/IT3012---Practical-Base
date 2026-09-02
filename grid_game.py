import random


class GridHuntGame:
    """
    A small Pacman-style grid environment (4×4) where an agent collects food.

    Changes vs. original starter code
    ──────────────────────────────────
    Bug fixes:
      • food_positions and walls now use tuples (lists are not hashable in sets).
      • get_percept() and execute_action() no longer take an unused `agent` argument.

    Practical 1 – Part 2 additions:
      • self.toxic_traps  – a set of hazard positions hidden from the agent by default.
      • get_percept() exposes 'smells_toxin' only when the sensor is enabled.
      • execute_action() deducts 15 points when the agent steps on a trap.
    """

    def __init__(self, width: int = 4, height: int = 4, expose_toxin_sensor: bool = False):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]          # Starting position (x, y)
        self.expose_toxin_sensor = expose_toxin_sensor

        # ── Fixed: use tuples so positions are hashable ──
        self.food_positions: set[tuple] = {(1, 2), (2, 3), (3, 0), (2, 1)}
        self.walls: set[tuple] = {(1, 1), (2, 2)}

        # ── Part 2: toxic traps (hidden hazard) ──────────
        # Populate avoiding (0,0), walls, and food.
        self.toxic_traps: set[tuple] = set()
        candidates = [
            (x, y)
            for x in range(width)
            for y in range(height)
            if (x, y) != (0, 0)
            and (x, y) not in self.walls
            and (x, y) not in self.food_positions
        ]
        # Place up to 2 traps (or fewer if the grid is small)
        num_traps = min(2, len(candidates))
        for pos in random.sample(candidates, num_traps):
            self.toxic_traps.add(pos)

        self.score = 0
        self.steps = 0

    # ── Perception ────────────────────────────────────────
    def get_percept(self) -> dict:
        percept = {
            'agent_pos':      list(self.agent_pos),
            'smells_food':    tuple(self.agent_pos) in self.food_positions,
            'hit_wall':       tuple(self.agent_pos) in self.walls,
            'score':          self.score,
            'remaining_food': len(self.food_positions),
        }

        # Step 2.2 (Part 2): expose toxin sensor only when enabled.
        # When *hidden*, the environment is Partially Observable because the
        # agent cannot sense a real hazard that affects its performance measure.
        if self.expose_toxin_sensor:
            percept['smells_toxin'] = tuple(self.agent_pos) in self.toxic_traps

        return percept

    # ── Action execution ──────────────────────────────────
    def execute_action(self, action: str):
        self.steps += 1
        new_pos = list(self.agent_pos)

        if action == 'Up':
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right':
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)
        # 'Stay' → no movement

        # Wall collision: penalise and do NOT move
        if tuple(new_pos) in self.walls:
            self.score -= 5
        else:
            self.agent_pos = new_pos

        current = tuple(self.agent_pos)

        # Eat food
        if current in self.food_positions:
            self.food_positions.remove(current)
            self.score += 20

        # Step 2.3 (Part 2): toxic trap penalty
        if current in self.toxic_traps:
            self.score -= 15

    # ── Terminal condition ────────────────────────────────
    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 20