import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
grid_size = 16
num_iterations = 1000
initial_elevation = 10
noise_scale = 2
rain_amount = 0.01
evaporation_rate = 0.9
erosion_rate = 0.1
deposition_rate = 0.05
min_slope = 0.001

# Initialize the elevation and water grids with random noise
elevation = initial_elevation * np.ones((grid_size, grid_size)) + noise_scale * np.random.rand(grid_size, grid_size)
water = np.zeros((grid_size, grid_size))

# D8 flow directions (row, column)
flow_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

def update(frameNum, img, elevation, water, grid_size, rain_amount, evaporation_rate, erosion_rate, deposition_rate, min_slope):
    print("Frame: " + str(frameNum) + "/" + str(num_iterations))
    # Add rain to the water grid
    water += rain_amount

    # Calculate flow direction, erosion, and deposition
    new_elevation = elevation.copy()
    new_water = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            max_slope = 0
            flow_direction = None

            for di, dj in flow_directions:
                ni = (i + di) % grid_size
                nj = (j + dj) % grid_size
                slope = (elevation[i, j] + water[i, j] - elevation[ni, nj] - water[ni, nj]) / np.sqrt(di ** 2 + dj ** 2)

                if slope > max_slope:
                    max_slope = slope
                    flow_direction = (di, dj)

            # If there is a downhill direction, move water, erode, and deposit sediment
            if max_slope > min_slope:
                ni, nj = (i + flow_direction[0]) % grid_size, (j + flow_direction[1]) % grid_size
                water_flow = water[i, j] * (max_slope / (max_slope + min_slope))
                erosion_amount = erosion_rate * water_flow
                deposition_amount = deposition_rate * water_flow

                new_elevation[i, j] -= erosion_amount
                new_elevation[ni, nj] += deposition_amount
                new_water[ni, nj] += water_flow

    # Evaporate water
    water = (1 - evaporation_rate) * new_water

    # Update elevation and plot
    elevation = new_elevation
    img.set_array(elevation)
    return img,

# Set up the animation
fig, ax = plt.subplots()
img = ax.imshow(elevation, cmap='terrain', interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, elevation, water, grid_size, rain_amount, evaporation_rate, erosion_rate, deposition_rate, min_slope),
                              frames=num_iterations, interval=1)

plt.show()
