import os

import numpy as np

import pycxsimulator
from random import *
from pylab import *
# from dotenv import load_dotenv, find_dotenv

width = 100  # Size of horizontal length
height = 100 # Size of vertical length
hostProb = 0.15  # Probability of the cell being occupied by a healthy host
infectedProb = 0.03  # Probability of cell being occupied by a host with parasite
infectedPoopProb = 0.001  # Probability of a cell being occupied with a poop

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
    config = zeros([width, height])
    #recently_infected = zeros([width, height])

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
                cell_state = 0

            if cell_state == 0:
                variableString = "empty"
            elif cell_state == 1:
                variableString = "healthy snail"
            elif cell_state == 2:
                variableString = "infected snail"
            else:
                variableString = "poop"
            print(f'[{x} {y}]: is  a {variableString} cell')
            config[x, y] = cell_state

    nextConfig = zeros([width, height])

    # Number of clean, healthy and infected
    empty = np.array([np.count_nonzero(config == 0)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 2)])
    poop = np.array([np.count_nonzero(config == 3)])

    print(f'===== Iteration: {time} =====')
    print(f'Number of Empty: {empty}')
    print(f'Number of Healthy: {healthy}')
    print(f'Number of Infected: {infected}')
    print(f'Number of Poops: {poop}\n')

def observe():
    cla()

    if plotCA:
        figure(plotCA)
        imshow(config, vmin=0, vmax=3, cmap=cm.rainbow)
        axis('image')
        title('t = ' + str(time))
        imsave(str(time) + ".png", config, vmin=0, vmax=3, cmap=cm.rainbow)

    if plotPhase:
        figure(plotCA + plotPhase)
        #plot(np.arange(time + 1), empty)
        plot(np.arange(time + 1), healthy)
        plot(np.arange(time + 1), infected)
        plot(np.arange(time + 1), poop)
        xlabel('Time')
        ylabel('Number of Cells')
        #legend(('Empty', 'Healthy', 'Infected', 'Poop with Parasite'))
        legend(('Healthy', 'Infected', 'Poop with Parasite'))
        title('t = ' + str(time))
#
# def update():
#     global time, config, nextConfig, state, empty, healthy, infected, poop
#     neighbours = neighbourhood(neighbourhood_selected)
#     time += 1
#     number_deaths = 0
#
#     for x in range(width):
#         for y in range(height):
#             state = config[x, y]
#
#             if state == 0: # this state is empty
#                 empty_cell_neighbour_list = neighbours(x, y)
#                 shuffle(empty_cell_neighbour_list)
#                 for empty_cell_neighbour in empty_cell_neighbour_list:
#                     if config[empty_cell_neighbour[0], empty_cell_neighbour[1]] == 1:
#                         snail_cell_neighbour_list = neighbours(empty_cell_neighbour[0], empty_cell_neighbour[1])
#                         shuffle(snail_cell_neighbour_list)
#                         for snail_cell_neighbour in snail_cell_neighbour_list:
#                             if





