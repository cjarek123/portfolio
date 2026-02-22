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
import sys
def evaluate_driver(driver: CCAgent, num_evals: int = 5):
    trials = 1000

    scores = []
    results = []
    for _ in range(num_evals):
        successes = 0
        for i in range(trials):
            car = Car(x=driver.x, v=driver.v)
            x_trajectory, v_trajectory, hit_target, steps = car.learned_park_car(driver)
            if hit_target:
                successes += 1
        score = (successes/trials) * 100
        rounded_score = round(score, 2)
        scores.append(rounded_score)
        results.append({ 'x_trajectory': x_trajectory, 'v_trajectory': v_trajectory, 'hit_target': hit_target, 'steps': steps })
    return np.mean(scores), results