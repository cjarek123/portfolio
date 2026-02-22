"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
from tqdm import tqdm
from environment import Environment
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt

import random


def run_learning(image_path: str = 'map1.bmp', size = (60, 60), target=None, starting_position=(0,0), learning_rate: float = .1, gamma: float = .75, epsilon=.2, episode_length=10000, steps_per_episode = 500):
    np.random.seed(101)
    random.seed(101)
    iterations = episode_length
    environment = Environment(image_path=image_path, size=size, target=target, starting_position=starting_position)
    agent = Agent(environment.allowed_states, learning_rate=learning_rate, gamma=gamma, epsilon=epsilon)

    total_target_hits = 0
    total_reward = 0
    avg_rewards = []
    episode_target_hit_history = []
    with tqdm(total=iterations) as pbar:
        for i in range(iterations):
            environment.reset()
            steps = 0
            episode_target_hits = 0
            episode_rewards = []
            while steps < steps_per_episode and environment.should_continue():

                current_position = environment.agent_position
                available_actions = environment.get_available_actions()
                action = agent.get_action(current_position, available_actions=available_actions)

                environment.move(current_position, action)
                reward = environment.calculate_reward()
                total_reward += reward
                episode_rewards.append(reward)
                agent.update(current_position, environment.agent_position, reward, action)
                if environment.hit_target():
                    total_target_hits += 1
                    episode_target_hits += 1
                steps += 1
            pbar.update(1)
            episode_target_hit_history.append(episode_target_hits)
            avg_rewards.append(np.mean(episode_rewards))
            if i % 100 == 0:
                pbar.set_description(f"Episode Avg Reward: {round(np.mean(episode_rewards), 2)} | Total Target Hits: {total_target_hits}")

    

    return agent, environment, avg_rewards, episode_target_hit_history


if __name__ == '__main__':
    run_learning()
