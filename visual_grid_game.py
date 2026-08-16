import random
import tkinter as tk

from agent import (
    SimpleReflexAgent,
    ModelBasedAgent,
    SearchAgent
)


class VisualGridHuntGame:

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=2,
        custom_walls=None,
        agent=None
    ):

        self.width = width
        self.height = height

        self.agent_pos = [0, 0]

        self.agent = agent

        # -----------------------------------------
        # Walls
        # -----------------------------------------

        if custom_walls is not None:

            self.walls = set(
                custom_walls
            )

        else:

            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # -----------------------------------------
        # Food
        # -----------------------------------------

        self.food_positions = set()

        while len(
            self.food_positions
        ) < num_food:

            fx = random.randint(
                0,
                self.width - 1
            )

            fy = random.randint(
                0,
                self.height - 1
            )

            position = (
                fx,
                fy
            )

            if (
                position != (0, 0)
                and
                position not in self.walls
            ):

                self.food_positions.add(
                    position
                )

        # -----------------------------------------
        # Opponents
        # -----------------------------------------

        self.opponents = []

        while len(
            self.opponents
        ) < num_opponents:

            ox = random.randint(
                0,
                self.width - 1
            )

            oy = random.randint(
                0,
                self.height - 1
            )

            opponent_position = [
                ox,
                oy
            ]

            if (
                tuple(opponent_position)
                != (0, 0)
                and
                tuple(opponent_position)
                not in self.walls
                and
                tuple(opponent_position)
                not in self.food_positions
            ):

                self.opponents.append(
                    opponent_position
                )

        self.facing = "Right"

        self.score = 0

        self.steps = 0

        self.collision = False

    def _forward_position(self):

        x, y = self.agent_pos

        if self.facing == "Up":

            y += 1

        elif self.facing == "Down":

            y -= 1

        elif self.facing == "Left":

            x -= 1

        elif self.facing == "Right":

            x += 1

        return (
            x,
            y
        )

    def get_percept(self):
        """
        Return the percept available to the agent.

        LAB 2:
            wall_ahead
            food_here

        LAB 3:
            grid_size
            walls
            all_food

        The three additional values expose the world model
        so that the SearchAgent can perform BFS, DFS and UCS.
        """

        forward = (
            self._forward_position()
        )

        # -----------------------------------------
        # Local percept from Lab 2
        # -----------------------------------------

        wall_ahead = (
            forward[0] < 0
            or forward[0] >= self.width
            or forward[1] < 0
            or forward[1] >= self.height
            or forward in self.walls
        )

        food_here = (
            forward
            in self.food_positions
        )

        # -----------------------------------------
        # Lab 3 global state
        # -----------------------------------------

        return {

            # Lab 2 local percept
            "wall_ahead": wall_ahead,

            "food_here": food_here,

            # Lab 3 world model
            "grid_size": (
                self.width,
                self.height
            ),

            "walls": list(
                self.walls
            ),

            "all_food": list(
                self.food_positions
            )
        }

    def execute_action(self, action):

        self.steps += 1

        # -----------------------------------------
        # Turn Left
        # -----------------------------------------

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

        # -----------------------------------------
        # Turn Right
        # -----------------------------------------

        elif action == "TurnRight":

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

        # -----------------------------------------
        # Movement
        # -----------------------------------------

        else:

            direction = self.facing

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

            # -----------------------------------------
            # Boundary collision
            # -----------------------------------------

            if (
                new_pos[0] < 0
                or
                new_pos[0] >= self.width
                or
                new_pos[1] < 0
                or
                new_pos[1] >= self.height
            ):

                self.score -= 5

            # -----------------------------------------
            # Wall collision
            # -----------------------------------------

            elif (
                tuple(new_pos)
                in self.walls
            ):

                self.score -= 5

            # -----------------------------------------
            # Successful movement
            # -----------------------------------------

            else:

                self.agent_pos = new_pos

                # Collect food
                if (
                    tuple(self.agent_pos)
                    in self.food_positions
                ):

                    self.food_positions.remove(
                        tuple(self.agent_pos)
                    )

                    self.score += 20

        # -----------------------------------------
        # Move opponents
        # -----------------------------------------

        for opponent in self.opponents:

            move = random.choice(
                [
                    "Up",
                    "Down",
                    "Left",
                    "Right",
                    "Stay"
                ]
            )

            if (
                move == "Up"
                and
                opponent[1]
                < self.height - 1
            ):

                opponent[1] += 1

            elif (
                move == "Down"
                and
                opponent[1] > 0
            ):

                opponent[1] -= 1

            elif (
                move == "Left"
                and
                opponent[0] > 0
            ):

                opponent[0] -= 1

            elif (
                move == "Right"
                and
                opponent[0]
                < self.width - 1
            ):

                opponent[0] += 1

            if (
                opponent
                == self.agent_pos
            ):

                self.score -= 50

                self.collision = True

    def is_done(self):

        return (
            len(
                self.food_positions
            ) == 0
            or
            self.steps >= 100
            or
            self.collision
        )


