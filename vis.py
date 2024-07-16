import numpy as np
import matplotlib.pyplot as plt

# Generate a noisy sine wave to simulate finger positions
time = np.linspace(0, 10, 100)
finger_positions = np.sin(time) + np.random.normal(0, 0.1, time.shape)

# Apply moving average smoothing
def moving_average(data, window_size):
    cumsum = np.cumsum(np.insert(data, 0, 0))
    return (cumsum[window_size:] - cumsum[:-window_size]) / window_size




# Calculate deltas after smoothing
smoothed_positions = moving_average(finger_positions, window_size=5)
delta_positions = np.diff(smoothed_positions)

# Calculate deltas before smoothing
delta_positions_before_smoothing = np.diff(finger_positions)
smoothed_positions_delta = moving_average(delta_positions_before_smoothing, window_size=5)



# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(time, finger_positions, label='Original Finger Positions', alpha=0.5)
plt.plot(time[2:-2], smoothed_positions, label='Smoothed Finger Positions')
plt.plot(time[3:-2], delta_positions, label='Deltas of Smoothed Positions', linestyle='--')
plt.plot(time[3: -2], smoothed_positions_delta, label='Smooth Deltas of position', alpha=0.5)
plt.legend()
plt.title('Smoothing Before Delta Calculation')
plt.show()
