import numpy as np
import matplotlib.pyplot as plt
from double_pendulum import DoublePendulum


'''
Ez a dupla inga jacobi-mátrixának eigenértékeinek valós részeinek
maximális értékeit rajzolja ki a szögek függvényében, ha a
szögsebességek értékei 0>
'''

def value(pendulum, angle1, angle2, ang_vel1, ang_vel2):
    pendulum.angle1=angle1
    pendulum.angle2=angle2
    pendulum.ang_vel1=ang_vel1
    pendulum.ang_vel2=ang_vel2
    return max(pendulum.real_eig_values())

n_x, n_y= 100, 100
min_x, max_x= -np.pi, np.pi
min_y, max_y= -np.pi, np.pi

pendulum=DoublePendulum(1,1,1,1, 0, 0, 0, 0, (0,0,0), 9.81)
x = np.linspace(min_x, max_x, n_x)
y = np.linspace(min_y, max_y, n_y)
z = np.array([value(pendulum, i, j, 0, 0) for j in y for i in x])

X, Y = np.meshgrid(x, y)
Z = z.reshape(n_x, n_y)

im=plt.imshow(Z, cmap='viridis', extent=[min_x, max_x, max_y, min_y], aspect=(max_x-min_x)/(max_y-min_y), origin='upper')
plt.xlabel('θ1')
plt.ylabel('θ2')
plt.colorbar(im)
plt.show()
