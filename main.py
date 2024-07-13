import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pygame
import threading


class DoublePendulum:
    def __init__(self, m1, m2, l1, l2, angles, angular_velocities, trace_color, g, subspace_crossed):
        self.m1=m1 # első súly tömege
        self.m2=m2 # második súly tömege
        self.l1=l1 # első inga hossza
        self.l2=l2 # második inga hossza
        self.angles=angles # pygame.math.Vector2, szögeket tárolja
        self.angular_velocities=angular_velocities # pygame.math.Vector2, szögek sebességeit tárolja
        self.trace_color=trace_color # szine az ingának és a húzott vonalának
        self.g=g
        self.subspace_crossed_callback=subspace_crossed
        self.refresh()

    # egy dt idő eltelése alatt számítja ki és frissíti az új szögekek és szögsebességeket
    def tick(self, dt):
        #prev_angles=pygame.math.Vector2(self.angles)
        #prev_angular_avelocities=pygame.math.Vector2(self.angular_velocities)

        # RK4 for 2nd order ODE
        k1=dt*self.angular_velocities
        l1=dt*self.get_accel(self.angles,self.angular_velocities)
        k2=dt*(self.angular_velocities+l1/2)
        l2=dt*self.get_accel(self.angles+k1/2,self.angular_velocities+l1/2)
        k3=dt*(self.angular_velocities+l2/2)
        l3=dt*self.get_accel(self.angles+k2/2,self.angular_velocities+l2/2)
        k4=dt*(self.angular_velocities+l3)
        l4=dt*self.get_accel(self.angles+k3, self.angular_velocities+l3)
        
        self.angles+=(k1+2*k2+2*k3+k4)/6
        self.angular_velocities+=(l1+2*l2+2*l3+l4)/6

        self.refresh()
        Ek=self.get_kinetic_energy()
        if self.get_kinetic_energy()<0.01:
            print(Ek)
        #is_on_right=self.angles.x%(np.pi*2)<np.pi
        #was_on_right=prev_angles.x%(np.pi*2)<np.pi
        #if (is_on_right and not was_on_right and self.angular_velocities.x>0) or (not is_on_right and was_on_right and self.angular_velocities.x<0):
        self.subspace_crossed_callback(self) # TODO pontos szogekkel es szogsebessegekkel

    # paraméterben megadott szögeknél és szögsebességeknel számítja ki a szöggyorsulásokat
    # runge kutta 4-hez kell
    def get_accel(self, angles, angular_velocities):
        a1=(self.m1+self.m2)*self.l1**2
        b1=self.m2*self.l1*self.l2*np.cos(angles.x-angles.y)
        c1=-(self.m1+self.m2)*self.g*self.l1*np.sin(angles.x)-self.m2*self.l1*self.l2*angular_velocities.y**2*np.sin(angles.x-angles.y)

        a2=self.m2*self.l1*self.l2*np.cos(angles.x-angles.y)
        b2=self.m2*self.l2**2
        c2=self.m2*self.l1*self.l2*angular_velocities.x**2*np.sin(angles.x-angles.y)-self.m2*self.g*self.l2*np.sin(angles.y)
    
        angular_accel1=(b2*c1-b1*c2)/(a1*b2-a2*b1)
        angular_accel2=(a2*c1-a1*c2)/(a2*b1-a1*b2)
        return pygame.math.Vector2(angular_accel1, angular_accel2)

    # kiszámítja az inga koordinátáit és energiáját és elmenti, hogy ne kelljen mindig kiszámolni
    def refresh(self):
        x=np.sin(self.angles.x)*self.l1
        y=-np.cos(self.angles.x)*self.l1
        self.pos1=pygame.math.Vector2(x,y)
        x=np.sin(self.angles.y)*self.l2
        y=-np.cos(self.angles.y)*self.l2
        self.pos2=pygame.math.Vector2(x,y)+self.pos1
        self.energy=self.get_potential_energy()+self.get_kinetic_energy()

    def get_potential_energy(self):
        h1 = self.pos1.y
        h2 = self.pos2.y
        return self.g*(self.m1*h1+self.m2*h2)
    
    def get_kinetic_energy(self):
        E1=self.m1*self.l1**2*self.angular_velocities.x**2/2
        E2=self.m2*(self.l2**2*self.angular_velocities.y**2+self.l1**2*self.angular_velocities.x**2+2*self.l1*self.l2*self.angular_velocities.x*self.angular_velocities.y*np.cos(self.angles.x-self.angles.y))/2
        return E1+E2


