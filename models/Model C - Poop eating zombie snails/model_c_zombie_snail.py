import os

import numpy as np

import pycxsimulator
from random import *
from pylab import *

# from dotenv import load_dotenv, find_dotenv

width = 100  # Size of horizontal length
height = 100  # Size of vertical length
hostProb = 0.01  # Probability of the cell being occupied by a healthy host
infectedProb = 0.003  # Probability of cell being occupied by a host with parasite
infectedPoopProb = 0.003  # Probability of a cell being occupied with a poop

infectionRate = 0.85  # Probability of getting infected with an parasite upon contact with it

regrowthRate = 0.005  # Probability of regrowing in cellular
deathProb = 0.01  # Probability of dying immediately (next iteration) after contracting the parasite
cureProb = 0.01  # Probability of the parasite die

neighbourhood_selected = "Von Neumann"
plotCA = 1
plotPhase = 1

simulator = pycxsimulator.GUI()


def initialize():
    global time, config, nextConfig, empty, healthy, infected, poop
    time = 0

    # Generate Initial Conditions based on configurations
    config = np.full((width, height), 10)  # State 10: yellow

    for x in range(width):
        for y in range(height):
            p = random()
            if p < infectedProb:
                cell_state = 5  # State 5: Red
            elif infectedProb < p < (min(infectedProb + hostProb, 1 - infectedPoopProb)):
                cell_state = 1  # State 1: Blue
            elif infectedProb + hostProb < p < (min(infectedProb + hostProb + infectedPoopProb, 1)):
                cell_state = 4  # State 4: Poop
            else:
                cell_state = 10

            config[x, y] = cell_state

    nextConfig = np.full((width, height), 10)

    # Number of clean, healthy and infected
    empty = np.array([np.count_nonzero(config == 10)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 5)])
    poop = np.array([np.count_nonzero(config == 4)])

    print(f'===== Iteration: {time} =====')
    print(f'Number of Empty: {empty}')
    print(f'Number of Healthy: {healthy}')
    print(f'Number of Infected: {infected}')
    print(f'Number of Poops: {poop}\n')


def observe():
    cla()

    if plotCA:
        figure(plotCA)
        imshow(config, vmin=0, vmax=12, cmap=cm.Paired)
        axis('image')
        title('t = ' + str(time))
        imsave(str(time) + ".png", config, vmin=0, vmax=12, cmap=cm.Paired)

    if plotPhase:
        figure(plotCA + plotPhase)
        # plot(np.arange(time + 1), empty)
        plot(np.arange(time + 1), healthy)
        plot(np.arange(time + 1), infected)
        plot(np.arange(time + 1), poop)
        xlabel('Time')
        ylabel('Number of Cells')
        # legend(('Empty', 'Healthy', 'Infected', 'Poop with Parasite'))
        legend(('Healthy', 'Infected', 'Poop with Parasite'))
        title('t = ' + str(time))


