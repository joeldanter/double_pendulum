import numpy as np
from pygame.math import Vector2


class DoublePendulum:
    def __init__(self, m1, m2, l1, l2, angle1, angle2, ang_vel1, ang_vel2, trace_color, g):
        self.m1=m1 # első súly tömege
        self.m2=m2 # második súly tömege
        self.l1=l1 # első inga hossza
        self.l2=l2 # második inga hossza
        self.angle1=angle1 # belső szög
        self.angle2=angle2 # külső szög
        self.ang_vel1=ang_vel1 # belső szögsebesség
        self.ang_vel2=ang_vel2 # külső szögsebesség
        self.trace_color=trace_color # szine az ingának és a húzott vonalának
        self.g=g

    # egy dt idő eltelése alatt számítja ki és frissíti az új szögekek és szögsebességeket
    def tick(self, dt):
        # RK4 for 2nd order ODE        
        angles=Vector2(self.angle1, self.angle2)
        ang_vels=Vector2(self.ang_vel1, self.ang_vel2)

        k1=dt*ang_vels
        l1=dt*Vector2(self.get_accel_with_params(angles.x, angles.y,ang_vels.x, ang_vels.y))
        k2=dt*(ang_vels+l1/2)
        p1, p2 = angles+k1/2, ang_vels+l1/2
        l2=dt*Vector2(self.get_accel_with_params(p1.x, p1.y, p2.x, p2.y))
        k3=dt*(ang_vels+l2/2)
        p1, p2 = angles+k2/2, ang_vels+l2/2
        l3=dt*Vector2(self.get_accel_with_params(p1.x, p1.y, p2.x, p2.y))
        k4=dt*(ang_vels+l3)
        p1, p2 = angles+k3, ang_vels+l3
        l4=dt*Vector2(self.get_accel_with_params(p1.x, p1.y, p2.x, p2.y))
        
        angles+=(k1+2*k2+2*k3+k4)/6
        ang_vels+=(l1+2*l2+2*l3+l4)/6
        self.angle1=angles.x
        self.angle2=angles.y
        self.ang_vel1=ang_vels.x
        self.ang_vel2=ang_vels.y

    # paraméterben megadott szögekkel és szögsebességekkel számítja ki a szöggyorsulásokat
    # runge kutta 4-hez kell
    def get_accel_with_params(self, angle1, angle2, ang_vel1, ang_vel2):
        a1=(self.m1+self.m2)*self.l1**2
        b1=self.m2*self.l1*self.l2*np.cos(angle1-angle2)
        c1=-(self.m1+self.m2)*self.g*self.l1*np.sin(angle1)-self.m2*self.l1*self.l2*ang_vel2**2*np.sin(angle1-angle2)

        a2=self.m2*self.l1*self.l2*np.cos(angle1-angle2)
        b2=self.m2*self.l2**2
        c2=self.m2*self.l1*self.l2*ang_vel1**2*np.sin(angle1-angle2)-self.m2*self.g*self.l2*np.sin(angle2)
    
        angular_accel1=(b2*c1-b1*c2)/(a1*b2-a2*b1)
        angular_accel2=(a2*c1-a1*c2)/(a2*b1-a1*b2)
        return angular_accel1, angular_accel2

    # visszaadja a belső és külső inga végeinek koordinátáit
    def get_positions(self):
        x1=np.sin(self.angle1)*self.l1
        y1=-np.cos(self.angle1)*self.l1
        pos1=Vector2(x1,y1)
        x2=np.sin(self.angle2)*self.l2
        y2=-np.cos(self.angle2)*self.l2
        pos2=Vector2(x2,y2)+pos1
        return pos1, pos2

    def get_energy(self):
        return self.get_potential_energy()+self.get_kinetic_energy()

    def get_potential_energy(self):
        h1 = -np.cos(self.angle1)*self.l1
        h2 = h1-np.cos(self.angle2)*self.l2
        return self.g*(self.m1*h1+self.m2*h2)
    
    def get_kinetic_energy(self):
        a=(self.m1+self.m2)*(self.l1**2)*(self.ang_vel1**2)/2
        b=self.m2*(self.l2**2)*(self.ang_vel2**2)/2
        c=self.m2*self.l1*self.l2*self.ang_vel1*self.ang_vel2*np.cos(self.angle1-self.angle2)
        return a+b+c
    
    def get_energy_with_params(self, angle1, angle2, ang_vel1, ang_vel2):
        h1 = -np.cos(angle1)*self.l1
        h2 = h1-np.cos(angle2)*self.l2
        Ep= self.g*(self.m1*h1+self.m2*h2)
        a=(self.m1+self.m2)*(self.l1**2)*(ang_vel1**2)/2
        b=self.m2*(self.l2**2)*(ang_vel2**2)/2
        c=self.m2*self.l1*self.l2*ang_vel1*ang_vel2*np.cos(angle1-angle2)
        Ek=a+b+c
        return Ep+Ek
    
    # a szögsebességeket módosítja úgy, hogy a rendszer energiája és
    # upsilon a paraméterben megadott legyen.
    # Ha viszont a potenciális energia nagyobb mint a target_E, akkor
    # a szögeket is kell módosítani. Ilyenkor ha adjust_Ep=False, hibát
    # dob, ha adjust_Ep=True, akkor lecsökkenti a potenciális energiát
    # target_E-Eptol érték alá a szögek módosításával Newton Raphson
    # módszerrel
    def set_ups_e(self, upsilon, target_E, adjust_Ep=False, Eptol=0, max_iter=1000):
        if upsilon<0 or 2*np.pi<=upsilon:
            raise ValueError('Invalid value was given for upsilon')
        if target_E<self.get_energy_with_params(0,0,0,0):
            raise ValueError('Invalid value was given for energy')
        if self.get_potential_energy()>target_E and adjust_Ep==False:
            raise ValueError('Potencial energy too big')
        
        # potenciális energia lecsőkkentése, ha kell
        target_Ep=target_E-Eptol
        if target_Ep<=self.get_energy_with_params(0,0,0,0):
            self.angle1=self.angle2=self.ang_vel1=self.ang_vel2=0
        else:
            dEp=self.get_potential_energy()-target_Ep
            iter=0
            while dEp>0:
                dEpdt1=self.g*(self.m1+self.m2)*self.l1*np.sin(self.angle1)
                dEpdt2=self.g*self.m2*self.l2*np.sin(self.angle2)
                
                self.angle1-=np.min((np.abs((dEp+(1e-8))/dEpdt1),np.pi/8))*np.sign(dEpdt1)/2
                self.angle2-=np.min((np.abs((dEp+(1e-8))/dEpdt2),np.pi/8))*np.sign(dEpdt2)/2
                
                if iter==max_iter:
                    raise Exception('panik, newton raphson nem konvergalt')
                dEp=self.get_potential_energy()-target_Ep
                iter+=1
        
        # kinetikus energia fixálása
        target_Ek=target_E-self.get_potential_energy()
        if upsilon == 0:
            self.ang_vel1=0
            self.ang_vel2=np.sqrt(2*target_Ek/(self.m2*self.l2**2))
        elif upsilon == np.pi:
            self.ang_vel1=0
            self.ang_vel2=-np.sqrt(2*target_Ek/(self.m2*self.l2**2))
        elif upsilon<np.pi:
            # k*w1=w2
            k=-np.tan(upsilon-np.pi/2)
            a=(self.m1+self.m2)*(self.l1**2)/2
            b=self.m2*(self.l2**2)*(k**2)/2
            c=self.m2*self.l1*self.l2*k*np.cos(self.angle1-self.angle2)
            self.ang_vel1=np.sqrt(target_Ek/(a+b+c))
            self.ang_vel2=k*self.ang_vel1
        else:
            k=-np.tan(upsilon-3*np.pi/2)
            a=(self.m1+self.m2)*(self.l1**2)/2
            b=self.m2*(self.l2**2)*(k**2)/2
            c=self.m2*self.l1*self.l2*k*np.cos(self.angle1-self.angle2)
            self.ang_vel1=-np.sqrt(target_Ek/(a+b+c))
            self.ang_vel2=k*self.ang_vel1
    
    def jacobian(self):
        a = lambda theta1: self.get_accel_with_params(theta1, self.angle2, self.ang_vel1, self.ang_vel2)[0]
        b = lambda theta2: self.get_accel_with_params(self.angle1, theta2, self.ang_vel1, self.ang_vel2)[0]
        c = lambda theta1: self.get_accel_with_params(theta1, self.angle2, self.ang_vel1, self.ang_vel2)[1]
        d = lambda theta2: self.get_accel_with_params(self.angle1, theta2, self.ang_vel1, self.ang_vel2)[1]

        da=self.derivative(a, self.angle1)
        db=self.derivative(b, self.angle2)
        dc=self.derivative(c, self.angle1)
        dd=self.derivative(d, self.angle2)
        
        J=[[0, 0,  1, 0],
           [0, 0,  0, 1],
           [da,db, 0, 0],
           [dc,dd, 0, 0]]
        return J

    def real_eig_values(self):
        J = self.jacobian()
        return [z.real for z in np.linalg.eig(J)[0]]
    
    # TODO ne kelljen ez
    def derivative(self, f, x, h=1e-6):
        return (f(x+h)-f(x))/h
    

class TrackedDoublePendulum(DoublePendulum):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_angle1s=[]
        self.old_angle2s=[]
        self.old_ang_vel1s=[]
        self.old_ang_vel2s=[]
    
    def tick(self, *args, **kwargs):
        super().tick(*args, **kwargs)
        self.append_points()
    
    def append_points(self):
        self.old_angle1s.append(self.angle1)
        self.old_angle2s.append(self.angle2)
        self.old_ang_vel1s.append(self.ang_vel1)
        self.old_ang_vel2s.append(self.ang_vel2)
