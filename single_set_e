from DoublePendulum import *
from World import *
from plotting import *


m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
E=-29
angle1, angle2=0, 0
ang_vel1, ang_vel2=0, 0
color= 'blue'
pendulum=TrackedDoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
pendulum.set_ups_e(3/8*np.pi, E, adjust_Ep=True, Eptol=1)
world = World([pendulum], (800,600), pygame.math.Vector2(400,300), 140, 0.002, 100)
world.start()

plot_phase_space([pendulum])
