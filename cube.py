#import modules
import pygame
import numpy as np

#initialize the pygame module
pygame.init()
#load and set the logo
logo = pygame.image.load("logo32x32.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("cube")

#create a surface on screen
screen_x = 1200
screen_y = 750
screen = pygame.display.set_mode((screen_x, screen_y))

#erase everything from the screen_x
def erase(screen):
    screen.fill((0,0,0))

#shape class
class Shape(object):
    def __init__(self, vertices, adjacency, omega, speed):
        self.vertices = vertices
        self.adjacency = adjacency
        self.omega = omega
        self.speed = speed
        self.num_vertices = np.shape(vertices)[0]

    def project(self):
        projected_vertices = []
        for vertex in self.vertices:
            projected_vertices.append([vertex[0],vertex[1]])
        return projected_vertices

    def get_lines(self):
        lines = []
        projected = self.project()
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.adjacency[i][j] == True:
                    lines.append([projected[i], projected[j]])
        return lines

    def drawlines(self):
        lines = self.get_lines()
        for x in lines:
            x[0][0] = int(x[0][0])
            x[1][0] = int(x[1][0])
            x[0][1] = int(x[0][1])
            x[1][1] = int(x[1][1])
        for line in lines:
            pygame.draw.line(screen, (255,0,0), line[0], line[1],10)

    def rotate(self):
        com = np.average((self.vertices), 0)
        for index, vertex in enumerate(self.vertices):
            r = np.array(vertex - com, dtype = np.longdouble)

            rotation_0 = np.array([[np.cos(self.omega[0]), -np.sin(self.omega[0]), 0],
                                   [np.sin(self.omega[0]), np.cos(self.omega[0]), 0],
                                   [0, 0, 1]], dtype = np.longdouble)

            rotation_1 = np.array([[1, 0, 0],
                                   [0, np.cos(self.omega[1]), -np.sin(self.omega[1])],
                                   [0, np.sin(self.omega[1]), np.cos(self.omega[1])]], dtype = np.longdouble)

            rotation = np.matmul(rotation_0, rotation_1)
            r_new = np.matmul(rotation, r)

            self.vertices[index] = com + r_new


    def move(self):
        for vertex in self.vertices:
            vertex += self.speed


#rotation velocity
omega_0 = [0, 0]
speed_0 = [0,0,0]

#instances of things
#triangle vertices
scale = 500
Tv = scale * np.array([(0,0,0),(0,1,0),(np.sqrt(3)/2,0.5,0)])
#triangle adjacency matrix
Ta = np.array([[0,1,1],
               [1,0,1],
               [0,1,1]])
#trianlge itself
#pointy = Shape(Tv, Ta, omega_0, speed_0)


Cv = scale * np.array([[0,0,0],
                       [1,0,0],
                       [0,0,1],
                       [1,0,1],
                       [0,1,0],
                       [1,1,0],
                       [0,1,1],
                       [1,1,1]], dtype = np.longdouble)

Ca = np.array([[0, 1, 1, 0, 1, 0, 0, 0],
               [1, 0, 0, 1, 0, 1, 0, 0],
               [1, 0, 0, 1, 0, 0, 1, 0],
               [0, 1, 1, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 1, 1, 0],
               [0, 1, 0, 0, 1, 0, 0, 1],
               [0, 0, 1, 0, 1, 0, 0, 1],
               [0, 0, 0, 1, 0, 1, 1, 0]])

pointy = Shape(Cv, Ca, omega_0, speed_0)


#define a variable to control main loop
running = True

#main loop
while running:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pointy.omega[0] += 0.01
    if keys[pygame.K_RIGHT]:
        pointy.omega[0] += -0.01
    if keys[pygame.K_UP]:
        pointy.omega[1] += 0.01
    if keys[pygame.K_DOWN]:
        pointy.omega[1] += -0.01
    if keys[pygame.K_d]:
        pointy.speed[0] = 5
        pointy.speed[1] = 0
    elif keys[pygame.K_w]:
        pointy.speed[1] = -5
        pointy.speed[0] = 0
    elif keys[pygame.K_a]:
        pointy.speed[0] = -5
        pointy.speed[1] = 0
    elif keys[pygame.K_s]:
        pointy.speed[1] = 5
        pointy.speed[0] = 0
    else:
        pointy.speed[0] = 0
        pointy.speed[1] = 0
    if keys[pygame.K_ESCAPE]:
        running = False

    #draw things
    erase(screen)
    pointy.rotate()
    pointy.move()
    pointy.drawlines()
    pygame.display.update()
