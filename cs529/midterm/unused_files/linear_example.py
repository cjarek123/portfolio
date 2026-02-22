from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from generate_data import generate_data
import numpy as np

RANDOM_STATE = 42
df = generate_data(1000, add_noise=False)

feature_cols = ['xk', 'vk']
target_cols = ['xk+1', 'vk+1']
reg = LinearRegression()

X = df[feature_cols].values
y = df[target_cols].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=RANDOM_STATE, shuffle=True)
reg.fit(X_train, y_train)

print("Mean Absolute Error:")
print(mean_absolute_error(y_test, reg.predict(X_test)))
xk, vk, = df.iloc[-1][feature_cols].values
state = [xk, vk]
trajectory = [state.copy()]

for i in range(20):
    inputs = [trajectory[-1]]
    pred = reg.predict(inputs)[0]
    xk = np.float64(pred[0])
    vk = np.float64(pred[1])
    next = np.array([xk, vk])
    trajectory.append(next)



# Print trajectory
for i, s in enumerate(trajectory):
    print(f"Step {i}: x = {s[0]:.2f}, v = {s[1]:.2f}")