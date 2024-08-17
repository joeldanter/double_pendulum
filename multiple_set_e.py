from double_pendulum import *
from world import *
from plotting import *
import numpy as np
from matplotlib import colors, colormaps


n=5
E=-29
m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
pendulums=[]
for i in range(n):
    angle1, angle2=i*0.0375, -i*0.0375
    ang_vel1, ang_vel2=0,0
    cmap = colormaps['viridis']
    rgb = cmap(i/n)[:3]
    color= colors.to_hex(rgb)
    pendulum=TrackedDoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
    pendulum.set_ups_e(np.pi/4, E, adjust_Ep=True, Eptol=0.001)
    pendulums.append(pendulum)
world = World(pendulums, (800,600), pygame.math.Vector2(400,300), 140, 0.003, 100)
world.start()

plot_phase_space(pendulums)
