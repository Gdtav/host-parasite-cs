import pycxsimulator
from pylab import *

width = 50
height = 50
initProb = 0.01
infectionRate = 0.85
regrowthRate = 0.15
deathProb = 0.5
cureProb = 0.3


def initialize():
    global time, config, nextConfig

    time = 0

    config = zeros([height, width])  # State 0: Blue
    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = 2  # State 2: Red
            else:
                state = 1  # State 1: Green
            config[x, y] = state

    nextConfig = zeros([height, width])


def observe():
    cla()
    imshow(config, vmin=0, vmax=2, cmap=cm.jet)
    axis('image')
    title('t = ' + str(time))


def update():
    global time, config, nextConfig, state
    neighbours = neighbourhood("Moore")
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
