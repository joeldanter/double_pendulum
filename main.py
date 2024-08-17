from double_pendulum import TrackedDoublePendulum
from world import World
from plotting import plot_phase_space
from matplotlib import colors, colormaps
import random
from pygame.math import Vector2
import numpy as np


# lehet az itteni dolgok módosításával szórakozni
# nem tettem bele fügvénybe mert 1000 dolgot lehetne megadni

m1, m2, l1, l2 = 1, 1, 1, 1
g=9.81
n=10
fix_E=True
pendulums=[]
for i in range(n):
    # randomizált értékek ha kellenének
    #angle1, angle2=(random.random()-0.5)*2*np.pi, (random.random()-0.5)*2*np.pi
    #ang_vel1, ang_vel2=(random.random()-0.5)*2*np.pi, (random.random()-0.5)*2*np.pi
    angle1, angle2=i*0.15, -i*0.15
    ang_vel1, ang_vel2=0,0        
    
    cmap = colormaps['ocean'] # viridis, autumn
    rgb = cmap(i/n)[:3]
    color= colors.to_hex(rgb)
    
    pendulum=TrackedDoublePendulum(m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, color, g)
    if fix_E:
        pendulum.set_ups_e(1/4*np.pi, target_E=-10, adjust_Ep=True, Eptol=0.001)
    pendulums.append(pendulum)

world = World(pendulums, screen_size=(800,600), screen_origin=Vector2(400,300), scale=140, dt=0.002, targeted_sim_speed=100)
world.start()

if fix_E:
    plot_phase_space(pendulums, False)
