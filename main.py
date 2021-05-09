import os

import pycxsimulator
from pylab import *
# from dotenv import load_dotenv, find_dotenv

width = 50 # Size of horizontal length
height = 50 # Size of vertical length
initProb = 0.01 # Probability of starting infected with parasite
infectionRate = 0.85 # Probability of getting infected
regrowthRate = 0.15 # Probability of regrowing in cellular
deathProb = 0.5 # Probability of dying after contracting the parasite
cureProb = 0.3 # Probability of the parasite die
neighnourhood_selected = "Moore"
plotCA = 1
plotPhase = 1

def initialize():
    global time, config, nextConfig, clean, healthy, infected
    time = 0

    # Generate Initial Conditions based on configurations
    config = zeros([height, width])  # State 0: Blue

    for x in range(width):
        for y in range(height):
            if random() < initProb:
                cell_state = 2  # State 2: Red
            else:
                cell_state = 1  # State 1: Green
            config[x, y] = cell_state

    nextConfig = zeros([height, width])

    # Number of clean, healthy and infectd
    clean = np.array([np.count_nonzero(config == 0)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 2)])

def observe():
    cla()

    if plotCA:
        figure(plotCA)
        imshow(config, vmin=0, vmax=2, cmap=cm.jet)
        axis('image')
        title('t = ' + str(time))

    if plotPhase:
        figure(plotCA + plotPhase)
        plot(np.arange(time + 1), clean)
        plot(np.arange(time + 1), healthy)
        plot(np.arange(time + 1), infected)
        xlabel('Time')
        ylabel('Number of Cells')
        legend(('Clean', 'Healthy', 'Infected'))
        title('t = ' + str(time))

def update():
    global time, config, nextConfig, state, clean, healthy, infected
    neighbours = neighbourhood(neighnourhood_selected)
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[x, y]
            # if state == 0:
            #     for dx in range(-1, 2):
            #         for dy in range(-1, 2):
            #             if config[(x + dx) % width, (y + dy) % height] == 1:
            #                 if random() < regrowthRate:
            #                     state = 1
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
                elif deathProb < p < (min(deathProb+cureProb, 1)):
                    state = 1  # Cured
                else:
                    state = 2

            nextConfig[x, y] = state

    config, nextConfig = nextConfig, config

    # Change state of stored values
    ## Clean - State 0
    number_cleaned_cells = np.count_nonzero(config == 0)
    clean = np.append(clean, number_cleaned_cells)

    ## Healthy - State 1
    number_healthy_cells = np.count_nonzero(config == 1)
    healthy = np.append(healthy, number_healthy_cells)

    ## Infected - State 2
    number_infected_cells = np.count_nonzero(config == 2)
    infected = np.append(infected, number_infected_cells)

    print(f'===== Iteration: {time} =====')
    print(f'Number of Clean: {number_cleaned_cells}')
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
    # load_dotenv(find_dotenv())  # take environment variables from .env
    # config = dotenv_values(".env")
    # print(os.getenv('WIDTH'))
