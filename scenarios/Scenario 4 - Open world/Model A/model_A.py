import pycxsimulator
from pylab import *

# This parasites when leave the body die and infects another

width = 100  # Size of horizontal length
height = 100  # Size of vertical length
hostProb = 0.1  # Probability of the cell being occupied by a healthy host
infectedProb = 0.03  # Probability of cell being occupied by a host with parasite

infectionRate = 0.85  # Probability of getting infected with an parasite
regrowthRate = 0.15  # Probability of regrowing in cellular
deathProb = 0.01  # Probability of dying after contracting the parasite
cureProb = 0.01  # Probability of the parasite die

neighbourhood_selected = "Moore"
plotCA = 1
plotPhase = 1

simulator = pycxsimulator.GUI()

def initialize():
    global time, config, nextConfig, empty, healthy, infected
    time = 0

    # Generate Initial Conditions based on configurations
    config = np.full((width, height), 10) # State 10: yellow

    for x in range(width):
        for y in range(height):
            p = random()
            if p < infectedProb:
                cell_state = 5  # State 5: Red
            elif infectedProb < p < (min(infectedProb + hostProb, 1)):
                cell_state = 1  # State 1: Green
            else:
                cell_state = 10  # State 10: yellow
            config[x, y] = cell_state

    nextConfig = np.full((width, height), 10)

    # Number of clean, healthy and infected
    empty = np.array([np.count_nonzero(config == 10)])
    healthy = np.array([np.count_nonzero(config == 1)])
    infected = np.array([np.count_nonzero(config == 5)])

def observe():
    cla()

    if plotCA:
        figure(plotCA)
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
        xlabel('Time')
        ylabel('Number of Cells')
        #legend(('Empty', 'Healthy', 'Infected'))
        legend(('Healthy', 'Infected'))
        title('t = ' + str(time))

def update():
    global time, config, nextConfig, state, empty, healthy, infected
    neighbours = neighbourhood1(neighbourhood_selected)
    time += 1

    for x in range(width):
        for y in range(height):
            state = config[x, y]
            neigh_list = neighbours(x, y)
            shuffle(neigh_list)
            if state == 10 and nextConfig[x, y] == 10:  # empty
                #print(f'Checking [{x} {y}]: that is empty')
                if random() < regrowthRate:
                    #print(f'[{x} {y}]: Regrowth healthy host')
                    state = 1
                else:
                    #print(f'[{x} {y}]: Does not regrowth healthy host')
                    state = 10

            elif state == 1:  # healthy
                #print(f'Checking [{x} {y}]: that is healthy')
                for neighbour in neigh_list:
                    if config[neighbour[0], neighbour[1]] == 5:  # if neighbour infected
                        if random() < infectionRate: # host becomes infected
                            state = 5  # this cell becomes infected too
                            nextConfig[neighbour[0], neighbour[1]] = 10  # other host die
                        break
                else:
                    for neighbour in neigh_list:
                        if config[neighbour[0], neighbour[1]] == 10 and nextConfig[neighbour[0], neighbour[1]] == 10:
                            nextConfig[neighbour[0], neighbour[1]] = 1  # healthy moves to a empty cell
                            state = 10  # will move so this cell will be empty
                            #print(f'[{x} {y}]: will be empty as healthy host moved')
                            #print(f'\t[{neighbour[0]} {neighbour[1]}]: Will be healthy host that just moved')
                            break
                    else:
                        #print(f'[{x} {y}]: Will remain a healthy host that did not moved')
                        state = 1  # does not move

            elif state == 5:
                p = random()
                if p < deathProb:
                    state = 10  # Death to both
                elif deathProb < p < (min(deathProb + cureProb, 1)):
                    state = 1 # parasite dies
                else:
                    for neighbour in neigh_list:
                        if config[neighbour[0], neighbour[1]] == 10 and nextConfig[neighbour[0], neighbour[1]] == 10:
                            nextConfig[neighbour[0], neighbour[1]] = 5  # healthy moves to a empty cell
                            state = 10  # will move so this cell will be empty
                            break
                    else:
                        state = 5  # infected does not move
            elif state != nextConfig[x, y]:  # empty
                state = nextConfig[x, y]

            nextConfig[x, y] = state
            # #print(nextConfig)

    config[:] = nextConfig
    nextConfig[:] = config[:]

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

    if number_infected_cells == 0:
        simulator.runEvent()
        #print("No more infected, victory!")
        input("Press enter to reset the simulation")
        simulator.resetModel()

    #print(f'===== Iteration: {time} =====')
    #print(f'Number of Empty: {number_empty_cells}')
    #print(f'Number of Healthy: {number_healthy_cells}')
    #print(f'Number of Infected: {number_infected_cells}\n')


def neighbourhood(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # #print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    neigh_list.append([min(max(0, x+dx), width -1), min(max(0, y+dy), height -1)])
                    # #print(f'Neighbour: {min(max(0, x+dx), width -1)} {min(max(0, y+dy), height -1)}')
        elif (type == "Von Neumann"):
            neigh_list.append([(x + 1) % width, (y) % height])
            neigh_list.append([(x - 1) % width, (y) % height])
            neigh_list.append([(x) % width, (y + 1) % height])
            neigh_list.append([(x) % width, (y - 1) % height])

        return neigh_list

    return neighbourhood


def neighbourhood1(type):
    def neighbourhood(x, y):

        neigh_list = list()
        # #print(f'Point: {x} {y}')
        if (type == "Moore"):
            for dx in range(-2, 3):
                for dy in range(-2, 3):
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
