"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
from Car import Car
from CCAgent import CCAgent
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random



def run_learning(bound: int = 5, size=21, learning_rate: float = .1, gamma: float = .95, epsilon: float = .2, iterations: int = 10000, steps_per_episode: int = 500):
    np.random.seed(101)
    random.seed(101)
    BOUND = bound
    x = np.linspace(-BOUND, BOUND, size)
    v = np.linspace(-BOUND, BOUND, size)

    control_inputs = np.array([-5, -1, -.1, -.01, -.001, -.0001, 0, .0001, .001, .01, .1, 1, 5])
    driver = CCAgent(x=x, v=v, learning_rate=learning_rate, control_inputs=control_inputs, epsilon=epsilon, gamma=gamma)
    car = Car(x=x, v=v, boundary=BOUND)

    avg_rewards = []
    total_target_hits = 0
    episode_target_hit_history = []
    total_steps = 0
    with tqdm(range(iterations)) as progress:
        for i in progress:
            steps = 0
            episode_rewards = []
            episode_target_hits = 0
            total_reward = 0
            while steps < steps_per_episode and car.should_continue(break_on_hit=True):
                current_state = car.get_position()
                action = driver.get_action(current_state)

                next = car.step(current_state, action)
                reward = car.calculate_reward(next)

                if car.hit_target(next):
                    total_target_hits += 1
                    episode_target_hits += 1

                episode_rewards.append(reward)
                total_reward += reward

                driver.update_qtable(current_state, next, reward, action)

                
                steps += 1
                total_steps += 1
            
            if(len(episode_rewards) > 0):
                avg_rewards.append(np.mean(episode_rewards))
            episode_target_hit_history.append(episode_target_hits)
            if i % 100 == 0:
                progress.set_description(f"Total Reward: {round(total_reward, 2)} | Total Target Hits: {total_target_hits}")
            car.reset()
    return driver, avg_rewards, episode_target_hit_history, total_target_hits
if __name__ == '__main__':

   
    driver, avg_rewards, episode_target_hit_history, total_target_hits = run_learning()

