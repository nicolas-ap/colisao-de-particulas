import numpy as np
import matplotlib.pyplot as plt
import pygame
import math
import random
import pymunk

pygame.init()
screen_width = 600
screen_height = 600
display = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, 0

FPS = 20

 
class Particle():
    def __init__(self,x,y,velocity, colision_type=1):
        self.colision_type = colision_type
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        self.body.velocity = np.random.uniform(-velocity, velocity), np.random.uniform(-velocity, velocity)
        self.shape = pymunk.Circle(self.body, 3)
        self.shape.mass = 6.6422e-27
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    def draw(self):
        x,y = (self.body.position)
        if math.isnan(x) or math.isnan(y):
            print("Invalid values for x or y.")
        else:
            pygame.draw.circle(display, (0, 0, 100), (int(self.body.position[0]), int(self.body.position[1])), 3)

class Limits():
    def __init__(self,a,b):
        self.a = a
        self.b = b
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, self.a, self.b, 5)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.line(display, (0, 0, 0), self.a, self.b, 5)
        
       

def game():
    particles = [Particle(random.randint(200,390), random.randint(200,390),50) for i in range(500)]
    floor = Limits((screen_width // 4, 3 * screen_height // 4), (3 * screen_width // 4, 3 * screen_height // 4))
    right_wall = Limits((3 * screen_width // 4, screen_height // 4), (3 * screen_width // 4, 3 * screen_height // 4))
    left_wall = Limits((screen_width // 4, screen_height // 4), (screen_width // 4, 3 * screen_height // 4))
    top_wall = Limits((screen_width // 4, screen_height // 4), (3 * screen_width // 4, screen_height // 4))

  


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill((255, 255, 255))
        
        speed_particles = np.array([(np.sqrt(particle.body.velocity[0]**2 + particle.body.velocity[1]**2)) for particle in particles])
        print(speed_particles)
        
        m = 6.6422e-27 #u em kg do gás hélio
        ec = 0

        for spd in speed_particles:
            spd = (spd/50)*1700
            ec += ((m/2) * (spd**2))
        #e_cinética = 1/2xmv^2

        ec_avg = ec/len(particles) 
        #média da energia cinética de todas as partículas

        k_b = 1.38064852e-23
        t = 2*ec_avg/(3*k_b)
        #t (em kelvin) 2xe_cinética/(2xk)

        v = np.arange(0,5000,0.1)
        fv = (4*np.pi*(m/(2*np.pi*k_b* t))**(3 / 2))*v**2*(np.exp(-m*v**2/(2*k_b*t)))
        
        plt.clf()
        print(t)
            
        #1700 é o fator de conversão de pixels para metros
        plt.hist(speed_particles*(1700/50), bins=50,density=True, label = "Histograma de velocidades")
        plt.plot(v,fv, label = "Maxwell-Boltzmann distribution")
        plt.ylim(0,0.0010)
        plt.xlabel('velocidade (m/s)')
        plt.ylabel('Densidade da frequência')
        plt.title('Densidade da frequência x velocidade')
        plt.pause(0.001)
       
        for particle in particles:
            particle.draw()

        #Desenha os limites da caixa
        floor.draw()
        right_wall.draw()
        left_wall.draw()
        top_wall.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()