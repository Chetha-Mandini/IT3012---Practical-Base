class SimpleReflexAgent:
    """Step 1.2: Simple Reflex Agent (Stateless, Pure IF-THEN Rules)."""
    def __init__(self):
        pass  # Strictly no internal memory state allowed

    def sense_and_act(self, percept):
        if percept.get('food_here'):
            return 'suck'
        elif percept.get('wall_ahead'):
            return 'turn_left'
        else:
            return 'move_forward'


class ModelBasedAgent:
    """Step 1.3: Model-Based Agent with memory state and transition tracker."""
    def __init__(self):
        self.visited_cells = set()
        self.current_pos = (0, 0)
        # Directions: 0: North (0, -1), 1: East (1, 0), 2: South (0, 1), 3: West (-1, 0)
        self.facing_idx = 1
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.last_action = None

    def sense_and_act(self, percept):
        # 1. Transition Model Update (update position/orientation from last action)
        if self.last_action == 'move_forward':
            dx, dy = self.directions[self.facing_idx]
            self.current_pos = (self.current_pos[0] + dx, self.current_pos[1] + dy)
        elif self.last_action == 'turn_left':
            self.facing_idx = (self.facing_idx - 1) % 4
        elif self.last_action == 'turn_right':
            self.facing_idx = (self.facing_idx + 1) % 4

        # 2. Sensor Model Update (record current state into memory)
        self.visited_cells.add(self.current_pos)

        # 3. Condition-Action Rules using Internal Memory State
        if percept.get('food_here'):
            action = 'suck'
        elif percept.get('wall_ahead'):
            action = 'turn_left'
        else:
            # Check if moving forward enters a cell already visited
            dx, dy = self.directions[self.facing_idx]
            next_pos = (self.current_pos[0] + dx, self.current_pos[1] + dy)

            if next_pos in self.visited_cells:
                # Loop mitigation rule: turn right to explore alternate options
                action = 'turn_right'
            else:
                action = 'move_forward'

        self.last_action = action
        return action