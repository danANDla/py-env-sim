coordinates = [0, 0]
time = 0
time_step = 1

speeds = [10, 10]
for _ in range(100):
    time += time_step
    for i in range(len(coordinates)):
        coordinates[i] += speeds[i] * time_step
    print(coordinates)