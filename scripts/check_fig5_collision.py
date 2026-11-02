import numpy as np
import matplotlib.pyplot as plt

# Check intersection in Fig 5
rates = 56.0
time_ms = 8.0 * (1000.0 / rates)
norm_y_ax1 = 11.0 / 20.0
norm_y_ax2 = time_ms / 250.0

print(f"At x = {rates}:")
print(f"Safety box y-norm on ax1: {norm_y_ax1:.3f}")
print(f"Blue line y-norm on ax2: {norm_y_ax2:.3f}")
print(f"Difference in normalized height: {abs(norm_y_ax1 - norm_y_ax2):.3f} (ONLY {abs(norm_y_ax1 - norm_y_ax2)*100:.1f}% apart!)")
