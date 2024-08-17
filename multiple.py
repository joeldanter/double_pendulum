from double_pendulum import DoublePendulum
from world import World
from matplotlib import colors, colormaps
from pygame.math import Vector2
import numpy as np


m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
n=50
pendulums=[]
for i in range(n):
    angle1, angle2=np.pi*4/6, np.pi*5/6 + i/1000000
    ang_vel1, ang_vel2=0, 0
    cmap = colormaps['autumn']
    rgb = cmap(i/n)[:3]
    color= colors.to_hex(rgb)
    pendulum=DoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
    pendulums.append(pendulum)
world = World(pendulums, (800,600), Vector2(400,300), 140, 0.002, 1)
world.start()