def update():
    global time, config, nextConfig, state, empty, healthy, infected, poop
    neighbours = neighbourhood(neighbourhood_selected)
    time += 1
    number_deaths = 0

    for x in range(width):
        for y in range(height):
            print(f'---------')
            state = config[x, y]
            #print(f'[{x} {y}] is {config[x, y]}')
            #print(f'[{x} {y}] will be {nextConfig[x, y]}')

            if state == 0 and nextConfig[x, y] != 0:
                print(f'[{x} {y}] is now {state} but will be {nextConfig[x, y]}')
                state = nextConfig[x, y]


            elif state == 1:  # healthy host
                print(f'[{x} {y}] is equal {state}')
                neigh_list = neighbours(x, y)
                shuffle(neigh_list)
                for neighbour in neigh_list:
                    if config[neighbour[0], neighbour[1]] == 3 and nextConfig[neighbour[0], neighbour[1]] == 3:  # poop in vicinity and no snail ate it
                        print("Poop in vicinity")
                        state = 0  # snail will move so this cell will be empty
                        if random() < infectionRate:
                            nextConfig[neighbour[0], neighbour[1]] = 2  # poop is eaten and snail is infected
                            print(f'[{neighbour[0]} {neighbour[1]}]: will be a infected snail cell')
                        else:
                            nextConfig[neighbour[0], neighbour[1]] = 1  # poop is eaten and snail is NOT infected
                            print(f'[{neighbour[0]} {neighbour[1]}]: will be a healthy snail cell')
                        break
                else:
                    # no poop in vicinity
                    shuffle(neigh_list)
                    #print(f'[{x} {y}] has a snail')
                    #print(neigh_list)
                    for neighbour in neigh_list:
                        if config[neighbour[0], neighbour[1]] == 0 and nextConfig[neighbour[0], neighbour[1]] == 0:
                            # empty cell now and next round
                            print(f'[{neighbour[0]} {neighbour[1]}] atualmente esta em {config[neighbour[0], neighbour[1]]}')
                            nextConfig[neighbour[0], neighbour[1]] = 1  # healthy snail moves to a empty cell
                            print(f'[{neighbour[0]} {neighbour[1]}] agora que atualizei no futuro, esta em {config[neighbour[0], neighbour[1]]}')

                            #print(f'[{x} {y}] agora esta {config[neighbour[0], neighbour[1]]}')
                            print(f'Snail moved from [{x} {y}] to [{neighbour[0]} {neighbour[1]}]\n fazendo break')

                            #config[neighbour[0], neighbour[1]] = 1  # this cell has a snail now
                            state = 0  # snail will move so this cell will be empty
                            #print(f'[{neighbour[0]} {neighbour[1]}]: will be a healthy snail cell')
                            break
                    else:
                        print(f'[{x} {y}]: will remain a healthy snail cell')
                        state = 1  # snail does not move

            elif state == 2:
                if random() < deathProb:
                    state = 0 # is now empty as it was eaten by a bird
                    print(f'[{x} {y}]: Eaten by a bird')

                    # Poop appears randomly in cell
                    x_ = randint(0, width)
                    y_ = randint(0, height)
                    tries = 0
                    while nextConfig[x_, y_] != 0:  # needs to be a place empty next round
                        x_ = randint(0, width)
                        y_ = randint(0, height)
                        tries = tries + 1
                        if tries > 200:
                            x_ = x
                            y_ = y
                            state = 3
                            break

                    nextConfig[x_, y_] = 3 # poop in this cell
                    print(f'[{x_} {y_}]: Will be infected poop')
                else:  # move infected snail randomly in neighbourhood
                    neigh_list = neighbours(x, y)
                    shuffle(neigh_list)
                    for neighbour in neigh_list:
                        if nextConfig[neighbour[0], neighbour[1]] == 0:  # move to empty cell
                            nextConfig[neighbour[0], neighbour[1]] = 2  # will be a infected snail
                            print(f'[{neighbour[0]} {neighbour[1]}]: Will be infected snail')
                            print(f'[{x} {y}]: Will be empty')
                            state = 0
                            break
                    else:
                        state = 2  # does not move
                        print(f'[{x} {y}]: Will remain infected snail')

            # elif state == 2:
            #     if random() < deathProb:
            #         config[x, y] = 0  # is now empty next round
            #         nextConfig[x, y] = 0 # will be empty next round
            #
            #         # poop appears randomly in a cell 0
            #         x_ = randint(0, width)
            #         y_ = randint(0, height)
            #         while config[x, y] != 0:
            #             x_ = randint(0, width)
            #             y_ = randint(0, height)
            #         nextConfig[x, y] = 3  # bird ate and poop somewhere, it can poop right in another poop creating a poop tower
            #         print(f'[{x} {y}]: will be a poop cell')
            #     else:
            #         neigh_list = neighbours(x, y)
            #         shuffle(neigh_list)
            #         index = randint(0, len(neigh_list))
            #         neighbour = neigh_list[index]
            #         nextConfig[neighbour[0], neighbour[1]] = 2  # move infected snail randomly
            #         state = 0  # will be empty next round
            #
            # print(f'HAS SAID [{x} {y}]: will be state {state}')
            if state != 0:
                nextConfig[x, y] = state

            if nextConfig[x, y] == 0:
                variableString = "empty"
            elif nextConfig[x, y] == 1:
                variableString = "healthy snail"
            elif nextConfig[x, y] == 2:
                variableString = "infected snail"
            else:
                variableString = "poop"
            #print(f'[{x} {y}]: will be a {variableString} cell')
            print(f'§---------§')

    print("Update board")
    config[:] = nextConfig
    nextConfig[:] = zeros([width, height])

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
        pass
        #simulator.runEvent()
        #simulator.drawModel()
        #print("No more infected, victory!")
        #input("Press enter to reset the simulation")
        #simulator.resetModel()

    print(f'===== Iteration: {time} =====')
    print(f'Number of Empty: {number_empty_cells}')
    print(f'Number of Healthy: {number_healthy_cells}')
    print(f'Number of Infected: {number_infected_cells}')
    print(f'Number of Poops: {number_poop_cells}\n')

def neighbourhood(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([min(max(0, x+dx), width -1), min(max(0, y+dy), height -1)])
                    # print(f'Neighbour: {min(max(0, x+dx), width -1)} {min(max(0, y+dy), height -1)}')
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])

        print()
        return neigh_list

    return neighbourhood


def neighbourhood1(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([(x + dx) % width, (y + dy) % height])
                    # print(f'Neighbour: {(x + dx) % width} {(y + dy) % height}')
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])

        return neigh_list

    return neighbourhood


if __name__ == '__main__':
    simulator.start(func=[initialize, observe, update])
