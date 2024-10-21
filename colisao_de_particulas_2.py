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


FPS = 30

def convert_cordinates(point):
    return point[0], 600 - point[1]


# class Button():
#     def __init__(self, x, y, width, height, text, color, hover_color, action=False) -> None:
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.text = text 
#         self.color = color
#         self.hover_color = hover_color
#         self.action = action
#         self.clicked = False
#     def draw(self):
#         mouse = pygame.mouse.get_pos()
#         click = pygame.mouse.get_pressed()

#         # if self.rect.collidepoint(mouse):
#         #     if pygame.mouse.get_pressed()[0] == 1:
#         #         print("hi")

#         if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
#             pygame.draw.rect(display, self.hover_color, (self.x, self.y, self.width, self.height))
#             if click[0] == 1 and not self.clicked:
#                 self.action = True
#                 return self.action
#             if click[0] == 0:
#                 self.action = False
                
                
#         else:
#             pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.height))
#         text = pygame.font.SysFont("Arial", 20).render(self.text, True, (0, 0, 0))
#         display.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))
        
#         return self.action
#     # def set_action(self, action):
#     #     self.action = action
#     # def get_action(self):
#     #     return self.action

    
class Particle():
    def __init__(self,x,y,velocity, colision_type=1):
        self.colision_type = colision_type
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        self.body.velocity = np.random.uniform(-velocity, velocity), np.random.uniform(-velocity, velocity)
        #self.body.velocity = 0, up*100
        self.shape = pymunk.Circle(self.body, 1)
        self.shape.mass = 4
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    # def change_velocity(self,incremento):
    #     angulo = np.arctan(self.body.velocity[1]/self.body.velocity[0])
    #     v = np.sqrt(self.body.velocity[0]**2 + self.body.velocity[1]**2) + incremento
    #     v_x = v*np.cos(np.degrees(angulo))
    #     v_y = v*np.sin(np.degrees(angulo))
    #     self.body.velocity = v_x, v_y
    def draw(self):
        x,y = convert_cordinates(self.body.position)
        if math.isnan(x) or math.isnan(y):
            print("Invalid values for x or y.")
        else:
            pygame.draw.circle(display, (0, 0, 0), (int(self.body.position[0]), int(self.body.position[1])), 3)

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
    # i = 0
    # fv_sum = [0]*50000
    # plus_button = Button(10, 600//4, 100, 40, "+", (210, 210, 210), (200, 200, 200))
    # less_button = Button(10, 600//3+50, 100, 40, "-", (210, 210, 210), (200, 200, 200))


    # plt.subplots_adjust(bottom=0.2,left=0.15)

    # ax.axis('equal')
    # ax.axis([-1, 30, -1, 30])

    # ax.xaxis.set_visible(False)
    # ax.yaxis.set_visible(False)

    particles = [Particle(random.randint(200,390), random.randint(200,390),50) for i in range(500)]

    #water = Particle( 300, 300,1)
    # water_2 = Particle( 300, 200, 2)
    # def total_Energy(particle_list, index): 
    #     return sum([particle_list[i].mass / 2. * particle_list[i].solvel_mag[index]**2  for i in range(len(particle_list))])

    # E = total_Energy(particles, 0)
    # Average_E = E/len(particles) 
    # k = 1.38064852e-23
    # T = 2*Average_E/(2*k)
    # m = 4
    # v = np.linspace(0,10,120)
    # fv = m*np.exp(-m*v**2/(2*T*k))/(2*np.pi*T*k)*2*np.pi*v
    # plt.hist.plot(v,fv, label = "Maxwell-Boltzmann distribution") 

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
        # plus_button.draw()
        # less_button.draw()

        speed_particles = np.array([(np.sqrt(particle.body.velocity[0]**2 + particle.body.velocity[1]**2)) for particle in particles])
        
        m = 6.6422e-27 #u em kg do gás hélio
        ec = 0

        for spd in speed_particles:
            spd = (spd/50)*1650
            ec += ((m/2) * (spd**2))
        #e_cinética = 1/2xmv^2

        ec_avg = ec/len(particles) 
        #média da energia cinética de todas as partículas

        k_b = 1.38064852e-23
        t = 2*ec_avg/(3*k_b)
        #t (em kelvin) 2xe_cinética/(2xk)

        v = np.arange(0,5000,0.1)
        fv = (4*np.pi*(m/(2*np.pi*k_b* t))**(3 / 2))*v**2*(np.exp(-m*v**2/(2*k_b*t)))
        # fv_sum += fv
        # fv_avg = fv_sum/(i+1)
        # i = i + 1
        plt.clf()
        print(t)
            
        #print(speed_particles)

        # sum_speed = sum(speed_particles)
        # v_mean = np.sqrt(sum_speed/len(particles))
        # print(v_mean)

        #1500 é o fator de conversão de pixels para metros
        plt.hist(speed_particles*(1650/50), bins=50,density=True, label = "Histograma de velocidades")
        plt.plot(v,fv, label = "Maxwell-Boltzmann distribution")
        plt.xlabel('velocidade (m/s)')
        plt.ylabel('Densidade da frequência')
        plt.title('Densidade da frequência x velocidade')
        plt.pause(0.001)

        # if plus_button.draw() and v_mean < 100:
        #     for particle in particles:
        #         particle.change_velocity(i)
        # if less_button.draw() and v_mean > 0:
        #     for particle in particles:
        #         particle.change_velocity(-i)

        for particle in particles:
            #particle.change_elasticity(var)
            particle.draw()

        
        

        #Desenha os limites da caixa
        floor.draw()
        right_wall.draw()
        left_wall.draw()
        top_wall.draw()

        # v_rms_show = font.render(f'{v_mean:.2f}', True, (0, 0, 0))
        # display.blit(v_rms_show, (25, 210))
        # temp_show = font.render(f'{(((v_mean)**2)*4)/(2*8.31):.2f}', True, (0, 0, 0))
        # display.blit(temp_show, (500, 210))
        # velocity_show = font_words.render("Velocidade média (m/s):", True, (0, 0, 0))
        # display.blit(velocity_show, (5, 140))
        # temperature_show = font_words.render("Temperatura (K):", True, (0, 0, 0))
        # display.blit(temperature_show, (500, 140))

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()