"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
import numpy as np
from scipy.integrate import odeint
from SystemState import SystemState
from CCAgent import CCAgent

class Car:

    def __init__(self, x: list[float], v: list[float], delta = .1, random_state = 42, boundary = 5, success_threshold = None):
        self.random_state = random_state
        self.steps = np.linspace(0, delta)
        self.x = x
        self.v = v
        self.boundary = boundary
        self.step_count = 0
        self.success_threshold = .05 if success_threshold is None else success_threshold
        self.trajectory = []
    
        self._position = self.init_random_state()

    def reset(self):
        '''
        Resets the position and the step count for the car
        '''
        self._position = self.init_random_state()
        self.step_count = 0

    def init_random_state(self) -> SystemState:
        '''
        Initializes a random SystemState, generally to be used as a starting point.
        '''
        random_state = SystemState(
            np.random.choice(self.x),
            np.random.choice(self.v)
            )
        return random_state
            
    
    def step(self, state: SystemState, u_i: float) -> SystemState:
        '''
        Given a state and an action, runs the odeint model 
        and gives the trajectory for the next step which is returned as a SystemState

        This also increments the internal tracking of step_count
        '''
        y = odeint(self._ode_model, (state.x, state.v), self.steps, args=((u_i,)))
        next_x = y[-1][0]
        next_v = y[-1][1]
        # Clip the state to the boundaries
        if next_x > 5:
            next_x = 5
        elif next_x < -5:
            next_x = -5
        if next_v > 5:
            next_v = 5
        elif next_v < -5:
            next_v = -5
        system_state = SystemState(next_x, next_v) # update position
        self._position = system_state
        self.trajectory.append(system_state)
        self.step_count += 1
        return system_state
    


    def _ode_model(self, s, t, u) -> list[float]:
        """
        ODE integration model from assignment PDF
        """
        dsdt = [s[1], u]
        return dsdt
    
    def hit_target(self, state: SystemState) -> bool:
        '''
        Determines whether a given state is within the success threshold, defaulting to .05
        '''
        return np.abs(state.x) < self.success_threshold and np.abs(state.v) < self.success_threshold

    
    def calculate_reward(self, state: SystemState) -> float:
        '''
        Calculates the reward to be given to the agent based on:
        1. being in bounds (harsh penalty)
        2. Whether the state hit the target (high reward)
        3. Basic distance from 0 measurement, returned as negative (higher distances from zero have harsher penalties)
        '''
        if not self.state_in_bounds(state):
            return -10
        if self.hit_target(state):
            return 100
        return 1 - 0.1 * (abs(state.x)**2 + abs(state.v)**2)
        
    
    
    def should_continue(self, break_on_hit: bool = False) -> bool:
        '''
        Determines if the training loop should continue.
        If the current position of the car is out of bounds, stop it immediately

        If the user decides to have the loop break on a success hit, return False
        '''
        if break_on_hit and self.hit_target(self.get_position()):
            return False
        out_of_bounds = self.state_in_bounds(self._position)
        return out_of_bounds
    
    def state_in_bounds(self, state: SystemState) -> bool:
        '''
        Determines whether a given state is within the system boundaries
        '''
        if state.x > self.boundary or state.x < -self.boundary:
            return False
        if state.v > self.boundary or state.v < -self.boundary:
            return False
        return True
    
    def get_position(self) -> SystemState:
        '''
        Return the cars current position
        '''
        return self._position
    
    def learned_park_car(self, driver: CCAgent):
        steps = 0
        MAX_STEPS = 1000
        x_trajectory = []
        v_trajectory = []
        should_quit = False
        hit_target = False
        while steps < MAX_STEPS and not should_quit:
            driver.epsilon = 0 # no exploration
            current_state = self.get_position()
            action = driver.get_action(current_state)

            next = self.step(current_state, action)

            x_trajectory.append(next.x)
            v_trajectory.append(next.v)
            if self.hit_target(next):
                should_quit = True
                hit_target = True
            if not self.state_in_bounds(next):
                should_quit = True
            steps += 1
        return x_trajectory, v_trajectory, hit_target, steps
            

