"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
from SystemState import SystemState

class CCAgent:

    def __init__(self, x: list[float], v: list[float], learning_rate = .1, gamma=.9, epsilon=0.2, control_inputs: list[float] = [], size: int = 21):
        self.gamma = gamma
        self.epsilon = epsilon
        self.control_inputs = np.array(control_inputs)
        self.learning_rate = learning_rate
        self.x = x
        self.v = v

        self.target = SystemState(0,0)

        self.q_table = np.zeros(
            (self.x.shape[0]
            , self.v.shape[0], 
            len(self.control_inputs))
            )


    def get_action(self, state: SystemState):
        '''
        Uses the input state to select an action using epsilon greedy
        '''
        action = None
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.control_inputs)
        else:
            action = self.max_a(state)
        return action


    def get_discrete_indices(self, state: SystemState, action: float = None):
        '''
        Gets discrete indices from the state values for the input state.

        If action is provided, it will use the index from control_inputs to provide a u_i.
        Otherwise, u_i is returned as none.
        '''
        x_i = np.argmin(np.abs(self.x - state.x))
        v_i = np.argmin(np.abs(self.v - state.v))
        u_i = None
        if action is not None:
            u_i = np.where(self.control_inputs == action)[0][0]
        return x_i, v_i, u_i
    
    def get_q_table_entry(self, state: SystemState, action: float):
        '''
        Gets a q-table entry based on the input state and provided action
        '''
        (x_i, v_i, u_i) = self.get_discrete_indices(state, action)
        return self.q_table[x_i][v_i][u_i]
    
    def set_q_table_entry(self, state: SystemState, value: float, action: float):
        '''
        Sets a q-table entry to input value at position discretized from input state and given action
        '''
        (x_i, v_i, u_i) = self.get_discrete_indices(state, action)
        self.q_table[x_i][v_i][u_i] = value

    def max_a(self, state: SystemState):
        (x_i, v_i, _) = self.get_discrete_indices(state)
        return self.control_inputs[np.argmax(self.q_table[x_i][v_i])]
    

    def update_qtable(self, current_state: SystemState, next_state: SystemState, reward: float, action: float):
        entry = self.get_q_table_entry(current_state, action)
        (x_i, v_i, _) = self.get_discrete_indices(next_state)
        max_q = np.max(self.q_table[x_i][v_i])
        new_value = entry + self.learning_rate * (reward + self.gamma * max_q - entry)
        self.set_q_table_entry(current_state, new_value, action)