import simcx
from pylab import *



class HostSimulator(simcx.simulators.Simulator):
    def __init__(self, func, init_state, Dt):


def initialize():


    time = 0

    config = zeros([height, width])
    for x in range(width):
        for y in range(height):
            if random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = zeros([height, width])


def observe():
    cla()
    imshow(config, vmin=0, vmax=2, cmap=cm.jet)
    axis('image')
    title('t = ' + str(time))


def update():
    global time, config, nextConfig

    time += 1

    for x in range(width):
        for y in range(height):
            state = config[y, x]
            if state == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % height, (x + dx) % width] == 1:
                            if random() < regrowthRate:
                                state = 1
            elif state == 1:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if config[(y + dy) % height, (x + dx) % width] == 2:
                            if random() < infectionRate:
                                state = 2
            else:
                state = 0

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config


if __name__ == '__main__':
    global time, config, nextConfig
    width = 50
    height = 50
    initProb = 0.01
    infectionRate = 0.85
    regrowthRate = 0.15

    sim = simcx.Simulator()
    vis = simcx.Visual(sim)
    display = simcx.Display()
    display.add_simulator(sim)
    display.add_visual(vis)
    simcx.run()
