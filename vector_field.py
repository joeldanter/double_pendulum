from double_pendulum import *
from plotting import *
import numpy as np


pendulum=DoublePendulum(1,1,1,1,1,1,1,1,'blue',9.81)
pendulum.set_ups_e(0, -29, adjust_Ep=True, Eptol=1)
vector_field(pendulum, min_x=-0.2, max_x=0.2, n_x=10, min_y=-0.3, max_y=0.3, n_y=15, min_z=0, max_z=2*np.pi-(1e-8), n_z=15, length=.08)
