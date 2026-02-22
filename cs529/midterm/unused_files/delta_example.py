from generate_delta import generate_delta
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from regression_tree import RegressionTree
import numpy as np
RANDOM_STATE = 42 
df = generate_delta(100, add_noise=False)
feature_cols = ['xk', 'vk']
target_cols = ['delta_xk', 'delta_vk']
reg = RegressionTree(max_depth=30, min_samples_leaf=2)

X = df[feature_cols].values
y = df[target_cols].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=RANDOM_STATE, shuffle=True)
reg.fit(X_train, y_train)

print("Mean Absolute Error:")
print(mean_absolute_error(y_test, reg.predict(X_test)))
xk, vk = df.iloc[-1][feature_cols].values

state = [xk, vk]
trajectory = [state.copy()]

print(f"Starting next state predictions at: xk = {str(state[0])}, vk = {str(state[1])}")
for i in range(20):
    inputs = [trajectory[-1]]
    pred = reg.predict(inputs)[0]
    delta_xk = pred[0]
    delta_vk = pred[1]
    xk = xk + delta_xk
    vk = vk + delta_vk
    next = np.array([xk, vk])
    trajectory.append(next)



# Print trajectory
for i, s in enumerate(trajectory):
    print(f"Step {i}: x = {s[0]:.2f}, v = {s[1]:.2f}")