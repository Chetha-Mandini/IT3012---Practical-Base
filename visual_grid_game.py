import pygame
import sys
from agent import SimpleReflexAgent, ModelBasedAgent

GRID_SIZE = 8
CELL_SIZE = 80
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FPS = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

class VisualGridGame:
    def __init__(self, agent_type='model_based'):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Grid World Simulation")
        self.clock = pygame.time.Clock()

        # Define grid bounds (1 represents walls)
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.agent_pos = [1, 1]
        # Directions: 0: North, 1: East, 2: South, 3: West
        self.directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.facing_idx = 1  # Start facing East

        self.food_positions = [(1, 5), (5, 1), (6, 5)]

        if agent_type == 'simple_reflex':
            self.agent = SimpleReflexAgent()
        else:
            self.agent = ModelBasedAgent()

    def is_valid_move(self, x, y):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            return self.grid[y][x] == 0
        return False

    def get_percept(self):
        """Step 1.1: Partial Observability Percept Generator."""
        dx, dy = self.directions[self.facing_idx]
        front_x = self.agent_pos[0] + dx
        front_y = self.agent_pos[1] + dy

        wall_ahead = not self.is_valid_move(front_x, front_y)
        food_here = tuple(self.agent_pos) in self.food_positions

        return {
            'wall_ahead': wall_ahead,
            'food_here': food_here
        }

    def step(self):
        percept = self.get_percept()
        action = self.agent.sense_and_act(percept)

        if action == 'suck':
            if tuple(self.agent_pos) in self.food_positions:
                self.food_positions.remove(tuple(self.agent_pos))
        elif action == 'turn_left':
            self.facing_idx = (self.facing_idx - 1) % 4
        elif action == 'turn_right':
            self.facing_idx = (self.facing_idx + 1) % 4
        elif action == 'move_forward':
            dx, dy = self.directions[self.facing_idx]
            next_x = self.agent_pos[0] + dx
            next_y = self.agent_pos[1] + dy
            if self.is_valid_move(next_x, next_y):
                self.agent_pos[0] = next_x
                self.agent_pos[1] = next_y

    def render(self):
        self.screen.fill(WHITE)

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

        for food in self.food_positions:
            fx = food[0] * CELL_SIZE + CELL_SIZE // 2
            fy = food[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.screen, GREEN, (fx, fy), CELL_SIZE // 4)

        ax = self.agent_pos[0] * CELL_SIZE + CELL_SIZE // 2
        ay = self.agent_pos[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, RED, (ax, ay), CELL_SIZE // 3)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.step()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Change parameter to 'simple_reflex' to test Step 1.2 failure
    # Change parameter to 'model_based' to test Step 1.3 memory escape behavior
    game = VisualGridGame(agent_type='model_based')
    game.run()