import os

import numpy as np

import pycxsimulator
from random import *
from pylab import *
# from dotenv import load_dotenv, find_dotenv

width = 10  # Size of horizontal length
height = 10  # Size of vertical length
hostProb = 0.30  # Probability of the cell being occupied by a healthy host
infectedProb = 0.30  # Probability of cell being occupied by a host with parasite
infectedPoopProb = 0.30  # Probability of a cell being occupied with a poop

infectionRate = 1  # Probability of getting infected with an parasite upon contact with it

regrowthRate = 0  # Probability of regrowing in cellular
deathProb = 0.1  # Probability of dying immediately (next iteration) after contracting the parasite
cureProb = 0  # Probability of the parasite die

neighbourhood_selected = "Moore"
plotCA = 1
plotPhase = 1

simulator = pycxsimulator.GUI()

def initialize():
    global time, config, recently_infected, nextConfig, empty, healthy, infected, poop
    time = 0

    # Generate Initial Conditions based on configurations
    config = zeros([height, width])  # State 0: Blue
    recently_infected = zeros([height, width])

    for x in range(width):
        for y in range(height):
            p = random()
            if p < infectedProb:
                cell_state = 2  # State 2: Red
            elif infectedProb < p < (min(infectedProb + hostProb, 1 - infectedPoopProb)):
                cell_state = 1  # State 1: Green
            elif infectedProb + hostProb < p < (min(infectedProb + hostProb + infectedPoopProb, 1)):
                cell_state = 3  # State 3: Poop
            else:
                continue # cell state remains zero (empty)
            config[x, y] = cell_state

    nextConfig = zeros([height, width])

    # Number of clean, healthy and infected
    empty = np.array([np.count_nonzero(config == 0)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 2)])
    poop = np.array([np.count_nonzero(config == 3)])

def observe():
    cla()

    if plotCA:
        figure(plotCA)
        imshow(config, vmin=0, vmax=2, cmap=cm.rainbow)
        axis('image')
        title('t = ' + str(time))
        imsave(str(time) + ".png", config, vmin=0, vmax=2, cmap=cm.gist_earth)

    if plotPhase:
        figure(plotCA + plotPhase)
        plot(np.arange(time + 1), empty)
        plot(np.arange(time + 1), healthy)
        plot(np.arange(time + 1), infected)
        plot(np.arange(time + 1), poop)
        xlabel('Time')
        ylabel('Number of Cells')
        legend(('Empty', 'Healthy', 'Infected', 'Poop with Parasite'))
        title('t = ' + str(time))

def update():
    global time, config, nextConfig, state, empty, healthy, infected, poop
    neighbours = neighbourhood(neighbourhood_selected)
    time += 1
    number_deaths = 0

    for x in range(width):
        for y in range(height):
            state = config[x, y]
            if state == 1:  # healthy host
                neigh_list = neighbours(x, y)
                shuffle(neigh_list)
                for neighbour in neigh_list:
                    if config[neighbour[0], neighbour[1]] == 3:  # poop in vicinity
                        state = 0  # snail will move
                        config[neighbour[0], neighbour[1]] = 0
                        if random() < infectionRate:
                            nextConfig[neighbour[0], neighbour[1]] = 2  # poop is eaten and snail is infected
                        else:
                            nextConfig[neighbour[0], neighbour[1]] = 1  # poop is eaten and snail is NOT infected
                        break
                else:
                    selectedNeighbour = neigh_list[randint(0, len(neigh_list))]
                    nextConfig[selectedNeighbour[0], selectedNeighbour[1]] = 1 # snail moves to another cell
                    state = 0

            if state == 2:
                if random() < deathProb:
                    state = 0 # will be empty next round
                    # poop appears randomly in a cell 0
                    x = randint(0, width)
                    y = randint(0, height)
                    while config[x, y] != 0:
                        x = randint(0, width)
                        y = randint(0, height)
                    nextConfig[x, y] = 3 # bird ate and poop somewhere, it can poop right in another poop creating a poop tower
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

    ## Poop - State 3
    number_poop_cells = np.count_nonzero(config == 3)
    poop = np.append(poop, number_poop_cells)

    if number_infected_cells == 0:
        simulator.runEvent()
        simulator.drawModel()
        print("No more infected, victory!")
        input("Press enter to reset the simulation")
        simulator.resetModel()

    print(f'===== Iteration: {time} =====')
    print(f'Number of Empty: {number_empty_cells}')
    print(f'Number of Healthy: {number_healthy_cells}')
    print(f'Number of Infected: {number_infected_cells}')
    print(f'Number of Poops: {number_poop_cells}\n')


def neighbourhood(type):
    def neighbourhood(x, y):
        neigh_list = list()
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([(x + dx) % width, (y + dy) % height])
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])
        return neigh_list

    return neighbourhood


if __name__ == '__main__':
    simulator.start(func=[initialize, observe, update])
