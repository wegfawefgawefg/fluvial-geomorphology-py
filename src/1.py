import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
grid_size = 100
num_iterations = 1000
sediment_probability = 0.1
transport_probability = 0.9

# Initialize the grid with random sediment
grid = np.random.choice([0, 1], size=(grid_size, grid_size), p=[1 - sediment_probability, sediment_probability])

def update(frameNum, img, grid, grid_size, transport_probability):
    new_grid = grid.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            # Check if the current cell has sediment
            if grid[i, j] == 1:
                # Choose a random neighbor
                ni = i + np.random.randint(-1, 2)
                nj = j + np.random.randint(-1, 2)
                ni = (ni + grid_size) % grid_size
                nj = (nj + grid_size) % grid_size

                # If the neighbor is empty, transport sediment with a certain probability
                if grid[ni, nj] == 0 and np.random.random() < transport_probability:
                    new_grid[ni, nj] = 1
                    new_grid[i, j] = 0

    img.set_array(new_grid)
    grid[:] = new_grid[:]
    return img,

# Set up the animation
fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='viridis', interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, grid_size, transport_probability),
                              frames=num_iterations, interval=100)

plt.show()
