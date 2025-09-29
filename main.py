import numpy as np

GRAVITY_CONST = 9.81

datatype = np.float32
current_coordinates = np.array([0, 0], dtype=datatype)
current_speed = np.array([0, 0], dtype=datatype)
prev_speed = np.array([0, 0], dtype=datatype)
current_force_applied = np.array([10000, 1], dtype=datatype)

rocket_mass = 900

time = 0
time_step = 1
for _ in range(100):
    time += time_step
    prev_speed = current_speed

    real_acceleration = current_force_applied
    real_acceleration[0] = current_force_applied[0] - GRAVITY_CONST * rocket_mass
    if real_acceleration[0] < 0: real_acceleration[0] = 0

    current_speed += current_force_applied * time_step 
    current_coordinates += ( current_speed * time_step + prev_speed * time_step ) / 2

    print(current_coordinates)