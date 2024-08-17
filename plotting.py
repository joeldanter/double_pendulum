import matplotlib.pyplot as plt
from double_pendulum import DoublePendulum
import numpy as np


def plot_phase_space(pendulums, transverses=True):
    # Ellenőrzés hogy az ingák energiái megegyeznek-e
    Es=[pendulum.get_energy() for pendulum in pendulums]
    maxdE=np.abs(min(Es)-max(Es))
    if maxdE>0.001:
        print('Energies not matching:', ', '.join(Es))

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    for pendulum in pendulums:
        x = pendulum.old_angle1s
        y = pendulum.old_angle2s
        # ha transverses=True, a szögek felvehetnek a (-pi,pi) intervallumon
        # kívül is értéket, különben kivon/hozzáad annyiszor 2pi-t, hogy
        # ebben az intervallumban legyen
        if transverses==False:
            for i in range(len(x)):
                x[i]=(x[i]+np.pi)%(2*np.pi)-np.pi
                y[i]=(y[i]+np.pi)%(2*np.pi)-np.pi
        
        us = [calc_upsilon(pendulum.old_ang_vel1s[i], pendulum.old_ang_vel2s[i]) for i in range(len(x))]

        # Hogyha upsilon pl 2pi nél növekszik akkor visszaugrik 0-ra,
        # de az a két pont között nem húzhatunk vonalat. ha transverses=True
        # a szögeknél is felmerül ez a probléma, ezt kerüli el azzal,
        # hogy részenként köti össze a pontokat vonalakkal.
        lasti=0
        for i in range(1, len(x)):
            if np.abs(int(x[i]-x[i-1]))==6 or np.abs(int(y[i]-y[i-1]))==6 or np.abs(int(us[i]-us[i-1]))==6:
                ax.plot3D(x[lasti:i], y[lasti:i], us[lasti:i], color=pendulum.trace_color)
                lasti=i
        ax.plot3D(x[lasti:-1], y[lasti:-1], us[lasti:-1], color=pendulum.trace_color)

        # vég- és kezdő pontok
        ax.scatter(x[0], y[0], us[0], color='red')
        ax.scatter(x[-1], y[-1], us[-1], color='green')
    
    ax.set_xlabel('θ1')
    ax.set_ylabel('θ2')
    ax.set_zlabel('υ')
    ax.set_zlim(0, 2*np.pi)
    ax.view_init(elev=90, azim=-90, roll=0)
    fig.canvas.manager.set_window_title(f'E≈{sum(Es)/len(Es)}, maxdE={maxdE}')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()

# upsilon képletének implementálása
def calc_upsilon(ang_vel1, ang_vel2):
    if ang_vel1==0:
        if ang_vel2>0:
            upsilon=0
        elif ang_vel2<0:
            upsilon=np.pi
        else:
            upsilon=0 # TODO fix this
    else:
        upsilon=np.arctan(-ang_vel2/ang_vel1)+np.pi/2
        if ang_vel1<0:
            upsilon+=np.pi
        return upsilon

def vector_field(pendulum, min_x=-np.pi, max_x=np.pi, n_x=10, min_y=-np.pi, max_y=np.pi, n_y=10, min_z=0, max_z=2*np.pi, n_z=10, length=1):
    # ebben a függvényben egy elég összetett problémába ütözünk ha n_x!=n_y!=n_z    
    E=pendulum.get_energy()
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    x = np.linspace(min_x, max_x, n_x)
    y = np.linspace(min_y, max_y, n_y)
    z = np.linspace(min_z, max_z, n_z)
    X,Y,Z=[],[],[]
    u,v,w=[],[],[]
    for i in range(n_x):
        for j in range(n_y):
            for k in range(n_z):
                # a vektorokat miután kiszámítjuk, megnyújtjuk annyira hogy egy fix hossza legyem
                # viszont ha n_x!=n_y!=n_z, akkor a fix hossz vizuálisan nem lesz fix
                # itt vizuálisan fixáljuk, de így meg a nyíl hegye helyenként nagyobb/kisebb lesz,
                # mert a nyíl hegyének mérete a vektor hosszából van kiszámítva, ami független a
                # vizualizációval. Ezért kissé csunya az egész :(
                # https://github.com/matplotlib/matplotlib/issues/11746
                dir=vector(pendulum, x[i], y[j], z[k], E)
                visual_dir=dir/np.array([max_x-min_x, max_y-min_y, max_z-min_z])
                mag=np.sqrt(visual_dir.dot(visual_dir))
                dir=length*(dir/mag)
                
                X.append(x[i])
                Y.append(y[j])
                Z.append(z[k])
                u.append(dir[0])
                v.append(dir[1])
                w.append(dir[2])

    ax.quiver(X, Y, Z, u, v, w)
    plt.show()

def vector(pendulum, angle1, angle2, upsilon, energy):
    pendulum.angle1=angle1
    pendulum.angle2=angle2
    # kiszámoltatjuk a szögsebességeket
    try:
        pendulum.set_ups_e(upsilon, energy, adjust_Ep=False, Eptol=0)
    except:
        return np.array([float('NaN'), float('NaN'), float('NaN')])
    
    u=pendulum.ang_vel1
    v=pendulum.ang_vel2
    
    ang_acc1, ang_acc2=pendulum.get_accel_with_params(pendulum.angle1, pendulum.angle2, pendulum.ang_vel1, pendulum.ang_vel2)
    w=(pendulum.ang_vel2*ang_acc1-pendulum.ang_vel1*ang_acc2)/(pendulum.ang_vel1**2+pendulum.ang_vel2**2)
    
    return np.array([u,v,w])