class World:
    def __init__(self, pendulums, screen_size, screen_origin, scale, dt, targeted_sim_speed):
        self.pendulums=pendulums
        self.screen_size=screen_size # képernyő mérete
        self.screen_origin=screen_origin # ahonnan az ingák lógnak
        self.scale=scale # 1m hány pixel
        self.dt=dt
        self.targeted_sim_speed=targeted_sim_speed

    def start(self):
        run = True
        self.t=0
        pygame.init()

        self.screen=pygame.display.set_mode(self.screen_size)
        self.trace_surface = pygame.surface.Surface(self.screen_size) # húzott vonalak ide lesznek berajzolva
        self.pendulum_surface = pygame.surface.Surface(self.screen_size).convert_alpha() # ingák ide lesznek berajzolva
        self.render_font=pygame.font.SysFont('monospace', 20)
        self.starttime=pygame.time.get_ticks()
        
        while run:
            self.tick()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False

            # időkezelés
            # -konstans delta időnél nehézkes a szimulációs időt és valós időt szinkronizálva tartani
            # -kis mértékben váltakozó delta időt sem akarok az inga kaotikus természete miatt
            # -itt mindig próbálja magát igazítani, a hibáit mindig javítja
            # -egyetlen probléme az hogyha egy időre belassul, akkor utána igyikszik addig
            # begyorsulni amíg a szimulációs idő (t) utol nem éri az igazi időt
            self.t+=self.dt
            realelapsedms=(pygame.time.get_ticks()-self.starttime)*self.targeted_sim_speed
            simelapsedms=self.t*1000
            if (realelapsedms<simelapsedms):
                pygame.time.wait(int((simelapsedms-realelapsedms)))

            # -itt egy alternatív módszer ahol az utoljára említett probléma nem merül fel
            # -egy idő után itt viszont eléggé eltérő lesz a szimulációs és valós idő
            #pygame.time.Clock.tick(int(1/self.dt))

        pygame.quit()
    
    def tick(self):
        total_energy=0
        self.pendulum_surface.fill((0,0,0,0))
        for pendulum in self.pendulums:            
            pendulum.tick(self.dt)
            
            # inga pontjainak koordinátái a képernyőn
            pos1=pendulum.pos1*self.scale
            pos2=pendulum.pos2*self.scale
            pos1.y*=-1
            pos2.y*=-1
            pos1+=self.screen_origin
            pos2+=self.screen_origin

            # inga energiája
            total_energy+=pendulum.energy

            # húzott vonal (pontok) kirajzolása
            self.trace_surface.set_at((int(pos2.x),int(pos2.y)), pendulum.trace_color)
            # inga kirajzolása
            #pygame.draw.line(self.pendulum_surface, pendulum.trace_color, self.screen_origin, pos1, 2)
            #pygame.draw.line(self.pendulum_surface, pendulum.trace_color, pos1, pos2, 2)
            #pygame.draw.circle(self.pendulum_surface, pendulum.trace_color, pos1, 5)
            #pygame.draw.circle(self.pendulum_surface, pendulum.trace_color, pos2, 5)

            pygame.draw.line(self.pendulum_surface, 'white', self.screen_origin, pos1, 2)
            pygame.draw.line(self.pendulum_surface, 'white', pos1, pos2, 2)
            pygame.draw.circle(self.pendulum_surface, 'white', pos1, 5)
            pygame.draw.circle(self.pendulum_surface, 'white', pos2, 5)
        
        self.screen.blit(self.trace_surface, (0,0))
        self.screen.blit(self.pendulum_surface, (0,0))

        # szövegek kirajzolása
        texts=[f'real t={(pygame.time.get_ticks()-self.starttime)/1000:0.3f}',
                f'sim t={self.t:0.3f}',
                f'sim speed={self.t/(pygame.time.get_ticks()-self.starttime)*1000:0.3f}',
                f'dt={self.dt}',
                f'E={total_energy:0.8f}']
        for i in range(len(texts)):
            label=self.render_font.render(texts[i], True, 'white')
            self.screen.blit(label, (5, 5+i*20))


lastdeg=0
def cross(pendulum):
    global lastdeg
    angs=pygame.math.Vector2(pendulum.angles.x,pendulum.angles.y)
    #if angs.x>np.pi:
    #    angs.x-=2*np.pi
    #if angs.y>np.pi:
    #    angs.y-=2*np.pi
    xpoints.append(angs.x)
    ypoints.append(angs.y)
    degree=np.arctan(-pendulum.angular_velocities.y/pendulum.angular_velocities.x)+np.pi/2
    if pendulum.angular_velocities.x<0:
        degree+=np.pi
    offset=round((lastdeg-degree)/(2*np.pi))
    degree+=offset*2*np.pi
    lastdeg=degree
    zpoints.append(degree)
    #xpoints.append(pendulum.angles.y%(np.pi*2))
    #ypoints.append(pendulum.angular_velocities.x)
    #zpoints.append(pendulum.angular_velocities.y)
    #print(pendulum.angles.y%(np.pi*2), pendulum.angular_velocities.x, pendulum.angular_velocities.y)

'''
pendulums=[]
amount_of_pendulums=10
for i in range(amount_of_pendulums):
    angles=pygame.math.Vector2(np.pi*2/6, np.pi*2/6 + i/10)
    angular_velocities=pygame.math.Vector2(0,0)
    color=(255, int(255*i/amount_of_pendulums), 0)
    #color=gradient(i/amount/6)
    pendulums.append(DoublePendulum(1,1,1,1,angles, angular_velocities, color, 9.81, cross))

world = World(pendulums, (800,600), pygame.math.Vector2(400,300), 150, 0.01, 1)
world.start()
'''

xpoints, ypoints, zpoints=[],[],[]
angles=pygame.math.Vector2(np.pi*2/6, np.pi*-2/6)
angular_velocities=pygame.math.Vector2(0,0)
color=(255, 0, 0)
pendulum=DoublePendulum(1,1,1,1,angles, angular_velocities, color, 9.81, cross)
world = World([pendulum], (800,600), pygame.math.Vector2(400,300), 140, 0.002, 100)
world.start()

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ax.plot3D(xpoints, ypoints, zpoints, color='blue')
ax.scatter(xpoints[0], ypoints[0], zpoints[0], color='red')
ax.scatter(xpoints[-1], ypoints[-1], zpoints[-1], color='green')
ax.set_xlabel('angle1')
ax.set_ylabel('angle2')
ax.set_zlabel('degree')
ax.view_init(elev=90, azim=-90, roll=0)
target=plt.show()
