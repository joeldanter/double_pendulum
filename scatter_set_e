from DoublePendulum import *
from World import *
from plotting import *
from matplotlib import colors, colormaps
import random


m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
n=10
E=-29
pendulums=[]
for i in range(n):
    angle1, angle2=(random.random()-0.5)*2*np.pi, (random.random()-0.5)*2*np.pi
    ang_vel1, ang_vel2=(random.random()-0.5)*2*np.pi, (random.random()-0.5)*2*np.pi
    cmap = colormaps['ocean']
    rgb = cmap(i/n)[:3]
    color= colors.to_hex(rgb)
    pendulum=TrackedDoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
    pendulum.set_ups_e(random.random()*2*np.pi, E, adjust_Ep=True, Eptol=1)
    pendulums.append(pendulum)
world = World(pendulums, (800,600), pygame.math.Vector2(400,300), 140, 0.002, 100)
world.start()

plot_phase_space(pendulums, False)
