import os

import pycxsimulator
from pylab import *
# from dotenv import load_dotenv, find_dotenv

width = 100 # Size of horizontal length
height = 100 # Size of vertical length
hostProb = 0.30 # Probability of the cell being occupied by a healthy host
infectedProb = 0.30 # Probability of cell being occupied by a host with parasite

infectionRate = 0 # Probability of getting infected with an parasite
regrowthRate = 0 # Probability of regrowing in cellular
deathProb = 1 # Probability of dying after contracting the parasite
cureProb = 0 # Probability of the parasite die

neighbourhood_selected = "Moore"
plotCA = 1
plotPhase = 1

def initialize():
    global time, config, nextConfig, empty, healthy, infected
    time = 0

    # Generate Initial Conditions based on configurations
    config = zeros([height, width])  # State 0: Blue

    for x in range(width):
        for y in range(height):
            p = random()
            if p < infectedProb:
                cell_state = 2  # State 2: Red
            elif infectedProb < p < (min(infectedProb + hostProb, 1)):
                cell_state = 1  # State 1: Green
            else:
                continue # cell state remains zero (empty)
            config[x, y] = cell_state

    nextConfig = zeros([height, width])

    # Number of clean, healthy and infected
    empty = np.array([np.count_nonzero(config == 0)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 2)])

def observe():
    cla()

    if plotCA:
        figure(plotCA)
        imshow(config, vmin=0, vmax=2, cmap=cm.jet)
        axis('image')
        title('t = ' + str(time))
        imsave(str(time) + ".png", config, vmin=0, vmax=2, cmap=cm.jet)

    if plotPhase:
        figure(plotCA + plotPhase)
        plot(np.arange(time + 1), empty)
        plot(np.arange(time + 1), healthy)
        plot(np.arange(time + 1), infected)
        xlabel('Time')
        ylabel('Number of Cells')
        legend(('Empty', 'Healthy', 'Infected'))
        title('t = ' + str(time))
        imsave(str(time) + "_Phase.png", config, vmin=0, vmax=2, cmap=cm.jet)

def update():
    global time, config, nextConfig, state, empty, healthy, infected
    neighbours = neighbourhood(neighbourhood_selected)
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[x, y]
            if state == 1:
                neigh_list = neighbours(x, y)
                for neighbour in neigh_list:
                    if neighbour == 2:
                        if random() < infectionRate:
                            state = 2
            elif state == 2:
                p = random()
                if p < deathProb:
                    state = 0  # Death
                else:
                    state = 2

            nextConfig[x, y] = state

    config, nextConfig = nextConfig, config

    # Change state of stored values
    ## Empty - State 0
    number_empty_cells = np.count_nonzero(config == 0)
    empty = np.append(empty, number_empty_cells)

    ## Healthy - State 1
    number_healthy_cells = np.count_nonzero(config == 1)
    healthy = np.append(healthy, number_healthy_cells)

    ## Infected - State 2
    number_infected_cells = np.count_nonzero(config == 2)
    infected = np.append(infected, number_infected_cells)

    print(f'===== Iteration: {time} =====')
    print(f'Number of Empty: {number_empty_cells}')
    print(f'Number of Healthy: {number_healthy_cells}')
    print(f'Number of Infected: {number_infected_cells}\n')


def neighbourhood(type):
    def neighbourhood(x, y):
        neigh_list = list()
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append(config[(x + dx) % width, (y + dy) % height])
        elif (type == "Von Neumann"):
            neigh_list.append(config[(x + 1) % width, (y) % height])
            neigh_list.append(config[(x - 1) % width, (y) % height])
            neigh_list.append(config[(x) % width, (y + 1) % height])
            neigh_list.append(config[(x) % width, (y - 1) % height])
        return neigh_list

    return neighbourhood


if __name__ == '__main__':
    pycxsimulator.GUI().start(func=[initialize, observe, update])
