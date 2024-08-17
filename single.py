from double_pendulum import TrackedDoublePendulum
from world import World
from plotting import plot_phase_space
import numpy as np
from pygame.math import Vector2


m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
angle1, angle2=np.pi*1/6, np.pi*0/6
ang_vel1, ang_vel2=2, 2
color= 'red'
pendulum=TrackedDoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
world = World([pendulum], (800,600), Vector2(400,300), 140, 0.002, 1)
world.start()

plot_phase_space([pendulum])