class GridGameGUI:

    def __init__(
        self,
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=0,
        walls=None,
        agent_type="search",
        search_algorithm="DFS"
    ):

        self.root = root

        self.root.title(
            "IT3012 - Goal Based Search Agent"
        )

        # -----------------------------------------
        # Select Agent
        # -----------------------------------------

        if (
            agent_type.lower()
            == "simple"
        ):

            agent = (
                SimpleReflexAgent()
            )

            self.agent_name = (
                "Simple Reflex Agent"
            )

        elif (
            agent_type.lower()
            == "model"
        ):

            agent = (
                ModelBasedAgent()
            )

            self.agent_name = (
                "Model-Based Agent"
            )

        else:

            agent = (
                SearchAgent()
            )

            # Select BFS / DFS / UCS
            agent.active_algo = (
                search_algorithm.upper()
            )

            self.agent_name = (
                "Search Agent - "
                + agent.active_algo
            )

        # -----------------------------------------
        # Environment
        # -----------------------------------------

        self.env = (
            VisualGridHuntGame(
                width=width,
                height=height,
                num_food=num_food,
                num_opponents=num_opponents,
                custom_walls=walls,
                agent=agent
            )
        )

        # -----------------------------------------
        # Canvas
        # -----------------------------------------

        max_canvas_size = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_size
                // self.env.width,

                max_canvas_size
                // self.env.height
            )
        )

        canvas_width = (
            self.env.width
            * self.cell_size
        )

        canvas_height = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )

        self.canvas.pack()

        self.label = tk.Label(
            root,
            text=(
                f"{self.agent_name} | "
                f"Score: 0 | "
                f"Steps: 0"
            ),
            font=("Arial", 14)
        )

        self.label.pack(
            pady=10
        )

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.btn.pack(
            pady=5
        )

        self.draw_grid()

    def draw_grid(self):

        self.canvas.delete(
            "all"
        )

        # -----------------------------------------
        # Grid
        # -----------------------------------------

        for x in range(
            self.env.width
        ):

            for y in range(
                self.env.height
            ):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    self.env.height
                    - 1
                    - y
                ) * self.cell_size

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                if (
                    x, y
                ) not in self.env.walls:

                    cell_fill = (
                        "#f1f5f9"
                    )

                else:

                    cell_fill = (
                        "#64748b"
                    )

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=cell_fill,
                    outline="#cbd5e1"
                )

        # -----------------------------------------
        # Food
        # -----------------------------------------

        for fx, fy in (
            self.env.food_positions
        ):

            offset = (
                self.cell_size
                * 0.25
            )

            x1 = (
                fx
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - fy
            ) * self.cell_size + offset

            self.canvas.create_oval(
                x1,
                y1,
                x1
                + self.cell_size * 0.5,
                y1
                + self.cell_size * 0.5,
                fill="#f59e0b",
                outline="#d97706"
            )

        # -----------------------------------------
        # Opponents
        # -----------------------------------------

        for ox, oy in (
            self.env.opponents
        ):

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                ox
                * self.cell_size
                + offset
            )

            y1 = (
                self.env.height
                - 1
                - oy
            ) * self.cell_size + offset

            self.canvas.create_rectangle(
                x1,
                y1,
                x1
                + self.cell_size * 0.6,
                y1
                + self.cell_size * 0.6,
                fill="#990000",
                outline="#7a0000"
            )

        # -----------------------------------------
        # Agent
        # -----------------------------------------

        ax, ay = (
            self.env.agent_pos
        )

        offset = (
            self.cell_size
            * 0.15
        )

        x1 = (
            ax
            * self.cell_size
            + offset
        )

        y1 = (
            self.env.height
            - 1
            - ay
        ) * self.cell_size + offset

        self.canvas.create_oval(
            x1,
            y1,
            x1
            + self.cell_size * 0.7,
            y1
            + self.cell_size * 0.7,
            fill="#000066",
            outline="#1e3a8a"
        )

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                # Get percept
                percept = (
                    self.env.get_percept()
                )

                # Ask agent for action
                action = (
                    self.env.agent.sense_and_act(
                        percept
                    )
                )

                # Execute action
                self.env.execute_action(
                    action
                )

                self.draw_grid()

                self.label.config(
                    text=(
                        f"{self.agent_name} | "
                        f"Action: {action} | "
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps}"
                    )
                )

                self.root.after(
                    200,
                    step
                )

            else:

                if self.env.collision:

                    end_text = (
                        "Collision! Game Over! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                else:

                    end_text = (
                        "Finished! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                self.btn.config(
                    state="normal"
                )

        step()


if __name__ == "__main__":

    root = tk.Tk()

    # ---------------------------------------------
    # LAB 3 SETTINGS
    # ---------------------------------------------
    #
    # Choose:
    #
    # agent_type="search"
    #
    # and choose:
    #
    # search_algorithm="BFS"
    # search_algorithm="DFS"
    # search_algorithm="UCS"
    #
    # ---------------------------------------------

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=5,
        num_opponents=0,
        agent_type="search",
        search_algorithm="BFS"
    )

    root.mainloop()