def update():
    global time, config, nextConfig, state, empty, healthy, infected, poop
    neighbours = neighbourhood(neighbourhood_selected)
    time += 1
    number_deaths = 0

    for x in range(width):
        for y in range(height):
            # print(f'---------')
            state = config[x, y]
            ##print(f'[{x} {y}] is {config[x, y]}')
            ##print(f'[{x} {y}] will be {nextConfig[x, y]}')

            if state == 10 and nextConfig[x, y] != 10:
                # print(f'[{x} {y}] is now {state} but will be {nextConfig[x, y]}')
                state = nextConfig[x, y]
            elif state == 10 and nextConfig[x, y] == 10:
                if random() < regrowthRate:
                    # print(f'[{x} {y}]: Regrowth healthy host')
                    state = 1
                else:
                    # print(f'[{x} {y}]: Does not regrowth healthy host')
                    state = 10

            elif state == 1:  # healthy host
                # print(f'[{x} {y}] is equal {state}')
                neigh_list = neighbours(x, y)
                shuffle(neigh_list)
                for neighbour in neigh_list:
                    if config[neighbour[0], neighbour[1]] == 4 and nextConfig[
                        neighbour[0], neighbour[1]] == 4:  # poop in vicinity and no snail ate it
                        # print("Poop in vicinity")
                        state = 10  # snail will move so this cell will be empty
                        if random() < infectionRate:
                            nextConfig[neighbour[0], neighbour[1]] = 5  # poop is eaten and snail is infected
                            # print(f'[{neighbour[0]} {neighbour[1]}]: will be a infected snail cell')
                        else:
                            nextConfig[neighbour[0], neighbour[1]] = 1  # poop is eaten and snail is NOT infected
                            # print(f'[{neighbour[0]} {neighbour[1]}]: will be a healthy snail cell')
                        break
                else:
                    # no poop in vicinity
                    shuffle(neigh_list)
                    ##print(f'[{x} {y}] has a snail')
                    ##print(neigh_list)
                    for neighbour in neigh_list:
                        if config[neighbour[0], neighbour[1]] == 10 and nextConfig[neighbour[0], neighbour[1]] == 10:
                            # empty cell now and next round
                            # print(f'[{neighbour[0]} {neighbour[1]}] atualmente esta em {config[neighbour[0], neighbour[1]]}')
                            nextConfig[neighbour[0], neighbour[1]] = 1  # healthy snail moves to a empty cell
                            # print(f'[{neighbour[0]} {neighbour[1]}] agora que atualizei no futuro, esta em {config[neighbour[0], neighbour[1]]}')

                            ##print(f'[{x} {y}] agora esta {config[neighbour[0], neighbour[1]]}')
                            # print(f'Snail moved from [{x} {y}] to [{neighbour[0]} {neighbour[1]}]\n fazendo break')

                            # config[neighbour[0], neighbour[1]] = 1  # this cell has a snail now
                            state = 10  # snail will move so this cell will be empty
                            ##print(f'[{neighbour[0]} {neighbour[1]}]: will be a healthy snail cell')
                            break
                    else:
                        # print(f'[{x} {y}]: will remain a healthy snail cell')
                        state = 1  # snail does not move

            elif state == 5:
                if random() < deathProb:
                    state = 10  # is now empty as it was eaten by a bird
                    # print(f'[{x} {y}]: Eaten by a bird')
                    i = randint(1, 10)
                    while i > 0:
                        # Poop appears randomly in cell
                        x_ = randint(0, width)
                        y_ = randint(0, height)
                        tries = 0
                        while nextConfig[x_, y_] != 10:  # needs to be a place empty next round
                            x_ = randint(0, width)
                            y_ = randint(0, height)
                            tries = tries + 1
                            if tries > 200:
                                x_ = x
                                y_ = y
                                state = 4
                                break
                        nextConfig[x_, y_] = 4  # poop in this cell
                        i -= 1
                    # print(f'[{x_} {y_}]: Will be infected poop')
                else:  # move infected snail randomly in neighbourhood
                    neigh_list = neighbours(x, y)
                    shuffle(neigh_list)
                    for neighbour in neigh_list:
                        if nextConfig[neighbour[0], neighbour[1]] == 10:  # move to empty cell
                            nextConfig[neighbour[0], neighbour[1]] = 5  # will be a infected snail
                            # print(f'[{neighbour[0]} {neighbour[1]}]: Will be infected snail')
                            # print(f'[{x} {y}]: Will be empty')
                            state = 10
                            break
                    else:
                        state = 5  # does not move
                        # print(f'[{x} {y}]: Will remain infected snail')

            if state != 10:
                nextConfig[x, y] = state

            if nextConfig[x, y] == 10:
                variableString = "empty"
            elif nextConfig[x, y] == 1:
                variableString = "healthy snail"
            elif nextConfig[x, y] == 5:
                variableString = "infected snail"
            else:
                variableString = "poop"
            ##print(f'[{x} {y}]: will be a {variableString} cell')
            # print(f'§---------§')

    # print("Update board")
    config[:] = nextConfig
    nextConfig[:] = np.full((width, height), 10)

    # Change state of stored values
    ## Empty - State 0
    number_empty_cells = np.count_nonzero(config == 10)
    empty = np.append(empty, number_empty_cells)

    ## Healthy - State 1
    number_healthy_cells = np.count_nonzero(config == 1)
    healthy = np.append(healthy, number_healthy_cells)

    ## Infected - State 2
    number_infected_cells = np.count_nonzero(config == 5)
    infected = np.append(infected, number_infected_cells)

    ## Poop - State 4
    number_poop_cells = np.count_nonzero(config == 4)
    poop = np.append(poop, number_poop_cells)

    if number_infected_cells == 0 and number_poop_cells == 0:
        simulator.runEvent()
        simulator.drawModel()
        # print("No more infected, victory!")
        input("Press enter to reset the simulation")
        # simulator.resetModel()

    # print(f'===== Iteration: {time} =====')
    # print(f'Number of Empty: {number_empty_cells}')
    # print(f'Number of Healthy: {number_healthy_cells}')
    # print(f'Number of Infected: {number_infected_cells}')
    # print(f'Number of Poops: {number_poop_cells}\n')


def neighbourhood(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # #print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([min(max(0, x + dx), width - 1), min(max(0, y + dy), height - 1)])
                    # #print(f'Neighbour: {min(max(0, x+dx), width -1)} {min(max(0, y+dy), height -1)}')
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])

        # print()
        return neigh_list

    return neighbourhood


def neighbourhood1(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # #print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([(x + dx) % width, (y + dy) % height])
                    # #print(f'Neighbour: {(x + dx) % width} {(y + dy) % height}')
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])

        return neigh_list

    return neighbourhood


if __name__ == '__main__':
    simulator.start(func=[initialize, observe, update])
