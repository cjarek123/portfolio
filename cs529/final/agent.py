"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np

class Agent:
    def __init__(self, states: list[tuple[int,int]], learning_rate: float = 0.1, gamma: float = 0.75, epsilon: float = .2):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon

        self.q_table = {}
        # init q_table to store q values for actions at index [state]

        # self.q_table[(0,0)] = {...}
        for state in states:
            self.q_table[state] = {
                'up': 0,
                'down': 0,
                'left': 0,
                'right': 0,
            }


    def get_action(self, state: tuple[int, int], available_actions: list[str]) -> str:
        next_action = None
        if np.random.random() < self.epsilon:
            next_action = np.random.choice(available_actions)
        else:
            # Get the action with the max q value
            # will initialize to the first available if none
            # after that, get the greater value
            q_map = {}
            for action in available_actions:
                q_value = self.q_table[state][action]
                q_map[action] = q_value
            next_action = max(q_map, key=q_map.get)
        return next_action

    def max_q(self, state) -> float:
        action_q_values = list(self.q_table[state].values())
        return np.max(action_q_values)
    
    def update(self, current_state: tuple[int, int], next_state: tuple[int,int], reward: float, action: str):
        max_q = self.max_q(next_state)
        current_q = self.q_table[current_state][action]
        self.q_table[current_state][action] = current_q + self.learning_rate * (reward + self.gamma * max_q - current_q)
