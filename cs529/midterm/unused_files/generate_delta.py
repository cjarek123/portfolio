import pandas as pd
import numpy as np
def generate_delta(num_points, add_noise = False):
    target_columns = ['delta_xk', 'delta_vk']
    vk = 10.0
    xk = 1.0

    data_dict = []
    for _ in range(num_points):
        xk_n = xk + 0.1*vk
        vk_n = vk
        data_dict.append({ 'xk': xk, 'vk': vk, 'delta_xk': xk_n - xk, 'delta_vk': vk_n - vk})
        xk = xk_n
        vk = vk_n
        
        
    
    df = pd.DataFrame(data_dict)
    if add_noise:
        noise = np.random.uniform(.5, 1, size=df[target_columns].shape)
        df[target_columns] = df[target_columns] + noise
    return df.dropna()
