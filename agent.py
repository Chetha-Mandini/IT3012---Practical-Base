from collections import deque
import heapq
import math

# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)


class SearchAgent:
    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'
        self.current_pos = (0, 0) 

    def sense_and_act(self, percept):
        if len(self.plan) == 0:
            all_food = percept['all_food']
            walls = percept['walls']
            grid_size = percept['grid_size']

            if not all_food:
                return "Stay"

            closest_food =None
            min_distance = float('inf')

            for food in all_food:
                distance = abs(self.current_pos[0] - food[0]) + abs(self.current_pos[1] - food[1])
                if distance < min_distance:
                    min_distance = distance
                    closest_food = food

            if self.active_algo == 'BFS':
                found, new_plan = self.bfs_search(self.current_pos, closest_food, walls, grid_size)
            elif self.active_algo == 'DFS':
                found, new_plan = self.dfs_search(self.current_pos, closest_food, walls, grid_size)
            elif self.active_algo == 'UCS':
                found, new_plan = self.ucs_search(self.current_pos, closest_food, walls, grid_size)
            elif self.active_algo == 'AStar':
                found, new_plan = self.astar_search(self.current_pos, closest_food, walls, grid_size)

            # 4. Save the calculated path to our master plan
            if found:
                self.plan = new_plan

        # 5. Execute the next step of the plan
        if len(self.plan) > 0:
            action = self.plan.pop(0) # Take the first action off the list
            
            # Update our internal position tracker so the agent knows where it moved
            self.current_pos = self.get_next_position(self.current_pos, action)
            return action
            
        return "Stay" # Fallback just in case

    def get_next_position(self, current_pos, action):
        x, y = current_pos
        if action == 'Up':
            return (x, y + 1)
        elif action == 'Down':
            return (x, y - 1)
        elif action == 'Left':
            return (x - 1, y)
        elif action == 'Right':
            return (x + 1, y)
        return current_pos 

    def is_valid_position(self, pos, walls, grid_size):
        x, y = pos
        width, height = grid_size

        if x < 0 or x >=width or y < 0 or y >= height:
            return False
        if pos in walls:
            return False
        return True

    def bfs_search(self, start, goal, walls, grid_size):

        frontier = deque([(start, [])]) #(current_coordinate, path_history)
        visited = set([start])

        while frontier:
            current, path = frontier.popleft()
            if current == goal:
                return True, path

            for action in ['Up', 'Down', 'Left', 'Right']:
                next_pos = self.get_next_position(current, action)
                if self.is_valid_position(next_pos, walls, grid_size) and next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path + [action]
                    frontier.append((next_pos, new_path))
        
        return False, []
    

    def dfs_search(self,start,goal, walls, grid_size):
        frontier = [(start, [])]  # (current_coordinate, path_history)
        visited = set([start])

        while frontier:
            current, path = frontier.pop()
            if current == goal:
                return True, path

            if current not in visited:
                visited.add(current)

                for action in ['Up', 'Down', 'Left', 'Right']:
                    next_pos = self.get_next_position(current, action)
                    if self.is_valid_position(next_pos, walls, grid_size):
                        new_path = path + [action]
                        frontier.append((next_pos, new_path))
        
        return False, []


    def ucs_search(self,start,goal,walls,grid_size):
        frontier = []
        heapq.heappush(frontier, (0, start, []))  # (cost, current_coordinate, path_history)
        visited = set()

        while frontier:
            cost, current, path = heapq.heappop(frontier)
            if current == goal:
                return True, path

            if current not in visited:
                visited.add(current)

                for action in ['Up', 'Down', 'Left', 'Right']:
                    next_pos = self.get_next_position(current, action)
                    if self.is_valid_position(next_pos, walls, grid_size):
                        new_path = path + [action]
                        new_cost = cost + 1
                        heapq.heappush(frontier, (new_cost, next_pos, new_path))
        return False, []
    
    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        frontier = []
        reached_states = set()
        
        g_cost = 0
        if heuristic_type == 'manhattan':
            h_cost = self.manhattan_distance(start_pos, goal_pos)
        else:
            h_cost = self.euclidean_distance(start_pos, goal_pos)
            
        f_cost = g_cost + h_cost
        
        heapq.heappush(frontier, (f_cost, g_cost, start_pos, []))
        
        while frontier:
            current_f, current_g, current_pos, path_taken = heapq.heappop(frontier)
            
            if current_pos == goal_pos:
                return True, path_taken 
            
            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)
            
            for action in ['Up', 'Down', 'Left', 'Right']:
                next_pos = self.get_next_position(current_pos, action)
                
                if self.is_valid_position(next_pos, walls, grid_size) and next_pos not in reached_states:
                
                    new_g = current_g + 1
                    
                    if heuristic_type == 'manhattan':
                        new_h = self.manhattan_distance(next_pos, goal_pos)
                    else:
                        new_h = self.euclidean_distance(next_pos, goal_pos)
                        
                    new_f = new_g + new_h
                    new_path = path_taken + [action]
                    
                    heapq.heappush(frontier, (new_f, new_g, next_pos, new_path))
                    
        return False, []


    
# --- Testing Checkpoint ---
if __name__ == "__main__":
    test_agent = SearchAgent()
    
    start = (0, 0)
    goal = (3, 4)
    
    print("Manhattan Distance:", test_agent.manhattan_distance(start, goal))
    print("Euclidean Distance:", test_agent.euclidean_distance(start, goal))