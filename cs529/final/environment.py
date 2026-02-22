"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
from matplotlib.style import available
import numpy as np
from agent import Agent
from shortestpath import load_map

ACTIONS = { 'down': (1, 0), 'up': (-1, 0), 'left': (0, -1), 'right': (0, 1) }


class Environment:


    def __init__(self, image_path: str = 'map1.bmp', size=(120,120), target = None, starting_position = (0,0)):
        self.image_path = image_path
        self.map = load_map(image_path, size)
        self.states = []
        self.allowed_states = []
        self.start = starting_position
        self.agent_position = starting_position

        for row_idx, row in enumerate(self.map):
            for i, _ in enumerate(row):
                self.states.append((row_idx, i))
                if self.is_allowed_position((row_idx, i)):
                    self.allowed_states.append((row_idx, i))
        self.y_max = size[0] - 1
        self.x_max = size[1] - 1
        # Init to the other end of the map
        # 120, 120, start = (0, 0), target = (119, 119)
        self.target = (size[0] - 1, size[1] - 1) if target is None else target
        
    def reset(self):
        self.agent_position = self.start

    def should_continue(self):
 
        if self.hit_target():
            return False
        return True

    def position_in_bounds(self, position: tuple[int, int]):
        (x, y) = position

        if x > self.x_max or x < 0:
            return False
        if y > self.y_max or y < 0:
            return False
        return True

    def is_allowed_position(self, position: tuple[int, int]):
        (x, y) = position

        return self.map[x, y] == 0
    
    def hit_target(self):
        (a_x, a_y) = self.agent_position
        (t_x, t_y) = self.target
        return a_x == t_x and a_y == t_y
    
    def get_available_actions(self):
        position = self.agent_position

        available_actions = []

        # Basically test every available action to see if the result 
        # is out of bounds or is in an obstacle
        # if not, append to available actions and return
        # this way the agent never leaves the map or hits an obstacle
        for action in ACTIONS.keys():
            (x, y) = position

            x += ACTIONS[action][0]
            y += ACTIONS[action][1]

            if self.position_in_bounds((x, y)) and self.is_allowed_position((x,y)):
                available_actions.append(action)
        return available_actions

    def calculate_reward(self):
        if self.hit_target():
            return 100
        distance = np.linalg.norm(np.subtract(self.agent_position, self.target))
        final = (1 / (1 + distance)) * 10
        return final


    def move(self, state: tuple[int, int], action: str):
        (x, y) = state
        x += ACTIONS[action][0]
        y += ACTIONS[action][1]
        self.agent_position = (x, y)

    
    def test_agent(self, learned_agent: Agent):
        learned_agent.epsilon = 0
        MAX_STEPS = 1000
        self.reset()
        steps = 0
        trajectory = []
        hit_target = False
        while steps < MAX_STEPS:
            current_position = self.agent_position
            available_actions = self.get_available_actions()
            action = learned_agent.get_action(current_position, available_actions=available_actions)

            self.move(current_position, action)
            trajectory.append(self.agent_position)
            if self.hit_target():
                hit_target = True
                break
            steps += 1
        return trajectory, steps, hit_target

    def evaluate_agent(self, learned_agent: Agent, num_evals = 5):
        trials = 1000
        scores = []
        results = []
        trial_steps = []
        for i in range(num_evals):
            successes = 0
            for _ in range(trials):
                trajectory, steps, hit_target = self.test_agent(learned_agent=learned_agent)
                if(hit_target):
                    successes += 1
            score = (successes/trials) * 100
            rounded_score = round(score, 2)
            scores.append(rounded_score)
            trial_steps.append(steps)
            results.append({ 'trajectory': trajectory, 'hit_target': hit_target, 'steps': steps })
        return np.mean(scores), results, np.mean(steps)