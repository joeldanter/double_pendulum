import pygame
from double_pendulum import *


class World:
    def __init__(self, pendulums, screen_size, screen_origin, scale, dt, targeted_sim_speed=1):
        self.pendulums=pendulums
        self.screen_size=screen_size # képernyő mérete
        self.screen_origin=screen_origin # pixel koordináta a képernyőn ahonnan az ingák lógnak
        self.scale=scale # 1m hány pixel
        self.dt=dt
        self.targeted_sim_speed=targeted_sim_speed

    def start(self):
        run = True
        self.t=0
        pygame.init()

        pygame.display.set_caption('Double Pendulum')
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
            pos1, pos2=pendulum.get_positions()
            pos1*=self.scale
            pos2*=self.scale
            pos1.y*=-1
            pos2.y*=-1
            pos1+=self.screen_origin
            pos2+=self.screen_origin

            # inga energiája
            total_energy+=pendulum.get_energy()

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
        self.draw_texts(texts)
    
    def draw_texts(self, texts):
        for i in range(len(texts)):
            label=self.render_font.render(texts[i], True, 'white')
            self.screen.blit(label, (5, 5+i*20))
